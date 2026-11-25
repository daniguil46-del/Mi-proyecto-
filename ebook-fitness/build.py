# -*- coding: utf-8 -*-
"""Genera el ebook 'Método DEFINE' (HTML listo para convertir a PDF A4).

Uso:  python3 build.py   ->  crea metodo-define.html
      node render.js     ->  crea metodo-define.pdf
"""
import random, math, os

BOOK = "MÉTODO DEFINE"
AUTHOR = "[Tu nombre o marca]"

PAGES = []      # (html, opts)
TOC = []        # (title, page_number, level)
IMAGES = []     # dicts

# ---------------------------------------------------------------- helpers
def page(html, toc=None, toc_level=1, cls="", footer=True):
    PAGES.append((html, {"cls": cls, "footer": footer}))
    n = len(PAGES)
    if toc:
        TOC.append((toc, n, toc_level))
    return n

CAM = ('<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
       'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7h3l2-3h6l2 3h3a1 1 0 0 1 1 1v11a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V8a1 1 0 0 1 1-1z"/>'
       '<circle cx="12" cy="13" r="4"/></svg>')

STYLE_SUFFIX = ("photorealistic editorial fitness photography, bright natural daylight, clean modern setting, "
                "warm neutral tones with subtle coral-orange accents, shallow depth of field, high detail, no text, no logos")

def img(title, desc, fmt, prompt, h="60mm", w="100%", dark=False, small=False):
    n = len(IMAGES) + 1
    IMAGES.append({"n": n, "title": title, "desc": desc, "fmt": fmt, "prompt": prompt})
    cls = "ph" + (" dark" if dark else "") + (" small" if small else "")
    d = "" if small else f'<div class="d">{desc}</div>'
    return (f'<div class="{cls}" style="height:{h};width:{w}">{CAM}'
            f'<span class="num">IMAGEN {n:02d}</span><div class="t">{title}</div>{d}'
            f'<div class="f">Formato {fmt} · Prompt en el Anexo A (pág. %%ANEXO%%)</div></div>')

def box(kind, label, body):
    return f'<div class="box {kind}"><span class="lbl">{label}</span>{body}</div>'

def tip(body, label="Consejo"):  return box("tip", label, body)
def warn(body, label="Error típico"): return box("warn", label, body)
def key(body, label="Dato clave"): return box("key", label, body)

def table(headers, rows, cls="", widths=None):
    col = ""
    if widths:
        col = "<colgroup>" + "".join(f'<col style="width:{w}">' for w in widths) + "</colgroup>"
    th = "".join(f"<th>{h}</th>" for h in headers)
    trs = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="{cls}">{col}<thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>'

def opener(num, title, intro):
    return (f'<div class="kicker">Capítulo {num}</div><h1 class="chap">{title}</h1>'
            f'<div class="bar"></div><p class="lead">{intro}</p>')

def ul(items, cls=""):
    return f'<ul class="{cls}">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"

def ol(items, cls=""):
    return f'<ol class="{cls}">' + "".join(f"<li>{i}</li>" for i in items) + "</ol>"

# ================================================================ PÁGINAS

# 1 · PORTADA ------------------------------------------------------------
page(f'''
<div class="cover-top">
  <div class="cover-kicker">GUÍA PRÁCTICA · 12 SEMANAS</div>
  <div class="cover-title">MÉTODO<br><span>DEFINE</span></div>
  <div class="cover-sub">Pierde grasa sin dietas extremas: entrenamiento, nutrición y plantillas para conseguirlo paso a paso.</div>
</div>
{img("Imagen de portada", "Persona en forma, sonriente y segura, de pie en un gimnasio luminoso con una mancuerna en la mano. Ropa deportiva negra con detalles naranjas. Encuadre de cintura para arriba, fondo oscuro desenfocado.", "vertical 3:4", "Fit confident person in their 30s smiling, standing in a modern gym holding a dumbbell, black athletic wear with coral-orange details, waist-up framing, dark blurred gym background with warm rim light, " + STYLE_SUFFIX, h="118mm", dark=True)}
<div class="cover-pills"><span>Entrenamiento gimnasio y casa</span><span>Plan de nutrición</span><span>Plantillas imprimibles</span></div>
<div class="cover-author">por {AUTHOR}</div>
''', cls="cover", footer=False)

# 2 · CRÉDITOS / AVISO ---------------------------------------------------
page(f'''
<div class="kicker">Antes de empezar</div>
<h1>Aviso importante</h1>
<div class="bar"></div>
<p>Esta guía tiene una finalidad <b>informativa y educativa</b>. Recoge principios de entrenamiento y nutrición
ampliamente aceptados para la pérdida de grasa en personas adultas y sanas.</p>
<p><b>No sustituye el consejo de un médico, dietista-nutricionista ni de otro profesional sanitario.</b> Consulta con
un profesional antes de empezar si:</p>
{ul(["tienes alguna enfermedad (cardiovascular, diabetes, hipertensión, problemas renales…) o tomas medicación;",
     "tienes una lesión o dolor articular;",
     "estás embarazada o en periodo de lactancia;",
     "tienes o has tenido algún trastorno de la conducta alimentaria;",
     "eres menor de 18 años."])}
<p>Si durante el ejercicio sientes dolor en el pecho, mareo, falta de aire anormal o dolor agudo, <b>detente
inmediatamente</b> y busca atención médica.</p>
<p>Los resultados varían de una persona a otra y dependen de muchos factores (constancia, punto de partida,
genética, descanso, salud…). <b>Esta guía no garantiza ningún resultado concreto.</b></p>
{key("Aquí no vas a encontrar dietas de 800 kcal, quemagrasas milagrosos ni promesas de «-10 kg en 2 semanas». "
     "Vas a encontrar un método sostenible que puedes mantener toda la vida.", "Nuestra filosofía")}
<div class="legal">
<p><b>© 2026 {AUTHOR}.</b> Todos los derechos reservados.</p>
<p>Queda prohibida la reproducción, distribución, comunicación pública o transformación total o parcial de esta obra
sin autorización expresa del autor. Esta copia es para uso personal del comprador.</p>
<p>Versión 1.0 · Diseño y maquetación: {AUTHOR}</p>
</div>
''')

# 3 · ÍNDICE -------------------------------------------------------------
page('<div class="kicker">Contenido</div><h1>Índice</h1><div class="bar"></div>%%TOC%%')

# 4 · CÓMO USAR ESTA GUÍA ------------------------------------------------
page(f'''
<div class="kicker">Bienvenida</div>
<h1>Cómo usar esta guía</h1>
<div class="bar"></div>
<p class="lead">Perder grasa no va de fuerza de voluntad infinita. Va de tener un plan claro, entender por qué
funciona y medir tu progreso. Eso es exactamente lo que tienes en tus manos.</p>
<h2>Tu hoja de ruta en 5 pasos</h2>
<div class="steps">
  <div class="step"><b>1</b><div><h3>Entiende lo básico</h3><p>Lee los capítulos 1 y 2. Son 15 minutos y te ahorrarán meses de errores.</p></div></div>
  <div class="step"><b>2</b><div><h3>Calcula tus números</h3><p>Usa la hoja del capítulo 2 para saber cuántas calorías y cuánta proteína necesitas.</p></div></div>
  <div class="step"><b>3</b><div><h3>Elige dónde entrenar</h3><p>Todas las rutinas tienen versión de <b>gimnasio</b> y versión de <b>casa</b>.</p></div></div>
  <div class="step"><b>4</b><div><h3>Imprime las plantillas</h3><p>Al final tienes registros de entrenamiento, hábitos, comidas y progreso.</p></div></div>
  <div class="step"><b>5</b><div><h3>Revisa cada semana</h3><p>Una vez por semana, compara tus medias y ajusta solo si hace falta.</p></div></div>
</div>
<div class="cols2">
<div>
<h3>Qué vas a necesitar</h3>
{ul(["Una báscula y una cinta métrica.",
     "Acceso a un gimnasio <i>o</i> un par de mancuernas, una garrafa o una mochila con peso.",
     "Una goma elástica (opcional, para casa).",
     "Las plantillas impresas o una libreta."])}
</div>
<div>
<h3>Iconos que verás</h3>
{tip("Trucos prácticos para aplicarlo en tu día a día.")}
{warn("Fallos frecuentes que frenan el progreso.")}
</div>
</div>
''', toc="Cómo usar esta guía")

# 5 · CAP 1 OPENER -------------------------------------------------------
page(f'''
{opener(1, "Cómo se pierde grasa de verdad",
        "Olvida los trucos milagro. La pérdida de grasa sigue unas reglas sencillas, y cuando las entiendes dejas de depender de modas.")}
{img("Persona caminando al aire libre", "Persona caminando a paso ligero por un parque al amanecer, auriculares puestos, ropa deportiva cómoda, expresión tranquila y decidida.", "horizontal 16:9", "Person power-walking in a city park at sunrise, wearing earphones and comfortable athletic clothes, calm determined expression, golden morning light, " + STYLE_SUFFIX, h="78mm")}
<h2>Las 3 ideas que debes llevarte</h2>
<div class="cards3">
  <div class="card"><div class="cnum">01</div><h3>Déficit calórico</h3><p>Solo pierdes grasa si, de media, gastas más energía de la que comes. Sin excepciones.</p></div>
  <div class="card"><div class="cnum">02</div><h3>Proteger el músculo</h3><p>Entrenar fuerza y comer suficiente proteína hace que lo que pierdas sea grasa, no músculo.</p></div>
  <div class="card"><div class="cnum">03</div><h3>Constancia</h3><p>Un plan «bueno» que cumples gana siempre a un plan «perfecto» que abandonas en dos semanas.</p></div>
</div>
''', toc="1. Cómo se pierde grasa de verdad")

# 6 · BALANCE ENERGÉTICO -------------------------------------------------
balance_svg = '''
<svg viewBox="0 0 520 216" width="100%" font-family="Inter">
  <g transform="translate(0,24)">
  <rect x="255" y="40" width="10" height="120" rx="3" fill="#15192B"/>
  <path d="M200 175 h120 l-20 -18 h-80 z" fill="#15192B"/>
  <g transform="rotate(7 260 45)">
    <rect x="60" y="40" width="400" height="9" rx="4" fill="#15192B"/>
    <line x1="100" y1="49" x2="80" y2="100" stroke="#15192B" stroke-width="2"/>
    <line x1="100" y1="49" x2="150" y2="100" stroke="#15192B" stroke-width="2"/>
    <path d="M65 100 h100 a50 22 0 0 1 -100 0z" fill="#FFB703"/>
    <line x1="420" y1="49" x2="370" y2="100" stroke="#15192B" stroke-width="2"/>
    <line x1="420" y1="49" x2="440" y2="100" stroke="#15192B" stroke-width="2"/>
    <path d="M355 100 h100 a50 22 0 0 1 -100 0z" fill="#FF5A36"/>
  </g>
  <text x="115" y="124" text-anchor="middle" font-size="13" font-weight="700" fill="#15192B">ENERGÍA QUE ENTRA</text>
  <text x="115" y="140" text-anchor="middle" font-size="11" fill="#6B7085">comida y bebida</text>
  <text x="405" y="168" text-anchor="middle" font-size="13" font-weight="700" fill="#15192B">ENERGÍA QUE GASTAS</text>
  <text x="405" y="184" text-anchor="middle" font-size="11" fill="#6B7085">metabolismo + movimiento</text>
  </g>
  <text x="260" y="14" text-anchor="middle" font-size="12" font-weight="700" fill="#FF5A36">Si gastas más de lo que comes → usas tu grasa como energía</text>
</svg>'''

stack_svg = '''
<svg viewBox="0 0 520 92" width="100%" font-family="Inter">
  <rect x="0" y="10" width="322" height="38" fill="#15192B" rx="4"/>
  <rect x="322" y="10" width="104" height="38" fill="#FF5A36"/>
  <rect x="426" y="10" width="52" height="38" fill="#FFB703"/>
  <rect x="478" y="10" width="42" height="38" fill="#2D6CDF" rx="4"/>
  <text x="161" y="34" text-anchor="middle" font-size="12" font-weight="700" fill="#fff">Metabolismo basal · 60–70 %</text>
  <text x="374" y="34" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">NEAT 15–30 %</text>
  <text x="452" y="34" text-anchor="middle" font-size="10" font-weight="700" fill="#15192B">Digestión</text>
  <text x="499" y="34" text-anchor="middle" font-size="9.5" font-weight="700" fill="#fff">Entreno</text>
  <text x="0" y="68" font-size="10" fill="#6B7085">Reparto aproximado del gasto diario. Digestión ≈ 10 % · Entrenamiento ≈ 5–10 %.</text>
  <text x="0" y="83" font-size="10" fill="#6B7085">El NEAT (pasos y movimiento diario) es la parte que más puedes cambiar.</text>
</svg>'''

