#!/usr/bin/env python3
"""Generador de datos 100% ficticios para IA DAY (iniciativas de Inteligencia Artificial).

Reproducible: semilla fija y fecha de corte fija (09/10/2026).
Escribe los CSV en ../OrigenDatos. Solo usa la biblioteca estandar.

Uso:  python scripts/generar_datos.py
"""
import csv
import datetime as dt
import random
from pathlib import Path

SEMILLA = 20261009
CORTE = dt.date(2026, 10, 9)
RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "OrigenDatos"
rnd = random.Random(SEMILLA)

# ----------------------------------------------------------------- utilidades
def f(s):
    return dt.date.fromisoformat(s)

def dia_habil_adelante(x):
    while x.weekday() >= 5:
        x += dt.timedelta(days=1)
    return x

def dia_habil_atras(x):
    while x.weekday() >= 5:
        x -= dt.timedelta(days=1)
    return x

def pct_plan(ini, fin, corte=CORTE):
    """R2: avance planificado lineal entre inicio y fin (0-100)."""
    if corte <= ini:
        return 0.0
    if corte >= fin:
        return 100.0
    return 100.0 * (corte - ini).days / (fin - ini).days

def escribir(nombre, columnas, filas):
    SALIDA.mkdir(parents=True, exist_ok=True)
    with open(SALIDA / nombre, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(columnas)
        w.writerows(filas)
    print(f"  {nombre}: {len(filas)} filas")

# --------------------------------------------------------------------- personas
PERSONAS = [
    # id, nombre, rol, area
    ("PER-001", "Valeria Montenegro Ríos", "Sponsor Ejecutivo", "Tecnología"),
    ("PER-002", "Andrés Salcedo Brunetti", "Sponsor Ejecutivo", "Datos"),
    ("PER-003", "Carolina Ibáñez Duarte", "Sponsor Ejecutivo", "Operaciones"),
    ("PER-004", "Julieta Quiroga Beltrán", "Coordinador de Portafolio IA", "PMO de IA"),
    ("PER-005", "Matías Ferreyra Cardozo", "Coordinador de Portafolio IA", "PMO de IA"),
    ("PER-006", "Nicolás Arrieta Solano", "Líder de Iniciativa", "Personas"),
    ("PER-007", "Florencia Landaeta Vidal", "Líder de Iniciativa", "Tecnología"),
    ("PER-008", "Emiliano Pedraza Corvalán", "Líder de Iniciativa", "Finanzas"),
    ("PER-009", "Renata Zubiría Maldonado", "Líder de Iniciativa", "Datos"),
    ("PER-010", "Tomás Echeverría Lagos", "Líder de Iniciativa", "Comercial"),
    ("PER-011", "Camila Bustos Ferrante", "Líder de Iniciativa", "Operaciones"),
    ("PER-012", "Joaquín Mansilla Peña", "Responsable de Actividad", "Tecnología"),
    ("PER-013", "Daniela Corrales Ugarte", "Responsable de Actividad", "Datos"),
    ("PER-014", "Federico Alsina Montero", "Responsable de Actividad", "Tecnología"),
    ("PER-015", "Lucía Berriozábal Sierra", "Responsable de Actividad", "Datos"),
    ("PER-016", "Martina Castellanos Orozco", "Responsable de Actividad", "Finanzas"),
    ("PER-017", "Ignacio Peralta Donoso", "Responsable de Actividad", "Operaciones"),
    ("PER-018", "Antonella Rojas Sabaté", "Responsable de Actividad", "Comercial"),
    ("PER-019", "Gonzalo Villaseca Mora", "Responsable de Actividad", "Tecnología"),
    ("PER-020", "Paula Quintana Olivera", "Responsable de Actividad", "Personas"),
    ("PER-021", "Bruno Cabrera Lanzillotta", "Responsable de Actividad", "Datos"),
]
RESPONSABLES = [p[0] for p in PERSONAS if p[2] == "Responsable de Actividad"]

# ------------------------------------------------------------------- iniciativas
# id, nombre, descripcion, area, tipo_ia, fase, gerente, lider, focal, inicio, fin, aprobado,
# perfil, sujeto, tareas especificas (reemplazan posiciones 5, 10 y 12 de la plantilla), n actividades
PROYECTOS = [
    ("INI-001", "Asistente IA RRHH",
     "Asistente conversacional que resuelve consultas de beneficios, licencias y políticas internas.",
     "Personas", "Generativa", "Despliegue", "PER-001", "PER-006", "PER-004",
     "2026-03-02", "2026-12-18", 418730, "sano", "asistente de RRHH",
     ["Carga y curado de la base de políticas de RRHH", "Integración con el portal del colaborador",
      "Piloto con el equipo de People"], 16),
    ("INI-002", "Copilot Corporativo",
     "Copiloto para redacción, resumen y búsqueda sobre documentos y correos de la compañía.",
     "Tecnología", "Generativa", "Desarrollo", "PER-002", "PER-007", "PER-004",
     "2026-02-02", "2027-03-31", 1847250, "moderado", "copilot corporativo",
     ["Conexión con repositorios documentales", "Integración con suite de ofimática",
      "Despliegue por oleadas"], 19),
    ("INI-003", "Automatización de Reportes",
     "Generación automática de reportes de gestión mensuales con narrativa explicada por IA.",
     "Finanzas", "Automatización", "Despliegue", "PER-001", "PER-008", "PER-004",
     "2026-01-12", "2026-11-27", 263480, "sano", "motor de reportes",
     ["Inventario de reportes manuales", "Plantillas dinámicas de reporte", "Validación con Control de Gestión"], 14),
    ("INI-004", "Data Quality IA",
     "Detección automática de anomalías y duplicados en los datos maestros mediante modelos de IA.",
     "Datos", "Predictiva", "Desarrollo", "PER-002", "PER-009", "PER-005",
     "2026-04-06", "2027-02-26", 684920, "critico", "motor de calidad de datos",
     ["Catálogo de reglas de calidad", "Conectores a fuentes maestras", "Tablero de calidad por dominio"], 17),
    ("INI-005", "Forecast Inteligente",
     "Pronóstico de demanda y ventas con modelos de series temporales y variables externas.",
     "Comercial", "Predictiva", "Desarrollo", "PER-003", "PER-010", "PER-005",
     "2026-03-16", "2027-01-29", 539610, "moderado", "modelo de forecast",
     ["Consolidación del histórico de ventas", "Publicación del forecast en el tablero comercial",
      "Backtesting contra el pronóstico manual"], 16),
    ("INI-006", "Procesamiento Documental",
     "Extracción y clasificación automática de datos desde facturas, contratos y formularios.",
     "Operaciones", "Generativa", "Despliegue", "PER-003", "PER-011", "PER-005",
     "2026-02-16", "2026-10-30", 391870, "critico", "procesador documental",
     ["Muestra etiquetada de documentos", "Integración con el flujo de aprobación", "Piloto con Cuentas por Pagar"], 13),
    ("INI-007", "Chat Corporativo IA",
     "Canal de chat interno con IA para consultas de soporte, procesos y normativas.",
     "Tecnología", "Generativa", "Piloto", "PER-002", "PER-007", "PER-004",
     "2026-05-04", "2027-04-30", 1203460, "sano", "chat corporativo",
     ["Indexación de la base de conocimiento", "Integración con mensajería corporativa", "Piloto con áreas voluntarias"], 18),
    ("INI-008", "Analítica Predictiva",
     "Modelos predictivos de abandono y propensión de compra para campañas comerciales.",
     "Comercial", "Predictiva", "Desarrollo", "PER-003", "PER-010", "PER-005",
     "2026-01-19", "2026-10-23", 452190, "critico", "modelo predictivo comercial",
     ["Construcción del dataset de clientes", "Integración con el CRM", "Prueba A/B de campañas"], 15),
    ("INI-009", "Clasificación Inteligente de Tickets",
     "Clasificación y ruteo automático de tickets de soporte según tema y urgencia.",
     "Operaciones", "Predictiva", "Desarrollo", "PER-003", "PER-011", "PER-005",
     "2026-05-18", "2027-01-15", 308740, "sano", "clasificador de tickets",
     ["Etiquetado histórico de tickets", "Integración con la mesa de ayuda", "Piloto en el turno de soporte"], 15),
    ("INI-010", "Automatización Power BI",
     "Generación y documentación asistida por IA de modelos y reportes de Power BI.",
     "Finanzas", "Automatización", "Despliegue", "PER-001", "PER-008", "PER-004",
     "2026-06-01", "2026-12-11", 124380, "moderado", "generador de reportes Power BI",
     ["Relevamiento de modelos existentes", "Generación asistida de medidas DAX", "Piloto con analistas"], 12),
    ("INI-011", "Agente de Conciliación Financiera",
     "Agente que concilia movimientos bancarios y contables y propone ajustes para su aprobación.",
     "Finanzas", "Generativa", "Piloto", "PER-001", "PER-006", "PER-004",
     "2026-08-03", "2027-05-28", 957310, "sano", "agente de conciliación",
     ["Extracción de movimientos bancarios", "Integración con el libro contable", "Piloto con Tesorería"], 15),
]

PLANTILLA = [
    "Relevamiento de casos de uso", "Definición de alcance y criterios de éxito",
    "Análisis de calidad de datos", "Diseño de arquitectura de la solución",
    "Preparación y curado de datos", None,  # 5 = especifica
    "Prototipo funcional", "Ingeniería de prompts y ajuste del modelo",
    "Evaluación de calidad y sesgos", "Revisión de seguridad y privacidad", None,  # 10 = especifica
    "Pruebas con usuarios clave", None,  # 12 = especifica
    "Plan de capacitación", "Despliegue en producción", "Monitoreo y observabilidad",
    "Documentación técnica y funcional", "Gestión del cambio y adopción",
    "Cierre y transferencia a operaciones",
]
POS_ESPECIFICAS = (5, 10, 12)
MOTIVOS_BLOQUEO = [
    "Falta de acceso a datos productivos", "Pendiente de aprobación de seguridad",
    "Dependencia de proveedor externo", "Capacidad de cómputo no disponible",
    "Definición funcional pendiente", "Observaciones de cumplimiento normativo",
]

def demora(perfil):
    r = rnd.random()
    if perfil == "sano":
        return rnd.randint(0, 5) if r < 0.55 else (rnd.randint(6, 9) if r < 0.85 else rnd.randint(10, 15))
    if perfil == "moderado":
        return rnd.randint(0, 5) if r < 0.25 else (rnd.randint(6, 9) if r < 0.65 else rnd.randint(10, 20))
    return rnd.randint(0, 5) if r < 0.10 else (rnd.randint(6, 9) if r < 0.30 else rnd.randint(10, 40))

def dias_sin_actualizar(perfil):
    r = rnd.random()
    if perfil == "sano":
        return rnd.randint(0, 7) if r < 0.80 else (rnd.randint(8, 14) if r < 0.95 else rnd.randint(15, 20))
    if perfil == "moderado":
        return rnd.randint(0, 7) if r < 0.50 else (rnd.randint(8, 14) if r < 0.80 else rnd.randint(15, 25))
    return rnd.randint(0, 7) if r < 0.30 else (rnd.randint(8, 14) if r < 0.55 else rnd.randint(15, 45))

P_FINALIZADA = {"sano": 0.97, "moderado": 0.88, "critico": 0.70}
P_BLOQUEO = {"sano": 0.04, "moderado": 0.10, "critico": 0.16}
P_SIN_FECHA = {"sano": 0.02, "moderado": 0.05, "critico": 0.10}

def estado_por_avance(real, bloqueada):
    """R1: En Revisión cuando el entregable está casi terminado (avance >= 70)."""
    if bloqueada:
        return "Bloqueado"
    if real >= 70 and rnd.random() < 0.80:
        return "En Revisión"
    return "En Curso"

# ------------------------------------------------------------------- actividades
def n_incompletas_cumplidas(perfil, m_past):
    """Cantidad de actividades con plazo cumplido que siguen sin completarse (las ultimas de la cadena)."""
    if perfil == "sano":
        n = 1 if rnd.random() < 0.35 else 0
    elif perfil == "moderado":
        n = rnd.randint(1, 2)
    else:
        n = rnd.randint(3, 5)
    return min(n, m_past)

def generar_actividades():
    filas = []
    n_act = 0
    for (pid, _n, _d, _a, _t, _fa, _g, _l, _fo, ini_s, fin_s, _ap, perfil, sujeto, espec, n) in PROYECTOS:
        p_ini, p_fin = f(ini_s), f(fin_s)
        dur = (p_fin - p_ini).days
        equipo = rnd.sample(RESPONSABLES, 4)
        idxs = sorted({round(i * 18 / (n - 1)) for i in range(n)})
        # --- fase 1: ventanas de fechas (no retroceden respecto de la predecesora)
        ventanas = []
        for k, idx in enumerate(idxs):
            s = dia_habil_adelante(p_ini + dt.timedelta(days=int(k / len(idxs) * dur * 0.90)))
            largo = max(10, int(dur / len(idxs) * rnd.uniform(2.5, 5.0)))
            e = dia_habil_atras(min(p_fin, s + dt.timedelta(days=largo)))
            if k == len(idxs) - 1:
                e = dia_habil_atras(p_fin)
            if ventanas:
                s = max(s, ventanas[-1][0])
                e = max(e, ventanas[-1][1])
            if e <= s:
                e = dia_habil_adelante(s + dt.timedelta(days=7))
            e = min(e, p_fin)
            if e <= s:
                s = dia_habil_atras(e - dt.timedelta(days=7))
            ventanas.append((s, e))
        m_past = sum(1 for (_s, e) in ventanas if e <= CORTE)
        limite = m_past - n_incompletas_cumplidas(perfil, m_past)   # desde aqui, las vencidas siguen incompletas
        # --- fase 2: estados respetando dependencias
        prev = None
        for k, idx in enumerate(idxs):
            n_act += 1
            s, e = ventanas[k]
            nombre = (espec[POS_ESPECIFICAS.index(idx)] if idx in POS_ESPECIFICAS
                      else f"{PLANTILLA[idx]} – {sujeto}")
            plan = pct_plan(s, e)
            nueva = None
            bloqueo = ""
            upd = None
            bloqueada = rnd.random() < P_BLOQUEO[perfil]
            if s > CORTE:                                    # no iniciada
                estado, real = "Pendiente", 0
            elif e <= CORTE:                                 # plazo cumplido
                if k < limite:
                    estado, real = "Completado", 100
                else:
                    real = rnd.randint(40, 95)
                    estado = estado_por_avance(real, bloqueada)
            else:                                            # en ejecucion
                if plan > 60 and rnd.random() < 0.05:
                    estado, real = "Completado", 100
                else:
                    real = max(1, min(99, round(plan - demora(perfil))))
                    estado = estado_por_avance(real, bloqueada)
            # dependencia: no se completa ni se avanza mas que la predecesora incompleta
            if prev and prev["estado"] != "Completado" and estado != "Pendiente":
                if estado == "Completado":
                    real = rnd.randint(50, 95)
                tope = prev["real"] - rnd.randint(4, 15) if prev["real"] > 15 else prev["real"]
                real = max(1, min(real, max(1, tope)))
                estado = estado_por_avance(real, bloqueada)
            if estado == "Completado":
                upd = (min(CORTE, max(s, e + dt.timedelta(days=rnd.randint(0, 5)))) if e <= CORTE
                       else CORTE - dt.timedelta(days=rnd.randint(0, 20)))
            if estado == "Bloqueado":
                bloqueo = rnd.choice(MOTIVOS_BLOQUEO)
            if estado not in ("Pendiente", "Completado"):
                if rnd.random() >= P_SIN_FECHA[perfil]:
                    upd = max(s, CORTE - dt.timedelta(days=dias_sin_actualizar(perfil)))
            # reprogramaciones (nueva fecha fin), acotadas a un plazo razonable
            if estado != "Completado" and s <= CORTE:
                if e <= CORTE and rnd.random() < (0.15 if perfil == "sano" else 0.35):
                    if (CORTE - e).days <= 45:
                        cand = min(p_fin, CORTE + dt.timedelta(days=rnd.randint(7, 40)))
                    else:
                        cand = min(p_fin, e + dt.timedelta(days=rnd.randint(14, 60)))
                    nueva = cand if cand > e else None
                elif e > CORTE and plan - real >= 6 and rnd.random() < 0.15:
                    cand = min(p_fin, e + dt.timedelta(days=rnd.randint(10, 30)))
                    nueva = cand if cand > e else None
            prioridad = rnd.choices(["Alta", "Media", "Baja"], [0.30, 0.50, 0.20])[0]
            aid = f"ACT-{n_act:04d}"
            filas.append([
                aid, pid, rnd.choice(equipo), nombre, estado, prioridad,
                s.isoformat(), e.isoformat(), nueva.isoformat() if nueva else "",
                real, upd.isoformat() if upd else "", bloqueo, prev["id"] if prev else "",
            ])
            prev = {"id": aid, "estado": estado, "real": real}
    return filas

# ------------------------------------------------------------------ flujo de fondos
def meses(ini, fin):
    y, m = ini.year, ini.month
    out = []
    while (y, m) <= (fin.year, fin.month):
        out.append(dt.date(y, m, 1))
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out

def generar_flujo():
    import math
    filas = []
    for (pid, _n, _d, _a, _t, _fa, _g, _l, _fo, ini_s, fin_s, aprobado, perfil, *_rest) in PROYECTOS:
        ms = meses(f(ini_s), f(fin_s))
        pesos = [math.sin(math.pi * (i + 0.5) / len(ms)) + 0.35 for i in range(len(ms))]
        total = aprobado * rnd.uniform(0.95, 1.05)
        rango = {"sano": (0.92, 1.05), "moderado": (0.85, 1.10), "critico": (0.60, 1.25)}[perfil]
        for mes, w in zip(ms, pesos):
            forecast = int(round(total * w / sum(pesos), -1))
            if mes < CORTE.replace(day=1):
                real = int(round(forecast * rnd.uniform(*rango), -1))
            elif mes == CORTE.replace(day=1):
                real = int(round(forecast * rnd.uniform(0.25, 0.45) * rnd.uniform(*rango), -1))
            else:
                real = ""
            if forecast % 1000 == 0:
                forecast += 10
            if real != "" and real % 1000 == 0:
                real += 10
            filas.append([pid, mes.isoformat(), forecast, real])
    return filas

# ------------------------------------------------------------------- solicitudes
TIPOS_SOL = {
    "Cambio de Alcance": 0.30,
    "Replanificación de Cronograma": 0.30,
    "Ajuste de Presupuesto": 0.25,
    "Cierre y Transición a Operaciones": 0.15,
}

def generar_solicitudes(actividades):
    por_proy = {p[0]: p for p in PROYECTOS}
    con_replan = {a[1] for a in actividades if a[8]}
    pedidos = []
    for p in PROYECTOS:
        pid = p[0]
        for _ in range(rnd.choice([1, 2, 2, 3])):
            tipo = rnd.choices(list(TIPOS_SOL), list(TIPOS_SOL.values()))[0]
            if tipo.startswith("Cierre") and pid not in ("INI-003", "INI-006", "INI-008"):
                tipo = "Cambio de Alcance"
            pedidos.append((pid, tipo))
    # Orden fijo (un set de textos varia entre ejecuciones de Python y haria cambiar los datos)
    orden_replan = ["INI-004", "INI-003", "INI-005", "INI-002"]
    for pid in sorted(con_replan, key=lambda x: (orden_replan.index(x), x) if x in orden_replan else (len(orden_replan), x)):
        if not any(x == (pid, "Replanificación de Cronograma") for x in pedidos):
            pedidos.append((pid, "Replanificación de Cronograma"))
    for pid in ("INI-003", "INI-006", "INI-008"):
        if not any(x == (pid, "Cierre y Transición a Operaciones") for x in pedidos):
            pedidos.append((pid, "Cierre y Transición a Operaciones"))
    filas = []
    for pid, tipo in pedidos:
        p = por_proy[pid]
        gerente, lider, focal = p[6], p[7], p[8]
        firmante = {"Ajuste de Presupuesto": gerente, "Cierre y Transición a Operaciones": gerente}.get(
            tipo, rnd.choice([lider, focal]))
        r = rnd.random()
        estado = "Pendiente de firma" if r < 0.37 else ("Firmada" if r < 0.92 else "Rechazada")
        if estado == "Pendiente de firma":
            ini = CORTE - dt.timedelta(days=rnd.randint(3, 45))
            res = ""
        else:
            ini = CORTE - dt.timedelta(days=rnd.randint(30, 170))
            res = (ini + dt.timedelta(days=rnd.randint(2, 30))).isoformat()
        ini = max(ini, f(p[9]) + dt.timedelta(days=15))
        if res and f(res) < ini:
            res = (ini + dt.timedelta(days=rnd.randint(2, 20))).isoformat()
        if res and f(res) > CORTE:
            estado, res = "Pendiente de firma", ""
        filas.append([pid, tipo, firmante, ini.isoformat(), res, estado])
    filas.sort(key=lambda x: (x[3], x[0]))
    return [[f"SOL-{i + 1:04d}"] + fila for i, fila in enumerate(filas)]

# ------------------------------------------------------------- equilibrio para la demo
def _sem(desvio):
    return "V" if desvio <= 5 else ("A" if desvio <= 9 else "R")

def equilibrado(act):
    """Criterios de representacion ejecutiva (ver docs/spec.md): semaforos y estados con variedad."""
    n = len(act)
    sem = {"V": 0, "A": 0, "R": 0}
    por_ini = {}
    for a in act:
        plan = int(pct_plan(f(a[6]), f(a[7])) + 0.5)
        sem[_sem(max(0, plan - a[9]))] += 1
        acc = por_ini.setdefault(a[1], [0, 0, 0])
        acc[0] += a[9]; acc[1] += plan; acc[2] += 1
    sem_ini = {"V": 0, "A": 0, "R": 0}
    for real, plan, c in por_ini.values():
        sem_ini[_sem(int(max(0, plan / c - real / c) + 0.5))] += 1
    estados = {}
    for a in act:
        estados[a[4]] = estados.get(a[4], 0) + 1
    return (sem["A"] >= 0.07 * n and 0.12 * n <= sem["R"] <= 0.25 * n
            and sem_ini["V"] >= 4 and sem_ini["A"] >= 2 and sem_ini["R"] >= 2
            and estados.get("En Revisión", 0) >= 0.06 * n and estados.get("Bloqueado", 0) >= 5
            and any(a[10] == "" and a[4] not in ("Pendiente", "Completado") for a in act))

# --------------------------------------------------------------------------- main
def main():
    print(f"Generando datos ficticios (semilla base {SEMILLA}, corte {CORTE.isoformat()}) en {SALIDA}")
    for intento in range(1, 2000):
        rnd.seed(SEMILLA + intento)
        act = generar_actividades()
        if equilibrado(act):
            break
    else:
        raise SystemExit("No se encontro una variante equilibrada")
    print(f"  variante equilibrada: intento {intento} (semilla {SEMILLA + intento})")
    escribir("dim_persona.csv", ["id_persona", "nombre_completo", "rol", "area"], PERSONAS)
    escribir("dim_proyecto.csv",
             ["id_proyecto", "nombre", "descripcion", "area", "tipo_ia", "fase", "id_sponsor", "id_lider",
              "id_coordinador_portafolio", "fecha_inicio", "fecha_fin", "presupuesto_aprobado_usd"],
             [[p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11]] for p in PROYECTOS])
    escribir("fact_actividades.csv",
             ["id_actividad", "id_proyecto", "id_responsable", "nombre", "estado", "prioridad", "fecha_inicio",
              "fecha_fin", "nueva_fecha_fin", "av_real", "fecha_actualizacion", "motivo_bloqueo",
              "id_predecesora"], act)
    escribir("fact_flujo_fondos.csv", ["id_proyecto", "mes", "forecast_usd", "real_usd"], generar_flujo())
    escribir("fact_solicitudes.csv",
             ["id_solicitud", "id_proyecto", "tipo", "id_firmante", "fecha_creacion", "fecha_resolucion", "estado"],
             generar_solicitudes(act))

if __name__ == "__main__":
    main()