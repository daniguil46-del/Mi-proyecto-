---
name: replicar-anuncio-con-ia
description: Replica con IA un anuncio de vídeo que ya está funcionando, cambiando solo a la persona que sale, y deja el resto igual (el mismo fondo, los mismos movimientos, el mismo producto y los mismos cortes). Parte de un enlace de TrendTrack o de un archivo .mp4, lo corta en trozos, los manda a Wan 3.0 a través de APImart, revisa cada trozo contra el original fotograma a fotograma y lo une con el audio original. Úsala cuando la persona diga "replícame este anuncio", "copia este vídeo de la competencia", "hazme este anuncio con otra persona", pegue un enlace de TrendTrack o de la Biblioteca de anuncios de Meta, o escriba /replicar-anuncio-con-ia.
---

# Replicar un anuncio ganador con IA

Rehace un anuncio que ya funciona cambiando **solo a la persona**. Todo lo demás se mantiene: el fondo, la luz, los movimientos, los cortes y el producto.

Habla con la persona en español y con frases cortas. Los prompts de Wan, en español. Los de imagen, en inglés.

## Antes de nada

```bash
python3 scripts/comprobar.py
```

Tiene que decir **LISTO**. Si falta algo, dice exactamente qué y cómo arreglarlo. No sigas sin eso.

## Las 6 reglas (salen de errores reales, no de la teoría)

**1. Réplica es réplica.** No añadas nada que el original no tenga. Ni planos de más, ni cámara lenta, ni textos nuevos. Si se te ocurre una mejora, la propones en una línea y la haces solo si te dicen que sí.

**1 bis. La voz la pone la IA, con el audio original como referencia.** `preparar.py` corta el audio del anuncio en los mismos trozos (`audios/tramoN.mp3`) y `lanzar.py` se los manda a Wan en `audio_urls`. Con eso Wan **genera** la voz, pero copiando la del original y diciendo las mismas palabras en los mismos tiempos — probado: la transcripción del clip generado sale idéntica a la del original con 2 centésimas de diferencia. **Y por eso la boca cuadra**, porque la voz y la imagen salen de la misma generación. No pegues nunca el audio del original encima de un clip que ya trae voz: los labios irían por un lado y la voz por otro. Límite de Wan: 15 s de audio de referencia, que es justo lo que mide un tramo.

**2. El MENOR número de trozos posible.** Wan acepta 15 segundos por tirada. Cada trozo se genera por separado, y entre uno y otro cambian un poco la cara, la luz y la postura. Eso se nota. Corta siempre en un **corte real del original**, nunca en mitad de un plano.

**3. Describe TODO lo que hay en el plano, no solo lo que se mueve.** Este es el fallo que más duele. Si en el original la persona tiene **una mano apoyada en la cara** mientras la otra trabaja, hay que escribirlo: *"la otra mano se queda apoyada sobre la cara y no se retira en ningún momento"*. Si no lo pones, Wan la borra a partir del segundo fotograma y el plano se rompe. Lo mismo con gafas, pendientes, un vaso en la mesa o lo que sea.

**4. El producto, clip a clip.** No digas "mantén el producto intacto" en general. Di cómo está **en ese trozo**: *"en el clip 1 todavía tiene el papel blanco; en el 3 ya está despegado; no aparece ningún papel blanco en ningún momento"*. Si lo describes en general, Wan lo pinta donde no toca.

**5. Si el anuncio enseña un antes y un después, hay que meterlo en la foto de referencia.** Un anuncio de cosmética suele estar grabado con **medio cuerpo o media cara ya tratada**. Wan tiende a igualar los dos lados y el "antes y después" desaparece, que es justo lo que vende el anuncio. Solución: crea la foto del avatar con esa diferencia ya pintada, y repite la descripción de la diferencia **en los prompts de todos los trozos**, no solo en el del reveal.

**6. El español cabe en la MITAD de palabras que el inglés.** Medido sobre un anuncio real: inglés
4,28 palabras/s, español de México 2,26. Si traduces el guion literal, la voz no llega al final y el
vídeo se corta a media frase. Cuenta las palabras del original y escribe la mitad, quedándote con la
idea. Y ojo: **la voz manda sobre el ritmo de los planos**. Si el texto va muy justo o muy sobrado,
Wan alarga o acorta el plano para que le quepa. Reparte las frases de forma que haya cosas que solo
se puedan decir con el producto ya en la posición que toca.