page(f'''
<h2 style="margin-top:0">El balance energético</h2>
<p>Tu cuerpo funciona como una balanza. En un lado está la energía que comes y bebes; en el otro, la que gastas
para vivir y moverte. Cuando durante semanas gastas un poco más de lo que comes (<b>déficit calórico</b>), tu cuerpo
cubre la diferencia usando sus reservas: principalmente, la grasa.</p>
{balance_svg}
<h2>¿En qué gastas la energía?</h2>
<p>Mucha gente cree que lo que más quema es el gimnasio. En realidad, el entrenamiento es la parte más pequeña del gasto
diario. Mira el reparto:</p>
{stack_svg}
{ul(["<b>Metabolismo basal:</b> lo que gastas solo por estar vivo (respirar, mantener la temperatura, órganos…).",
     "<b>NEAT:</b> todo el movimiento que no es entrenamiento: caminar, subir escaleras, limpiar, estar de pie.",
     "<b>Digestión:</b> procesar la comida también gasta energía, sobre todo la proteína.",
     "<b>Entrenamiento:</b> importante para tu salud y tu músculo, pero no es lo que más calorías quema."])}
{key("La pérdida de grasa se decide sobre todo en la <b>cocina</b> y en los <b>pasos diarios</b>. El entrenamiento de fuerza "
     "se encarga de que el peso que pierdas sea grasa y no músculo.")}
''')

# 7 · EXPECTATIVAS REALISTAS ----------------------------------------------
random.seed(7)
days = 28
pts = []
for d in range(days):
    trend = 75 - d * (1.6 / days)
    noise = [0.5, -0.3, 0.2, 0.7, -0.4, 0.1, -0.2][d % 7] + random.uniform(-0.25, 0.25)
    pts.append(trend + noise)
W, H, X0, Y0 = 500, 150, 34, 12
lo, hi = 72.5, 76.0
def sx(d): return X0 + d * (W - X0 - 10) / (days - 1)
def sy(v): return Y0 + (hi - v) * (H - Y0 - 22) / (hi - lo)
poly = " ".join(f"{sx(d):.1f},{sy(v):.1f}" for d, v in enumerate(pts))
avg = []
for wk in range(4):
    seg = pts[wk*7:(wk+1)*7]
    avg.append((wk*7 + 3, sum(seg)/7))
avgline = " ".join(f"{sx(d):.1f},{sy(v):.1f}" for d, v in avg)
grid = "".join(f'<line x1="{X0}" x2="{W-10}" y1="{sy(v):.1f}" y2="{sy(v):.1f}" stroke="#E6E2DD"/>'
               f'<text x="{X0-6}" y="{sy(v)+4:.1f}" font-size="9.5" text-anchor="end" fill="#6B7085">{v:.0f}</text>'
               for v in [73, 74, 75, 76])
dots = "".join(f'<circle cx="{sx(d):.1f}" cy="{sy(v):.1f}" r="2.6" fill="#B9BCC8"/>' for d, v in enumerate(pts))
adots = "".join(f'<circle cx="{sx(d):.1f}" cy="{sy(v):.1f}" r="5" fill="#FF5A36" stroke="#fff" stroke-width="2"/>'
                f'<text x="{sx(d):.1f}" y="{sy(v)-10:.1f}" font-size="10" text-anchor="middle" font-weight="700" fill="#FF5A36">{v:.1f}</text>' for d, v in avg)
wklabels = "".join(f'<text x="{sx(w*7+3):.1f}" y="{H}" font-size="10" text-anchor="middle" fill="#6B7085">Semana {w+1}</text>' for w in range(4))
chart = f'''<svg viewBox="0 0 {W} {H+6}" width="100%" font-family="Inter">{grid}
<polyline points="{poly}" fill="none" stroke="#B9BCC8" stroke-width="1.4"/>{dots}
<polyline points="{avgline}" fill="none" stroke="#FF5A36" stroke-width="3"/>{adots}{wklabels}</svg>
<div class="legend"><span class="lg grey"></span>Peso diario <span class="lg orange"></span>Media semanal (kg)</div>'''

page(f'''
<h2 style="margin-top:0">Expectativas realistas</h2>
<p>Un ritmo sano y sostenible de pérdida de grasa es de <b>entre el 0,5 % y el 1 % de tu peso corporal por semana</b>.
Más rápido suele significar perder músculo, pasar hambre y recuperar el peso después.</p>
{table(["Peso actual", "Pérdida semanal recomendada", "En 12 semanas (aprox.)"],
       [["60 kg", "0,3 – 0,6 kg", "3,5 – 7 kg"], ["70 kg", "0,35 – 0,7 kg", "4 – 8 kg"],
        ["80 kg", "0,4 – 0,8 kg", "5 – 9,5 kg"], ["90 kg", "0,45 – 0,9 kg", "5,5 – 10,5 kg"]])}
<p class="small muted">Cifras orientativas. El ritmo suele ser mayor al principio y más lento a medida que te acercas a tu objetivo.</p>
<h2>Tu peso sube y baja cada día (y es normal)</h2>
<p>El peso de la báscula cambia hasta 1–2 kg de un día para otro por el agua, la sal, los hidratos, la digestión o
el ciclo menstrual. Por eso <b>no importa el peso de un día, sino la tendencia</b>. Fíjate en este ejemplo real de 4 semanas:</p>
{chart}
{warn("Pesarse un lunes después de una cena con amigos, ver +1 kg y abandonar. Ese kilo es agua y comida en tránsito, "
      "no grasa. Para ganar 1 kg de grasa harían falta unas 7.000 kcal de más.")}
''')

# 8 · CAP 2 · FÓRMULAS ---------------------------------------------------
page(f'''
{opener(2, "Calcula tus números", "Con 3 datos y 5 minutos vas a saber cuántas calorías y cuánta proteína necesitas. Sin adivinar.")}
<h2>Paso 1 · Tu metabolismo basal (TMB)</h2>
<p>Usamos la fórmula de <b>Mifflin-St Jeor</b>, una de las más precisas para la población general:</p>
<div class="formula"><span>Hombres</span>TMB = (10 × peso en kg) + (6,25 × altura en cm) − (5 × edad) <b>+ 5</b></div>
<div class="formula"><span>Mujeres</span>TMB = (10 × peso en kg) + (6,25 × altura en cm) − (5 × edad) <b>− 161</b></div>
<h2>Paso 2 · Tu gasto diario (mantenimiento)</h2>
<p>Multiplica tu TMB por tu factor de actividad. El resultado son las calorías que mantienen tu peso estable.</p>
{table(["Nivel de actividad", "Descripción", "Factor"],
       [["Sedentario", "Trabajo sentado, menos de 5.000 pasos, sin entrenar", "× 1,2"],
        ["Ligero", "Entrenas 1–3 días/semana o caminas bastante", "× 1,375"],
        ["Moderado", "Entrenas 3–5 días/semana y te mueves a diario", "× 1,55"],
        ["Muy activo", "Entrenas 6–7 días o trabajo físico", "× 1,725"]], widths=["24%", "60%", "16%"])}
{tip("Si dudas entre dos niveles, elige <b>el más bajo</b>. Casi todos sobreestimamos lo que nos movemos.")}
<h2>Paso 3 · Tus calorías para perder grasa</h2>
<p>Resta entre un <b>15 % y un 25 %</b> a tus calorías de mantenimiento. Te recomendamos empezar con un <b>20 %</b>:</p>
<div class="formula"><span>Objetivo</span>Calorías objetivo = Mantenimiento × 0,80</div>
{warn("Recortar a lo bestia. Sin supervisión profesional, no bajes de unas 1.200 kcal (mujeres) o 1.500 kcal (hombres) "
      "ni por debajo de tu TMB. Un déficit enorme dispara el hambre y hace que pierdas músculo.", "Cuidado")}
''', toc="2. Calcula tus números")

# 9 · CAP 2 · MACROS + EJEMPLOS -------------------------------------------
page(f'''
<h2 style="margin-top:0">Paso 4 · Reparte tus macronutrientes</h2>
<p>Las calorías deciden si pierdes peso. Los macronutrientes deciden <b>qué</b> pierdes (grasa o músculo) y cómo te sientes.</p>
<div class="macros">
  <div class="macro p"><div class="mt">Proteína</div><div class="mv">1,6 – 2,2 g</div><div class="mu">por kg de peso · 4 kcal/g</div><p>Protege el músculo y es la que más sacia. Empieza con 1,8 g/kg.</p></div>
  <div class="macro g"><div class="mt">Grasas</div><div class="mv">0,7 – 1 g</div><div class="mu">por kg de peso · 9 kcal/g</div><p>Necesarias para tus hormonas. Empieza con 0,8 g/kg.</p></div>
  <div class="macro c"><div class="mt">Hidratos</div><div class="mv">El resto</div><div class="mu">de tus calorías · 4 kcal/g</div><p>Tu gasolina para entrenar con energía.</p></div>
</div>
<h2>Ejemplo resuelto: Laura</h2>
<p class="small muted">30 años · 68 kg · 165 cm · entrena 2–3 días y camina poco (factor ligero)</p>
{table(["Paso", "Cálculo", "Resultado"],
       [["1. TMB", "(10 × 68) + (6,25 × 165) − (5 × 30) − 161", "≈ 1.400 kcal"],
        ["2. Mantenimiento", "1.400 × 1,375", "≈ 1.925 kcal"],
        ["3. Objetivo (−20 %)", "1.925 × 0,80", "<b>≈ 1.550 kcal</b>"],
        ["4a. Proteína", "68 × 1,8 = 122 g → 122 × 4", "122 g · 490 kcal"],
        ["4b. Grasas", "68 × 0,8 = 54 g → 54 × 9", "54 g · 485 kcal"],
        ["4c. Hidratos", "(1.550 − 490 − 485) ÷ 4", "≈ 145 g"]], widths=["24%", "50%", "26%"])}
<h2>Ejemplo rápido: Carlos</h2>
<p class="small muted">35 años · 85 kg · 178 cm · entrena 4 días y trabaja de pie (factor moderado)</p>
{table(["TMB", "Mantenimiento", "Objetivo", "Proteína", "Grasas", "Hidratos"],
       [["≈ 1.790", "≈ 2.780", "<b>≈ 2.200 kcal</b>", "153 g", "68 g", "≈ 245 g"]])}
{tip("No hace falta que cuadres los gramos al milímetro. Si cada día aciertas tus calorías ±100 kcal y llegas a tu proteína, vas por el buen camino.")}
''')

# 10 · HOJA DE CÁLCULO -----------------------------------------------------
def field(label, unit=""):
    return f'<div class="field"><span>{label}</span><i></i><em>{unit}</em></div>'
page(f'''
<div class="kicker">Plantilla</div>
<h1>Tu hoja de cálculo</h1>
<div class="bar"></div>
<p>Rellénala con lápiz. La volverás a usar cada vez que recalcules.</p>
<div class="sheet">
  <h3>Mis datos</h3>
  <div class="fields3">{field("Peso", "kg")}{field("Altura", "cm")}{field("Edad", "años")}</div>
  <div class="fields2">{field("Sexo")}{field("Fecha")}</div>
  <h3>Mis calorías</h3>
  {field("1. TMB (fórmula del paso 1)", "kcal")}
  {field("2. Factor de actividad", "×")}
  {field("3. Mantenimiento (TMB × factor)", "kcal")}
  {field("4. Calorías objetivo (mantenimiento × 0,80)", "kcal")}
  <h3>Mis macros</h3>
  {field("Proteína: peso × 1,8 =", "g/día")}
  {field("Grasas: peso × 0,8 =", "g/día")}
  {field("Hidratos: (objetivo − proteína×4 − grasas×9) ÷ 4 =", "g/día")}
  <h3>Mis objetivos de hábitos</h3>
  <div class="fields2">{field("Pasos diarios", "pasos")}{field("Días de entreno", "/semana")}</div>
</div>
{key("Recalcula cuando hayas perdido 4–5 kg, o si llevas <b>3 semanas seguidas</b> sin que baje tu media semanal "
     "(y estás cumpliendo el plan).", "¿Cuándo recalcular?")}
''')

