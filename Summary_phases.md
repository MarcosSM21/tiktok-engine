## Fase 1: Generador de Imagen Base

### Objetivo
Generar automáticamente una imagen vertical tipo TikTok del formato "Encuentra el elemento diferente", sin edición manual.

### Hecho en esta fase
- Se creó la estructura mínima del proyecto para el MVP.
- Se implementó `src/main.py` como punto de entrada.
- Se implementó `src/formats/find_difference.py` para generar la imagen.
- Se genera un lienzo vertical de 1080x1920.
- Se dibuja un hook superior centrado.
- Se genera una cuadrícula con elementos repetidos.
- Se sustituye un único elemento por el diferente.
- Se mejoró la legibilidad visual básica.
- Se ajustó el hook para respetar márgenes y hacer salto de línea automático.
- Se validó que cambiando parámetros se generan variantes distintas.

### Decisiones tomadas
- Se usa Python con Pillow para construir el formato base.
- Se prioriza una salida simple y funcional antes que un diseño pulido.
- La configuración se mantiene todavía dentro de `main.py` para no complicar el MVP.

### Límites actuales
- Todavía no hay vídeo.
- Todavía no hay cuenta atrás ni revelación animada.
- Todavía no hay generación por lotes.
- Todavía no hay presets externos en JSON/CSV.

### Estado al cierre
La Fase 1 queda completada con un generador funcional de imágenes base sobre el que construiremos el primer vídeo automático en la siguiente fase.