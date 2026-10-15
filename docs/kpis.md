# KPIs y medidas DAX

> **Estado: implementado y cuadrado.** Las medidas viven en `IADAY.SemanticModel/definition/tables/Medidas.tmdl` y las columnas calculadas en las tablas de hechos y dimensiones.
> Cada medida se cuadra contra `docs/validacion-kpis.md` mediante `scripts/cuadrar_dax.ps1` (resultado en `docs/cuadre-dax.md`).
> Convención: `[Fecha Corte]` devuelve el parámetro `fecha_corte` (09/10/2026); nunca se usa `TODAY()`.

## 1. Supuestos de interpretación

Interpretaciones que no están en R1–R10. Los marcados como **Confirmado** fueron aprobados por el usuario.

| # | Supuesto | Estado |
|---|---|---|
| S1 | R2 usa la `fecha_fin` **original** (la nueva fecha solo afecta a R6 y R7) | ✅ Confirmado |
| S2 | El avance planificado se redondea al **entero** antes de calcular el desvío | ✅ Confirmado |
| S3 | R8 **no evalúa** actividades Completadas (además de las no iniciadas) | ✅ Confirmado |
| S4 | Una actividad "no iniciada" es la que tiene `fecha_inicio` posterior al corte (en los datos coincide con el estado Pendiente) | ✅ Confirmado |
| S5 | R7 **no incluye** actividades Completadas | ✅ Confirmado |
| S6 | Flujo de fondos: % ejecución sobre el forecast total; además se informa el cumplimiento de meses cerrados (anteriores al mes de corte) | ✅ Confirmado |
| S7 | **Semáforo de solicitudes (días de firma):** Verde ≤ 15 días, Amarillo de 16 a 30 días, Rojo > 30 días. Misma lógica del dashboard de referencia | ✅ Confirmado (regla aprobada) |
| S8 | El semáforo de la iniciativa usa el desvío entre los promedios de avance (R5), redondeado a entero | ✅ Confirmado |
| S9 | Los tipos de solicitud usan nombres descriptivos propios | ✅ Confirmado |

### Regla del semáforo de solicitudes (S7)

- **Días de firma:** si la solicitud tiene `fecha_resolucion`, son los días entre la creación y la resolución; si está abierta (`Pendiente de firma`), son los días entre la creación y la fecha de corte.
- **Semáforo:** Verde ≤ 15, Amarillo > 15 y ≤ 30, Rojo > 30.
- **Implementación:** columnas `Días de Firma` y `Semáforo Firma` en `fact_solicitudes`; medidas `Solicitudes Verde/Amarillo/Rojo` (todas) y `Abiertas Verde/Amarillo/Rojo` (solo abiertas).

## 2. Columnas calculadas

### dim_proyecto[Sponsor Ejecutivo]

- **Objetivo:** Nombre del sponsor ejecutivo de la iniciativa (permite filtrar sin relación adicional con `dim_persona`).
- **Regla de negocio:** –
- **Tablas utilizadas:** `dim_proyecto`, `dim_persona`

```dax
LOOKUPVALUE ( dim_persona[nombre_completo], dim_persona[id_persona], dim_proyecto[id_sponsor] )
```

### dim_proyecto[Líder de Iniciativa]

- **Objetivo:** Nombre del líder de la iniciativa.
- **Regla de negocio:** –
- **Tablas utilizadas:** `dim_proyecto`, `dim_persona`

```dax
LOOKUPVALUE ( dim_persona[nombre_completo], dim_persona[id_persona], dim_proyecto[id_lider] )
```

### dim_proyecto[Coordinador de Portafolio IA]

- **Objetivo:** Nombre del coordinador de portafolio IA (PMO) de la iniciativa.
- **Regla de negocio:** –
- **Tablas utilizadas:** `dim_proyecto`, `dim_persona`

