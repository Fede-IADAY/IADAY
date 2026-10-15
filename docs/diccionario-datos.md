# Diccionario de datos

Formato de todos los CSV: UTF-8, separador coma, fechas ISO `AAAA-MM-DD`, decimal con punto, vacío = sin valor.
Todos los datos son **ficticios**.

## dim_proyecto (iniciativas de IA)
| Campo | Tipo | Nulo | Descripción | Dominio / ejemplo |
|---|---|---|---|---|
| `id_proyecto` | Texto | No | Identificador de la iniciativa (PK) | `INI-001` |
| `nombre` | Texto | No | Nombre de la iniciativa | `Asistente IA RRHH` |
| `descripcion` | Texto | No | Descripción breve | – |
| `area` | Texto | No | Área de negocio | Personas, Tecnología, Finanzas, Datos, Comercial, Operaciones |
| `tipo_ia` | Texto | No | Tipo de solución de IA | Generativa, Predictiva, Automatización |
| `fase` | Texto | No | Fase actual | Piloto, Desarrollo, Despliegue |
| `id_sponsor` | Texto | No | FK → `dim_persona` (rol Sponsor Ejecutivo) | `PER-001` |
| `id_lider` | Texto | No | FK → `dim_persona` (rol Líder de Iniciativa) | `PER-006` |
| `id_coordinador_portafolio` | Texto | No | FK → `dim_persona` (rol Coordinador de Portafolio IA) | `PER-004` |
| `fecha_inicio` | Fecha | No | Inicio planificado | `2026-03-02` |
| `fecha_fin` | Fecha | No | Fin planificado | `2026-12-18` |
| `presupuesto_aprobado_usd` | Entero | No | Presupuesto aprobado en USD (50.000–2.000.000) | – |

## dim_persona
| Campo | Tipo | Nulo | Descripción | Dominio |
|---|---|---|---|---|
| `id_persona` | Texto | No | PK | `PER-001` |
| `nombre_completo` | Texto | No | Nombre ficticio | – |
| `rol` | Texto | No | Rol en el proyecto | Sponsor Ejecutivo, Líder de Iniciativa, Responsable de Actividad, Coordinador de Portafolio IA |
| `area` | Texto | No | Área de pertenencia | – |

## fact_actividades
| Campo | Tipo | Nulo | Descripción | Dominio / regla |
|---|---|---|---|---|
| `id_actividad` | Texto | No | PK | `ACT-0001` |
| `id_proyecto` | Texto | No | FK → `dim_proyecto` | – |
| `id_responsable` | Texto | No | FK → `dim_persona` (rol Responsable de Actividad) | – |
| `nombre` | Texto | No | Nombre de la actividad | – |
| `estado` | Texto | No | Estado (R1) | Pendiente, En Curso, En Revisión, Completado, Bloqueado |
| `prioridad` | Texto | No | Prioridad | Alta, Media, Baja |
| `fecha_inicio` | Fecha | No | Inicio planificado | – |
| `fecha_fin` | Fecha | No | Fin planificado original | > `fecha_inicio` |
| `nueva_fecha_fin` | Fecha | Sí | Fin reprogramado | > `fecha_fin`; solo si se reprogramó |
| `av_real` | Entero | No | Avance real, 0–100 | 100 solo si Completado |
| `fecha_actualizacion` | Fecha | Sí | Última actualización del estado | Vacío si no iniciada o sin actualizar |
| `motivo_bloqueo` | Texto | Sí | Motivo del bloqueo | Solo si Bloqueado |
| `id_predecesora` | Texto | Sí | FK → `fact_actividades` (misma iniciativa): actividad de la que depende. Vacío en la primera de cada iniciativa | Ver reglas de dependencia en `docs/modelo-datos.md` |

**Campos calculados en el modelo (no están en el CSV):** `Fin Efectivo`, `Avance Planificado` (R2), `Desvío` (R3),
`Semáforo` (R4), `Días sin Actualizar` y `Semáforo Actualización` (R8). Fórmulas en `docs/kpis.md`.

**En `dim_proyecto` el modelo agrega** las columnas calculadas `Sponsor Ejecutivo`, `Líder de Iniciativa` y `Coordinador de Portafolio IA` (nombres obtenidos de `dim_persona`).

## fact_flujo_fondos
| Campo | Tipo | Nulo | Descripción | Regla |
|---|---|---|---|---|
| `id_proyecto` | Texto | No | FK → `dim_proyecto` | – |
| `mes` | Fecha | No | Primer día del mes | Un registro por iniciativa y mes |
| `forecast_usd` | Entero | No | Gasto previsto del mes (USD) | – |
| `real_usd` | Entero | Sí | Gasto real del mes (USD) | Vacío solo para meses posteriores al corte; el mes de corte (octubre 2026) es parcial |

## fact_solicitudes
| Campo | Tipo | Nulo | Descripción | Dominio |
|---|---|---|---|---|
| `id_solicitud` | Texto | No | PK | `SOL-0001` |
| `id_proyecto` | Texto | No | FK → `dim_proyecto` | – |
| `tipo` | Texto | No | Tipo de solicitud | Cambio de Alcance, Replanificación de Cronograma, Ajuste de Presupuesto, Cierre y Transición a Operaciones |
| `id_firmante` | Texto | No | FK → `dim_persona` | – |
| `fecha_creacion` | Fecha | No | Alta de la solicitud | ≤ corte |
| `fecha_resolucion` | Fecha | Sí | Fecha de firma o rechazo | Vacío si está pendiente |
| `estado` | Texto | No | Estado de la solicitud | Pendiente de firma, Firmada, Rechazada |

Los días de firma se calculan en el modelo (`Días de Firma`): resolución − creación (resueltas) o corte − creación (pendientes).
El semáforo de firma (`Semáforo Firma`, regla S7) es: Verde ≤ 15 días, Amarillo de 16 a 30, Rojo > 30.
