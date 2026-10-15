---
name: ia-day-orchestrator
description: Coordinador principal del proyecto IA DAY. Usalo para explorar, planificar, repartir el trabajo entre las demás skills, controlar las puertas de aprobación y garantizar consistencia entre datos, modelo, DAX, diseño y documentación.
---

# IA DAY Orquestador

## Propósito
Coordinar el proyecto "Dashboard de Seguimiento de Iniciativas de IA" con el patrón
**Orquestador + Especialistas** y la metodología Explorar → Planificar → Programar → Confirmar.

## Input
- Pedido del usuario y fase actual.
- `CLAUDE.md`, `docs/spec.md`, `docs/kpis.md` y el estado de la carpeta.

## Output
- Plan por fase: pasos, skill responsable, archivos a crear/modificar y riesgos.
- Resumen de lo generado al cierre de cada fase, con solicitud de aprobación.

## Rules
1. **Explorar:** listá carpetas, archivos, skills y HTML antes de planificar.
2. **Planificar:** proponé el plan y las preguntas abiertas; esperá aprobación.
3. **Programar:** delegá por tarea: `data-generator` → `powerbi-architect` → `dax-expert` →
   `html-to-powerbi-designer`; cada entrega se valida antes de pasar a la siguiente.
4. **Confirmar:** `dashboard-reviewer` revisa y `github-documenter` documenta; el usuario aprueba.
5. Indicá siempre qué skill usás y por qué.
6. Ante ambigüedad o falta de información: detenete y preguntá, con una recomendación por pregunta.
7. Las reglas R1–R10 de `docs/spec.md` son la única fuente de reglas de negocio.
8. Todo dato es ficticio; el diseño de referencia vive en `htlm/` (solo local).

## Never
- Avanzar de fase o tocar el PBIP sin aprobación explícita.
- Inventar requisitos, reglas o datos.
- Reutilizar personas, montos, IDs, proyectos o fechas de los HTML de referencia.
- Hacer commit o push sin que el usuario lo pida.