```dax
LOOKUPVALUE ( dim_persona[nombre_completo], dim_persona[id_persona], dim_proyecto[id_coordinador_portafolio] )
```

### fact_actividades[Fin Efectivo]

- **Objetivo:** Fecha de fin vigente de la actividad.
- **Regla de negocio:** R6: la mayor entre `fecha_fin` y `nueva_fecha_fin`
- **Tablas utilizadas:** `fact_actividades`

```dax
IF ( ISBLANK ( fact_actividades[nueva_fecha_fin] ),
     fact_actividades[fecha_fin],
     MAX ( fact_actividades[fecha_fin], fact_actividades[nueva_fecha_fin] ) )
```

### fact_actividades[Avance Planificado]

- **Objetivo:** Avance esperado al corte según el calendario.
- **Regla de negocio:** R2: lineal entre inicio y fin, tope 0–100, redondeado a entero (S1, S2)
- **Tablas utilizadas:** `fact_actividades`, `parametros`

```dax
VAR c = [Fecha Corte]
VAR i = fact_actividades[fecha_inicio]
VAR f = fact_actividades[fecha_fin]
RETURN
    ROUND ( IF ( c <= i, 0, IF ( c >= f, 100, 100 * DIVIDE ( c - i, f - i ) ) ), 0 )
```

### fact_actividades[Desvío]

- **Objetivo:** Atraso del avance real frente al planificado.
- **Regla de negocio:** R3: max(0, planificado − real)
- **Tablas utilizadas:** `fact_actividades`

```dax
MAX ( 0, fact_actividades[Avance Planificado] - fact_actividades[av_real] )
```

### fact_actividades[Semáforo]

- **Objetivo:** Estado de salud de la actividad.
- **Regla de negocio:** R4: Verde 0–5, Amarillo 6–9, Rojo ≥ 10
- **Tablas utilizadas:** `fact_actividades`

```dax
SWITCH ( TRUE (),
    fact_actividades[Desvío] <= 5, "Verde",
    fact_actividades[Desvío] <= 9, "Amarillo",
    "Rojo" )
```

### fact_actividades[Días sin Actualizar]

- **Objetivo:** Días desde la última actualización del estado.
- **Regla de negocio:** R8
- **Tablas utilizadas:** `fact_actividades`, `parametros`

```dax
IF ( ISBLANK ( fact_actividades[fecha_actualizacion] ), BLANK (),
     INT ( [Fecha Corte] - fact_actividades[fecha_actualizacion] ) )
```

### fact_actividades[Semáforo Actualización]

- **Objetivo:** Frescura de la información. Vacío si no se evalúa.
- **Regla de negocio:** R8: ≤ 7 verde, 8–14 amarillo, > 14 o sin fecha rojo; no evalúa no iniciadas ni Completadas (S3, S4)
- **Tablas utilizadas:** `fact_actividades`, `parametros`

```dax
VAR evaluable = fact_actividades[fecha_inicio] <= [Fecha Corte] && fact_actividades[estado] <> "Completado"
VAR d = fact_actividades[Días sin Actualizar]
RETURN
    IF ( NOT evaluable, BLANK (),
         IF ( ISBLANK ( d ), "Rojo",
              IF ( d <= 7, "Verde", IF ( d <= 14, "Amarillo", "Rojo" ) ) ) )
```

### fact_actividades[Días para Fin Efectivo]

- **Objetivo:** Días entre el fin efectivo y la fecha de corte (negativo o cero = vencida).
- **Regla de negocio:** R6 y R7
- **Tablas utilizadas:** `fact_actividades`, `parametros`

```dax
INT ( fact_actividades[Fin Efectivo] - [Fecha Corte] )
```

### fact_actividades[Situación de Plazo]

- **Objetivo:** Clasifica la actividad según su plazo: Completada, Vencida, Por vencer 1-30 días, Por vencer 31-60 días o En plazo.
- **Regla de negocio:** R6 y R7: vencida si el fin efectivo es menor o igual al corte y no está Completada; por vencer entre 1 y 60 días
- **Tablas utilizadas:** `fact_actividades`