# 11 · CAP 3 OPENER + PLATO ----------------------------------------------
plate_svg = '''
<svg viewBox="0 0 520 250" width="100%" font-family="Inter">
  <circle cx="140" cy="125" r="118" fill="#F2EFEA"/>
  <circle cx="140" cy="125" r="104" fill="#fff" stroke="#E6E2DD" stroke-width="2"/>
  <path d="M140 125 L140 21 A104 104 0 0 0 140 229 Z" fill="#7BC67E"/>
  <path d="M140 125 L140 21 A104 104 0 0 1 244 125 Z" fill="#FF5A36"/>
  <path d="M140 125 L244 125 A104 104 0 0 1 140 229 Z" fill="#FFB703"/>
  <text x="88" y="130" text-anchor="middle" font-size="15" font-weight="800" fill="#fff">½</text>
  <text x="88" y="148" text-anchor="middle" font-size="10.5" font-weight="700" fill="#fff">VERDURAS</text>
  <text x="182" y="88" text-anchor="middle" font-size="14" font-weight="800" fill="#fff">¼</text>
  <text x="182" y="104" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">PROTEÍNA</text>
  <text x="182" y="165" text-anchor="middle" font-size="14" font-weight="800" fill="#15192B">¼</text>
  <text x="182" y="181" text-anchor="middle" font-size="10" font-weight="700" fill="#15192B">HIDRATOS</text>
  <circle cx="262" cy="40" r="14" fill="#2D6CDF"/><text x="262" y="45" text-anchor="middle" font-size="13" fill="#fff" font-weight="800">+</text>
  <text x="282" y="36" font-size="11" font-weight="700" fill="#15192B">Grasa saludable</text>
  <text x="282" y="51" font-size="10" fill="#6B7085">AOVE, aguacate o frutos secos</text>
  <g font-size="11" fill="#15192B">
    <rect x="300" y="78" width="12" height="12" rx="3" fill="#7BC67E"/><text x="320" y="88" font-weight="700">Verduras y hortalizas</text>
    <text x="320" y="103" fill="#6B7085" font-size="10">Ensalada, brócoli, pimiento…</text>
    <rect x="300" y="122" width="12" height="12" rx="3" fill="#FF5A36"/><text x="320" y="132" font-weight="700">Proteína</text>
    <text x="320" y="147" fill="#6B7085" font-size="10">Pollo, pescado, huevos, tofu…</text>
    <rect x="300" y="166" width="12" height="12" rx="3" fill="#FFB703"/><text x="320" y="176" font-weight="700">Hidratos de calidad</text>
    <text x="320" y="191" fill="#6B7085" font-size="10">Arroz, patata, pasta, avena…</text>
  </g>
</svg>'''
page(f'''
{opener(3, "Nutrición sin complicaciones", "Comida normal, de supermercado y con sabor. Sin alimentos prohibidos: solo con cantidades y elecciones inteligentes.")}
<h2>El método del plato</h2>
<p>¿No te apetece contar calorías todos los días? Construye tus comidas principales así y estarás muy cerca de tus números:</p>
{plate_svg}
<h2>Tu mano como medida</h2>
{table(["Grupo", "Ración por comida", "Equivale a…"],
       [["Proteína", "1–2 palmas", "100–150 g de carne o pescado, 2–3 huevos"],
        ["Hidratos", "1 puño", "½–1 taza de arroz o pasta cocidos, 1 patata mediana"],
        ["Verduras", "2 puños", "Un buen plato de ensalada o verdura"],
        ["Grasas", "1 pulgar", "1 cucharada de aceite, 1 puñado pequeño de frutos secos"]], widths=["18%", "24%", "58%"])}
''', toc="3. Nutrición sin complicaciones")

# 12 · PROTEÍNA ------------------------------------------------------------
page(f'''
<h2 style="margin-top:0">La proteína, tu mejor aliada</h2>
<p>Comer suficiente proteína mientras pierdes grasa tiene tres ventajas enormes: <b>protege tu músculo</b>, es el
nutriente que <b>más sacia</b> y tu cuerpo <b>gasta más energía</b> en digerirla. Repártela en 3–4 comidas de 25–40 g.</p>
{table(["Alimento", "Ración", "Proteína aprox."],
       [["Pechuga de pollo o pavo", "100 g (en crudo)", "22–23 g"],
        ["Ternera magra", "100 g (en crudo)", "21 g"],
        ["Merluza u otro pescado blanco", "150 g", "25 g"],
        ["Salmón", "100 g", "20 g"],
        ["Atún al natural", "1 lata (≈ 80 g escurrido)", "20 g"],
        ["Huevos", "2 unidades", "13 g"],
        ["Claras de huevo", "150 ml", "16 g"],
        ["Skyr o yogur griego 0 %", "200 g", "20 g"],
        ["Queso fresco batido 0 %", "250 g", "20 g"],
        ["Tofu firme", "150 g", "18–20 g"],
        ["Lentejas o garbanzos cocidos", "200 g", "16–18 g"]], widths=["44%", "32%", "24%"])}
<div class="cols2">
<div>{key("<b>Alimentos que más sacian:</b> verduras, legumbres, patata cocida, fruta entera, avena, huevos y yogur. Úsalos para no pasar hambre.")}</div>
<div>{warn("Olvidarse de lo que se bebe. Refrescos, zumos y alcohol suman muchas calorías sin saciar. El alcohol aporta 7 kcal por gramo.")}</div>
</div>
{tip("Truco fácil: empieza cada comida principal por la proteína y la verdura. Llegarás antes a la saciedad y comerás menos sin darte cuenta.")}
''')

# 13 · LISTA DE LA COMPRA --------------------------------------------------
def check_list(title, items):
    lis = "".join(f'<li><span class="cb"></span>{i}</li>' for i in items)
    return f'<div class="shop"><h3>{title}</h3><ul class="checks">{lis}</ul></div>'
page(f'''
<div class="kicker">Plantilla</div>
<h1>Lista de la compra base</h1>
<div class="bar"></div>
<p>Con esta lista puedes preparar todas las comidas y recetas de la guía. Marca lo que necesites y llévala al súper.</p>
<div class="shopgrid">
{check_list("Proteínas", ["Pechuga de pollo / pavo", "Ternera magra", "Salmón", "Merluza o bacalao", "Atún al natural (latas)", "Huevos y claras", "Pavo o jamón serrano en lonchas", "Tofu firme"])}
{check_list("Lácteos", ["Skyr o yogur griego 0 %", "Queso fresco batido 0 %", "Leche o bebida vegetal", "Queso fresco tipo Burgos"])}
{check_list("Hidratos", ["Arroz (blanco o integral)", "Patatas", "Copos de avena", "Pan integral", "Pasta o fideos de arroz", "Legumbres cocidas (bote)", "Quinoa o cuscús"])}
{check_list("Verduras", ["Espinacas / mezclum", "Brócoli", "Calabacín", "Pimientos", "Tomates y pepino", "Champiñones", "Cebolla y ajo", "Verduras congeladas para wok"])}
{check_list("Frutas", ["Plátanos", "Manzanas", "Frutos rojos (congelados)", "Naranjas o mandarinas", "Fruta de temporada"])}
{check_list("Grasas y despensa", ["Aceite de oliva virgen extra", "Aguacate", "Nueces o almendras", "Semillas de chía", "Especias, salsa de soja, mostaza", "Café e infusiones"])}
</div>
{tip("Haz la compra una vez a la semana con lista y dedica 1 hora el domingo a cocinar proteína, arroz y verduras para 3–4 días. "
     "Es el hábito que más ayuda a cumplir la dieta.", "Batch cooking")}
''')

# 14-15 · MENÚ SEMANAL -----------------------------------------------------
menu = {
 "Lunes": ["Overnight oats con frutos rojos ★", "Bowl de pollo, arroz y verduras ★", "1 yogur natural + 1 pieza de fruta", "Tortilla de claras con espinacas ★ + ensalada"],
 "Martes": ["Tostada integral con tomate, AOVE y pavo + café con leche", "Lentejas estofadas con verduras + 1 fruta", "Skyr con 15 g de nueces", "Merluza a la plancha con verduras asadas"],
 "Miércoles": ["Yogur griego con 30 g de avena y fruta", "Ensalada de garbanzos y atún ★", "1 manzana + queso fresco batido", "Salmón al horno con patata y brócoli ★"],
 "Jueves": ["Overnight oats con frutos rojos ★", "Wok de ternera y verduras ★", "Vaso de leche + 1 plátano", "Revuelto de 2 huevos con champiñones + pan integral"],
 "Viernes": ["Tostada integral con aguacate y huevo a la plancha", "Pollo al horno con patata y ensalada", "1 yogur natural + 1 pieza de fruta", "Crema de calabacín + pavo a la plancha"],
 "Sábado": ["Tortitas de avena y claras con fruta", "Paella (ración moderada) + ensalada grande", "1 pieza de fruta", "Ensalada completa: atún, huevo, garbanzos y verduras"],
 "Domingo": ["Café con leche + tostada con tomate y jamón serrano", "Comida libre con cabeza (ver consejo)", "Skyr con frutos rojos", "Tortilla de claras con verduras ★"],
}
def menu_table(dlist):
    rows = []
    for meal_i, meal in enumerate(["Desayuno", "Comida", "Merienda", "Cena"]):
        rows.append([f"<b>{meal}</b>"] + [menu[d][meal_i] for d in dlist])
    return table([""] + dlist, rows, cls="menu", widths=["16%"] + [f"{84/len(dlist):.1f}%"] * len(dlist))

page(f'''
<div class="kicker">Ejemplo de menú</div>
<h1>Una semana de comidas</h1>
<div class="bar"></div>
<p>Menú orientativo de unas <b>1.500–1.700 kcal</b> y más de 110 g de proteína al día. Si tus calorías son más altas,
aumenta las raciones de hidratos y grasas; si son más bajas, redúcelas. Las recetas marcadas con ★ las tienes en las páginas siguientes.</p>
{menu_table(["Lunes", "Martes", "Miércoles", "Jueves"])}
{tip("Repetir comidas no es aburrido, es práctico. La mayoría de personas que pierden grasa con éxito comen 10–15 platos que les gustan y los van rotando.")}
''', toc="Menú semanal de ejemplo", toc_level=2)

page(f'''
{menu_table(["Viernes", "Sábado", "Domingo"])}
<h2>Comer fuera y fines de semana</h2>
<div class="cols2">
<div>
<h3>En el restaurante</h3>
{ul(["Elige un plato con proteína clara: pescado, carne a la plancha, legumbres.",
     "Pide la guarnición de ensalada o verduras en lugar de patatas fritas.",
     "Pan o postre: uno de los dos, no ambos.",
     "Bebe agua, refresco zero o una sola caña/copa."])}
</div>
<div>
<h3>La «comida libre con cabeza»</h3>
{ul(["Una comida a la semana sin contar, pero sin atracón.",
     "Come despacio y para cuando estés satisfecho, no lleno.",
     "Al día siguiente, vuelve a tu plan normal sin compensar ni castigarte.",
     "Es una comida, no un fin de semana entero."])}
</div>
</div>
{warn("Cumplir de lunes a viernes y «desmadrarse» el fin de semana. Dos días muy por encima pueden borrar todo el déficit "
      "de la semana. El objetivo es que los fines de semana se parezcan bastante al resto.")}
''')