**7. Nada engañoso.** No prometas lo que el producto no hace. Adapta los textos a la ley del país. No pongas envíos ni formas de pago que la tienda no ofrezca.

## Paso 0 · Preguntar (todo en un solo mensaje)

1. **El anuncio**: enlace de TrendTrack, de la Biblioteca de anuncios de Meta, o un archivo `.mp4`.
2. **Qué cambiar**: por defecto, solo la persona. ¿Hombre o mujer, de qué edad, de qué país?
3. **El mercado**: ¿para qué país y en qué idioma lo quieres? El mercado manda **solo sobre la voz y
   los textos**: se traduce lo que dice y lo que sale escrito, y se pide el acento de ese país. No
   cambia el fondo, ni los movimientos, ni los cortes, ni el producto. Si es el mismo idioma del
   original, se deja la voz tal cual.
4. **El avatar**: ¿tiene una foto, o se la generamos?
5. **El producto**: si sale en pantalla, que lo describa (forma, color, si cambia de estado).

## Paso 1 · Bajar y analizar

```bash
python3 scripts/bajar.py "<enlace o ruta>" <carpeta>
python3 scripts/preparar.py <carpeta>
```

`preparar.py` detecta los cortes, propone los trozos, los recorta y deja una hoja de fotogramas.

**Mira la hoja** y escribe en el chat esta tabla, que es lo que la persona tiene que validar:

| Clip | Segundos | Qué se ve | Dónde están las manos | Estado del producto | Texto en pantalla | Elementos encima |
|---|---|---|---|---|---|---|

La última columna es para el **paso 8**: capturas de pantalla, vídeos insertados, emojis, flechas o carteles. Apuntar de cada uno qué era, en qué segundo entra y sale, dónde está y qué tamaño ocupa. Si no se apunta aquí, luego no se puede recolocar.

Di también si el anuncio lleva **voz hablando a cámara** o solo música, y si la cara tiene alguna **asimetría** del tipo antes/después (regla 5).

## Paso 2 · El plan ✋

Enseña la tabla de trozos con el coste (**0,066 $ por segundo a 480P**) y **para hasta que te digan que sí**. No gastes dinero sin el OK.

## Paso 3 · La foto del avatar

Si no la tienen, se genera a partir de un fotograma limpio del original: así el cuarto, la luz, la ropa y el encuadre ya coinciden.

Para generarla, el prompt va en inglés y tiene que decir: a quién cambiamos, que **todo lo demás sigue igual**, y que se renderice **la cara entera de una pasada, sin costura en la frente**.

**Cuidado con la izquierda y la derecha**: los modelos de imagen las confunden a menudo. Si necesitas la asimetría en un lado concreto, genera las dos versiones, mira cuál salió bien y usa esa. Si solo te sale bien la del lado contrario, dale la vuelta a la imagen con un espejo horizontal: el fondo se invierte, pero da igual, porque el fondo lo coge Wan del vídeo, no de la foto.

## Paso 4 · Los prompts

Uno por trozo, a partir de `plantillas/prompt.txt`. En todos:

- La **misma descripción de la persona, palabra por palabra**. Si la cambias, sale otra persona en cada trozo.
- La **misma foto de referencia** (`"ref"` en `pruebas.json`).
- El **audio de referencia** se coge solo de `audios/<nombre>.mp3`. No hay que ponerlo en `pruebas.json`.
- La **asimetría repetida**, si la hay (regla 5).
- **Las dos manos** y todo lo que esté quieto en el plano (regla 3).
- El **producto clip a clip** (regla 4).
- `"Quita el texto del vídeo, tanto si sale arriba como abajo, y también los emojis."`
- `"Mantén los mismos N clips en el mismo orden y con la misma duración que el original, incluido el último: …"`

Se guarda en `<carpeta>/ronda1/pruebas.json`:
```json
[{"nombre":"tramo1","video":"tramo1.mp4","ref":"avatar/avatar.jpg","duracion":15,"prompt":"..."}]
```

## Paso 5 · Lanzar y revisar