```dax
VAR d = fact_actividades[Días para Fin Efectivo]
RETURN
    SWITCH ( TRUE (),
        fact_actividades[estado] = "Completado", "Completada",
        d <= 0, "Vencida",
        d <= 30, "Por vencer 1-30 días",
        d <= 60, "Por vencer 31-60 días",
        "En plazo" )
```

### fact_actividades[Color Semáforo]

- **Objetivo:** Color hexadecimal del semáforo de la actividad (para formato condicional).
- **Regla de negocio:** R4
- **Tablas utilizadas:** `fact_actividades`

```dax
SWITCH ( fact_actividades[Semáforo], "Verde", "#1E9E5A", "Amarillo", "#F5B800", "#D64545" )
```

### fact_actividades[Color Semáforo Actualización]

- **Objetivo:** Color hexadecimal del semáforo de actualización (para formato condicional).
- **Regla de negocio:** R8
- **Tablas utilizadas:** `fact_actividades`

```dax
SWITCH ( fact_actividades[Semáforo Actualización],
    "Verde", "#1E9E5A", "Amarillo", "#F5B800", "Rojo", "#D64545", BLANK () )
```

### fact_actividades[Color Situación de Plazo]

- **Objetivo:** Color hexadecimal de la situación de plazo (para formato condicional).
- **Regla de negocio:** R6 y R7
- **Tablas utilizadas:** `fact_actividades`

```dax
SWITCH ( fact_actividades[Situación de Plazo],
    "Vencida", "#D64545", "Por vencer 1-30 días", "#E8A020", "Por vencer 31-60 días", "#F5B800",
    "En plazo", "#1E9E5A", "#7A8699" )
```

### fact_solicitudes[Días de Firma]

- **Objetivo:** Días que tardó (o lleva) la firma de la solicitud.
- **Regla de negocio:** S7: resolución − creación; si está abierta, corte − creación
- **Tablas utilizadas:** `fact_solicitudes`, `parametros`

```dax
IF ( ISBLANK ( fact_solicitudes[fecha_resolucion] ),
     INT ( [Fecha Corte] - fact_solicitudes[fecha_creacion] ),
     INT ( fact_solicitudes[fecha_resolucion] - fact_solicitudes[fecha_creacion] ) )
```

### fact_solicitudes[Semáforo Firma]

- **Objetivo:** Semáforo del tiempo de firma.
- **Regla de negocio:** S7: ≤ 15 verde, 16–30 amarillo, > 30 rojo
- **Tablas utilizadas:** `fact_solicitudes`

```dax
SWITCH ( TRUE (),
    fact_solicitudes[Días de Firma] <= 15, "Verde",
    fact_solicitudes[Días de Firma] <= 30, "Amarillo",
    "Rojo" )
```

### fact_solicitudes[Color Semáforo Firma]

- **Objetivo:** Color hexadecimal del semáforo de firma (para formato condicional).
- **Regla de negocio:** S7
- **Tablas utilizadas:** `fact_solicitudes`

```dax
SWITCH ( fact_solicitudes[Semáforo Firma], "Verde", "#1E9E5A", "Amarillo", "#F5B800", "#D64545" )
```

## 3. Medidas