# 16-18 · RECETAS -----------------------------------------------------------
recipes = [
 ("Overnight oats con frutos rojos", "360", "27", "5 min + noche",
  ["40 g de copos de avena", "200 g de skyr o yogur griego 0 %", "100 g de frutos rojos (pueden ser congelados)", "10 g de semillas de chía", "Canela y unas gotas de vainilla"],
  ["Mezcla en un tarro la avena, el skyr, la chía y la canela.", "Añade un chorrito de leche si te gusta más líquido.", "Cubre con los frutos rojos y deja en la nevera toda la noche.", "Por la mañana, remueve y listo. Dura 2 días en la nevera."],
  "Tarro de cristal con overnight oats en capas: avena cremosa, yogur blanco y frutos rojos encima, sobre una mesa de madera clara con luz de mañana.",
  "Glass jar of layered overnight oats with creamy yogurt and fresh mixed berries on top, chia seeds, light wooden table, soft morning window light, overhead three-quarter angle, food photography, " + STYLE_SUFFIX,
  "Prepara 2 tarros a la vez y tendrás dos desayunos listos. Variante: cambia los frutos rojos por plátano y canela."),
 ("Tortilla de claras con espinacas", "340", "31", "10 min",
  ["1 huevo + 150 ml de claras", "80 g de espinacas frescas", "40 g de queso fresco tipo Burgos", "1 rebanada de pan integral (40 g)", "Sal, pimienta y un spray de aceite"],
  ["Saltea las espinacas 1 minuto en una sartén antiadherente.", "Bate el huevo con las claras, sal y pimienta y viértelo sobre las espinacas.", "Añade el queso troceado, tapa y cocina a fuego medio 3–4 minutos.", "Dobla la tortilla y sirve con el pan tostado."],
  "Tortilla francesa jugosa doblada, rellena de espinacas y queso fresco, en un plato blanco con una tostada integral al lado.",
  "Fluffy folded egg white omelette filled with spinach and fresh white cheese on a white plate, slice of toasted whole grain bread on the side, kitchen counter, " + STYLE_SUFFIX,
  "Añade champiñones, pimiento o cebolla: más volumen y saciedad por casi las mismas calorías."),
 ("Bowl de pollo, arroz y verduras", "490", "35", "20 min",
  ["130 g de pechuga de pollo", "60 g de arroz (en crudo)", "150 g de verduras (pimiento, calabacín, brócoli)", "10 g de aceite de oliva virgen extra", "Pimentón, ajo en polvo, sal y limón"],
  ["Cuece el arroz (o usa arroz ya cocido del batch cooking).", "Corta el pollo en tiras y sazónalo con pimentón, ajo y sal.", "Saltea el pollo con la mitad del aceite y reserva; saltea las verduras con el resto.", "Monta el bowl y añade unas gotas de limón."],
  "Bowl visto desde arriba con arroz blanco, tiras de pollo dorado con pimentón y verduras salteadas de colores.",
  "Overhead shot of a healthy bowl with white rice, golden paprika chicken strips and colorful sautéed vegetables (bell pepper, zucchini, broccoli), lemon wedge, " + STYLE_SUFFIX,
  "Con el batch cooking del domingo lo montas en 3 minutos. Variante: cambia el pollo por pavo o tofu."),
 ("Salmón al horno con patata y brócoli", "520", "34", "30 min",
  ["130 g de lomo de salmón", "200 g de patata", "150 g de brócoli", "5 g de aceite de oliva virgen extra", "Eneldo o perejil, limón, sal y pimienta"],
  ["Precalienta el horno a 200 °C. Corta la patata en rodajas finas y hornéala 15 minutos.", "Añade a la bandeja el salmón y el brócoli con el aceite y las especias.", "Hornea 12–15 minutos más hasta que el salmón esté hecho.", "Sirve con limón por encima."],
  "Lomo de salmón al horno dorado con rodajas de patata y ramilletes de brócoli en una bandeja de horno, con rodajas de limón.",
  "Oven-baked salmon fillet with herbs, golden sliced potatoes and broccoli florets on a baking tray, lemon slices, rustic kitchen, " + STYLE_SUFFIX,
  "Usa papel de horno y una sola bandeja: cena completa y casi nada que fregar."),
 ("Ensalada de garbanzos y atún", "410", "32", "10 min",
  ["150 g de garbanzos cocidos (escurridos)", "1 lata de atún al natural", "1 tomate, ½ pepino y ¼ de cebolla morada", "10 g de aceite de oliva virgen extra", "Vinagre, orégano y sal"],
  ["Lava y escurre los garbanzos.", "Trocea el tomate, el pepino y la cebolla.", "Mezcla todo con el atún escurrido.", "Aliña con aceite, vinagre, orégano y sal. Ideal para llevar en táper."],
  "Ensalada fresca de garbanzos con atún, tomate, pepino y cebolla morada en un bol de cerámica, vista cenital.",
  "Fresh chickpea and tuna salad with tomato, cucumber and red onion in a ceramic bowl, olive oil drizzle, oregano, overhead view, Mediterranean style, " + STYLE_SUFFIX,
  "Lleva el aliño aparte en el táper para que la ensalada no se ablande. Perfecta para el trabajo."),
 ("Wok de ternera y verduras", "495", "33", "15 min",
  ["130 g de ternera magra en tiras", "200 g de verduras para wok", "60 g de fideos de arroz (en crudo)", "10 ml de salsa de soja baja en sal", "5 g de aceite, jengibre y ajo"],
  ["Hidrata los fideos según el envase.", "Saltea la ternera a fuego fuerte 2 minutos con el aceite, el ajo y el jengibre. Reserva.", "Saltea las verduras 3–4 minutos para que queden crujientes.", "Junta todo con los fideos y la salsa de soja, y saltea 1 minuto más."],
  "Wok humeante con tiras de ternera, fideos de arroz y verduras crujientes de colores, palillos al lado.",
  "Steaming wok with beef strips, rice noodles and crunchy colorful stir-fry vegetables, soy sauce, chopsticks beside, dark kitchen background with warm light, " + STYLE_SUFFIX,
  "Las verduras congeladas para wok son igual de nutritivas y te ahorran 10 minutos de cortar."),
]
def recipe_html(r):
    name, kcal, prot, time, ing, steps, desc, prompt, rtip = r
    return f'''<div class="recipe">
  {img(name, desc, "vertical 4:5", prompt, h="96mm", w="72mm")}
  <div class="rbody">
    <h2>{name}</h2>
    <div class="badges"><span>{kcal} kcal</span><span>{prot} g proteína</span><span>⏱ {time}</span><span>1 ración</span></div>
    <h3>Ingredientes</h3>{ul(ing, "small")}<h3>Preparación</h3>{ol(steps, "small")}
    <div class="rtip"><b>Truco:</b> {rtip}</div>
  </div></div>'''
for i in range(0, 6, 2):
    hdr = '<div class="kicker">Recetas</div><h1>Recetas fáciles y saciantes</h1><div class="bar"></div>' if i == 0 else ""
    page(hdr + recipe_html(recipes[i]) + recipe_html(recipes[i+1]) +
         ('<p class="small muted">Valores nutricionales aproximados por ración.</p>'),
         toc="Recetas" if i == 0 else None, toc_level=2)

# 19 · CAP 4 OPENER --------------------------------------------------------
page(f'''
{opener(4, "Entrenar para perder grasa", "El objetivo del entrenamiento no es «quemar calorías», sino mantener (o ganar) músculo mientras pierdes grasa. Ese es el secreto de un cuerpo definido.")}
{img("Entrenamiento de fuerza en gimnasio", "Mujer haciendo remo con mancuerna en un banco, concentrada, gimnasio moderno y luminoso, buena técnica, espalda recta.", "horizontal 16:9", "Woman performing a single-arm dumbbell row on a bench with perfect form, focused expression, bright modern gym with large windows, " + STYLE_SUFFIX, h="70mm")}
<h2>Los 4 pilares del método</h2>
<div class="pillars">
  <div><b>1</b><h3>Fuerza</h3><p>3 días por semana de cuerpo completo. Le dice a tu cuerpo: «este músculo lo necesito».</p></div>
  <div><b>2</b><h3>Pasos</h3><p>7.000–10.000 pasos diarios. Es el «cardio» que más grasa quema a la larga.</p></div>
  <div><b>3</b><h3>Cardio</h3><p>Un complemento, no la base. De 1 a 3 sesiones cortas según la fase.</p></div>
  <div><b>4</b><h3>Descanso</h3><p>Dormir 7–9 horas. Sin descanso no hay progreso ni control del hambre.</p></div>
</div>
{warn("Hacer solo cardio para adelgazar. En déficit calórico, si no entrenas fuerza, una parte importante del peso que pierdes es músculo: "
      "acabas más pequeño, pero no más definido, y tu metabolismo baja.")}
''', toc="4. Entrenar para perder grasa")

# 20 · PROGRESIÓN + RIR ---------------------------------------------------
rir_colors = ["#D7263D", "#FF5A36", "#FF8C42", "#FFB703", "#8AC926", "#52B788"]
rir_lbl = ["Fallo", "1", "2", "3", "4", "5+"]
rir_txt = ["Ni una más", "Quedaba 1", "Quedaban 2", "Quedaban 3", "Fácil", "Muy fácil"]
rir_svg = '<svg viewBox="0 0 520 96" width="100%" font-family="Inter">'
for i in range(6):
    x = 6 + i * 85
    rir_svg += (f'<rect x="{x}" y="22" width="80" height="34" rx="5" fill="{rir_colors[i]}"/>'
                f'<text x="{x+40}" y="45" text-anchor="middle" font-size="14" font-weight="800" fill="#fff">{rir_lbl[i]}</text>'
                f'<text x="{x+40}" y="78" text-anchor="middle" font-size="9" fill="#6B7085">{rir_txt[i]}</text>')
rir_svg += ('<rect x="89" y="14" width="250" height="50" rx="8" fill="none" stroke="#15192B" stroke-width="2.5" stroke-dasharray="5 4"/>'
            '<text x="214" y="10" text-anchor="middle" font-size="10.5" font-weight="800" fill="#15192B">ZONA DE TRABAJO: RIR 1–3</text>'
            '<text x="260" y="92" text-anchor="middle" font-size="10" fill="#6B7085">RIR = repeticiones en reserva (las que te quedaban «en el depósito» al terminar la serie)</text></svg>')
page(f'''
<h2 style="margin-top:0">La clave: progresar poco a poco</h2>
<p>Para que tu cuerpo mantenga el músculo, necesita un motivo. Ese motivo es la <b>sobrecarga progresiva</b>: hacer un
poquito más con el tiempo (más repeticiones o más peso). Usaremos el sistema más sencillo y eficaz: la <b>doble progresión</b>.</p>
<h3>Cómo funciona la doble progresión</h3>
{ol(["Cada ejercicio tiene un rango de repeticiones, por ejemplo <b>3 × 8–12</b>.",
     "Empieza con un peso que te permita hacer 8 repeticiones con buena técnica.",
     "Cada sesión intenta hacer alguna repetición más con el mismo peso.",
     "Cuando completes <b>12 repeticiones en todas las series</b>, sube el peso y vuelve a empezar desde 8."])}
{table(["Semana", "Serie 1", "Serie 2", "Serie 3", "Qué haces"],
       [["1", "10 kg × 9", "10 kg × 8", "10 kg × 8", "Empiezas"],
        ["2", "10 kg × 11", "10 kg × 10", "10 kg × 9", "Sumas repeticiones"],
        ["3", "10 kg × 12", "10 kg × 12", "10 kg × 12", "¡Rango completado!"],
        ["4", "12 kg × 9", "12 kg × 8", "12 kg × 8", "Subes peso y vuelves a 8"]])}
<h2>¿Cuánto esfuerzo? La escala RIR</h2>
<p>No hace falta llegar al fallo en cada serie. Lo ideal es terminar cada serie dejando <b>1–3 repeticiones en reserva</b>.</p>
{rir_svg}
{tip("La técnica va primero. Si para hacer una repetición más tienes que deformar el movimiento, esa repetición no cuenta.")}
''')

# 21 · CARDIO Y NEAT ------------------------------------------------------
page(f'''
<h2 style="margin-top:0">Pasos: el arma secreta</h2>
<p>Caminar es fácil, no genera fatiga, no da más hambre como el cardio intenso y se puede hacer todos los días. Pasar de 4.000
a 10.000 pasos diarios puede suponer <b>entre 200 y 350 kcal más de gasto al día</b>, según tu peso y ritmo.</p>
{table(["Si ahora haces…", "Objetivo semanas 1–4", "Objetivo semanas 5–12"],
       [["Menos de 5.000 pasos", "6.000–7.000", "8.000–10.000"],
        ["5.000–8.000 pasos", "8.000–9.000", "10.000+"],
        ["Más de 8.000 pasos", "Mantén", "+1.000–2.000"]])}
<h3>Ideas para sumar pasos sin darte cuenta</h3>
<div class="cols2">{ul(["Paseo de 10–15 min después de comer y cenar.", "Escaleras en lugar de ascensor.", "Llamadas por teléfono caminando."])}
{ul(["Bájate una parada antes del bus o metro.", "Aparca más lejos.", "Queda con amigos para caminar, no solo para tomar algo."])}</div>
<h2>Cardio: dos tipos, dos usos</h2>
{table(["", "LISS (baja intensidad)", "HIIT (alta intensidad)"],
       [["Qué es", "Caminar rápido, bici suave, elíptica", "Intervalos cortos muy intensos con descansos"],
        ["Duración", "30–45 minutos", "15–25 minutos"],
        ["Intensidad", "Puedes mantener una conversación", "Al final de cada intervalo no puedes hablar"],
        ["Ventajas", "Poca fatiga, apto para todos los niveles", "Muy eficiente en poco tiempo"],
        ["Cuidado con", "Que te quite tiempo de fuerza", "No más de 2 por semana; fatiga acumulada"]], widths=["18%", "41%", "41%"])}
{key("En la Fase 1 solo usamos LISS y pasos. El HIIT entra a partir de la semana 5, cuando ya tienes base.")}
''')

# 22 · CALENTAMIENTO + CÓMO LEER --------------------------------------------
page(f'''
<div class="kicker">Antes de cada sesión</div>
<h1>Calentamiento de 8 minutos</h1>
<div class="bar"></div>
<p>Calentar prepara articulaciones y músculos, mejora tu rendimiento y reduce el riesgo de lesión. No te lo saltes.</p>
{table(["Bloque", "Ejercicio", "Cantidad"],
       [["1. Activación", "Bici, elíptica, cinta o saltos suaves en casa", "3 minutos"],
        ["2. Movilidad", "Círculos de cadera", "10 por lado"],
        ["", "Gato-camello (a cuatro patas)", "8 repeticiones"],
        ["", "Rotaciones torácicas a cuatro patas", "6 por lado"],
        ["", "Sentadilla profunda con pausa de 2 s", "8 repeticiones"],
        ["", "Puente de glúteo", "10 repeticiones"],
        ["3. Aproximación", "1–2 series del primer ejercicio con poco peso", "8–10 repeticiones"]], widths=["22%", "56%", "22%"])}
<h2>Cómo leer las rutinas</h2>
<div class="legendgrid">
  <div><b>3 × 10–12</b><span>3 series de entre 10 y 12 repeticiones</span></div>
  <div><b>Desc. 90 s</b><span>Descanso entre series</span></div>
  <div><b>RIR 2</b><span>Termina la serie con 2 repeticiones en reserva</span></div>
  <div><b>c/lado</b><span>Las repeticiones son por cada lado</span></div>
  <div><b>SS</b><span>Superserie: dos ejercicios seguidos sin descanso</span></div>
  <div><b>Casa</b><span>Alternativa con garrafa, mochila o goma</span></div>
</div>
{tip("Si en casa no tienes mancuernas, una garrafa de 5–8 litros o una mochila con libros o botellas sirve para casi todos los ejercicios. "
     "Más adelante, unas mancuernas ajustables son la mejor inversión.")}
''')

