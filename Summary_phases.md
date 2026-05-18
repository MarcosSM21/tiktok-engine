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

## Fase 2: Generador del Primer Video Automatico

### Objetivo
Convertir el formato "Encuentra el elemento diferente" en un video vertical automatico, listo para reproducirse, con reto, cuenta atras y revelacion final.

### Hecho en esta fase
- Se definio una estructura temporal simple para el primer video.
- Se reutilizo la escena base del reto creada en la Fase 1.
- Se preparo la generacion de imagenes en memoria para poder usarlas en video.
- Se anadio una cuenta atras visual sobre la escena del reto.
- Se creo una escena de revelacion marcando la respuesta correcta.
- Se unieron las escenas en un video vertical mediante MoviePy.
- Se exporto el video en `output/videos/`.
- Se verifico que el video se reproduce correctamente de principio a fin.

### Decisiones tomadas
- Se mantiene un video simple y funcional antes de mejorar animaciones o estilo.
- Se usa MoviePy para unir escenas estaticas y exportar el `.mp4`.
- La cuenta atras se representa como imagenes sucesivas para reducir complejidad.
- La revelacion se hace marcando la posicion correcta con un circulo.

### Limites actuales
- La cuenta atras todavia no tiene animacion suave.
- No hay audio, musica ni efectos.
- No hay generacion por lotes.
- La configuracion sigue estando dentro de `main.py`.
- El formato todavia no esta preparado como sistema reutilizable para multiples tipos de video.

### Estado al cierre
La Fase 2 queda completada con el primer video automatico funcional del proyecto. El sistema ya puede generar un video vertical basico sin abrir un editor de video.

## Fase 3: Variaciones Automaticas del Formato

### Objetivo
Hacer que el formato "Encuentra el elemento diferente" pueda generar videos distintos automaticamente cambiando parametros basicos sin editar el codigo cada vez.

### Hecho en esta fase
- Se definieron los parametros principales que pueden variar.
- Se creo una funcion para generar configuraciones aleatorias.
- Se automatizo la seleccion del numero base y del numero diferente.
- Se automatizo la seleccion del tamano de cuadricula.
- Se automatizo la posicion de la respuesta correcta.
- Se anadieron varios hooks posibles.
- Se anadieron varias paletas de color.
- Se generaron nombres de salida unicos usando fecha, hora e identificador corto.

### Decisiones tomadas
- La configuracion aleatoria vive temporalmente en `src/main.py` para mantener el MVP simple.
- Se usan valores predefinidos controlados en lugar de aleatoriedad total.
- La posicion de la respuesta se calcula con `random.randrange(rows * cols)` para garantizar que siempre este dentro de la cuadricula.
- Los nombres de salida incluyen un identificador corto para evitar sobrescrituras.

### Limites actuales
- Todavia no hay generacion por lotes.
- Los presets no estan en archivos externos.
- Las duraciones del video siguen fijas.
- La variacion visual sigue siendo limitada.
- Solo existe un formato de video.

### Estado al cierre
La Fase 3 queda completada con un sistema capaz de generar variantes automaticas del formato base. El proyecto ya no produce siempre el mismo video, sino versiones distintas a partir de una configuracion generada por codigo.

## Fase 4: Generacion por Lotes

### Objetivo
Generar varios videos automaticos en una sola ejecucion hasta alcanzar el primer hito del proyecto: producir 10 videos usables sin abrir un editor.

### Hecho en esta fase
- Se anadio una constante `VIDEOS_TO_GENERATE` para controlar el tamano del lote.
- Se adapto `main()` para generar varios videos en una sola ejecucion.
- Se genera una configuracion aleatoria distinta para cada video.
- Se renderiza un video por cada configuracion.
- Se incluyo el numero de video en los nombres de salida.
- Se mantienen fecha, hora e identificador corto para evitar sobrescrituras.
- Se anadio un resumen final en consola con los videos generados.

### Decisiones tomadas
- El tamano del lote se mantiene temporalmente como constante en `src/main.py`.
- La generacion por lotes reutiliza la misma funcion de configuracion aleatoria de la Fase 3.
- Los nombres de salida incluyen numeracion con dos digitos para mantener orden visual en carpetas.
- El resumen final se imprime en consola en lugar de guardarse todavia en una base de datos o archivo.

### Limites actuales
- El numero de videos todavia no se pasa por argumentos de terminal.
- No hay registro persistente de videos generados.
- No hay control de duplicados de ideas mas alla de la aleatoriedad actual.
- Los presets siguen dentro de `main.py`.
- El lote solo genera el formato "Encuentra el elemento diferente".

### Estado al cierre
La Fase 4 queda completada con un generador por lotes capaz de producir 10 videos automaticos en una sola ejecucion. Con esto se alcanza el primer hito funcional del MVP.