| Carpeta | Medida | Regla |
|---|---|---|
| Parámetros | Fecha Corte | Fecha de corte única del tablero (09/10/2026) |
| Actividades | Total Actividades | R1 |
| Actividades | Completadas | R1 |
| Actividades | Bloqueadas | R1 |
| Actividades | En Curso | R1 |
| Actividades | En Revisión | R1 |
| Actividades | Pendientes | R1 |
| Avance | % Avance Real | R5 |
| Avance | % Avance Planificado | R2 y R5 |
| Avance | Desvío Global | R3 |
| Avance | Semáforo Iniciativa | R4 |
| Semáforo | Actividades Verde | R4 |
| Semáforo | Actividades Amarillo | R4 |
| Semáforo | Actividades Rojo | R4 |
| Vencimientos | Vencidas | R6 |
| Vencimientos | Por Vencer 60 | R7 |
| Vencimientos | Por Vencer 30 | R7 |
| Actualización | Actividades Evaluables Actualización | R8 |
| Actualización | Actualización Verde | R8 |
| Actualización | Actualización Amarillo | R8 |
| Actualización | Actualización Rojo | R8 |
| Actualización | Sin Fecha de Actualización | R8 |
| Flujo de Fondos | Presupuesto Aprobado | R10 |
| Flujo de Fondos | Forecast Total | R9 |
| Flujo de Fondos | Real Total | R9 |
| Flujo de Fondos | Pendiente | R9 |
| Flujo de Fondos | % Ejecución | R9 |
| Flujo de Fondos | Forecast Meses Cerrados | S6 |
| Flujo de Fondos | Real Meses Cerrados | S6 |
| Flujo de Fondos | % Cumplimiento Meses Cerrados | S6 |
| Flujo de Fondos | % Inversión Ejecutada | R9 |
| Solicitudes | Total Solicitudes | Cantidad de solicitudes |
| Solicitudes | Solicitudes Abiertas | Solicitudes pendientes de firma |
| Solicitudes | Días Promedio Abiertas | Días promedio de las solicitudes abiertas al corte |
| Solicitudes | Solicitudes Verde | S7 |
| Solicitudes | Solicitudes Amarillo | S7 |
| Solicitudes | Solicitudes Rojo | S7 |
| Solicitudes | Abiertas Verde | S7 |
| Solicitudes | Abiertas Amarillo | S7 |
| Solicitudes | Abiertas Rojo | S7 |
| Semáforo | Color Semáforo Iniciativa | R4 |
| Vencimientos | Por Vencer 31-60 | R7 |
| Vencimientos | Actividades En Plazo | R7 |
| Vencimientos | Días de Atraso Promedio | R6 |

### Carpeta: Parámetros

#### Fecha Corte

- **Objetivo:** Reemplaza a TODAY().
- **Regla de negocio:** Fecha de corte única del tablero (09/10/2026)
- **Tablas utilizadas:** `parametros`
- **Formato:** `dd/mm/yyyy`

```dax
Fecha Corte = MAX ( parametros[fecha_corte] )
```

### Carpeta: Actividades

#### Total Actividades

- **Objetivo:** Cantidad de actividades.
- **Regla de negocio:** R1
- **Tablas utilizadas:** –
- **Formato:** `#,0`

```dax
Total Actividades = COUNTROWS ( fact_actividades )
```

#### Completadas

- **Objetivo:** Actividades en estado Completado.
- **Regla de negocio:** R1
- **Tablas utilizadas:** `fact_actividades`
- **Formato:** `#,0`

```dax
Completadas = CALCULATE ( [Total Actividades], fact_actividades[estado] = "Completado" )
```

#### Bloqueadas

- **Objetivo:** Actividades en estado Bloqueado.
- **Regla de negocio:** R1
- **Tablas utilizadas:** `fact_actividades`
- **Formato:** `#,0`

```dax
Bloqueadas = CALCULATE ( [Total Actividades], fact_actividades[estado] = "Bloqueado" )
```

#### En Curso

- **Objetivo:** Actividades en estado En Curso.
- **Regla de negocio:** R1
- **Tablas utilizadas:** `fact_actividades`
- **Formato:** `#,0`

```dax
En Curso = CALCULATE ( [Total Actividades], fact_actividades[estado] = "En Curso" )
```

#### En Revisión

- **Objetivo:** Actividades en estado En Revisión.
- **Regla de negocio:** R1
- **Tablas utilizadas:** `fact_actividades`
- **Formato:** `#,0`