# 23-26 · BIBLIOTECA DE EJERCICIOS ----------------------------------------
exercises = [
 ("Sentadilla goblet", "Cuádriceps, glúteos, core", "Mancuerna o kettlebell",
  ["Sujeta la mancuerna pegada al pecho, pies algo más abiertos que la cadera.", "Baja sentándote entre tus talones, con el pecho alto.", "Sube empujando el suelo con todo el pie."],
  "Levantar los talones o que las rodillas se vayan hacia dentro.", "Con una garrafa o mochila pegada al pecho.",
  "Persona en la posición baja de la sentadilla goblet sujetando una mancuerna pegada al pecho, vista lateral.",
  "Side view of a person at the bottom of a goblet squat holding a dumbbell against the chest, upright torso, knees tracking over toes, "),
 ("Peso muerto rumano", "Isquiotibiales, glúteos, espalda baja", "Mancuernas o barra",
  ["De pie, mancuernas delante de los muslos, rodillas ligeramente flexionadas.", "Lleva la cadera atrás deslizando el peso pegado a las piernas.", "Baja hasta notar estiramiento detrás del muslo y sube apretando glúteos."],
  "Redondear la espalda o convertirlo en una sentadilla.", "Con mochila o garrafa sujeta con ambas manos.",
  "Persona inclinada con la cadera hacia atrás y espalda recta, mancuernas a la altura de las rodillas, vista lateral.",
  "Side view of a person performing a dumbbell Romanian deadlift, hips pushed back, flat back, dumbbells at knee height, "),
 ("Hip thrust", "Glúteos", "Banco y barra o mancuerna",
  ["Apoya la parte alta de la espalda en el banco y el peso sobre la cadera.", "Pies apoyados a la anchura de la cadera, barbilla al pecho.", "Sube la cadera hasta alinear rodillas, cadera y hombros; aprieta 1 s."],
  "Arquear la zona lumbar en lugar de subir con el glúteo.", "Espalda en el sofá y mochila sobre la cadera.",
  "Persona haciendo hip thrust con la espalda apoyada en un banco y una barra sobre la cadera, en la posición alta.",
  "Person performing a barbell hip thrust with upper back on a bench, hips fully extended at the top position, side view, "),
 ("Zancada atrás", "Cuádriceps, glúteos, equilibrio", "Mancuernas (opcional)",
  ["De pie, da un paso largo hacia atrás.", "Baja hasta que la rodilla de atrás casi toque el suelo.", "Vuelve empujando con la pierna de delante."],
  "Dar un paso demasiado corto o inclinar el tronco hacia delante.", "Igual, con peso corporal o mochila.",
  "Persona en posición baja de zancada hacia atrás con mancuernas a los lados, vista lateral.",
  "Side view of a person in the bottom position of a reverse lunge holding dumbbells at the sides, upright torso, "),
 ("Press de banca con mancuernas", "Pectoral, tríceps, hombro", "Banco y mancuernas",
  ["Túmbate en el banco con las mancuernas a la altura del pecho.", "Junta ligeramente las escápulas y apoya bien los pies.", "Empuja hacia arriba y baja controlando en 2 segundos."],
  "Abrir mucho los codos (90°) o rebotar abajo.", "Flexiones (ver siguiente ejercicio).",
  "Persona tumbada en un banco empujando dos mancuernas hacia arriba, codos a unos 45°.",
  "Person lying on a flat bench pressing two dumbbells upward, elbows at about 45 degrees, three-quarter view, "),
 ("Flexiones", "Pectoral, tríceps, core", "Peso corporal",
  ["Manos algo más abiertas que los hombros, cuerpo recto de cabeza a talones.", "Baja el pecho hacia el suelo con los codos a 45°.", "Empuja el suelo hasta estirar los brazos."],
  "Dejar caer la cadera o no bajar del todo.", "Progresión: pared → mesa → rodillas → suelo.",
  "Persona haciendo flexiones inclinadas con las manos apoyadas en un banco, cuerpo recto.",
  "Person doing incline push-ups with hands on a bench, straight body line from head to heels, side view, "),
 ("Remo con mancuerna", "Dorsal, espalda media, bíceps", "Banco y mancuerna",
  ["Apoya una mano y una rodilla en el banco, espalda recta.", "Tira de la mancuerna hacia la cadera llevando el codo atrás.", "Baja controlando hasta estirar el brazo."],
  "Girar el tronco para subir el peso o tirar con el bíceps.", "Con garrafa o mochila, apoyado en una silla.",
  "Persona con una rodilla y una mano en el banco tirando de una mancuerna hacia la cadera.",
  "Person performing a one-arm dumbbell row with one knee and hand on a bench, elbow pulled back to the hip, flat back, side view, "),
 ("Jalón al pecho", "Dorsal, bíceps", "Polea alta",
  ["Agarra la barra algo más abierta que los hombros.", "Saca pecho y lleva la barra hacia la parte alta del pecho.", "Sube controlando hasta estirar los brazos."],
  "Balancearse hacia atrás o bajar la barra por detrás de la nuca.", "Goma anclada en lo alto de una puerta, o remo invertido bajo una mesa.",
  "Persona sentada en la máquina de jalón tirando de la barra hacia el pecho.",
  "Person seated at a lat pulldown machine pulling the bar to the upper chest, chest up, slight lean back, front three-quarter view, "),
 ("Press militar con mancuernas", "Hombros, tríceps", "Mancuernas (sentado o de pie)",
  ["Mancuernas a la altura de los hombros, palmas al frente.", "Empuja hacia arriba hasta estirar los brazos.", "Baja controlando hasta la altura de las orejas."],
  "Arquear mucho la espalda baja.", "Con garrafas o botellas grandes, o goma bajo los pies.",
  "Persona sentada en un banco con respaldo empujando dos mancuernas por encima de la cabeza.",
  "Person seated on an upright bench pressing two dumbbells overhead, neutral spine, front view, "),
 ("Plancha frontal", "Core (abdomen profundo)", "Peso corporal",
  ["Apoya antebrazos y puntas de los pies.", "Aprieta glúteos y abdomen; cuerpo en línea recta.", "Respira con normalidad y mantén la posición."],
  "Dejar caer la cadera o subirla demasiado.", "Igual. Más fácil: con las rodillas apoyadas.",
  "Persona en plancha sobre los antebrazos con el cuerpo totalmente recto, vista lateral.",
  "Side view of a person holding a forearm plank on a mat, perfectly straight body line, "),
 ("Dead bug", "Core, control lumbar", "Peso corporal",
  ["Boca arriba, brazos al techo y rodillas a 90°.", "Pega la zona lumbar al suelo.", "Estira a la vez el brazo y la pierna contrarios sin despegar la espalda; alterna."],
  "Despegar la zona lumbar del suelo o hacerlo rápido.", "Igual.",
  "Persona boca arriba en una esterilla estirando un brazo y la pierna contraria.",
  "Person lying on their back on a mat doing a dead bug exercise, extending opposite arm and leg, lower back flat, overhead view, "),
 ("Burpee sin salto", "Cuerpo completo, cardio", "Peso corporal",
  ["Agáchate y apoya las manos en el suelo.", "Lleva los pies atrás (uno a uno o juntos) hasta posición de plancha.", "Vuelve a traer los pies y ponte de pie."],
  "Dejar caer la cadera en la plancha.", "Igual. Más difícil: añade el salto al final.",
  "Secuencia de una persona pasando de cuclillas a posición de plancha en un salón luminoso.",
  "Person doing a no-jump burpee in a bright living room, moving from squat to plank position, motion sequence feel, "),
]
def ex_html(e, idx):
    name, mus, mat, steps, err, home, desc, prompt = e
    return f'''<div class="ex">
  {img(name, desc, "4:5 vertical", prompt + STYLE_SUFFIX, h="74mm", w="56mm")}
  <div class="exbody">
    <div class="exnum">{idx:02d}</div><h2>{name}</h2>
    <div class="exmeta"><span><b>Músculos:</b> {mus}</span><span><b>Material:</b> {mat}</span></div>
    {ol(steps, "small")}
    <div class="exfoot"><div class="exerr"><b>✕ Error:</b> {err}</div><div class="exhome"><b>⌂ Casa:</b> {home}</div></div>
  </div></div>'''
for p in range(4):
    hdr = ('<div class="kicker">Capítulo 5</div><h1 class="chap sm">Biblioteca de ejercicios</h1><div class="bar"></div>' if p == 0 else "")
    body = "".join(ex_html(exercises[p*3+k], p*3+k+1) for k in range(3))
    page(hdr + body, toc="5. Biblioteca de ejercicios" if p == 0 else None, cls="exlib" + (" first" if p == 0 else ""))

# 27 · PLAN 12 SEMANAS -----------------------------------------------------
timeline = '''
<svg viewBox="0 0 520 150" width="100%" font-family="Inter">
  <rect x="0" y="40" width="168" height="44" rx="6" fill="#FFB703"/>
  <rect x="176" y="40" width="168" height="44" rx="6" fill="#FF5A36"/>
  <rect x="352" y="40" width="168" height="44" rx="6" fill="#15192B"/>
  <text x="84" y="60" text-anchor="middle" font-size="12" font-weight="800" fill="#15192B">FASE 1 · BASE</text>
  <text x="84" y="76" text-anchor="middle" font-size="10.5" fill="#15192B">Semanas 1–4</text>
  <text x="260" y="60" text-anchor="middle" font-size="12" font-weight="800" fill="#fff">FASE 2 · CONSTRUCCIÓN</text>
  <text x="260" y="76" text-anchor="middle" font-size="10.5" fill="#fff">Semanas 5–8</text>
  <text x="436" y="60" text-anchor="middle" font-size="12" font-weight="800" fill="#fff">FASE 3 · DEFINICIÓN</text>
  <text x="436" y="76" text-anchor="middle" font-size="10.5" fill="#fff">Semanas 9–12</text>
  <g font-size="10" fill="#15192B">
    <text x="4" y="104">• Aprender la técnica</text><text x="4" y="119">• 3 × 10–12 · RIR 3</text><text x="4" y="134">• Solo pasos + LISS</text>
    <text x="180" y="104">• Más series y peso</text><text x="180" y="119">• 3–4 × 8–10 · RIR 2</text><text x="180" y="134">• Entra 1 HIIT/semana</text>
    <text x="356" y="104">• Máxima intensidad</text><text x="356" y="119">• 4 × 6–10 · RIR 1–2</text><text x="356" y="134">• Hasta 2 HIIT/semana</text>
  </g>
  <g fill="#6B7085" font-size="9">''' + "".join(
      f'<circle cx="{14 + i*44.7:.1f}" cy="20" r="9" fill="{"#FFB703" if i<4 else ("#FF5A36" if i<8 else "#15192B")}"/>'
      f'<text x="{14 + i*44.7:.1f}" y="23.5" text-anchor="middle" fill="{"#15192B" if i<4 else "#fff"}" font-weight="700">{i+1}</text>'
      for i in range(12)) + '''</g>
</svg>'''
week = [("Lun", "Fuerza A", "a"), ("Mar", "Pasos + LISS", "c"), ("Mié", "Fuerza B", "a"), ("Jue", "Descanso activo", "r"),
        ("Vie", "Fuerza A", "a"), ("Sáb", "HIIT o actividad libre", "c"), ("Dom", "Descanso", "r")]
weekhtml = '<div class="week">' + "".join(f'<div class="wd {c}"><b>{d}</b><span>{t}</span></div>' for d, t, c in week) + "</div>"
page(f'''
{opener(6, "Tu plan de 12 semanas", "Tres fases de 4 semanas. Cada fase sube un poco la exigencia para que tu cuerpo siga progresando mientras pierdes grasa.")}
{timeline}
<h2>Tu semana tipo</h2>
{weekhtml}
<p class="small muted">Alterna las sesiones: semana impar A-B-A, semana par B-A-B. El sábado haz HIIT solo a partir de la Fase 2; en la Fase 1, sustitúyelo por una caminata larga o cualquier actividad que te guste (bici, nadar, pádel…).</p>
<div class="cols2">
<div>{tip("Si solo puedes entrenar 2 días, haz A y B cada semana y sube tus pasos. Seguirás progresando, algo más despacio.", "¿Poco tiempo?")}</div>
<div>{key("Si en la semana 7 u 8 te notas muy cansado, haz una <b>semana de descarga</b>: mismos ejercicios con la mitad de series.", "Semana de descarga")}</div>
</div>
''', toc="6. Tu plan de 12 semanas")

def routine(rows):
    return table(["Ejercicio (gimnasio)", "Alternativa casa", "Series × reps", "Desc.", "RIR"], rows,
                 cls="routine", widths=["29%", "33%", "16%", "10%", "12%"])
