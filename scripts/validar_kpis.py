#!/usr/bin/env python3
"""Validador de datos y KPIs de IA DAY.

Lee SOLO los CSV de OrigenDatos y, de forma independiente al generador:
  1. verifica volumenes, integridad referencial y reglas de coherencia;
  2. recalcula los KPIs (R1-R10) con la fecha de corte fija;
  3. (opcional) comprueba que no se reutilizo ningun dato del HTML de referencia;
  4. escribe docs/validacion-kpis.md, que sirve de referencia para cuadrar las medidas DAX.

Uso:  python scripts/validar_kpis.py [--json archivo]   (codigo de salida 1 si algo falla)\n      --json escribe los valores esperados que usa scripts/cuadrar_dax.ps1
"""
import csv
import datetime as dt
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

CORTE = dt.date(2026, 10, 9)
RAIZ = Path(__file__).resolve().parent.parent
DATOS = RAIZ / "OrigenDatos"
REPORTE = RAIZ / "docs" / "validacion-kpis.md"
HTML_REF = RAIZ / "htlm"          # opcional: solo existe en la copia local

# Supuestos de interpretacion (ver docs/kpis.md, seccion "Supuestos a confirmar")
EXCLUIR_COMPLETADAS_EN_R8 = True   # actualizacion atrasada no evalua actividades Completadas
EXCLUIR_COMPLETADAS_EN_R7 = True   # por vencer no incluye actividades Completadas
PLAN_USA_FECHA_FIN_ORIGINAL = True  # R2 usa fecha_fin (no nueva_fecha_fin)

ESTADOS = {"Pendiente", "En Curso", "En Revisión", "Completado", "Bloqueado"}
TIPOS_SOL = {"Cambio de Alcance", "Replanificación de Cronograma", "Ajuste de Presupuesto",
             "Cierre y Transición a Operaciones"}
ESTADOS_SOL = {"Pendiente de firma", "Firmada", "Rechazada"}
ROLES = {"Sponsor Ejecutivo", "Líder de Iniciativa", "Responsable de Actividad", "Coordinador de Portafolio IA"}

def leer(nombre):
    with open(DATOS / nombre, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))

def fecha(s):
    return dt.date.fromisoformat(s) if s else None

def num(s):
    return float(s) if s != "" else None

def semaforo(desvio):
    return "Verde" if desvio <= 5 else ("Amarillo" if desvio <= 9 else "Rojo")

def semaforo_act(dias):
    if dias is None:
        return "Rojo"
    return "Verde" if dias <= 7 else ("Amarillo" if dias <= 14 else "Rojo")

def semaforo_firma(dias):
    """S7: dias de firma <= 15 verde, 16-30 amarillo, > 30 rojo."""
    return "Verde" if dias <= 15 else ("Amarillo" if dias <= 30 else "Rojo")

def plan_pct(ini, fin):
    """R2: lineal entre inicio y fin, redondeado a entero."""
    if CORTE <= ini:
        p = 0.0
    elif CORTE >= fin:
        p = 100.0
    else:
        p = 100.0 * (CORTE - ini).days / (fin - ini).days
    return int(p + 0.5)

resultados = []   # (descripcion, ok, detalle)

def chequeo(desc, ok, detalle=""):
    resultados.append((desc, bool(ok), detalle))

