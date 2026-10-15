# Trazabilidad

Conecta cada regla, KPI y decisión con su origen y su verificación.
Los HTML de referencia aportan solo **lógica conceptual y diseño**; ningún dato.

## 1. Reglas de negocio
| Regla | Origen conceptual | Dónde se implementa | Verificación |
|---|---|---|---|
| R1 Estados | Skill `data-generator` | `fact_actividades.estado` | Validador (dominio) |
| R2 Avance planificado lineal | `av_estimado` del HTML (allí es un dato; aquí se calcula) | Columna `Avance Planificado` | Recálculo en `validar_kpis.py` |
| R3 Desvío | Campo `desvio` del HTML | Columna `Desvío` | Recálculo |
| R4 Semáforo | Campo `semaforo` del HTML (umbrales observados en sus datos) | Columna `Semáforo` | Recálculo; aprobado por el usuario |
| R5 Promedio simple | Avance global del HTML (promedio) | `% Avance Real` / `% Avance Planificado` | Recálculo |
| R6 Vencida | `esVencidoEstricto()`, `finEfectivo()` | `Fin Efectivo` y `Vencidas` | Recálculo |
| R7 Por vencer | `esPorVencer()` (1–60 días) | `Por Vencer 30/60` | Recálculo |
| R8 Actualización | `semFecha()`, `atrasadoActualizacion()`, `noIniciado()` | `Semáforo Actualización` | Recálculo |
| R9 Flujo de fondos | `FF_DATA` (forecast, real, pendiente) | Medidas de flujo | Recálculo |
| R10 USD | Decisión del usuario | Formato de medidas | Revisión |
| R11 (S7) Semáforo de solicitudes | `semFirma()` del HTML (≤ 15 verde, ≤ 30 amarillo, > 30 rojo); el usuario pidió replicar esa lógica | Columnas `Días de Firma` y `Semáforo Firma`; medidas `Solicitudes *` y `Abiertas *` | Recálculo y cuadre DAX |

## 2. Páginas y diseño
| Elemento del HTML de referencia | Equivalente en IA DAY | Página |
|---|---|---|
| Cabecera azul con título, fecha y badge | Cabecera con etiqueta IA DAY y fecha de corte | Todas |
| Pestañas con contadores | Barra de navegación superior con 5 páginas | Todas |
| Tarjetas de resumen (total, plazo, atención, desvío, vencidos) | Tarjetas de KPI con semáforo | 1 |
| Banda de avance real contra planificado | Tarjeta/medidor de avance | 1 |
| Banda de inversión ejecutada | Tarjeta de ejecución presupuestaria | 1, 5 |
| Tabla por gerente con 13 columnas | Matriz/tabla por iniciativa y actividad | 1, 2, 3 |
| Pestaña "Mayores Desvíos" | Página Riesgos y Desvíos | 2 |
| Pestañas "Vencidos" y "Por Vencer" | Página Vencidos y Por Vencer | 3 |
| Pestaña "Actualización Atrasada" | Página Actualización Atrasada | 4 |
| Pestaña "Flujo de Fondos" (filas desplegables) | Página Flujo de Fondos (jerarquía y drill) | 5 |
| Pestaña "Solicitudes" | Detalle de apoyo con `fact_solicitudes` | 2 (a definir) |
| Pestañas "Líderes" y "Responsables" | Fuera de las 5 páginas; sus campos quedan disponibles en el modelo | – |
| Filtros (semáforo, gerente, tipo, área, búsqueda, limpiar) | Segmentadores (sponsor ejecutivo, tipo de IA, área, coordinador de portafolio IA) y botón "Limpiar" | Todas |
| Selector ES/EN/PT | **No se implementa** (decisión del usuario) | – |