PTIPS = [['Elige pesos con los que podrías hacer 3 repeticiones más.', 'Graba alguna serie con el móvil para revisar tu técnica.', 'Apunta cada sesión en el registro desde el primer día.', 'Si algún ejercicio te molesta, usa la alternativa de casa o pregunta a un profesional.'], ['Sube el peso en cuanto completes el rango en todas las series.', 'Haz el HIIT después de la fuerza o en otro día, nunca antes.', 'Revisa tu media semanal: si no baja en 3 semanas, consulta la sección de estancamientos.', 'Mantén la proteína alta: el volumen de entreno sube.'], ['En déficit es normal que los pesos se estanquen: mantenerlos ya es un éxito.', 'Prioriza el sueño; la fatiga se acumula al final del plan.', 'Usa descansos más largos en los ejercicios principales.', 'Semana 12: fotos y medidas finales para comparar con el inicio.']]
phases = [
 ("Fase 1 · Base", "Semanas 1–4", "Objetivo: aprender la técnica y crear el hábito. Usa pesos con los que te sientas cómodo.",
  [["Sentadilla goblet", "Sentadilla con garrafa", "3 × 10–12", "90 s", "3"],
   ["Press banca mancuernas", "Flexiones inclinadas", "3 × 10–12", "90 s", "3"],
   ["Remo con mancuerna", "Remo con garrafa", "3 × 10–12 c/lado", "60 s", "3"],
   ["Peso muerto rumano", "Peso muerto con mochila", "3 × 10–12", "90 s", "3"],
   ["Plancha frontal", "Plancha frontal", "3 × 20–30 s", "45 s", "–"]],
  [["Hip thrust", "Hip thrust en sofá", "3 × 10–12", "90 s", "3"],
   ["Jalón al pecho", "Remo con goma", "3 × 10–12", "90 s", "3"],
   ["Zancada atrás", "Zancada atrás", "2 × 10 c/lado", "60 s", "3"],
   ["Press militar mancuernas", "Press con garrafas", "3 × 10–12", "60 s", "3"],
   ["Dead bug", "Dead bug", "3 × 8 c/lado", "45 s", "–"]],
  "Cardio: 2 sesiones de LISS de 30 min + objetivo de pasos."),
 ("Fase 2 · Construcción", "Semanas 5–8", "Objetivo: más trabajo total. Sube el peso respecto a la Fase 1 y aplica la doble progresión.",
  [["Sentadilla goblet", "Sentadilla con mochila pesada", "4 × 8–10", "90 s", "2"],
   ["Press banca mancuernas", "Flexiones (rodillas o suelo)", "4 × 8–10", "90 s", "2"],
   ["Remo con mancuerna", "Remo con garrafa", "3 × 8–10 c/lado", "60 s", "2"],
   ["Peso muerto rumano", "Peso muerto a una pierna", "3 × 8–10", "90 s", "2"],
   ["Plancha frontal", "Plancha frontal", "3 × 30–40 s", "45 s", "–"]],
  [["Hip thrust", "Hip thrust a una pierna", "4 × 8–10", "90 s", "2"],
   ["Jalón al pecho", "Remo invertido bajo mesa", "4 × 8–10", "90 s", "2"],
   ["Zancada atrás", "Zancada atrás con mochila", "3 × 10 c/lado", "60 s", "2"],
   ["Press militar mancuernas", "Pike push-up o garrafas", "3 × 8–10", "60 s", "2"],
   ["Dead bug", "Dead bug", "3 × 10 c/lado", "45 s", "–"]],
  "Cardio: 1 HIIT + 1 LISS por semana + objetivo de pasos."),
 ("Fase 3 · Definición", "Semanas 9–12", "Objetivo: mantener la fuerza al máximo mientras el déficit avanza. Menos repeticiones, más intensidad.",
  [["Sentadilla goblet", "Sentadilla con mochila + pausa 2 s", "4 × 6–10", "2 min", "1–2"],
   ["Press banca mancuernas", "Flexiones con pausa abajo", "4 × 6–10", "2 min", "1–2"],
   ["Remo con mancuerna", "Remo con garrafa", "4 × 8–10 c/lado", "75 s", "1–2"],
   ["Peso muerto rumano", "Peso muerto a una pierna", "3 × 8", "90 s", "1–2"],
   ["Finisher: burpee sin salto", "Burpee (con o sin salto)", "4 × 30 s / 30 s", "–", "–"]],
  [["Hip thrust", "Hip thrust a una pierna + pausa", "4 × 6–10", "2 min", "1–2"],
   ["Jalón al pecho", "Remo invertido bajo mesa", "4 × 8–10", "90 s", "1–2"],
   ["Zancada atrás", "Zancada búlgara en silla", "3 × 10 c/lado", "75 s", "1–2"],
   ["Press militar mancuernas", "Pike push-up", "3 × 8–10", "75 s", "1–2"],
   ["SS: Dead bug + plancha", "SS: Dead bug + plancha", "3 rondas", "60 s", "–"]],
  "Cardio: 2 HIIT, o 1 HIIT + 2 LISS + objetivo de pasos (9.000–10.000)."),
]
for (name, weeks, goal, A, B, cardio), ptip in zip(phases, PTIPS):
    page(f'''
<div class="phasehead"><div><div class="kicker">{weeks}</div><h1 class="sm">{name}</h1></div></div>
<div class="bar"></div>
<p>{goal}</p>
<h2 class="day"><span>A</span> Día A · Cuerpo completo</h2>
{routine(A)}
<h2 class="day"><span>B</span> Día B · Cuerpo completo</h2>
{routine(B)}
<div class="cols2"><div>{key(cardio, "Cardio de esta fase")}</div><div class="box tip"><span class="lbl">Claves de esta fase</span>{ul(ptip, "small")}</div></div>
''', toc=f"{name} (semanas {weeks.split()[1]})", toc_level=2)

# 31 · PROTOCOLOS CARDIO --------------------------------------------------
page(f'''
<div class="kicker">Cardio</div>
<h1>Protocolos de cardio</h1>
<div class="bar"></div>
<div class="cols2">
<div class="proto">
<h2>HIIT A · Máquina</h2>
<p class="small muted">Bici estática, elíptica o remo · 23 minutos</p>
{table(["Bloque", "Tiempo"], [["Calentamiento suave", "5 min"], ["<b>Rápido</b> (esfuerzo 8–9/10)", "30 s"], ["Suave (esfuerzo 3/10)", "90 s"], ["Repite rápido + suave", "8 rondas"], ["Vuelta a la calma", "2 min"]])}
</div>
<div class="proto">
<h2>HIIT B · En casa</h2>
<p class="small muted">Sin material · 4 rondas · ≈ 20 minutos</p>
{table(["Ejercicio", "Trabajo / descanso"], [["Sentadilla", "40 s / 20 s"], ["Mountain climbers", "40 s / 20 s"], ["Burpee sin salto", "40 s / 20 s"], ["Zancada alterna", "40 s / 20 s"], ["Plancha", "40 s / 20 s"]])}
<p class="small">1 minuto de descanso entre rondas.</p>
</div>
</div>
<h2>LISS · Caminata o bici suave</h2>
<p>30–45 minutos a ritmo constante. En cinta, prueba la caminata inclinada: 5–8 % de inclinación a 5–5,5 km/h.
Deberías poder mantener una conversación, aunque con algo de esfuerzo.</p>
<h2>Escala de esfuerzo percibido</h2>
{table(["Nivel", "Sensación", "Uso"],
       [["1–2", "Muy suave, como pasear", "Descanso activo"],
        ["3–4", "Cómodo, puedes hablar sin problema", "Calentamiento, recuperación en HIIT"],
        ["5–6", "Algo exigente, hablas con frases cortas", "LISS"],
        ["7–8", "Duro, solo puedes decir palabras sueltas", "Final de intervalos"],
        ["9–10", "Máximo, no puedes hablar", "Intervalos rápidos del HIIT"]], widths=["14%", "50%", "36%"])}
{warn("Hacer HIIT todos los días. Genera mucha fatiga, empeora tus entrenamientos de fuerza y aumenta el riesgo de lesión. Dos sesiones por semana son suficientes.")}
''', toc="Protocolos de cardio", toc_level=2)

# 32 · HÁBITOS ------------------------------------------------------------
page(f'''
{opener(7, "Hábitos que marcan la diferencia", "Lo que haces fuera del gimnasio y de la cocina también cuenta. Y mucho.")}
{img("Rutina de descanso nocturno", "Dormitorio acogedor con luz cálida tenue, persona leyendo un libro en la cama antes de dormir, móvil apartado en la mesilla.", "horizontal 16:9", "Cozy bedroom with dim warm light, person reading a paper book in bed before sleep, phone face-down on the nightstand, calm atmosphere, " + STYLE_SUFFIX, h="64mm")}
<div class="cols2">
<div>
<h3>😴 Sueño: 7–9 horas</h3>
<p class="small">Dormir poco aumenta las hormonas del hambre, te da antojos de comida calórica y te quita energía para entrenar.
Intenta acostarte y levantarte a la misma hora, y aparta las pantallas 30 minutos antes de dormir.</p>
<h3>💧 Agua</h3>
<p class="small">Como referencia, unos 30–35 ml por kg de peso al día (más si sudas mucho). Lleva siempre una botella contigo.</p>
</div>
<div>
<h3>🧘 Estrés</h3>
<p class="small">El estrés crónico dispara el picoteo emocional. Caminar, respirar profundo 5 minutos o hablar con alguien ayudan más que cualquier suplemento.</p>
<h3>📅 Constancia, no perfección</h3>
<p class="small">Si cumples el plan el 80–90 % del tiempo, vas a progresar. Un mal día no arruina nada; abandonar sí.
Si fallas, vuelve al plan en la siguiente comida, no el lunes.</p>
</div>
</div>
{tip("Encadena hábitos: «después de desayunar, salgo a caminar 10 minutos». Pegar un hábito nuevo a uno que ya tienes multiplica las probabilidades de cumplirlo.")}
''', toc="7. Hábitos que marcan la diferencia")

# 33 · ESTANCAMIENTOS -----------------------------------------------------
page(f'''
<div class="kicker">Solución de problemas</div>
<h1>¿Te has estancado?</h1>
<div class="bar"></div>
<p>Es normal que el progreso se frene en algún momento. Antes de cambiar nada, comprueba que realmente es un estancamiento:
<b>tu media semanal de peso y tu cintura no han bajado en 2–3 semanas seguidas</b>.</p>
<h2>Sigue este orden</h2>
<div class="steps">
  <div class="step"><b>1</b><div><h3>Revisa con honestidad</h3><p>Aceite «a ojo», picoteos, bebidas, salsas y fines de semana. Apunta todo durante 7 días.</p></div></div>
  <div class="step"><b>2</b><div><h3>Sube los pasos</h3><p>Añade 1.500–2.000 pasos diarios a tu media actual.</p></div></div>
  <div class="step"><b>3</b><div><h3>Ajusta las calorías</h3><p>Resta 100–150 kcal al día, preferiblemente de hidratos o grasas. Nunca de la proteína.</p></div></div>
  <div class="step"><b>4</b><div><h3>Revisa sueño y estrés</h3><p>Dormir mal y el estrés pueden retener líquidos y ocultar la pérdida de grasa varias semanas.</p></div></div>
  <div class="step"><b>5</b><div><h3>Haz un descanso de dieta</h3><p>Si llevas más de 10–12 semanas en déficit, come 1–2 semanas a mantenimiento y luego retoma.</p></div></div>
</div>
<h2>Los 6 errores más comunes</h2>
<div class="errgrid">
  <div><b>Déficit extremo</b>Más hambre, menos músculo y efecto rebote.</div>
  <div><b>Solo cardio</b>Pierdes músculo y el cuerpo no se define.</div>
  <div><b>Poca proteína</b>Más hambre y peor recuperación.</div>
  <div><b>Compensar el lunes</b>Castigarse con ayunos tras un exceso alimenta el ciclo de atracones.</div>
  <div><b>Vivir pegado a la báscula</b>Mira la media semanal, no el dato de un día.</div>
  <div><b>Cambiar de plan cada semana</b>Dale al método al menos 4 semanas antes de juzgarlo.</div>
</div>
''', toc="Estancamientos y errores comunes", toc_level=2)