```bash
python3 scripts/lanzar.py <carpeta>/ronda1
python3 scripts/comparar.py <carpeta>/tramo1.mp4 <carpeta>/ronda1/tramo1.mp4 rev1.jpg
```

- **No hay que subir nada a ningún sitio.** La API solo acepta enlaces públicos, pero `lanzar.py` ya sube cada trozo y cada foto de referencia a uguu.se (alojamiento temporal, 24 h) y le pasa la URL. No preguntes dónde subirlos ni se lo pidas a la persona: ya está hecho.
- Tarda entre 6 y 18 minutos por trozo. Van todos a la vez.
- Si el filtro de contenido bloquea un trozo, **no cuesta nada** y lo sabes en menos de un minuto. Cambia la frase que lo haya disparado. Con barrigas o ropa interior, evita cosas como "deja ver la piel".
- **Revisa cada trozo con `comparar.py` antes de unir.** Busca: persona igual, producto correcto, **ninguna mano desaparecida**, sin texto, último plano presente.
- Lo que falle se repite cambiando **solo esa frase** del prompt. No lo repitas entero.

## Paso 6 · Unir

```bash
python3 scripts/unir.py <carpeta> <carpeta>/ronda1
```

Elige el modo solo y lo dice al empezar:

- **Voz de la IA** (si los clips traen audio y existe `audios/`): **recorta** la cola sobrante de cada trozo y se queda con la voz generada. Nunca estira: la voz ya está en su sitio.
- **Audio del original encima** (si los clips vienen mudos): devuelve cada trozo a su duración exacta clavando los fotogramas y le pega el audio del `viral_full.mp4`.

Al final dice el desfase: si pasa de 0,15 s, algo está mal en `tramos.json`.

## Paso 7 · Enseñar el borrador ✋

**Antes de preguntar nada, se enseña el vídeo.** La persona no puede decidir sobre subtítulos ni formato si todavía no ha visto cómo ha quedado.

```bash
python3 scripts/comparativa.py <carpeta>/viral_full.mp4 <carpeta>/REPLICA.mp4
```

- Deja los **dos** archivos en `~/Downloads` y ábrelos: la réplica sola y la comparativa.
- La comparativa lleva el original a la izquierda y la réplica a la derecha, y suena el audio de la réplica.
- Decir el **coste real** hasta aquí, sumando los `resultados.json`.
- Decir **qué no salió perfecto**. Siempre hay algo. Es mejor decirlo que esperar a que lo vean.
- **Parar aquí.** Si algo no les convence, se repite solo ese trozo antes de seguir.

## Paso 8 · El acabado, preguntando de una en una

Cada persona replica un tipo de anuncio distinto y quiere cosas distintas. **No preguntar todo de golpe ni dar una lista.** Se pregunta **una cosa, se hace, se enseña, y se pasa a la siguiente.** Si dicen que no a algo, se salta y se sigue.

Este es el orden, porque cada paso se monta encima del anterior:

**1 · Subtítulos**

> ¿Le pongo subtítulos? ¿En el mismo idioma o traducidos?

```bash
python3 scripts/subtitular.py <video.mp4> <idioma> <estilo> --clave palabra,palabra,...
```

| Estilo | Cómo queda |
|---|---|
| **`original`** (por defecto) | Una palabra cada vez, blanca con sombra, a la altura del pecho, con un golpecito al entrar. Las de `--clave` en **amarillo** |
| `limpio` | Grupos de 3 palabras, blanco con borde negro, abajo. Sin animación |

- `idioma`: código de dos letras (`en`, `es`…) o `auto`.
- **`--clave` lo eliges tú**, no la persona: el producto, el problema, los números y las promesas. Entre 8 y 12 en un anuncio de 45 s.
- Whisper devuelve la frase entera, no palabra a palabra: el script reparte el hueco **según lo que mide cada palabra**. A ojo no se nota.
- Deja un `_texto.srt` al lado: si hay una palabra mal transcrita, se corrige ahí y se vuelve a quemar sin volver a pagar.

**2 · Sus textos en pantalla**

> ¿Quieres poner tu titular, tu oferta o tu llamada a la acción encima?

```bash
python3 scripts/texto.py "Linea 1|Linea 2 😍" <carpeta>/elementos/titular.png --estilo caja
```