```dax
En Revisión = CALCULATE ( [Total Actividades], fact_actividades[estado] = "En Revisión" )
```

#### Pendientes

- **Objetivo:** Actividades en estado Pendiente.
- **Regla de negocio:** R1
- **Tablas utilizadas:** `fact_actividades`
- **Formato:** `#,0`

```dax
Pendientes = CALCULATE ( [Total Actividades], fact_actividades[estado] = "Pendiente" )
```

### Carpeta: Avance

#### % Avance Real

- **Objetivo:** Promedio simple del avance real.
- **Regla de negocio:** R5
- **Tablas utilizadas:** `fact_actividades`
- **Formato:** `0.0%`

```dax
% Avance Real = AVERAGE ( fact_actividades[av_real] ) / 100
```

#### % Avance Planificado

- **Objetivo:** Promedio simple del avance planificado lineal.
- **Regla de negocio:** R2 y R5
- **Tablas utilizadas:** `fact_actividades`
- **Formato:** `0.0%`

```dax
% Avance Planificado = AVERAGE ( fact_actividades[Avance Planificado] ) / 100
```

#### Desvío Global

- **Objetivo:** Desvío en puntos porcentuales entre promedios.
- **Regla de negocio:** R3
- **Tablas utilizadas:** –
- **Formato:** `0.0`

```dax
Desvío Global = MAX ( 0, [% Avance Planificado] - [% Avance Real] ) * 100
```

#### Semáforo Iniciativa

- **Objetivo:** Semáforo agregado según el desvío entre promedios (supuesto S8).
- **Regla de negocio:** R4
- **Tablas utilizadas:** –
- **Formato:** `general`

```dax
Semáforo Iniciativa =
VAR d = ROUND ( [Desvío Global], 0 )
RETURN
    SWITCH ( TRUE (), d <= 5, "Verde", d <= 9, "Amarillo", "Rojo" )
```

### Carpeta: Semáforo

#### Actividades Verde

- **Objetivo:** Actividades con desvío de 0 a 5.
- **Regla de negocio:** R4
- **Tablas utilizadas:** `fact_actividades`
- **Formato:** `#,0`

```dax
Actividades Verde = CALCULATE ( [Total Actividades], fact_actividades[Semáforo] = "Verde" )
```

#### Actividades Amarillo

- **Objetivo:** Actividades con desvío de 6 a 9.
- **Regla de negocio:** R4
- **Tablas utilizadas:** `fact_actividades`
- **Formato:** `#,0`

```dax
Actividades Amarillo = CALCULATE ( [Total Actividades], fact_actividades[Semáforo] = "Amarillo" )
```

#### Actividades Rojo

- **Objetivo:** Actividades con desvío de 10 o más.
- **Regla de negocio:** R4
- **Tablas utilizadas:** `fact_actividades`
- **Formato:** `#,0`

```dax
Actividades Rojo = CALCULATE ( [Total Actividades], fact_actividades[Semáforo] = "Rojo" )
```

### Carpeta: Vencimientos

#### Vencidas

- **Objetivo:** Fin efectivo menor o igual al corte y no Completada.
- **Regla de negocio:** R6
- **Tablas utilizadas:** `fact_actividades`, `parametros`
- **Formato:** `#,0`

```dax
Vencidas =
VAR c = [Fecha Corte]
RETURN
    CALCULATE ( [Total Actividades],
        fact_actividades[estado] <> "Completado",
        fact_actividades[Fin Efectivo] <= c )
```

#### Por Vencer 60

- **Objetivo:** Vencen en 1 a 60 días (no Completadas).
- **Regla de negocio:** R7
- **Tablas utilizadas:** `fact_actividades`, `parametros`
- **Formato:** `#,0`

