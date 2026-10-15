# Validación de datos y KPIs

> Generado por `scripts/validar_kpis.py`. Fecha de corte: **09/10/2026**. Este documento es la **referencia contra la que se cuadran las medidas DAX**.

**Resultado: APROBADO** — 48/48 chequeos correctos.

## 1. Chequeos

| # | Chequeo | Resultado | Detalle |
|---|---|---|---|
| 1 | Iniciativas entre 10 y 12 | ✅ | 11 |
| 2 | Actividades entre 150 y 200 | ✅ | 170 |
| 3 | IDs únicos (proyecto, persona, actividad, solicitud) | ✅ |  |
| 4 | Roles de dim_persona válidos | ✅ |  |
| 5 | Sponsor, Líder y Coordinador de Portafolio de cada iniciativa existen con el rol correcto | ✅ |  |
| 6 | fact_actividades: proyecto y responsable existen (rol Responsable) | ✅ |  |
| 7 | fact_flujo_fondos: proyectos existen | ✅ |  |
| 8 | fact_solicitudes: proyecto y firmante existen | ✅ |  |
| 9 | Estados de actividad válidos (R1) | ✅ |  |
| 10 | Tipos y estados de solicitud válidos | ✅ |  |
| 11 | Todas las iniciativas tienen actividades | ✅ |  |
| 12 | Coherencia de actividades: inicio < fin | ✅ |  |
| 13 | Coherencia de actividades: actividad dentro de la ventana de la iniciativa | ✅ |  |
| 14 | Coherencia de actividades: nueva_fecha_fin posterior a fecha_fin | ✅ |  |
| 15 | Coherencia de actividades: av_real entre 0 y 100 | ✅ |  |
| 16 | Coherencia de actividades: Completado implica av_real = 100 | ✅ |  |
| 17 | Coherencia de actividades: av_real = 100 solo si Completado | ✅ |  |
| 18 | Coherencia de actividades: Pendiente implica av 0, inicio futuro y sin actualización | ✅ |  |
| 19 | Coherencia de actividades: inicio futuro solo si Pendiente | ✅ |  |
| 20 | Coherencia de actividades: fecha_actualizacion entre inicio y corte | ✅ |  |
| 21 | Coherencia de actividades: motivo_bloqueo solo si Bloqueado | ✅ |  |
| 22 | Coherencia de actividades: Completado tiene fecha de actualización | ✅ |  |
| 23 | Dependencias: la primera actividad no tiene predecesora | ✅ |  |
| 24 | Dependencias: predecesora existente, de la misma iniciativa y anterior | ✅ |  |
| 25 | Dependencias: Completado exige predecesora Completada | ✅ |  |
| 26 | Dependencias: no se inicia con predecesora Pendiente | ✅ |  |
| 27 | Dependencias: el avance no supera al de una predecesora incompleta | ✅ |  |
| 28 | Dependencias: las fechas no retroceden respecto de la predecesora | ✅ |  |
| 29 | Proyectos: inicio < fin | ✅ |  |
| 30 | Presupuesto aprobado en rango USD 50.000-2.000.000 | ✅ |  |
| 31 | Flujo de fondos: real vacío solo para meses posteriores al corte | ✅ |  |
| 32 | Flujo de fondos: un registro por proyecto y mes | ✅ |  |
| 33 | Forecast total entre 93% y 107% del presupuesto aprobado por iniciativa | ✅ |  |
| 34 | Solicitudes: fechas coherentes y estado consistente con resolución | ✅ |  |
| 35 | Cada iniciativa con reprogramaciones tiene una solicitud de cronograma | ✅ |  |
| 36 | KPI: Verde + Amarillo + Rojo = Total actividades | ✅ |  |
| 37 | KPI: Vencidas y Por vencer son disjuntas | ✅ |  |
| 38 | KPI: Vencidas nunca Completadas | ✅ |  |
| 39 | KPI: Actualización Verde + Amarillo + Rojo = actividades evaluables | ✅ |  |
| 40 | KPI: hay casos de cada tipo (verde, amarillo, rojo, vencida, por vencer, bloqueada, sin fecha) | ✅ |  |
| 41 | KPI: hay actividades reprogramadas, vencidas y no vencidas por reprogramación | ✅ |  |
| 42 | Cartera con variedad: al menos 2 colores de semáforo a nivel iniciativa | ✅ | {'Verde': 6, 'Rojo': 3, 'Amarillo': 2} |
| 43 | Equilibrio (demo): cada color de semáforo de iniciativa aparece al menos 2 veces | ✅ | {'Verde': 6, 'Rojo': 3, 'Amarillo': 2} |
| 44 | Equilibrio (demo): entre 15% y 35% de las actividades no están en verde | ✅ | 30.6% |
| 45 | Equilibrio (demo): amarillo y rojo con al menos 5% cada uno | ✅ | amarillo 7.1%, rojo 23.5% |
| 46 | Equilibrio (demo): 'En Revisión' representa al menos 5% de las actividades | ✅ | 11 (6.5%) |
| 47 | Solicitudes: el semáforo de firma (S7) cubre todas las solicitudes | ✅ |  |
| 48 | Sin reutilización de datos del HTML de referencia (personas, proyectos, montos, IDs) | ✅ | coincidencias: personas=0, proyectos=0, montos=0, ids=0 |

## 2. Volúmenes

| Tabla | Filas |
|---|---|
| dim_persona | 21 |
| dim_proyecto | 11 |
| fact_actividades | 170 |
| fact_flujo_fondos | 114 |
| fact_solicitudes | 26 |

