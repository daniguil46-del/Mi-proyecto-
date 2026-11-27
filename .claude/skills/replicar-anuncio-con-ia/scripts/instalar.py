"""Lo deja todo listo de una sola vez.
uso: python3 instalar.py

Hace cuatro cosas:
  1. copia la skill a ~/.claude/skills/replicar-anuncio-con-ia
  2. instala Pillow
  3. instala ffmpeg (Mac con brew, Windows con winget)
  4. crea ~/.apimart.env vacio si no existe

Lo unico que NO puede hacer es darte de alta en apimart.ai ni meter tu clave:
eso lo tienes que hacer tu, y la clave no se escribe nunca en un chat."""
import os, platform, shutil, subprocess, sys

ORIGEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTINO = os.path.expanduser("~/.claude/skills/replicar-anuncio-con-ia")
ENV = os.path.expanduser("~/.apimart.env")
MAC = platform.system() == "Darwin"


def sh(*a):
    return subprocess.run(a, capture_output=True, text=True)


print("=" * 58)
print(" INSTALANDO: replicar un anuncio ganador con IA")
print("=" * 58)

# 1 · la skill en su sitio -----------------------------------------------
print("\n[1/4] Dejando la skill en su sitio")
if os.path.abspath(ORIGEN) == os.path.abspath(DESTINO):
    print("      Ya estaba en su sitio.")
else:
    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    if os.path.exists(DESTINO):
        shutil.rmtree(DESTINO)
    shutil.copytree(ORIGEN, DESTINO,
                    ignore=shutil.ignore_patterns("__pycache__", ".DS_Store"))
    print("      Copiada en", DESTINO)

# 2 · Pillow --------------------------------------------------------------
print("\n[2/4] Pillow")
try:
    import PIL  # noqa: F401
    print("      Ya estaba.")
except ImportError:
    r = sh(sys.executable, "-m", "pip", "install", "--user", "--quiet", "pillow")
    print("      Instalado." if r.returncode == 0 else
          "      NO se ha podido. Prueba a mano:  pip3 install --user pillow")

# 3 · ffmpeg --------------------------------------------------------------
print("\n[3/4] ffmpeg")
if shutil.which("ffmpeg") and shutil.which("ffprobe"):
    print("      Ya estaba.")
elif MAC:
    if shutil.which("brew"):
        print("      Instalando con brew, esto tarda un par de minutos...")
        r = subprocess.run(["brew", "install", "ffmpeg"])
        print("      Listo." if r.returncode == 0 else "      NO se ha podido.")
    else:
        print("      No tienes brew, que es lo que hace falta para instalarlo.")
        print("      NO lo instales tu a mano. Escribele esto a Claude:")
        print("          instalame ffmpeg")
        print("      El se encarga. Te va a pedir una vez la contrasena de tu")
        print("      ordenador: es normal, es para instalar el programa.")
elif shutil.which("winget"):
    print("      Instalando con winget...")
    r = subprocess.run(["winget", "install", "--id", "Gyan.FFmpeg", "-e",
                        "--accept-source-agreements", "--accept-package-agreements"])
    print("      Listo. Cierra y vuelve a abrir Claude." if r.returncode == 0
          else "      NO se ha podido.")
else:
    print("      Instalalo a mano desde ffmpeg.org y anadelo al PATH.")

# 4 · el archivo de la clave ----------------------------------------------
print("\n[4/4] El archivo de tu clave de APImart")
if os.path.exists(ENV):
    print("      Ya existe:", ENV)
else:
    with open(ENV, "w", encoding="utf-8") as f:
        f.write("APIMART_KEY=\n")
    print("      Creado vacio:", ENV)

print("\n" + "=" * 58)
print(" TE TOCA A TI (1 minuto, y solo esta vez)")
print("=" * 58)
print(f"""
  1. Entra en apimart.ai, crea la cuenta y mete saldo.
  2. Copia tu clave.
  3. Abre este archivo:  {ENV}
  4. Dejalo asi, con tu clave pegada detras del igual:

         APIMART_KEY=tu_clave

  Esa clave es como la contrasena de tu tarjeta. No la pegues nunca
  en un chat, ni aqui ni en ningun sitio. Solo va en ese archivo.

  Cuando lo tengas, comprueba que esta todo bien:
      python3 ~/.claude/skills/replicar-anuncio-con-ia/scripts/comprobar.py

  Y para empezar, escribe:   /replicar-anuncio-con-ia
""")