# 34 · MEDIR PROGRESO -----------------------------------------------------
page(f'''
<div class="kicker">Seguimiento</div>
<h1>Cómo medir tu progreso</h1>
<div class="bar"></div>
<p>La báscula es solo una de las formas de medir. Combinando varias tendrás la foto completa, sobre todo cuando pierdes grasa y ganas algo de músculo a la vez.</p>
<div class="measure">
{img("Dónde medir el cuerpo", "Ilustración limpia de una silueta humana de frente con líneas marcando dónde medir: cintura (a la altura del ombligo), cadera (parte más ancha), muslo y brazo.", "vertical 3:4", "Clean minimal flat vector illustration of a human body silhouette front view with measurement lines at the waist (navel level), hips (widest point), mid-thigh and upper arm, coral-orange measuring tape lines, white background, infographic style, no text", h="98mm", w="72mm")}
<div>
<h3>⚖️ Báscula</h3>
<p class="small">Pésate 3–7 días por semana, en ayunas y después de ir al baño. Apunta la <b>media semanal</b>.</p>
<h3>📏 Cinta métrica</h3>
<p class="small">Cada 2 semanas, por la mañana: cintura (a la altura del ombligo), cadera (parte más ancha), muslo y brazo. La cintura es el mejor indicador de pérdida de grasa.</p>
<h3>📸 Fotos</h3>
<p class="small">Cada 2–4 semanas: frente, perfil y espalda. Misma luz, misma ropa y misma hora. Las fotos muestran cambios que la báscula no ve.</p>
<h3>💪 Rendimiento</h3>
<p class="small">Si mantienes o subes tus pesos mientras bajas de peso, estás conservando el músculo. ¡Buena señal!</p>
</div>
</div>
{key("Tu peso puede estancarse una semana mientras tu cintura baja. Eso es pérdida de grasa con retención de líquidos o ganancia de músculo. "
     "Por eso usamos varias medidas.")}
''', toc="Cómo medir tu progreso", toc_level=2)

# 35-39 · PLANTILLAS -----------------------------------------------------
def session_tpl(label):
    rows = [["", "", "", "", "", "", ""] for _ in range(6)]
    return (f'<div class="tplhead"><b>{label}</b><span>Semana ____ · Fase ____ · Fecha ___ / ___ / ___</span></div>' +
            table(["Ejercicio", "Serie 1<br><small>kg × reps</small>", "Serie 2", "Serie 3", "Serie 4", "RIR", "Notas"], rows,
                  cls="tpl", widths=["24%", "13%", "13%", "13%", "13%", "8%", "16%"]) +
            '<div class="tplfoot"><span>Energía (1–5): ____</span><span>Duración: ______ min</span><span>Cardio / pasos: __________</span></div>')
page(f'''
<div class="kicker">Plantilla imprimible</div>
<h1 class="sm">Registro de entrenamiento</h1>
<div class="bar"></div>
<p class="small">Imprime tantas copias como necesites. Apuntar cada serie es la forma más fácil de aplicar la doble progresión.</p>
{session_tpl("SESIÓN 1 · Día A / B")}
{session_tpl("SESIÓN 2 · Día A / B")}
''', toc="Plantillas imprimibles", toc_level=1)

steps_rows = [[f"<b>{w}</b>"] + [""] * 8 for w in range(1, 13)]
page(f'''
<div class="kicker">Plantilla imprimible</div>
<h1 class="sm">Registro de pasos y cardio</h1>
<div class="bar"></div>
<p class="small">Anota tus pasos de cada día (en miles, por ejemplo 8,4) y marca con una letra el cardio: <b>L</b> = LISS, <b>H</b> = HIIT.</p>
{table(["Sem.", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom", "Media"], steps_rows, cls="tpl grid", widths=["9%"] + ["11%"] * 7 + ["14%"])}
{tip("Divide el total de la semana entre 7 para sacar la media. Si una semana baja mucho, revisa qué ha pasado (tiempo, trabajo, cansancio) y planifica cómo compensarlo.")}
''')

check_rows = [["<b>Inicio</b>"] + [""] * 7] + [[f"<b>S{w}</b>"] + [""] * 7 for w in range(1, 13)]
page(f'''
<div class="kicker">Plantilla imprimible</div>
<h1 class="sm">Revisión semanal</h1>
<div class="bar"></div>
<p class="small">Rellénala cada semana el mismo día. Las medidas, cada 2 semanas.</p>
{table(["Sem.", "Fecha", "Peso medio", "Cintura", "Cadera", "Muslo", "Pasos/día", "Energía 1–5"], check_rows, cls="tpl grid", widths=["10%", "13%", "14%", "12%", "12%", "12%", "13%", "14%"])}
<div class="notes"><b>Notas y ajustes de este bloque:</b></div>
''')

habits = ["Llegué a mi proteína", "Objetivo de pasos", "2 litros de agua", "Dormí 7 h o más", "Entreno / cardio hecho", "5 raciones fruta/verdura", "Sin alcohol", "Dentro de mis calorías"]
def habit_grid(title):
    rows = [[h] + ['<span class="cb"></span>'] * 7 for h in habits]
    return f'<h3>{title}</h3>' + table(["Hábito", "L", "M", "X", "J", "V", "S", "D"], rows, cls="tpl habits", widths=["37%"] + ["9%"] * 7)
page(f'''
<div class="kicker">Plantilla imprimible</div>
<h1 class="sm">Hábitos semanales</h1>
<div class="bar"></div>
<p class="small">Marca cada hábito que cumplas. El objetivo no es tenerlo todo perfecto, sino ver más casillas marcadas cada semana.</p>
{habit_grid("Semana ____")}
{habit_grid("Semana ____")}
''')

meal_rows = [[f"<b>{d}</b>", "", "", "", ""] for d in ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]]
page(f'''
<div class="kicker">Plantilla imprimible</div>
<h1 class="sm">Planificador de comidas</h1>
<div class="bar"></div>
<p class="small">Planifica la semana el domingo y haz la lista de la compra a partir de aquí.</p>
{table(["Día", "Desayuno", "Comida", "Merienda", "Cena"], meal_rows, cls="tpl meals", widths=["14%", "21.5%", "21.5%", "21.5%", "21.5%"])}
<div class="cols2">
<div class="notes tall"><b>Lista de la compra:</b></div>
<div class="notes tall"><b>Batch cooking del domingo:</b></div>
</div>
''')

# ANEXO · IMÁGENES -------------------------------------------------------
ANEXO_START = len(PAGES) + 1
per_page = [8, 9, 9]
chunks, i = [], 0
for n in per_page:
    if i >= len(IMAGES): break
    chunks.append(IMAGES[i:i+n]); i += n
while i < len(IMAGES):
    chunks.append(IMAGES[i:i+9]); i += 9
for ci, ch in enumerate(chunks):
    hdr = ""
    if ci == 0:
        hdr = f'''<div class="kicker">Anexo A</div><h1 class="sm">Lista de imágenes y prompts</h1><div class="bar"></div>
<p class="small">Todas las imágenes del ebook con su descripción y un prompt en inglés listo para pegar en Higgsfield, APIMart u otro
generador. Todos terminan con el mismo bloque de estilo para que el libro tenga una estética uniforme.
<b>Bloque de estilo común:</b> <i>{STYLE_SUFFIX}</i>.</p>'''
    items = "".join(f'''<div class="ai"><div class="ain">{im["n"]:02d}</div><div><b>{im["title"]}</b> <span class="aif">· {im["fmt"]}</span>
<div class="aid">{im["desc"]}</div><div class="aip">{im["prompt"].replace(STYLE_SUFFIX, "<i>[estilo común]</i>")}</div></div></div>''' for im in ch)
    page(hdr + items, toc="Anexo A · Lista de imágenes y prompts" if ci == 0 else None)

# CIERRE -------------------------------------------------------------------
page(f'''
<div class="end">
  <div class="kicker">Y ahora…</div>
  <h1>Empieza hoy,<br>no el lunes.</h1>
  <div class="bar"></div>
  <p class="lead">Tienes el método, las rutinas, el plan de comidas y las plantillas. Lo único que falta es dar el primer paso.</p>
  {ol(["Calcula tus números (página %%CALC%%).", "Imprime las plantillas.", "Haz tu primera sesión de Fuerza A esta semana.", "Revisa tu progreso cada domingo."])}
  <div class="share">
    <h3>Comparte tu progreso</h3>
    <p>Etiquétanos en tus redes con <b>#MetodoDEFINE</b> y cuéntanos cómo te va.</p>
    <p class="small">Instagram: @[tu_usuario] · TikTok: @[tu_usuario] · Web: [tu web]</p>
  </div>
  <p class="small muted">Gracias por confiar en este método. — {AUTHOR}</p>
</div>
''', cls="endpage", footer=False)