```dax
Por Vencer 60 =
VAR c = [Fecha Corte]
RETURN
    CALCULATE ( [Total Actividades],
        fact_actividades[estado] <> "Completado",
        fact_actividades[Fin Efectivo] > c,
        fact_actividades[Fin Efectivo] <= c + 60 )
```

#### Por Vencer 30

- **Objetivo:** Vencen en 1 a 30 días (no Completadas).
- **Regla de negocio:** R7
- **Tablas utilizadas:** `fact_actividades`, `parametros`
- **Formato:** `#,0`

```dax
Por Vencer 30 =
VAR c = [Fecha Corte]
RETURN
    CALCULATE ( [Total Actividades],
        fact_actividades[estado] <> "Completado",
        fact_actividades[Fin Efectivo] > c,
        fact_actividades[Fin Efectivo] <= c + 30 )
```

### Carpeta: Actualización

#### Actividades Evaluables Actualización

- **Objetivo:** Iniciadas y no Completadas.
- **Regla de negocio:** R8
- **Tablas utilizadas:** `fact_actividades`
- **Formato:** `#,0`

```dax
Actividades Evaluables Actualización = CALCULATE ( [Total Actividades], NOT ISBLANK ( fact_actividades[Semáforo Actualización] ) )
```

#### Actualización Verde

- **Objetivo:** Actualizadas hace 7 días o menos.
- **Regla de negocio:** R8
- **Tablas utilizadas:** `fact_actividades`
- **Formato:** `#,0`

```dax
Actualización Verde = CALCULATE ( [Total Actividades], fact_actividades[Semáforo Actualización] = "Verde" )
```

#### Actualización Amarillo

- **Objetivo:** Actualizadas hace 8 a 14 días.
- **Regla de negocio:** R8
- **Tablas utilizadas:** `fact_actividades`
- **Formato:** `#,0`

```dax
Actualización Amarillo = CALCULATE ( [Total Actividades], fact_actividades[Semáforo Actualización] = "Amarillo" )
```

#### Actualización Rojo

- **Objetivo:** Más de 14 días o sin fecha de actualización.
- **Regla de negocio:** R8
- **Tablas utilizadas:** `fact_actividades`
- **Formato:** `#,0`

```dax
Actualización Rojo = CALCULATE ( [Total Actividades], fact_actividades[Semáforo Actualización] = "Rojo" )
```

#### Sin Fecha de Actualización

- **Objetivo:** Evaluables sin fecha de actualización.
- **Regla de negocio:** R8
- **Tablas utilizadas:** `fact_actividades`
- **Formato:** `#,0`

```dax
Sin Fecha de Actualización =
CALCULATE ( [Total Actividades],
    NOT ISBLANK ( fact_actividades[Semáforo Actualización] ),
    ISBLANK ( fact_actividades[fecha_actualizacion] ) )
```

### Carpeta: Flujo de Fondos

#### Presupuesto Aprobado

- **Objetivo:** Presupuesto aprobado (USD).
- **Regla de negocio:** R10
- **Tablas utilizadas:** `dim_proyecto`
- **Formato:** `\$#,0`

```dax
Presupuesto Aprobado = SUM ( dim_proyecto[presupuesto_aprobado_usd] )
```

#### Forecast Total

- **Objetivo:** Gasto previsto (USD).
- **Regla de negocio:** R9
- **Tablas utilizadas:** `fact_flujo_fondos`
- **Formato:** `\$#,0`

```dax
Forecast Total = SUM ( fact_flujo_fondos[forecast_usd] )
```

#### Real Total

- **Objetivo:** Gasto real acumulado (USD).
- **Regla de negocio:** R9
- **Tablas utilizadas:** `fact_flujo_fondos`
- **Formato:** `\$#,0`

```dax
Real Total = SUM ( fact_flujo_fondos[real_usd] )
```

#### Pendiente

- **Objetivo:** Forecast menos real.
- **Regla de negocio:** R9
- **Tablas utilizadas:** –
- **Formato:** `\$#,0`

