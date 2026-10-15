# Especificación funcional – Dashboard de Seguimiento de Iniciativas de IA

> Estado: **aprobada para generación de datos y documentación**. El PBIP y las páginas se construyen en la fase siguiente, con aprobación previa.

## 1. Objetivo
Reemplazar el reporte manual de seguimiento con un dashboard ejecutivo en Power BI que muestre, de forma
consistente y auditable, el estado, los riesgos, los vencimientos, la actualización de la información y la
ejecución del presupuesto de las iniciativas de Inteligencia Artificial de IA DAY.

## 2. Alcance
**Incluye**
- 11 iniciativas de IA ficticias y 170 actividades, con flujo de fondos y solicitudes de cambio.
- Modelo semántico con medidas DAX documentadas.
- Reporte de 5 páginas con identidad visual IA DAY.
- Dataset generado por IA (reproducible), documentación y estructura lista para GitHub.

**No incluye**
- Datos reales ni conexión a sistemas productivos.
- Versión web (sin Vercel ni Railway).
- Selector de idioma (todo en español).
- Escritura de vuelta ni actualización en tiempo real.

## 3. Decisiones aprobadas
| Tema | Decisión |
|---|---|
| Nivel de datos | Modelo mixto: iniciativas + actividades |
| Idioma | Solo español |
| Formato del reporte | Se autoriza convertir a PBIR (el enfoque más estable y compatible con GitHub) |
| Paleta | La del dashboard de referencia (azul oscuro, ámbar, verde, rojo), adaptada a IA DAY |
| Entregable | PBIP + GitHub + documentación + dataset. Sin web |
| `fact_solicitudes` | Incluida como tabla de soporte |
| Repositorio | Público, `IADAY`; sin commits todavía |
| Skills | Copiadas a `.claude/skills/` con name, description, input, output, rules y never |
| Archivo de flujo de fondos | `fact_flujo_fondos.csv` |
| Personas | Una única `dim_persona` con los roles Sponsor Ejecutivo, Líder de Iniciativa, Responsable de Actividad y Coordinador de Portafolio IA |
| Nomenclatura PMO | "Focal PMO" pasa a **Coordinador de Portafolio IA**; Gerente → Sponsor Ejecutivo; Líder → Líder de Iniciativa; Responsable → Responsable de Actividad |
| Realismo de datos | Dependencias lógicas entre actividades, mayor presencia de "En Revisión" y semáforos equilibrados para la demo |
| Moneda y fecha de corte | USD; 09/10/2026 |

## 4. Reglas de negocio aprobadas (R1–R10)
| # | Regla |
|---|---|
| R1 | Estados de actividad: Pendiente, En Curso, En Revisión, Completado, Bloqueado |
| R2 | Avance planificado: lineal entre fecha de inicio y de fin, al corte, con tope de 0 a 100 |
| R3 | Desvío = max(0, planificado − real), en puntos porcentuales |
| R4 | Semáforo por desvío: Verde 0–5, Amarillo 6–9, Rojo ≥ 10 |
| R5 | Avance de la iniciativa = promedio simple de sus actividades |
| R6 | Vencida: fin efectivo ≤ corte y estado distinto de Completado. Fin efectivo = la mayor entre `fecha_fin` y `nueva_fecha_fin` |
| R7 | Por vencer: vence en 1–60 días; subconteos de 30 y 60 días |
| R8 | Actualización atrasada: ≤ 7 días verde, 8–14 amarillo, > 14 o sin fecha rojo. No se evalúan actividades no iniciadas |
| R9 | Flujo de fondos: forecast y real por mes; % ejecución = real / forecast; pendiente = forecast − real |
| R10 | Moneda USD |
| R11 (S7) | Semáforo de solicitudes por días de firma: Verde ≤ 15 días, Amarillo > 15 y ≤ 30, Rojo > 30 (misma lógica que el dashboard de referencia). Días de firma = resolución − creación; si está abierta, corte − creación |