## 3. Relación con la charla IA DAY
| Práctica de la charla | Cómo se aplica |
|---|---|
| Spec antes del código | `docs/spec.md` aprobada antes de generar datos |
| `CLAUDE.md` con instrucciones fijas | `CLAUDE.md` en la raíz |
| Skills como recetas | 7 skills en `.claude/skills/` con input, output, rules y never |
| Orquestador + especialistas | `ia-day-orchestrator` coordina las demás |
| Humano en el circuito | Aprobación explícita entre fases y antes de tocar el PBIP |
| Trazabilidad ("cada punto con su cita") | Este documento y `docs/kpis.md` |
| "Si te falta un dato, preguntá antes de inventar" | Regla permanente; lista de supuestos en `docs/kpis.md` |
| Git básico (rama única, commits claros, preguntar antes de borrar) | Sección "Gestión de Git" de `CLAUDE.md` |
| Claves fuera del repo | `.gitignore` y sección "Seguridad" |

## 4. Decisiones del usuario (registro)
Tomadas el 09/10/2026: reglas R1–R10, idioma español, conversión a PBIR autorizada, paleta del dashboard de
referencia con identidad IA DAY, sin versión web, `fact_solicitudes` incluida, repositorio público
`IADAY` sin commits todavía, skills en `.claude/skills`, `fact_flujo_fondos.csv`, `dim_persona` única.

## 4b. Implementación del PBIP
| Elemento | Evidencia |
|---|---|
| Reporte convertido a PBIR | `IADAY.Report/definition/` (validado con `powerbi-report-author validate`: 0 errores, 0 advertencias). La "Página 1" vacía se conservó; las páginas finales siguen pendientes de aprobación |
| Modelo semántico (TMDL) | `IADAY.SemanticModel/definition/` (8 tablas, 9 relaciones, 1 parámetro, 44 medidas) |
| Medidas contra el recálculo | `scripts/cuadrar_dax.ps1` → `docs/cuadre-dax.md` (104 de 104 comparaciones correctas) |

## 4c. Páginas del reporte
| Evidencia | Detalle |
|---|---|
| Páginas | 5 páginas con 23 a 24 visuales cada una en IADAY.Report/definition/pages/ |
| Revisión visual | docs/qa-visual.md y capturas en docs/capturas/ |
| Tema | IADAY.Report/StaticResources/RegisteredResources/ (paleta azul, ámbar y semáforos) |

## 4d. Portada
| Elemento | Detalle |
|---|---|
| Página | `Portada`, primera del reporte y página activa al abrir |
| Fondo | `fotos de portada/Forma 3.png`, registrada como recurso del reporte y usada como fondo de página con ajuste "Fill" (cubre sin deformar) |
| Logotipo | `fotos de portada/flock_logo_2021_Isologotipo negro (2).png`, en la esquina superior izquierda sobre una placa blanca |
| Navegación | 5 botones con acción de navegación a cada página; efecto ámbar al pasar el cursor |
| Evidencia | `docs/capturas/0-portada.png` y prueba funcional de los 5 botones en Power BI Desktop |

## 5. Datos
| Aspecto | Evidencia |
|---|---|
| Origen | `scripts/generar_datos.py` (semilla 20261009, corte 09/10/2026) |
| Sin reutilización del HTML | Chequeo automático en `scripts/validar_kpis.py` (personas, proyectos, montos e IDs) |
| Valores de referencia de KPIs | `docs/validacion-kpis.md` |

## 6. Decisiones posteriores (09/10/2026)
| Decisión | Detalle |
|---|---|
| Nomenclatura | Focal PMO → Coordinador de Portafolio IA; Gerente → Sponsor Ejecutivo; Líder → Líder de Iniciativa; Responsable → Responsable de Actividad |
| Tabla de flujo de fondos | `factflujofondos` → `fact_flujo_fondos` |
| Realismo de datos | Dependencias lógicas (`id_predecesora`), mayor presencia de En Revisión y semáforos equilibrados |
| Supuestos | S4, S8 y S9 confirmados |