```dax
Pendiente = [Forecast Total] - [Real Total]
```

#### % Ejecución

- **Objetivo:** Real sobre forecast total.
- **Regla de negocio:** R9
- **Tablas utilizadas:** –
- **Formato:** `0.0%`

```dax
% Ejecución = DIVIDE ( [Real Total], [Forecast Total] )
```

#### Forecast Meses Cerrados

- **Objetivo:** Forecast de meses anteriores al mes de corte.
- **Regla de negocio:** S6
- **Tablas utilizadas:** `fact_flujo_fondos`, `parametros`
- **Formato:** `\$#,0`

```dax
Forecast Meses Cerrados =
VAR c = [Fecha Corte]
RETURN
    CALCULATE ( [Forecast Total], fact_flujo_fondos[mes] < DATE ( YEAR ( c ), MONTH ( c ), 1 ) )
```

#### Real Meses Cerrados

- **Objetivo:** Real de meses anteriores al mes de corte.
- **Regla de negocio:** S6
- **Tablas utilizadas:** `fact_flujo_fondos`, `parametros`
- **Formato:** `\$#,0`

```dax
Real Meses Cerrados =
VAR c = [Fecha Corte]
RETURN
    CALCULATE ( [Real Total], fact_flujo_fondos[mes] < DATE ( YEAR ( c ), MONTH ( c ), 1 ) )
```

#### % Cumplimiento Meses Cerrados

- **Objetivo:** Real sobre forecast de meses cerrados.
- **Regla de negocio:** S6
- **Tablas utilizadas:** –
- **Formato:** `0.0%`

```dax
% Cumplimiento Meses Cerrados = DIVIDE ( [Real Meses Cerrados], [Forecast Meses Cerrados] )
```

#### % Inversión Ejecutada

- **Objetivo:** Real sobre presupuesto aprobado.
- **Regla de negocio:** R9
- **Tablas utilizadas:** –
- **Formato:** `0.0%`

```dax
% Inversión Ejecutada = DIVIDE ( [Real Total], [Presupuesto Aprobado] )
```

### Carpeta: Solicitudes

#### Total Solicitudes

- **Objetivo:** Cantidad de solicitudes.
- **Regla de negocio:** Cantidad de solicitudes.
- **Tablas utilizadas:** –
- **Formato:** `#,0`

```dax
Total Solicitudes = COUNTROWS ( fact_solicitudes )
```

#### Solicitudes Abiertas

- **Objetivo:** Solicitudes pendientes de firma.
- **Regla de negocio:** Solicitudes pendientes de firma.
- **Tablas utilizadas:** `fact_solicitudes`
- **Formato:** `#,0`

```dax
Solicitudes Abiertas = CALCULATE ( [Total Solicitudes], fact_solicitudes[estado] = "Pendiente de firma" )
```

#### Días Promedio Abiertas

- **Objetivo:** Días promedio de las solicitudes abiertas al corte.
- **Regla de negocio:** Días promedio de las solicitudes abiertas al corte.
- **Tablas utilizadas:** `fact_solicitudes`
- **Formato:** `0.0`

```dax
Días Promedio Abiertas = CALCULATE ( AVERAGE ( fact_solicitudes[Días de Firma] ), fact_solicitudes[estado] = "Pendiente de firma" )
```

#### Solicitudes Verde

- **Objetivo:** Días de firma menores o iguales a 15.
- **Regla de negocio:** S7
- **Tablas utilizadas:** `fact_solicitudes`
- **Formato:** `#,0`

```dax
Solicitudes Verde = CALCULATE ( [Total Solicitudes], fact_solicitudes[Semáforo Firma] = "Verde" )
```

#### Solicitudes Amarillo

- **Objetivo:** Días de firma de 16 a 30.
- **Regla de negocio:** S7
- **Tablas utilizadas:** `fact_solicitudes`
- **Formato:** `#,0`