**Supuestos de interpretación:** ver `docs/kpis.md`, sección "Supuestos de interpretación" (S1 a S9 confirmados).

## 5. Páginas
| # | Página | Contenido principal |
|---|---|---|
| 0 | Portada | Página de inicio: fondo gráfico a pantalla completa, logotipo, título "IA DAY 2026" y menú de navegación hacia las 5 páginas |
| 1 | Resumen Ejecutivo | KPIs globales (total, completadas, bloqueadas, vencidas, % avance real vs. planificado), distribución del semáforo, estado por iniciativa y ejecución presupuestaria |
| 2 | Riesgos y Desvíos | Actividades e iniciativas ordenadas por desvío; bloqueadas con su motivo |
| 3 | Vencidos y Por Vencer | Vencidas, por vencer a 30 y 60 días, con días de atraso o restantes |
| 4 | Actualización Atrasada | Frescura del estado por responsable e iniciativa; sin fecha |
| 5 | Flujo de Fondos | Forecast contra real por mes e iniciativa; pendiente y % de ejecución |

Todas comparten cabecera, fecha de corte visible, navegación superior, filtros (semáforo, área, iniciativa,
responsable, estado) y botón "Limpiar". `fact_solicitudes` alimenta un detalle de apoyo (por ejemplo, en
Riesgos y Desvíos); la ubicación exacta se define en el diseño.

## 6. Identidad visual
- Base del dashboard de referencia: azul oscuro (`#0d1b2a` / `#1b3a5c`), ámbar `#e8a020`, fondo gris claro, tarjetas blancas.
- Semáforos: verde, amarillo/ámbar y rojo, con el mismo significado en todo el reporte.
- Adaptación IA DAY, inspirada en la charla: etiquetas tipo `[ IA DAY // SEGUIMIENTO ]`, tipografía moderna
  (la charla usa Plus Jakarta Sans y JetBrains Mono; en Power BI se usan Segoe UI y Consolas como alternativa segura).

## 7. Casos de uso
1. El directorio ve la salud global de la cartera de IA en menos de 10 segundos.
2. El PMO detecta qué responsables no actualizaron su información.
3. Un sponsor ejecutivo revisa las actividades vencidas, bloqueadas y por vencer de sus iniciativas.
4. Finanzas compara el forecast con lo ejecutado por iniciativa y mes.

## 8. Beneficios
Una única fuente de verdad, sin armado manual, con reglas explícitas, reproducible y trazable.

## 9. Criterios de aceptación
- [ ] Los KPIs de la portada coinciden con `docs/validacion-kpis.md`.
- [ ] Cada medida DAX tiene su regla, fórmula y tablas documentadas en `docs/kpis.md`.
- [ ] Los filtros funcionan en las 5 páginas y la fecha de corte es visible.
- [ ] Los datos son 100% ficticios y ninguno proviene del HTML de referencia (chequeo automático).
- [ ] No hay claves ni archivos locales en el repositorio.
- [ ] El README explica cómo abrir, regenerar y validar el proyecto.
- [ ] `dashboard-reviewer` entrega un informe sin hallazgos críticos abiertos.
- [ ] El proyecto abre en Power BI Desktop sin errores.

## 10. Estado de las fases
| Fase | Estado |
|---|---|
| Explorar | ✅ Completa |
| Planificar | ✅ Aprobada |
| Programar – documentación, skills, datos y validación | ✅ Aprobado |
| Programar – PBIR, modelo semántico, relaciones, calendario, parámetros y medidas DAX | ✅ Hecho (pendiente de aprobación; ver `docs/cuadre-dax.md`) |
| Programar – páginas visuales del reporte | ✅ Construidas y revisadas (ver `docs/qa-visual.md`) |
| Programar – portada de inicio | ✅ Construida y probada |
| Confirmar – preparación del repositorio (rutas locales neutralizadas, `.gitignore`, README) | ✅ Hecha; publicación a la espera de la aprobación final |
| Confirmar – publicación en GitHub | ⏳ Pendiente |
