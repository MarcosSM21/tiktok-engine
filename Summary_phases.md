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

## Fase 5: Presets Externos en JSON

### Objetivo
Sacar hooks, paletas, tamanos de cuadricula y otros valores configurables de `src/main.py` para controlarlos desde archivos JSON sin tocar codigo.

### Hecho en esta fase
- Se definieron los datos configurables que pasan a vivir fuera del codigo.
- Se creo el archivo `data/presets/find_difference.json`.
- Se movieron hooks, tamanos de cuadricula, numeros disponibles, paletas, medidas y cantidad de videos al JSON.
- Se anadio carga de presets desde `src/main.py`.
- Se adapto la generacion aleatoria para usar los datos cargados desde JSON.
- Se convirtieron los colores del JSON a tuplas antes de usarlos con Pillow.
- Se dejo `main.py` como orquestador del lote y no como archivo de presets creativos.

### Decisiones tomadas
- Se usa JSON como primera fuente externa por ser simple, editable y suficiente para el MVP.
- El preset vive en `data/presets/find_difference.json`.
- La cantidad de videos por lote se controla desde el JSON.
- La configuracion del timeline y del layout interno se mantiene todavia en codigo para no abrir demasiados frentes.

### Limites actuales
- Solo existe un preset para el formato "Encuentra el elemento diferente".
- No hay validacion formal del JSON.
- No hay argumentos de terminal para elegir otro preset.
- Los textos finales y tiempos del video aun no estan externalizados.
- La logica de configuracion aleatoria sigue dentro de `main.py`.

### Estado al cierre
La Fase 5 queda completada con presets externos en JSON. El sistema ya permite ajustar contenido y parametros principales del lote sin modificar directamente la logica del programa.

## Fase 6: Mejora Visual del Formato

### Objetivo
Mejorar la calidad visual del formato "Encuentra el elemento diferente" sin cambiar el motor base ni anadir dependencias complejas.

### Hecho en esta fase
- Se sustituyo el fondo plano por un gradiente vertical simple.
- Se anadio un bloque visual para el hook superior.
- Se fijo el hook principal para controlar mejor su composicion.
- Se implemento padding real del texto dentro del bloque del hook.
- Se mejoro la cuadrícula con panel, borde y lineas internas.
- Se redujo el tamano de los numeros para mejorar la lectura del conjunto.
- Se recoloco la cuadrícula mas arriba para dejar espacio al contador.
- Se rediseño el contador y se elimino la palabra "segundos".
- Se mejoro la revelacion para marcar la respuesta sin tapar el numero.
- Se centralizaron medidas de layout para alinear reto y revelacion.

### Decisiones tomadas
- Se mantiene el render programatico con Pillow para conservar control total.
- No se incorpora ComfyUI ni assets generados en esta fase.
- El hook deja de variar temporalmente para asegurar una composicion consistente.
- Se prioriza legibilidad y control visual por encima de maxima variacion.

### Limites actuales
- El estilo visual sigue siendo basico.
- No hay animaciones suaves ni transiciones.
- No hay musica, TTS ni efectos sonoros.
- El layout aun esta definido en codigo.
- Solo se ha mejorado el formato "Encuentra el elemento diferente".

### Estado al cierre
La Fase 6 queda completada con una version visualmente mas clara y controlada del primer formato. El video mantiene la simplicidad del MVP, pero ya se percibe mas cuidado y menos plano.

## Fase 7: Audio Base y Efectos Simples

### Objetivo
Anadir audio basico a los videos para que se perciban mas completos, empezando con musica de fondo opcional sin incorporar todavia TTS ni mezcla compleja.

### Hecho en esta fase
- Se creo una carpeta para assets de audio en `assets/audio/`.
- Se anadio un archivo de musica de fondo local.
- Se incorporo la ruta del audio al preset JSON.
- Se anadio control de volumen desde `background_music_volume`.
- Se anadio control del punto de inicio desde `background_music_start`.
- Se paso la configuracion de audio desde `main.py` al generador de video.
- Se anadio soporte opcional de audio con `AudioFileClip`.
- Se recorta la musica a la duracion exacta del video.
- Se exporta el `.mp4` con codec de audio `aac`.

### Decisiones tomadas
- La musica de fondo es opcional: si no hay ruta o el archivo no existe, el video se genera sin audio.
- Se usa un volumen bajo por defecto para dejar espacio a futura voz narrada.
- El audio se controla desde JSON para evitar tocar codigo al cambiar musica o volumen.
- Se deja TTS para una fase posterior.

### Limites actuales
- Solo hay una pista de musica de fondo.
- No hay efectos sonoros sincronizados con contador o revelacion.
- No hay fundido de entrada o salida.
- No hay seleccion aleatoria entre varias canciones.
- No hay voz narrada.

### Estado al cierre
La Fase 7 queda completada con soporte de musica de fondo opcional. El sistema ya puede generar videos con imagen, movimiento por escenas y audio en un unico `.mp4`.

## Fase 8: Voz Pregrabada y Mezcla de Audio

### Objetivo
Anadir voz narrada al video usando audios pregrabados o generados fuera del sistema, evitando depender de APIs o TTS local de baja calidad.

### Hecho en esta fase
- Se descarto la generacion local con `pyttsx3` por baja calidad de voz.
- Se elimino la generacion automatica de archivos de voz desde codigo.
- Se preparo el preset JSON para recibir una ruta de voz pregrabada.
- Se organizo el audio en carpetas separadas para musica y voces.
- Se anadio soporte para cargar una voz existente desde `voiceover_path`.
- Se anadio control de volumen de voz con `voiceover_volume`.
- Se mezclo la voz pregrabada con la musica de fondo.
- Se usa `CompositeAudioClip` para combinar varias pistas de audio.
- Se mantiene la exportacion final en `.mp4` con audio `aac`.

### Decisiones tomadas
- La voz se crea fuera del sistema con herramientas especializadas de voces tipo TikTok.
- El sistema no genera voces, solo consume audios ya existentes.
- Se separa `assets/audio/music/` para musica y `assets/audio/voiceovers/` para voces.
- La musica y la voz se controlan desde JSON para poder ajustar rutas y volumen sin tocar codigo.

### Limites actuales
- Solo se usa una voz pregrabada fija por preset.
- No hay seleccion aleatoria entre varias voces.
- No hay sincronizacion precisa entre voz y escenas.
- No hay ducking automatico de musica cuando entra la voz.
- No hay fades de entrada o salida.

### Estado al cierre
La Fase 8 queda completada con voz pregrabada mezclada con musica de fondo. El sistema ya puede producir videos con audio mas cercano a un formato de TikTok, manteniendo el control desde archivos locales y JSON.
