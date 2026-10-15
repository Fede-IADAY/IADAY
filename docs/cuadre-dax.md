# Cuadre de medidas DAX contra el validador

> Generado por `scripts/cuadrar_dax.ps1`. Fecha de corte: **09/10/2026**. Esperado = `scripts/validar_kpis.py`; DAX = medidas del modelo `IADAY.SemanticModel`.

**Resultado: CUADRA** — 107/107 comparaciones correctas.

| Ámbito | Medida | Esperado (validador) | Obtenido (DAX) | OK |
|---|---|---|---|---|
| Global | Total Actividades | 170 | 170 | ✅ |
| Global | Completadas | 65 | 65 | ✅ |
| Global | Bloqueadas | 6 | 6 | ✅ |
| Global | En Curso | 43 | 43 | ✅ |
| Global | En Revisión | 11 | 11 | ✅ |
| Global | Pendientes | 45 | 45 | ✅ |
| Global | % Avance Real | 0.530765 | 0.530765 | ✅ |
| Global | % Avance Planificado | 0.615412 | 0.615412 | ✅ |
| Global | Desvío Global | 8.464706 | 8.464706 | ✅ |
| Global | Actividades Verde | 118 | 118 | ✅ |
| Global | Actividades Amarillo | 12 | 12 | ✅ |
| Global | Actividades Rojo | 40 | 40 | ✅ |
| Global | Vencidas | 17 | 17 | ✅ |
| Global | Por Vencer 60 | 37 | 37 | ✅ |
| Global | Por Vencer 30 | 19 | 19 | ✅ |
| Global | Por Vencer 31-60 | 18 | 18 | ✅ |
| Global | Actividades En Plazo | 51 | 51 | ✅ |
| Global | Días de Atraso Promedio | 27.294118 | 27.294118 | ✅ |
| Global | Actividades Evaluables Actualización | 60 | 60 | ✅ |
| Global | Actualización Verde | 33 | 33 | ✅ |
| Global | Actualización Amarillo | 13 | 13 | ✅ |
| Global | Actualización Rojo | 14 | 14 | ✅ |
| Global | Sin Fecha de Actualización | 2 | 2 | ✅ |
| Global | Presupuesto Aprobado | 7191940 | 7191940 | ✅ |
| Global | Forecast Total | 7085630 | 7085630 | ✅ |
| Global | Real Total | 4055980 | 4055980 | ✅ |
| Global | Pendiente | 3029650 | 3029650 | ✅ |
| Global | % Ejecución | 0.572423 | 0.572423 | ✅ |
| Global | Forecast Meses Cerrados | 4011430 | 4011430 | ✅ |
| Global | Real Meses Cerrados | 3791410 | 3791410 | ✅ |
| Global | % Cumplimiento Meses Cerrados | 0.945152 | 0.945152 | ✅ |
| Global | % Inversión Ejecutada | 0.563962 | 0.563962 | ✅ |
| Global | Total Solicitudes | 26 | 26 | ✅ |
| Global | Solicitudes Abiertas | 10 | 10 | ✅ |
| Global | Días Promedio Abiertas | 26.1 | 26.1 | ✅ |
| Global | Solicitudes Verde | 10 | 10 | ✅ |
| Global | Solicitudes Amarillo | 12 | 12 | ✅ |
| Global | Solicitudes Rojo | 4 | 4 | ✅ |
| Global | Abiertas Verde | 2 | 2 | ✅ |
| Global | Abiertas Amarillo | 4 | 4 | ✅ |
| Global | Abiertas Rojo | 4 | 4 | ✅ |
| INI-001 | Total Actividades | 16 | 16 | ✅ |
| INI-001 | Completadas | 11 | 11 | ✅ |
| INI-001 | Bloqueadas | 0 | 0 | ✅ |
| INI-001 | Vencidas | 0 | 0 | ✅ |
| INI-001 | Desvío Global | 1 | 1 | ✅ |
| INI-001 | Semáforo Iniciativa | Verde | Verde | ✅ |
| INI-002 | Total Actividades | 19 | 19 | ✅ |
| INI-002 | Completadas | 7 | 7 | ✅ |
| INI-002 | Bloqueadas | 0 | 0 | ✅ |
| INI-002 | Vencidas | 1 | 1 | ✅ |
| INI-002 | Desvío Global | 3.368421 | 3.368421 | ✅ |
| INI-002 | Semáforo Iniciativa | Verde | Verde | ✅ |
| INI-003 | Total Actividades | 14 | 14 | ✅ |
| INI-003 | Completadas | 8 | 8 | ✅ |
| INI-003 | Bloqueadas | 0 | 0 | ✅ |
| INI-003 | Vencidas | 1 | 1 | ✅ |
| INI-003 | Desvío Global | 9.571429 | 9.571429 | ✅ |
| INI-003 | Semáforo Iniciativa | Rojo | Rojo | ✅ |
| INI-004 | Total Actividades | 17 | 17 | ✅ |
| INI-004 | Completadas | 2 | 2 | ✅ |
| INI-004 | Bloqueadas | 2 | 2 | ✅ |
| INI-004 | Vencidas | 4 | 4 | ✅ |
| INI-004 | Desvío Global | 20.176471 | 20.176471 | ✅ |
| INI-004 | Semáforo Iniciativa | Rojo | Rojo | ✅ |
| INI-005 | Total Actividades | 16 | 16 | ✅ |
| INI-005 | Completadas | 7 | 7 | ✅ |
| INI-005 | Bloqueadas | 0 | 0 | ✅ |
| INI-005 | Vencidas | 1 | 1 | ✅ |
| INI-005 | Desvío Global | 4.1875 | 4.1875 | ✅ |
| INI-005 | Semáforo Iniciativa | Verde | Verde | ✅ |
| INI-006 | Total Actividades | 13 | 13 | ✅ |
| INI-006 | Completadas | 7 | 7 | ✅ |
| INI-006 | Bloqueadas | 1 | 1 | ✅ |
| INI-006 | Vencidas | 3 | 3 | ✅ |
| INI-006 | Desvío Global | 9.461538 | 9.461538 | ✅ |
| INI-006 | Semáforo Iniciativa | Amarillo | Amarillo | ✅ |
| INI-007 | Total Actividades | 18 | 18 | ✅ |
| INI-007 | Completadas | 4 | 4 | ✅ |
| INI-007 | Bloqueadas | 1 | 1 | ✅ |
| INI-007 | Vencidas | 1 | 1 | ✅ |
| INI-007 | Desvío Global | 2.555556 | 2.555556 | ✅ |
| INI-007 | Semáforo Iniciativa | Verde | Verde | ✅ |
| INI-008 | Total Actividades | 15 | 15 | ✅ |
| INI-008 | Completadas | 8 | 8 | ✅ |
| INI-008 | Bloqueadas | 0 | 0 | ✅ |
| INI-008 | Vencidas | 4 | 4 | ✅ |
| INI-008 | Desvío Global | 32.066667 | 32.066667 | ✅ |
| INI-008 | Semáforo Iniciativa | Rojo | Rojo | ✅ |
| INI-009 | Total Actividades | 15 | 15 | ✅ |
| INI-009 | Completadas | 7 | 7 | ✅ |
| INI-009 | Bloqueadas | 0 | 0 | ✅ |
| INI-009 | Vencidas | 0 | 0 | ✅ |
| INI-009 | Desvío Global | 2.466667 | 2.466667 | ✅ |
| INI-009 | Semáforo Iniciativa | Verde | Verde | ✅ |
| INI-010 | Total Actividades | 12 | 12 | ✅ |
| INI-010 | Completadas | 4 | 4 | ✅ |
| INI-010 | Bloqueadas | 2 | 2 | ✅ |
| INI-010 | Vencidas | 2 | 2 | ✅ |
| INI-010 | Desvío Global | 7.583333 | 7.583333 | ✅ |
| INI-010 | Semáforo Iniciativa | Amarillo | Amarillo | ✅ |
| INI-011 | Total Actividades | 15 | 15 | ✅ |
| INI-011 | Completadas | 0 | 0 | ✅ |
| INI-011 | Bloqueadas | 0 | 0 | ✅ |
| INI-011 | Vencidas | 0 | 0 | ✅ |
| INI-011 | Desvío Global | 2.466667 | 2.466667 | ✅ |
| INI-011 | Semáforo Iniciativa | Verde | Verde | ✅ |
