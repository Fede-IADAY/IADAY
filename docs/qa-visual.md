# QA visual del dashboard

Revisión de las 5 páginas con capturas generadas desde Power BI Desktop (puente de automatización), en 8 iteraciones.
Alcance: solo diseño, espaciado, tamaños, jerarquía visual, legibilidad y experiencia de usuario. **No se modificaron el
modelo, las relaciones, las medidas DAX, las reglas de negocio ni los CSV.**

Capturas finales: [`capturas/`](capturas/).

## Resultado por página

### 1. Resumen Ejecutivo
| | |
|---|---|
| **Problemas encontrados** | Fecha de corte cortada en la cabecera; botones de navegación sin texto ni relleno; el gráfico y la tabla mostraban solo 4 y 9 de 11 iniciativas (con barras de desplazamiento); encabezados de tabla en minúscula técnica ("nombre", "fase"); eje con título "nombre" y leyenda con nombres de medida; tabla demasiado ancha para su espacio |
| **Correcciones** | Tarjeta de fecha rediseñada; botones con relleno y texto; gráfico de semáforo a alto completo (11 barras); tabla con 9 columnas de ancho fijo y 11 filas sin desplazamiento; encabezados amigables ("Iniciativa", "Sponsor", "% Real"); ejes sin título; leyenda "Verde / Amarillo / Rojo"; panel "Cómo leer el semáforo" (inspirado en la leyenda del HTML de referencia) |
| **Mejoras visuales** | Semáforo en celdas con color de relleno y texto azul oscuro (contraste legible); tarjetas con barra lateral de color por significado; tabla ordenada por desvío (lo más crítico arriba) |

### 2. Riesgos y Desvíos
| | |
|---|---|
| **Problemas** | La tabla de actividades críticas fallaba con "Error al capturar los datos"; texto truncado y desplazamiento horizontal con solo 3 columnas visibles; gráfico de desvío con 4 barras visibles |
| **Correcciones** | Causa del error: dos columnas llamadas `nombre` (iniciativa y actividad) con el mismo alias de consulta; ahora cada una tiene alias único y encabezado propio. Tablas con anchos fijos que caben en el panel; el gráfico muestra las 11 iniciativas; tabla de solicitudes abiertas más compacta |
| **Mejoras visuales** | Dos tablas y un gráfico con jerarquía clara: desvío por iniciativa → detalle crítico → solicitudes de firma con su semáforo; motivo de bloqueo visible |

### 3. Vencidos y Por Vencer
| | |
|---|---|
| **Problemas** | Misma falla de datos y desbordamiento horizontal; etiquetas de iniciativa truncadas; eje con título automático largo ("Vencidas, Por Vencer 30 y Por Venc...") |
| **Correcciones** | Tabla de 7 columnas con anchos fijos, texto de 9 pt y orden por días (lo más atrasado primero); etiquetas de categoría con más espacio; leyenda legible ("Vencen en 30 días") |
| **Mejoras visuales** | Los días aparecen con signo (negativo = vencida) y la situación con color; las tarjetas separan vencidas, 30 días y 31–60 días con colores distintos |

### 4. Actualización Atrasada
| | |
|---|---|
| **Problemas** | Misma falla de datos; fechas en formato largo ("miércoles, 02 de septiembre de 2026") que desbordaban la tabla; leyenda con nombres de medida |
| **Correcciones** | Se quitó la fecha cruda y se dejó "Días sin actualizar" más el semáforo (ver "Hallazgo para el modelo" abajo); leyenda "Al día / Atraso leve / Atraso crítico"; tabla con anchos fijos |
| **Mejoras visuales** | Barras por responsable con colores consistentes con el resto del reporte |

### 5. Flujo de Fondos
| | |
|---|---|
| **Problemas** | Tarjetas con "$7 mill." (perdían precisión); etiquetas y ejes con títulos técnicos; tabla con solo 6 de 11 filas |
| **Correcciones** | Tarjetas en millones con 2 decimales ("$7,19 mill."); etiquetas del gráfico en miles; se quitó la fila de total (las tarjetas ya la muestran) y se ajustaron alturas: ahora se ven las 11 iniciativas |
| **Mejoras visuales** | Separador de miles y formato USD en la tabla; barras navy (forecast) y ámbar (real) que repiten la paleta |

## Cabecera, navegación y filtros (todas las páginas)
- Cabecera azul oscuro con la etiqueta `[ IA DAY // PMO DE INICIATIVAS DE IA ]` en ámbar y tipografía monoespaciada (guiño a la charla), título blanco y tarjeta de **fecha de corte** con borde ámbar.
- Botonera de 5 páginas: la activa en ámbar, las demás en blanco con contorno azul; botón **"Limpiar filtros"** con la acción nativa "borrar todos los segmentadores".
- 4 filtros sincronizados entre páginas: Sponsor Ejecutivo, Área, Tipo de IA y Coordinador de Portafolio IA.
- Se compactó el encabezado (de 60 a 54 px) y se reordenó la distribución vertical para ganar espacio útil para tablas.