# ================================================================ CSS
CSS = r'''
@page { size: A4; margin: 0; }
:root{--ink:#15192B;--accent:#FF5A36;--amber:#FFB703;--blue:#2D6CDF;--muted:#6B7085;--line:#E6E2DD;--soft:#FFF4EF}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#ddd}
body{font-family:'Inter',sans-serif;color:var(--ink);font-size:10pt;line-height:1.48;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:210mm;height:297mm;padding:15mm 17mm 20mm;position:relative;overflow:hidden;background:#fff;break-after:page;page-break-after:always;margin:0 auto}
@media screen{.page{margin:8mm auto;box-shadow:0 2px 12px rgba(0,0,0,.15)}}
.foot{position:absolute;left:17mm;right:17mm;bottom:9mm;display:flex;justify-content:space-between;font-size:7.5pt;color:var(--muted);border-top:1px solid var(--line);padding-top:2.5mm;letter-spacing:.06em}
.foot b{color:var(--accent)}
h1,h2,h3{font-family:'Inter Display','Inter',sans-serif;margin:0}
h1{font-size:28pt;line-height:1.05;font-weight:800;letter-spacing:-.01em;margin:1.5mm 0 3mm}
h1.chap{font-size:30pt}
h1.sm,h1.chap.sm{font-size:22pt}
h2{font-size:14.5pt;font-weight:800;margin:5mm 0 2mm;letter-spacing:-.005em}
h3{font-size:11pt;font-weight:700;margin:3.5mm 0 1.2mm}
p{margin:0 0 2.3mm}
.lead{font-size:11.5pt;color:#3A3F55;line-height:1.5}
.small{font-size:8.8pt}
.muted{color:var(--muted)}
.kicker{font-size:8.5pt;letter-spacing:.2em;font-weight:800;color:var(--accent);text-transform:uppercase}
.bar{width:22mm;height:1.6mm;background:var(--accent);border-radius:1mm;margin:0 0 5mm}
ul,ol{margin:0 0 2.5mm;padding-left:5.5mm}
li{margin:0 0 1.1mm}
ul li::marker{color:var(--accent)}
ol li::marker{color:var(--accent);font-weight:800}
.box{border-radius:2.5mm;padding:3mm 4.5mm;margin:3.5mm 0;font-size:9.3pt;line-height:1.45}
.box .lbl{display:block;font-size:7.6pt;font-weight:800;letter-spacing:.14em;text-transform:uppercase;margin-bottom:.8mm}
.tip{background:#FFF1EC;border-left:1.5mm solid var(--accent)} .tip .lbl{color:var(--accent)}
.warn{background:#FFF7DE;border-left:1.5mm solid #F2A900} .warn .lbl{color:#A87400}
.key{background:#EAF2FF;border-left:1.5mm solid var(--blue)} .key .lbl{color:var(--blue)}
table{width:100%;border-collapse:collapse;font-size:8.8pt;margin:2mm 0 3mm;table-layout:fixed}
th{background:var(--ink);color:#fff;text-align:left;font-weight:600;padding:1.8mm 2.4mm;font-size:8.4pt}
th:first-child{border-top-left-radius:1.5mm} th:last-child{border-top-right-radius:1.5mm}
td{padding:1.6mm 2.4mm;border-bottom:1px solid var(--line);vertical-align:top}
tbody tr:nth-child(even) td{background:#FAF8F5}
.cols2{display:grid;grid-template-columns:1fr 1fr;gap:6mm}
.cols2.tight{gap:4mm}
/* placeholder */
.ph{border:.5mm dashed #EE8A6C;border-radius:3mm;background:repeating-linear-gradient(45deg,#FFF7F3 0 7px,#FFEFE8 7px 14px);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:4mm 6mm;color:#C2533A;margin:2mm 0 3mm;flex-shrink:0}
.ph .num{font-size:7pt;font-weight:800;letter-spacing:.16em;background:var(--accent);color:#fff;padding:.7mm 2.6mm;border-radius:10mm;margin-top:1.5mm}
.ph .t{font-family:'Inter Display';font-weight:800;font-size:10.5pt;color:var(--ink);margin:1.6mm 0 1mm}
.ph .d{font-size:7.8pt;line-height:1.38;color:#7A5245;max-width:120mm}
.ph .f{font-size:6.8pt;color:#B36A55;margin-top:1.6mm;font-weight:600}
.ph.dark{background:repeating-linear-gradient(45deg,#20253A 0 7px,#252B42 7px 14px);border-color:#FF7A5C;color:#FF8A6E}
.ph.dark .t{color:#fff} .ph.dark .d{color:#C9CCD8} .ph.dark .f{color:#FF9C84}
/* cover */
.cover{background:var(--ink);color:#fff;padding:18mm 17mm}
.cover-kicker{font-size:9pt;letter-spacing:.3em;font-weight:800;color:var(--amber)}
.cover-title{font-family:'Inter Display';font-weight:900;font-size:56pt;line-height:.92;margin:4mm 0 4mm;letter-spacing:-.02em}
.cover-title span{color:var(--accent)}
.cover-sub{font-size:12.5pt;color:#C9CCD8;max-width:150mm;line-height:1.45;margin-bottom:6mm}
.cover-pills{display:flex;gap:3mm;flex-wrap:wrap;margin-top:4mm}
.cover-pills span{border:1px solid #FF5A36;color:#fff;border-radius:10mm;padding:1.6mm 4mm;font-size:8.8pt;font-weight:600}
.cover-author{position:absolute;bottom:16mm;left:17mm;font-size:10pt;color:#9DA1B3;letter-spacing:.08em}
.cover .ph{margin-top:2mm}
/* misc components */
.legal{margin-top:6mm;font-size:8pt;color:var(--muted);border-top:1px solid var(--line);padding-top:3mm}
.legal p{margin-bottom:1.2mm}
.toc{margin-top:2mm}
.toc .row{display:flex;align-items:baseline;gap:2mm;padding:1.9mm 0;border-bottom:1px solid var(--line);font-size:10.5pt}
.toc .row.l1{font-weight:700;font-family:'Inter Display';font-size:11.5pt;padding-top:3mm}
.toc .row.l2{padding-left:7mm;color:#3A3F55;font-size:9.6pt;border-bottom:1px dotted var(--line)}
.toc .row .dots{flex:1}
.toc .row .pg{font-weight:700;color:var(--accent);min-width:8mm;text-align:right}
.steps{display:flex;flex-direction:column;gap:2.2mm;margin:2mm 0 3mm}
.step{display:flex;gap:4mm;align-items:flex-start;background:#FAF8F5;border-radius:2.5mm;padding:2.6mm 4mm}
.step>b{flex:0 0 9mm;height:9mm;border-radius:50%;background:var(--accent);color:#fff;display:flex;align-items:center;justify-content:center;font-family:'Inter Display';font-size:13pt}
.step h3{margin:0 0 .5mm;font-size:10.5pt}
.step p{margin:0;font-size:9pt;color:#3A3F55}
.cards3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:4mm;margin-top:2mm}
.card{background:#FAF8F5;border-radius:3mm;padding:4mm;border-top:1.4mm solid var(--accent)}
.card .cnum{font-family:'Inter Display';font-weight:900;font-size:20pt;color:var(--accent);line-height:1}
.card h3{margin:2mm 0 1mm}
.card p{font-size:9pt;margin:0;color:#3A3F55}
svg{display:block;width:100%;height:auto;margin:1mm 0 2mm}
.ph svg,.cam svg{width:22px;height:22px;display:inline;margin:0}
.legend{font-size:8.5pt;color:var(--muted);display:flex;align-items:center;gap:2mm;margin:-1mm 0 2mm}
.lg{display:inline-block;width:7mm;height:1.3mm;border-radius:1mm;margin-left:3mm}
.lg.grey{background:#B9BCC8}.lg.orange{background:var(--accent);height:2mm}
.formula{background:var(--ink);color:#fff;border-radius:2.5mm;padding:3mm 4.5mm;margin:2mm 0;font-size:10pt;font-family:'JetBrains Mono',monospace}
.formula span{display:inline-block;background:var(--accent);color:#fff;font-family:'Inter';font-weight:800;font-size:7.5pt;letter-spacing:.12em;text-transform:uppercase;padding:.6mm 2.4mm;border-radius:1mm;margin-right:3mm}
.formula b{color:var(--amber)}
.macros{display:grid;grid-template-columns:1fr 1fr 1fr;gap:4mm;margin:2mm 0 2mm}
.macro{border-radius:3mm;padding:3.5mm 4mm;color:#fff}
.macro.p{background:var(--accent)}.macro.g{background:var(--blue)}.macro.c{background:var(--amber);color:var(--ink)}
.macro .mt{font-size:8pt;font-weight:800;letter-spacing:.14em;text-transform:uppercase;opacity:.9}
.macro .mv{font-family:'Inter Display';font-size:17pt;font-weight:900;line-height:1.1;margin:1mm 0 .3mm}
.macro .mu{font-size:7.8pt;opacity:.9;margin-bottom:1.5mm}
.macro p{font-size:8.4pt;margin:0;line-height:1.35}
.sheet{border:1.2px solid var(--ink);border-radius:3mm;padding:2mm 6mm 5mm;margin:2mm 0 3mm}
.sheet h3{color:var(--accent);text-transform:uppercase;font-size:8.6pt;letter-spacing:.14em;margin:4.5mm 0 1mm}
.field{display:flex;align-items:flex-end;gap:2mm;padding:2.6mm 0 0;font-size:9.6pt}
.field span{white-space:nowrap}
.field i{flex:1;border-bottom:1px solid #9AA0B2;height:5mm}
.field em{font-style:normal;color:var(--muted);font-size:8.6pt;min-width:12mm}
.fields3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:5mm}
.fields2{display:grid;grid-template-columns:1fr 1fr;gap:5mm}
.shopgrid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:3mm 5mm}
.shop h3{border-bottom:1.4mm solid var(--accent);padding-bottom:1mm;margin-top:2mm}
.checks{list-style:none;padding:0;margin:1mm 0 0}
.checks li{display:flex;align-items:center;gap:2mm;font-size:9pt;padding:1mm 0;border-bottom:1px dotted var(--line)}
.cb{display:inline-block;width:3.6mm;height:3.6mm;border:1.2px solid #8C91A5;border-radius:.8mm;flex-shrink:0}
table.menu td{font-size:8.3pt;line-height:1.35;height:24mm}
table.menu td:first-child{background:#FFF1EC!important;color:var(--accent)}
.recipe{display:flex;gap:6mm;margin:2mm 0 4mm;padding-bottom:3mm;border-bottom:1px solid var(--line)}
.recipe .rbody{flex:1}
.recipe h2{margin:2mm 0 1.5mm;font-size:13.5pt}
.recipe h3{margin:2mm 0 1mm;font-size:9.6pt;color:var(--accent);text-transform:uppercase;letter-spacing:.1em}
.recipe ul,.recipe ol{font-size:8.6pt}
.recipe li{margin-bottom:.7mm}
.rtip{background:#FFF1EC;border-radius:2mm;padding:2mm 3mm;font-size:8.4pt;margin-top:1.5mm}
.rtip b{color:var(--accent)}
.badges{display:flex;gap:1.6mm;flex-wrap:wrap}
.badges span{background:var(--soft);color:#B8432A;font-weight:700;font-size:7.8pt;padding:.9mm 2.4mm;border-radius:10mm}
.badges span:first-child{background:var(--accent);color:#fff}
.pillars{display:grid;grid-template-columns:repeat(4,1fr);gap:3mm;margin:2mm 0 2mm}
.pillars>div{background:#FAF8F5;border-radius:3mm;padding:3.5mm}
.pillars b{display:flex;width:8mm;height:8mm;border-radius:50%;background:var(--ink);color:#fff;align-items:center;justify-content:center;font-family:'Inter Display'}
.pillars h3{margin:2mm 0 1mm}
.pillars p{font-size:8.5pt;margin:0;color:#3A3F55;line-height:1.38}
.legendgrid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:3mm;margin:2mm 0 3mm}
.legendgrid div{background:#FAF8F5;border-radius:2.5mm;padding:3mm;border-left:1.2mm solid var(--accent)}
.legendgrid b{display:block;font-family:'JetBrains Mono';font-size:10pt;color:var(--ink)}
.legendgrid span{font-size:8.4pt;color:#3A3F55}
.exlib .ex{display:flex;gap:6mm;padding:3mm 0;border-bottom:1px solid var(--line);height:81mm}
.exlib.first .ex{height:74mm}
.exlib.first .ex .ph{height:68mm!important}
.ex .ph{margin:0}
.exbody{flex:1;position:relative}
.exnum{position:absolute;right:0;top:0;font-family:'Inter Display';font-weight:900;font-size:24pt;color:#F1EDE8;line-height:1}
.ex h2{margin:1mm 0 1.5mm;font-size:14pt}
.exmeta{display:flex;flex-direction:column;gap:.4mm;font-size:8.4pt;color:#3A3F55;margin-bottom:2mm}
.ex ol{font-size:8.8pt}
.exfoot{display:grid;grid-template-columns:1fr 1fr;gap:3mm;font-size:8.2pt;line-height:1.35}
.exerr{background:#FFF7DE;border-radius:2mm;padding:2mm 2.6mm}
.exerr b{color:#A87400}
.exhome{background:#EAF2FF;border-radius:2mm;padding:2mm 2.6mm}
.exhome b{color:var(--blue)}
.week{display:grid;grid-template-columns:repeat(7,1fr);gap:2mm;margin:2mm 0 2mm}
.wd{border-radius:2.5mm;padding:3mm 2mm;text-align:center;min-height:22mm}
.wd b{display:block;font-family:'Inter Display';font-size:10.5pt;margin-bottom:1mm}
.wd span{font-size:8pt;line-height:1.3;display:block}
.wd.a{background:var(--accent);color:#fff}.wd.c{background:#FFE6A3}.wd.r{background:#EEF0F4;color:#4A4F66}
.phasehead{display:flex;justify-content:space-between;align-items:flex-end}
h2.day{display:flex;align-items:center;gap:3mm;font-size:13pt;margin-top:4mm}
h2.day span{display:inline-flex;width:8mm;height:8mm;border-radius:2mm;background:var(--accent);color:#fff;align-items:center;justify-content:center;font-size:11pt}
table.routine td{font-size:8.8pt;padding:2.2mm 2.4mm}
table.routine td:first-child{font-weight:700}
table.routine td:nth-child(2){color:#4A4F66}
.proto h2{margin-top:1mm}
.errgrid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:3mm}
.errgrid div{background:#FFF7DE;border-radius:2.5mm;padding:3mm;font-size:8.5pt;line-height:1.38;color:#3A3F55}
.errgrid b{display:block;color:var(--ink);font-size:9.5pt;margin-bottom:.8mm}
.measure{display:flex;gap:6mm;align-items:flex-start}
.measure h3:first-child{margin-top:1mm}
.tplhead{display:flex;justify-content:space-between;align-items:center;margin-top:5mm;font-size:9pt}
.tplhead b{font-family:'Inter Display';font-size:11pt;color:var(--accent)}
.tplhead span{color:var(--muted)}
table.tpl td{height:11mm;background:#fff!important;border:1px solid #D9D5CF}
table.tpl th{font-size:8pt}
table.tpl th small{font-weight:400;opacity:.8}
table.tpl.grid td{height:12.5mm}
table.tpl.habits td{height:9mm;vertical-align:middle;font-size:8.8pt}
table.tpl.habits td .cb{display:block;margin:0 auto}
table.tpl.meals td{height:24mm}
.tplfoot{display:flex;justify-content:space-between;font-size:8.6pt;color:#3A3F55;border:1px solid #D9D5CF;border-top:none;padding:2.4mm 3mm;margin-top:-3mm}
.notes{border:1px solid #D9D5CF;border-radius:2mm;padding:3mm;min-height:28mm;font-size:9pt;margin-top:3mm}
.notes.tall{min-height:40mm}
.ai{display:flex;gap:3.5mm;padding:2.2mm 0;border-bottom:1px solid var(--line);font-size:8.4pt;line-height:1.38}
.ain{flex:0 0 8mm;height:8mm;border-radius:2mm;background:var(--accent);color:#fff;font-weight:800;display:flex;align-items:center;justify-content:center;font-size:8.5pt}
.aif{color:var(--muted);font-weight:400}
.aid{color:#3A3F55;margin:.5mm 0}
.aip{font-family:'JetBrains Mono',monospace;font-size:7.2pt;color:#5A5F75;background:#F6F4F1;border-radius:1.5mm;padding:1.4mm 2mm;line-height:1.4}
.endpage{background:var(--ink);color:#fff}
.endpage .end{padding-top:40mm}
.endpage h1{font-size:40pt;color:#fff}
.endpage .lead{color:#C9CCD8}
.endpage ol{font-size:11pt;color:#fff}
.endpage .share{border:1px solid var(--accent);border-radius:3mm;padding:2mm 6mm 3mm;margin:10mm 0 8mm}
.endpage .share h3{color:var(--accent)}
.endpage .muted{color:#9DA1B3}
'''

# ================================================================ ENSAMBLADO
toc_html = '<div class="toc">' + "".join(
    f'<div class="row l{lvl}"><span>{t}</span><span class="dots"></span><span class="pg">{p}</span></div>'
    for t, p, lvl in TOC) + "</div>"
calc_page = next(p for t, p, l in TOC if t.startswith("2."))

out = []
for i, (html, o) in enumerate(PAGES, 1):
    html = html.replace("%%TOC%%", toc_html).replace("%%ANEXO%%", str(ANEXO_START)).replace("%%CALC%%", str(calc_page))
    foot = f'<div class="foot"><span>{BOOK}</span><span><b>{i:02d}</b></span></div>' if o["footer"] else ""
    out.append(f'<section class="page {o["cls"]}" data-n="{i}">{html}{foot}</section>')

doc = f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Método DEFINE</title>
<style>{CSS}</style></head><body>{"".join(out)}</body></html>'''
here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "metodo-define.html"), "w", encoding="utf-8") as f:
    f.write(doc)
print(f"OK: {len(PAGES)} páginas, {len(IMAGES)} imágenes, anexo en pág. {ANEXO_START}")