`caja` es texto negro sobre caja blanca redondeada, el estilo más usado en anuncios. `limpio` es blanco con borde negro. Los emojis salen a color en Mac. El PNG luego se coloca con `elementos.py`.

**3 · Los elementos que llevaba el original**

> El anuncio original tenía [una captura de un estudio en el segundo 6 / un vídeo insertado / unos emojis]. ¿Tienes algo tuyo para poner ahí?

```bash
python3 scripts/elementos.py plantilla <carpeta>
python3 scripts/elementos.py montar <video.mp4> <carpeta>/elementos.json
```

Esto es lo que hace que una réplica parezca la misma campaña y no una imitación. **Lo apuntas tú en el paso 1**, en la columna "Elementos encima" de la tabla de clips: qué era, en qué segundo entra y sale, dónde está y qué tamaño ocupa. Si no se apunta ahí, luego no se puede recolocar.

`elementos.json`, un objeto por elemento:

| Campo | Qué es |
|---|---|
| `desde` / `hasta` | Segundo en que entra y sale, copiado del original |
| `archivo` | Un `.png`, un `.mp4` para vídeo dentro del vídeo, o `emoji:🧪` (solo Mac) |
| `x` / `y` | Centro del elemento, de 0 a 1. `0.5` es el medio |
| `ancho` | Lo que ocupa respecto al ancho del vídeo |
| `entrada` | `fade`, `pop` (entra con un golpecito) o `ninguna` |
| `que_era` | Qué había ahí en el original. Solo para acordarse |

- La **`y` entre 0.16 y 0.84** para que quepa en la zona segura 4:5. Si el original lo tenía más arriba, avisar de que en Instagram se puede tapar.
- Si no tienen nada para un hueco, se quita de la lista. Mejor vacío que relleno con cualquier cosa.
- **Nunca reutilizar la captura ni el logo del competidor.** Ese es justo el elemento que hay que cambiar.

**4 · El formato**

> ¿Lo quieres también en otro formato? Para Meta suele interesar el 4:5.

```bash
python3 scripts/formato.py <video.mp4> 4:5
```

`9:16` (1080×1920) · `4:5` (1080×1350) · `1:1` (1080×1080) · `16:9` (1920×1080). Recorta del centro, que es lo normal en anuncios. Con `--rellenar` no recorta nada y rellena los lados con el propio vídeo desenfocado.

**Después de cada cambio**, abrir el resultado y enseñarlo. No encadenar tres cosas y enseñar solo el final: si algo no gusta, no se sabe cuál fue.

## Paso 9 · Entregar

- Deja en `~/Downloads` el MP4 final y la comparativa, y ábrelos con `open`.
- Si hay varios formatos, dilo claro: cuál es para dónde.
- Di el **coste real** total.
- Di otra vez **qué no quedó perfecto**, aunque ya lo dijeras en el paso 7.

## Trampas conocidas

- **Windows**: dentro de un filtro de ffmpeg, una ruta tipo `C:\carpeta` revienta — la barra invertida escapa y los dos puntos separan opciones. Los scripts ya la convierten (`para_filtro`), pero si escribes un filtro a mano, acuérdate. Lo mismo con la lista del `concat`: barras normales siempre.
- **Emojis**: en Mac salen con la fuente de Apple, en Windows con Segoe UI Emoji. En Linux no hay, así que ahí hay que usar un PNG.

- **zsh**: dentro de un filtro de ffmpeg, escribe `${VAR}` y no `$VAR`. Un `$F:t` se interpreta como un modificador de zsh y revienta el comando.
- **Rutas con espacios** en las fuentes de `drawtext`: copia la fuente a una ruta sin espacios.
- **480P siempre**: si no pones la resolución, la API cobra 1080P.
- **Apunta los `task_id`**: el script lo hace solo en `task_ids.txt`. Una tarea perdida es un vídeo pagado que no se recupera.

## Cuánto cuesta

| | |
|---|---|
| Wan 3.0 a 480P | ~0,066 $ por segundo |
| Un anuncio de 15 s | ~1 $ |
| Un anuncio de 75 s | ~5 $ la pasada, 7 $ con las repeticiones |
| Un trozo bloqueado por el filtro | 0 $ |