## Revisión de KPIs
| Aspecto | Resultado |
|---|---|
| Tamaño de fuente | Valor 20 pt en negrita y etiqueta 10 pt; sin recortes en las 30 tarjetas |
| Formato numérico | Enteros con separador de miles; porcentajes con 1 decimal; USD en millones con 2 decimales; desvíos con 1 decimal |
| Alineación | Cifras alineadas a la derecha en las tablas; tarjetas alineadas a la izquierda |
| Colores condicionales | Semáforo de iniciativa, actividad, actualización, plazo y firma con el color calculado en el modelo |
| Espaciado interno | Tarjetas de 64 px con 2 px de padding y barra lateral de 5 px |

### KPIs de poco valor ejecutivo y propuestas de reemplazo
Estas propuestas requieren medidas nuevas, así que **no se aplicaron** en esta fase (el modelo no se podía tocar):
| Tarjeta actual | Por qué aporta poco | Reemplazo propuesto |
|---|---|---|
| "Actividades" (170) en Resumen | Es un conteo estático y no orienta una decisión | "Iniciativas en rojo" (3 de 11) |
| "Completadas" en Vencidos y Por Vencer | No se relaciona con los plazos | "Vencen esta semana" |
| "Completadas (excluidas)" en Actualización Atrasada | Explica un criterio, no el estado | "% al día" (Verde sobre evaluadas) |
| "% Cumpl. meses cerrados" junto a "% Ejecución" | Dos porcentajes parecidos | "Desvío presupuestario" (real contra forecast, en USD) |

## Hallazgo para el modelo (no corregido en esta fase)
Las columnas de fecha importadas desde los CSV (por ejemplo `fecha_actualizacion`) llegan a Power BI con formato de fecha larga,
aunque el TMDL declara `dd/mm/yyyy`; las columnas calculadas sí conservan el formato. Es un ajuste de modelo (formato de columna
o transformación en Power Query), por eso la fecha cruda se quitó de la página 4 en lugar de corregirse.

## Puntuación final (1 a 10)
| Criterio | Nota | Fundamento |
|---|---|---|
| Diseño | 8,5 | Identidad coherente, paleta del HTML de referencia, jerarquía clara; resta la saturación de las columnas de semáforo cuando casi todo es rojo |
| UX | 8,0 | Navegación, filtros sincronizados y limpieza de filtros funcionan; faltan interacciones avanzadas (detalle por iniciativa, tooltips) |
| Legibilidad | 8,5 | Sin cortes ni desplazamientos horizontales; algunos nombres largos se truncan con puntos suspensivos en las tablas densas |
| Storytelling | 8,0 | Cada página responde una pregunta ejecutiva; el resumen podría destacar mejor "qué iniciativas atender primero" |
| Calidad ejecutiva | 8,5 | Cifras cuadradas contra el recálculo (107/107) y datos equilibrados para demostración |

## Diferencias frente al HTML de referencia
| Elemento del HTML | En el dashboard |
|---|---|
| Selector de idioma ES/EN/PT | No aplica (decisión del proyecto: solo español) |
| Filas desplegables por gerente | Se reemplazan por tablas ordenadas por desvío |
| Emojis en pestañas y badges con contadores | Botonera sin contadores; los números están en las tarjetas |
| Banda de inversión y avance global | Tarjetas de avance (real y planificado) y página de Flujo de Fondos |

## Recomendaciones finales
1. Corregir el formato de las columnas de fecha importadas (ajuste de modelo) y recuperar la fecha de última actualización.
2. Incorporar las 4 medidas propuestas para reemplazar las tarjetas de poco valor.
3. Agregar una página de detalle por iniciativa (drillthrough) para una demostración más narrativa.
4. Revisar el contraste del semáforo en pantallas con poco brillo.

## Portada (página de inicio)
| | |
|---|---|
| **Ubicación de las imágenes** | Fondo: `Forma 3.png`, a pantalla completa y enviado al fondo (propiedad de fondo de la página, no un visual). Logotipo: esquina superior izquierda (x 24, y 20), 250 × 86 px, sobre una placa blanca redondeada |
| **Ubicación de los botones** | Menú de 5 botones de 520 × 54 px dentro de un panel translúcido centrado ligeramente a la derecha (x 400 a 1000, centro en 700 de 1280): Resumen Ejecutivo, Riesgos y Desvíos, Vencidos y Por Vencer, Actualización Atrasada y Flujo de Fondos |
| **Título** | "IA DAY 2026" (56 px) con la etiqueta `[ FLOCK // AI DAY 2026 ]` en ámbar y el subtítulo en dos líneas equilibradas |
| **Verificación visual** | La imagen cubre toda la página sin deformarse (se recorta la parte superior e inferior de la figura, que es cuadrada); el logotipo no tapa información; botones legibles y con efecto ámbar al pasar el cursor |
| **Verificación funcional** | Los 5 botones se probaron con Ctrl + clic en Power BI Desktop y cada uno abre su página |