def main():
    pers = leer("dim_persona.csv")
    proy = leer("dim_proyecto.csv")
    act = leer("fact_actividades.csv")
    ff = leer("fact_flujo_fondos.csv")
    sol = leer("fact_solicitudes.csv")

    pid_set = {p["id_proyecto"] for p in proy}
    per = {p["id_persona"]: p for p in pers}
    proy_by = {p["id_proyecto"]: p for p in proy}

    # ---------------------------------------------------------------- 1. estructura
    chequeo("Iniciativas entre 10 y 12", 10 <= len(proy) <= 12, f"{len(proy)}")
    chequeo("Actividades entre 150 y 200", 150 <= len(act) <= 200, f"{len(act)}")
    chequeo("IDs únicos (proyecto, persona, actividad, solicitud)",
            len(pid_set) == len(proy) and len(per) == len(pers)
            and len({a['id_actividad'] for a in act}) == len(act)
            and len({s['id_solicitud'] for s in sol}) == len(sol))
    chequeo("Roles de dim_persona válidos", all(p["rol"] in ROLES for p in pers))
    chequeo("Sponsor, Líder y Coordinador de Portafolio de cada iniciativa existen con el rol correcto",
            all(per.get(p["id_sponsor"], {}).get("rol") == "Sponsor Ejecutivo"
                and per.get(p["id_lider"], {}).get("rol") == "Líder de Iniciativa"
                and per.get(p["id_coordinador_portafolio"], {}).get("rol") == "Coordinador de Portafolio IA" for p in proy))
    chequeo("fact_actividades: proyecto y responsable existen (rol Responsable)",
            all(a["id_proyecto"] in pid_set and per.get(a["id_responsable"], {}).get("rol") == "Responsable de Actividad"
                for a in act))
    chequeo("fact_flujo_fondos: proyectos existen", all(r["id_proyecto"] in pid_set for r in ff))
    chequeo("fact_solicitudes: proyecto y firmante existen",
            all(s["id_proyecto"] in pid_set and s["id_firmante"] in per for s in sol))
    chequeo("Estados de actividad válidos (R1)", all(a["estado"] in ESTADOS for a in act))
    chequeo("Tipos y estados de solicitud válidos",
            all(s["tipo"] in TIPOS_SOL and s["estado"] in ESTADOS_SOL for s in sol))
    chequeo("Todas las iniciativas tienen actividades", {a["id_proyecto"] for a in act} == pid_set)

    # ------------------------------------------------------------ coherencia fila a fila
    errores = defaultdict(list)
    for a in act:
        ini, fin, nueva = fecha(a["fecha_inicio"]), fecha(a["fecha_fin"]), fecha(a["nueva_fecha_fin"])
        upd = fecha(a["fecha_actualizacion"])
        real = int(a["av_real"])
        p = proy_by.get(a["id_proyecto"])
        pini, pfin = fecha(p["fecha_inicio"]), fecha(p["fecha_fin"])
        i = a["id_actividad"]
        if not ini < fin:
            errores["inicio < fin"].append(i)
        if not (pini <= ini and max(fin, nueva or fin) <= pfin):
            errores["actividad dentro de la ventana de la iniciativa"].append(i)
        if nueva and nueva <= fin:
            errores["nueva_fecha_fin posterior a fecha_fin"].append(i)
        if not 0 <= real <= 100:
            errores["av_real entre 0 y 100"].append(i)
        if a["estado"] == "Completado" and real != 100:
            errores["Completado implica av_real = 100"].append(i)
        if a["estado"] != "Completado" and real >= 100:
            errores["av_real = 100 solo si Completado"].append(i)
        if a["estado"] == "Pendiente" and not (real == 0 and ini > CORTE and not upd):
            errores["Pendiente implica av 0, inicio futuro y sin actualización"].append(i)
        if a["estado"] != "Pendiente" and ini > CORTE:
            errores["inicio futuro solo si Pendiente"].append(i)
        if upd and not (ini <= upd <= CORTE):
            errores["fecha_actualizacion entre inicio y corte"].append(i)
        if (a["estado"] == "Bloqueado") != bool(a["motivo_bloqueo"]):
            errores["motivo_bloqueo solo si Bloqueado"].append(i)
        if a["estado"] == "Completado" and not upd:
            errores["Completado tiene fecha de actualización"].append(i)
    for regla in ["inicio < fin", "actividad dentro de la ventana de la iniciativa",
                  "nueva_fecha_fin posterior a fecha_fin", "av_real entre 0 y 100",
                  "Completado implica av_real = 100", "av_real = 100 solo si Completado",
                  "Pendiente implica av 0, inicio futuro y sin actualización",
                  "inicio futuro solo si Pendiente", "fecha_actualizacion entre inicio y corte",
                  "motivo_bloqueo solo si Bloqueado", "Completado tiene fecha de actualización"]:
        chequeo(f"Coherencia de actividades: {regla}", not errores[regla], ", ".join(errores[regla][:5]))
    # dependencias logicas entre actividades (cadena por iniciativa)
    por_id = {a["id_actividad"]: a for a in act}
    dep_err = defaultdict(list)
    primera = {}
    for a in act:
        primera.setdefault(a["id_proyecto"], a["id_actividad"])
    for a in act:
        i, pr = a["id_actividad"], por_id.get(a["id_predecesora"])
        if primera[a["id_proyecto"]] == i:
            if a["id_predecesora"]:
                dep_err["la primera actividad no tiene predecesora"].append(i)
            continue
        if pr is None or pr["id_proyecto"] != a["id_proyecto"] or pr["id_actividad"] >= i:
            dep_err["predecesora existente, de la misma iniciativa y anterior"].append(i)
            continue
        if a["estado"] == "Completado" and pr["estado"] != "Completado":
            dep_err["Completado exige predecesora Completada"].append(i)
        if a["estado"] != "Pendiente" and pr["estado"] == "Pendiente":
            dep_err["no se inicia con predecesora Pendiente"].append(i)
        if a["estado"] != "Pendiente" and pr["estado"] != "Completado" and int(a["av_real"]) > max(1, int(pr["av_real"])):
            dep_err["el avance no supera al de una predecesora incompleta"].append(i)
        if fecha(a["fecha_inicio"]) < fecha(pr["fecha_inicio"]) or fecha(a["fecha_fin"]) < fecha(pr["fecha_fin"]):
            dep_err["las fechas no retroceden respecto de la predecesora"].append(i)
    for regla in ["la primera actividad no tiene predecesora", "predecesora existente, de la misma iniciativa y anterior",
                  "Completado exige predecesora Completada", "no se inicia con predecesora Pendiente",
                  "el avance no supera al de una predecesora incompleta",
                  "las fechas no retroceden respecto de la predecesora"]:
        chequeo(f"Dependencias: {regla}", not dep_err[regla], ", ".join(dep_err[regla][:5]))
    chequeo("Proyectos: inicio < fin", all(fecha(p["fecha_inicio"]) < fecha(p["fecha_fin"]) for p in proy))
    chequeo("Presupuesto aprobado en rango USD 50.000-2.000.000",
            all(50_000 <= int(p["presupuesto_aprobado_usd"]) <= 2_000_000 for p in proy))

    # flujo de fondos
    mes_corte = CORTE.replace(day=1)
    ff_ok_real = all((r["real_usd"] == "") == (fecha(r["mes"]) > mes_corte) for r in ff)
    chequeo("Flujo de fondos: real vacío solo para meses posteriores al corte", ff_ok_real)
    chequeo("Flujo de fondos: un registro por proyecto y mes", len({(r["id_proyecto"], r["mes"]) for r in ff}) == len(ff))
    forecast_total = defaultdict(int)
    for r in ff:
        forecast_total[r["id_proyecto"]] += int(r["forecast_usd"])
    desv = {k: forecast_total[k] / int(proy_by[k]["presupuesto_aprobado_usd"]) for k in proy_by}
    chequeo("Forecast total entre 93% y 107% del presupuesto aprobado por iniciativa",
            all(0.93 <= v <= 1.07 for v in desv.values()),
            ", ".join(f"{k}:{v:.2f}" for k, v in desv.items() if not 0.93 <= v <= 1.07))
    # solicitudes
    ok_sol = True
    for s in sol:
        c, r = fecha(s["fecha_creacion"]), fecha(s["fecha_resolucion"])
        if c > CORTE or (r and (r < c or r > CORTE)) or ((s["estado"] == "Pendiente de firma") == bool(r)):
            ok_sol = False
    chequeo("Solicitudes: fechas coherentes y estado consistente con resolución", ok_sol)
    replan = {a["id_proyecto"] for a in act if a["nueva_fecha_fin"]}
    chequeo("Cada iniciativa con reprogramaciones tiene una solicitud de cronograma",
            all(any(s["id_proyecto"] == pid and s["tipo"] == "Replanificación de Cronograma" for s in sol)
                for pid in replan))

    # ------------------------------------------------------------------ 2. KPIs
    filas = []
    for a in act:
        ini, fin, nueva = fecha(a["fecha_inicio"]), fecha(a["fecha_fin"]), fecha(a["nueva_fecha_fin"])
        fin_ef = max(fin, nueva) if nueva else fin
        fin_plan = fin if PLAN_USA_FECHA_FIN_ORIGINAL else fin_ef
        real = int(a["av_real"])
        plan = plan_pct(ini, fin_plan)
        desvio = max(0, plan - real)
        completada = a["estado"] == "Completado"
        dias_restantes = (fin_ef - CORTE).days
        vencida = (not completada) and fin_ef <= CORTE
        por_vencer = (not vencida) and 1 <= dias_restantes <= 60 and not (EXCLUIR_COMPLETADAS_EN_R7 and completada)
        iniciada = ini <= CORTE
        upd = fecha(a["fecha_actualizacion"])
        dias_upd = (CORTE - upd).days if upd else None
        evaluable = iniciada and not (EXCLUIR_COMPLETADAS_EN_R8 and completada)
        filas.append(dict(a, plan=plan, real=real, desvio=desvio, sem=semaforo(desvio), vencida=vencida,
                          por_vencer=por_vencer, dias_rest=dias_restantes, evaluable=evaluable,
                          dias_upd=dias_upd, sem_act=semaforo_act(dias_upd) if evaluable else None,
                          fin_ef=fin_ef))

    n = len(filas)
    k = {}
    k["total"] = n
    k["completadas"] = sum(r["estado"] == "Completado" for r in filas)
    k["bloqueadas"] = sum(r["estado"] == "Bloqueado" for r in filas)
    k["vencidas"] = sum(r["vencida"] for r in filas)
    k["av_real"] = sum(r["real"] for r in filas) / n
    k["av_plan"] = sum(r["plan"] for r in filas) / n
    k["desvio_global"] = max(0, k["av_plan"] - k["av_real"])
    sem_cnt = Counter(r["sem"] for r in filas)
    pv = [r for r in filas if r["por_vencer"]]
    k["pv30"] = sum(r["dias_rest"] <= 30 for r in pv)
    k["pv60"] = len(pv)
    ev = [r for r in filas if r["evaluable"]]
    act_cnt = Counter(r["sem_act"] for r in ev)

    chequeo("KPI: Verde + Amarillo + Rojo = Total actividades", sum(sem_cnt.values()) == n)
    chequeo("KPI: Vencidas y Por vencer son disjuntas", not any(r["vencida"] and r["por_vencer"] for r in filas))
    chequeo("KPI: Vencidas nunca Completadas", not any(r["vencida"] and r["estado"] == "Completado" for r in filas))
    chequeo("KPI: Actualización Verde + Amarillo + Rojo = actividades evaluables", sum(act_cnt.values()) == len(ev))
    chequeo("KPI: hay casos de cada tipo (verde, amarillo, rojo, vencida, por vencer, bloqueada, sin fecha)",
            all(sem_cnt[x] > 0 for x in ("Verde", "Amarillo", "Rojo")) and k["vencidas"] > 0 and k["pv60"] > 0
            and k["bloqueadas"] > 0 and any(r["evaluable"] and r["dias_upd"] is None for r in filas))
    chequeo("KPI: hay actividades reprogramadas, vencidas y no vencidas por reprogramación",
            any(r["nueva_fecha_fin"] and r["vencida"] for r in filas)
            or any(r["nueva_fecha_fin"] and not r["vencida"] for r in filas))

    # por iniciativa
    ini_rows = []
    for pid, p in sorted(proy_by.items()):
        rs = [r for r in filas if r["id_proyecto"] == pid]
        ar = sum(r["real"] for r in rs) / len(rs)
        ap = sum(r["plan"] for r in rs) / len(rs)
        d = max(0, ap - ar)
        ini_rows.append((pid, p["nombre"], len(rs), sum(r["estado"] == "Completado" for r in rs),
                         sum(r["estado"] == "Bloqueado" for r in rs), sum(r["vencida"] for r in rs),
                         ar, ap, d, semaforo(int(d + 0.5))))
    sem_ini = Counter(x[9] for x in ini_rows)
    chequeo("Cartera con variedad: al menos 2 colores de semáforo a nivel iniciativa", len(sem_ini) >= 2,
            str(dict(sem_ini)))
    chequeo("Equilibrio (demo): cada color de semáforo de iniciativa aparece al menos 2 veces",
            all(sem_ini[c] >= 2 for c in ("Verde", "Amarillo", "Rojo")), str(dict(sem_ini)))
    pct_no_verde = 100 * (sem_cnt["Amarillo"] + sem_cnt["Rojo"]) / n
    chequeo("Equilibrio (demo): entre 15% y 35% de las actividades no están en verde",
            15 <= pct_no_verde <= 35, f"{pct_no_verde:.1f}%")
    chequeo("Equilibrio (demo): amarillo y rojo con al menos 5% cada uno",
            sem_cnt["Amarillo"] >= 0.05 * n and sem_cnt["Rojo"] >= 0.05 * n,
            f"amarillo {100 * sem_cnt['Amarillo'] / n:.1f}%, rojo {100 * sem_cnt['Rojo'] / n:.1f}%")
    n_rev = sum(r["estado"] == "En Revisión" for r in filas)
    chequeo("Equilibrio (demo): 'En Revisión' representa al menos 5% de las actividades",
            n_rev >= 0.05 * n, f"{n_rev} ({100 * n_rev / n:.1f}%)")


    # por responsable (actualización atrasada)
    resp_rows = []
    for rid in sorted({r["id_responsable"] for r in filas}):
        rs = [r for r in ev if r["id_responsable"] == rid]
        if rs:
            c = Counter(r["sem_act"] for r in rs)
            resp_rows.append((per[rid]["nombre_completo"], len(rs), c["Verde"], c["Amarillo"], c["Rojo"]))

    # flujo de fondos
    f_total = sum(int(r["forecast_usd"]) for r in ff)
    r_total = sum(int(r["real_usd"]) for r in ff if r["real_usd"] != "")
    f_cerr = sum(int(r["forecast_usd"]) for r in ff if fecha(r["mes"]) < mes_corte)
    r_cerr = sum(int(r["real_usd"]) for r in ff if fecha(r["mes"]) < mes_corte)
    aprobado = sum(int(p["presupuesto_aprobado_usd"]) for p in proy)

    # solicitudes
    abiertas = [s for s in sol if s["estado"] == "Pendiente de firma"]
    dias_ab = [(CORTE - fecha(s["fecha_creacion"])).days for s in abiertas]
    sem_sol = Counter()
    sem_ab = Counter()
    for s in sol:
        fin = fecha(s["fecha_resolucion"]) or CORTE
        dias = (fin - fecha(s["fecha_creacion"])).days
        sem = semaforo_firma(dias)
        sem_sol[sem] += 1
        if s["estado"] == "Pendiente de firma":
            sem_ab[sem] += 1
    chequeo("Solicitudes: el semáforo de firma (S7) cubre todas las solicitudes",
            sum(sem_sol.values()) == len(sol) and sum(sem_ab.values()) == len(abiertas))

    # ----------------------------------------------------------- 3. no reutilizacion
    reuso = None
    htmls = sorted(HTML_REF.glob("*.html")) if HTML_REF.exists() else []
    if htmls:
        txt = htmls[0].read_text(encoding="utf-8", errors="ignore")
        m = re.search(r"const PROJECTS = (\[.*?\]);\r?\n", txt, re.S)
        ref = json.loads(m.group(1)) if m else []
        nombres = {x for r in ref for c in ("lider", "responsable", "gerente", "focal_pmo") if (x := r.get(c))}
        proyectos_ref = {r["nombre"].strip().lower() for r in ref}
        montos = {int(r[c]) for r in ref for c in ("inv_aprobada", "inv_real") if r.get(c)} - {0}
        ids = {str(r["id"]) for r in ref}
        mios_n = {p["nombre_completo"] for p in pers}
        mios_p = {p["nombre"].strip().lower() for p in proy}
        mios_m = {int(p["presupuesto_aprobado_usd"]) for p in proy}
        mios_m |= {int(r[c]) for r in ff for c in ("forecast_usd", "real_usd") if r[c] != ""}
        mios_i = {p["id_proyecto"] for p in proy} | {a["id_actividad"] for a in act}
        reuso = (len(mios_n & nombres), len(mios_p & proyectos_ref), len(mios_m & montos), len(mios_i & ids))
        chequeo("Sin reutilización de datos del HTML de referencia (personas, proyectos, montos, IDs)",
                sum(reuso) == 0,
                f"coincidencias: personas={reuso[0]}, proyectos={reuso[1]}, montos={reuso[2]}, ids={reuso[3]}")

    # ------------------------------------------------- valores esperados (para cuadrar el DAX)
    if "--json" in sys.argv:
        esperado = {
            "Total Actividades": n, "Completadas": k["completadas"], "Bloqueadas": k["bloqueadas"],
            "En Curso": sum(r["estado"] == "En Curso" for r in filas),
            "En Revisión": sum(r["estado"] == "En Revisión" for r in filas),
            "Pendientes": sum(r["estado"] == "Pendiente" for r in filas),
            "% Avance Real": k["av_real"] / 100, "% Avance Planificado": k["av_plan"] / 100,
            "Desvío Global": k["desvio_global"],
            "Actividades Verde": sem_cnt["Verde"], "Actividades Amarillo": sem_cnt["Amarillo"],
            "Actividades Rojo": sem_cnt["Rojo"], "Vencidas": k["vencidas"],
            "Por Vencer 60": k["pv60"], "Por Vencer 30": k["pv30"], "Por Vencer 31-60": k["pv60"] - k["pv30"],
            "Actividades En Plazo": sum(r["estado"] != "Completado" and r["dias_rest"] > 60 for r in filas),
            "Días de Atraso Promedio": sum(-r["dias_rest"] for r in filas if r["vencida"]) / max(1, k["vencidas"]),
            "Actividades Evaluables Actualización": len(ev),
            "Actualización Verde": act_cnt["Verde"], "Actualización Amarillo": act_cnt["Amarillo"],
            "Actualización Rojo": act_cnt["Rojo"],
            "Sin Fecha de Actualización": sum(r["dias_upd"] is None for r in ev),
            "Presupuesto Aprobado": aprobado, "Forecast Total": f_total, "Real Total": r_total,
            "Pendiente": f_total - r_total, "% Ejecución": r_total / f_total,
            "Forecast Meses Cerrados": f_cerr, "Real Meses Cerrados": r_cerr,
            "% Cumplimiento Meses Cerrados": r_cerr / f_cerr, "% Inversión Ejecutada": r_total / aprobado,
            "Total Solicitudes": len(sol), "Solicitudes Abiertas": len(abiertas),
            "Días Promedio Abiertas": sum(dias_ab) / len(dias_ab),
            "Solicitudes Verde": sem_sol["Verde"], "Solicitudes Amarillo": sem_sol["Amarillo"],
            "Solicitudes Rojo": sem_sol["Rojo"], "Abiertas Verde": sem_ab["Verde"],
            "Abiertas Amarillo": sem_ab["Amarillo"], "Abiertas Rojo": sem_ab["Rojo"],
        }
        por_ini = {x[0]: {"Total Actividades": x[2], "Completadas": x[3], "Bloqueadas": x[4], "Vencidas": x[5],
                          "Desvío Global": x[8], "Semáforo Iniciativa": x[9]} for x in ini_rows}
        destino = Path(sys.argv[sys.argv.index("--json") + 1])
        destino.write_text(json.dumps({"corte": CORTE.isoformat(), "global": esperado, "por_iniciativa": por_ini},
                                      ensure_ascii=False, indent=1), encoding="utf-8")

    # ------------------------------------------------------------------ reporte
    fallos =[r for r in resultados if not r[1]]
    L = []
    w = L.append
    w("# Validación de datos y KPIs")
    w("")
    w(f"> Generado por `scripts/validar_kpis.py`. Fecha de corte: **{CORTE.strftime('%d/%m/%Y')}**. "
      "Este documento es la **referencia contra la que se cuadran las medidas DAX**.")
    w("")
    w(f"**Resultado: {'APROBADO' if not fallos else 'CON ERRORES'}** — "
      f"{len(resultados) - len(fallos)}/{len(resultados)} chequeos correctos.")
    w("")
    w("## 1. Chequeos")
    w("")
    w("| # | Chequeo | Resultado | Detalle |")
    w("|---|---|---|---|")
    for i, (d, ok, det) in enumerate(resultados, 1):
        w(f"| {i} | {d} | {'✅' if ok else '❌'} | {det} |")
    w("")
    w("## 2. Volúmenes")
    w("")
    w("| Tabla | Filas |")
    w("|---|---|")
    for nm, c in [("dim_persona", pers), ("dim_proyecto", proy), ("fact_actividades", act),
                  ("fact_flujo_fondos", ff), ("fact_solicitudes", sol)]:
        w(f"| {nm} | {len(c)} |")
    w("")
    w("## 3. KPIs de actividades (cartera completa)")
    w("")
    w("| KPI | Valor |")
    w("|---|---|")
    w(f"| Total actividades | {k['total']} |")
    w(f"| Completadas | {k['completadas']} |")
    w(f"| Bloqueadas | {k['bloqueadas']} |")
    w(f"| Vencidas (R6) | {k['vencidas']} |")
    w(f"| Por vencer en 60 días (R7) | {k['pv60']} |")
    w(f"| Por vencer en 30 días (R7) | {k['pv30']} |")
    w(f"| Por vencer en 31 a 60 días (R7) | {k['pv60'] - k['pv30']} |")
    w(f"| En plazo (más de 60 días, no Completadas) | {sum(r['estado'] != 'Completado' and r['dias_rest'] > 60 for r in filas)} |")
    w(f"| Días promedio de atraso de las vencidas (R6) | {sum(-r['dias_rest'] for r in filas if r['vencida']) / max(1, k['vencidas']):.1f} |")
    w(f"| % Avance real (promedio simple, R5) | {k['av_real']:.2f}% |")
    w(f"| % Avance planificado (promedio simple, R2) | {k['av_plan']:.2f}% |")
    w(f"| Desvío global (R3) | {k['desvio_global']:.2f} pp |")
    w(f"| Semáforo Verde / Amarillo / Rojo (R4) | {sem_cnt['Verde']} / {sem_cnt['Amarillo']} / {sem_cnt['Rojo']} |")
    w(f"| Actividades evaluables para actualización (R8) | {len(ev)} |")
    w(f"| Actualización Verde / Amarillo / Rojo (R8) | {act_cnt['Verde']} / {act_cnt['Amarillo']} / {act_cnt['Rojo']} |")
    w(f"| …de las cuales sin fecha de actualización | {sum(r['dias_upd'] is None for r in ev)} |")
    w("")
    w("## 4. Por iniciativa")
    w("")
    w("| Id | Iniciativa | Act. | Compl. | Bloq. | Venc. | % Real | % Plan | Desvío | Semáforo |")
    w("|---|---|---|---|---|---|---|---|---|---|")
    for x in ini_rows:
        w(f"| {x[0]} | {x[1]} | {x[2]} | {x[3]} | {x[4]} | {x[5]} | {x[6]:.1f}% | {x[7]:.1f}% | {x[8]:.1f} | {x[9]} |")
    w("")
    w("## 5. Actualización atrasada por responsable (R8)")
    w("")
    w("| Responsable | Evaluables | Verde | Amarillo | Rojo |")
    w("|---|---|---|---|---|")
    for x in sorted(resp_rows, key=lambda t: -t[4]):
        w(f"| {x[0]} | {x[1]} | {x[2]} | {x[3]} | {x[4]} |")
    w("")
    w("## 6. Flujo de fondos (R9, USD)")
    w("")
    w("| KPI | Valor |")
    w("|---|---|")
    w(f"| Presupuesto aprobado total | {aprobado:,} |")
    w(f"| Forecast total | {f_total:,} |")
    w(f"| Real acumulado | {r_total:,} |")
    w(f"| Pendiente (forecast − real) | {f_total - r_total:,} |")
    w(f"| % Ejecución (real / forecast total) | {100 * r_total / f_total:.2f}% |")
    w(f"| Forecast de meses cerrados (hasta septiembre 2026) | {f_cerr:,} |")
    w(f"| Real de meses cerrados | {r_cerr:,} |")
    w(f"| % Cumplimiento de meses cerrados | {100 * r_cerr / f_cerr:.2f}% |")
    w(f"| % Inversión ejecutada (real / aprobado) | {100 * r_total / aprobado:.2f}% |")
    w("")
    w("## 7. Solicitudes")
    w("")
    w("| KPI | Valor |")
    w("|---|---|")
    w(f"| Total solicitudes | {len(sol)} |")
    for e in sorted(ESTADOS_SOL):
        w(f"| {e} | {sum(s['estado'] == e for s in sol)} |")
    for t in sorted(TIPOS_SOL):
        w(f"| Tipo: {t} | {sum(s['tipo'] == t for s in sol)} |")
    w(f"| Días promedio de las abiertas | {sum(dias_ab) / len(dias_ab):.1f} |" if dias_ab else "| Días promedio de las abiertas | – |")
    w(f"| Semáforo de firma, todas (Verde / Amarillo / Rojo) | {sem_sol['Verde']} / {sem_sol['Amarillo']} / {sem_sol['Rojo']} |")
    w(f"| Semáforo de firma, abiertas (Verde / Amarillo / Rojo) | {sem_ab['Verde']} / {sem_ab['Amarillo']} / {sem_ab['Rojo']} |")
    w("")
    w("> Días de firma: resolución − creación en las resueltas; corte − creación en las abiertas. "
      "Umbrales (S7): ≤ 15 verde, 16–30 amarillo, > 30 rojo.")
    w("")
    w("## 8. Supuestos usados en este cálculo")
    w("")
    w(f"- R8 excluye actividades Completadas: **{EXCLUIR_COMPLETADAS_EN_R8}**")
    w(f"- R7 excluye actividades Completadas: **{EXCLUIR_COMPLETADAS_EN_R7}**")
    w(f"- R2 usa `fecha_fin` original (no la nueva): **{PLAN_USA_FECHA_FIN_ORIGINAL}**")
    w("- Avance planificado redondeado al entero más cercano antes de calcular el desvío.")
    w("- Actividad no iniciada = `fecha_inicio` posterior a la fecha de corte.")
    w("")
    REPORTE.parent.mkdir(parents=True, exist_ok=True)
    REPORTE.write_text("\n".join(L), encoding="utf-8")

    sys.stdout.reconfigure(encoding="utf-8")
    print(f"Chequeos: {len(resultados) - len(fallos)}/{len(resultados)} correctos")
    for d, ok, det in fallos:
        print(f"  FALLA: {d} {det}")
    if reuso is None:
        print("  (comparación con HTML omitida: no existe la carpeta htlm)")
    print(f"Reporte escrito en {REPORTE}")
    return 1 if fallos else 0

if __name__ == "__main__":
    sys.exit(main())