```dax
Solicitudes Amarillo = CALCULATE ( [Total Solicitudes], fact_solicitudes[Semáforo Firma] = "Amarillo" )
```

#### Solicitudes Rojo

- **Objetivo:** Días de firma mayores a 30.
- **Regla de negocio:** S7
- **Tablas utilizadas:** `fact_solicitudes`
- **Formato:** `#,0`

```dax
Solicitudes Rojo = CALCULATE ( [Total Solicitudes], fact_solicitudes[Semáforo Firma] = "Rojo" )
```

#### Abiertas Verde

- **Objetivo:** Abiertas con 15 días o menos.
- **Regla de negocio:** S7
- **Tablas utilizadas:** `fact_solicitudes`
- **Formato:** `#,0`

```dax
Abiertas Verde = CALCULATE ( [Total Solicitudes], fact_solicitudes[estado] = "Pendiente de firma", fact_solicitudes[Semáforo Firma] = "Verde" )
```

#### Abiertas Amarillo

- **Objetivo:** Abiertas con 16 a 30 días.
- **Regla de negocio:** S7
- **Tablas utilizadas:** `fact_solicitudes`
- **Formato:** `#,0`

```dax
Abiertas Amarillo = CALCULATE ( [Total Solicitudes], fact_solicitudes[estado] = "Pendiente de firma", fact_solicitudes[Semáforo Firma] = "Amarillo" )
```

#### Abiertas Rojo

- **Objetivo:** Abiertas con más de 30 días.
- **Regla de negocio:** S7
- **Tablas utilizadas:** `fact_solicitudes`
- **Formato:** `#,0`

```dax
Abiertas Rojo = CALCULATE ( [Total Solicitudes], fact_solicitudes[estado] = "Pendiente de firma", fact_solicitudes[Semáforo Firma] = "Rojo" )
```

### Carpeta: Semáforo

#### Color Semáforo Iniciativa

- **Objetivo:** Color hexadecimal del semáforo de la iniciativa (para formato condicional).
- **Regla de negocio:** R4
- **Tablas utilizadas:** –
- **Formato:** `general`

```dax
Color Semáforo Iniciativa = SWITCH ( [Semáforo Iniciativa], "Verde", "#1E9E5A", "Amarillo", "#F5B800", "Rojo", "#D64545", BLANK () )
```

### Carpeta: Vencimientos

#### Por Vencer 31-60

- **Objetivo:** Vencen en 31 a 60 días (no Completadas).
- **Regla de negocio:** R7
- **Tablas utilizadas:** `fact_actividades`
- **Formato:** `#,0`

```dax
Por Vencer 31-60 = CALCULATE ( [Total Actividades], fact_actividades[Situación de Plazo] = "Por vencer 31-60 días" )
```

#### Actividades En Plazo

- **Objetivo:** No Completadas con más de 60 días para vencer.
- **Regla de negocio:** R7
- **Tablas utilizadas:** `fact_actividades`
- **Formato:** `#,0`

```dax
Actividades En Plazo = CALCULATE ( [Total Actividades], fact_actividades[Situación de Plazo] = "En plazo" )
```

#### Días de Atraso Promedio

- **Objetivo:** Días promedio de atraso de las actividades vencidas.
- **Regla de negocio:** R6
- **Tablas utilizadas:** `fact_actividades`
- **Formato:** `0.0`

```dax
Días de Atraso Promedio =
CALCULATE ( - AVERAGE ( fact_actividades[Días para Fin Efectivo] ),
    fact_actividades[Situación de Plazo] = "Vencida" )
```

## 4. Validación

1. `python scripts/validar_kpis.py` recalcula todos los KPIs desde los CSV (`docs/validacion-kpis.md`).
2. `scripts/cuadrar_dax.ps1` consulta cada medida en el modelo cargado y la compara con el recálculo (`docs/cuadre-dax.md`), globalmente y por iniciativa.