## 3. KPIs de actividades (cartera completa)

| KPI | Valor |
|---|---|
| Total actividades | 170 |
| Completadas | 65 |
| Bloqueadas | 6 |
| Vencidas (R6) | 17 |
| Por vencer en 60 días (R7) | 37 |
| Por vencer en 30 días (R7) | 19 |
| Por vencer en 31 a 60 días (R7) | 18 |
| En plazo (más de 60 días, no Completadas) | 51 |
| Días promedio de atraso de las vencidas (R6) | 27.3 |
| % Avance real (promedio simple, R5) | 53.08% |
| % Avance planificado (promedio simple, R2) | 61.54% |
| Desvío global (R3) | 8.46 pp |
| Semáforo Verde / Amarillo / Rojo (R4) | 118 / 12 / 40 |
| Actividades evaluables para actualización (R8) | 60 |
| Actualización Verde / Amarillo / Rojo (R8) | 33 / 13 / 14 |
| …de las cuales sin fecha de actualización | 2 |

## 4. Por iniciativa

| Id | Iniciativa | Act. | Compl. | Bloq. | Venc. | % Real | % Plan | Desvío | Semáforo |
|---|---|---|---|---|---|---|---|---|---|
| INI-001 | Asistente IA RRHH | 16 | 11 | 0 | 0 | 73.3% | 74.3% | 1.0 | Verde |
| INI-002 | Copilot Corporativo | 19 | 7 | 0 | 1 | 51.3% | 54.7% | 3.4 | Verde |
| INI-003 | Automatización de Reportes | 14 | 8 | 0 | 1 | 72.7% | 82.3% | 9.6 | Rojo |
| INI-004 | Data Quality IA | 17 | 2 | 2 | 4 | 34.9% | 55.1% | 20.2 | Rojo |
| INI-005 | Forecast Inteligente | 16 | 7 | 0 | 1 | 58.4% | 62.6% | 4.2 | Verde |
| INI-006 | Procesamiento Documental | 13 | 7 | 1 | 3 | 82.1% | 91.5% | 9.5 | Amarillo |
| INI-007 | Chat Corporativo IA | 18 | 4 | 1 | 1 | 38.7% | 41.2% | 2.6 | Verde |
| INI-008 | Analítica Predictiva | 15 | 8 | 0 | 4 | 63.1% | 95.2% | 32.1 | Rojo |
| INI-009 | Clasificación Inteligente de Tickets | 15 | 7 | 0 | 0 | 51.8% | 54.3% | 2.5 | Verde |
| INI-010 | Automatización Power BI | 12 | 4 | 2 | 2 | 54.8% | 62.4% | 7.6 | Amarillo |
| INI-011 | Agente de Conciliación Financiera | 15 | 0 | 0 | 0 | 12.3% | 14.7% | 2.5 | Verde |

## 5. Actualización atrasada por responsable (R8)

| Responsable | Evaluables | Verde | Amarillo | Rojo |
|---|---|---|---|---|
| Martina Castellanos Orozco | 7 | 4 | 0 | 3 |
| Antonella Rojas Sabaté | 9 | 5 | 1 | 3 |
| Joaquín Mansilla Peña | 4 | 2 | 0 | 2 |
| Lucía Berriozábal Sierra | 6 | 3 | 1 | 2 |
| Daniela Corrales Ugarte | 5 | 3 | 1 | 1 |
| Federico Alsina Montero | 5 | 3 | 1 | 1 |
| Ignacio Peralta Donoso | 4 | 3 | 0 | 1 |
| Paula Quintana Olivera | 11 | 3 | 7 | 1 |
| Gonzalo Villaseca Mora | 8 | 6 | 2 | 0 |
| Bruno Cabrera Lanzillotta | 1 | 1 | 0 | 0 |

## 6. Flujo de fondos (R9, USD)

| KPI | Valor |
|---|---|
| Presupuesto aprobado total | 7,191,940 |
| Forecast total | 7,085,630 |
| Real acumulado | 4,055,980 |
| Pendiente (forecast − real) | 3,029,650 |
| % Ejecución (real / forecast total) | 57.24% |
| Forecast de meses cerrados (hasta septiembre 2026) | 4,011,430 |
| Real de meses cerrados | 3,791,410 |
| % Cumplimiento de meses cerrados | 94.52% |
| % Inversión ejecutada (real / aprobado) | 56.40% |

## 7. Solicitudes

| KPI | Valor |
|---|---|
| Total solicitudes | 26 |
| Firmada | 12 |
| Pendiente de firma | 10 |
| Rechazada | 4 |
| Tipo: Ajuste de Presupuesto | 8 |
| Tipo: Cambio de Alcance | 9 |
| Tipo: Cierre y Transición a Operaciones | 3 |
| Tipo: Replanificación de Cronograma | 6 |
| Días promedio de las abiertas | 26.1 |
| Semáforo de firma, todas (Verde / Amarillo / Rojo) | 10 / 12 / 4 |
| Semáforo de firma, abiertas (Verde / Amarillo / Rojo) | 2 / 4 / 4 |

> Días de firma: resolución − creación en las resueltas; corte − creación en las abiertas. Umbrales (S7): ≤ 15 verde, 16–30 amarillo, > 30 rojo.

## 8. Supuestos usados en este cálculo

- R8 excluye actividades Completadas: **True**
- R7 excluye actividades Completadas: **True**
- R2 usa `fecha_fin` original (no la nueva): **True**
- Avance planificado redondeado al entero más cercano antes de calcular el desvío.
- Actividad no iniciada = `fecha_inicio` posterior a la fecha de corte.
