"""Une los trozos generados y les pone el audio que toca.
uso: python3 unir.py <carpeta> <carpeta_con_los_mp4_buenos> [salida.mp4]

DOS MODOS, se elige solo:

  · VOZ DE LA IA (el bueno, y el que sale si usaste audio de referencia)
    Cuando a Wan se le manda el trozo de voz del original como referencia, devuelve el
    clip con esa misma voz diciendo las mismas palabras y en los mismos tiempos. O sea
    que la boca cuadra. Aqui solo hay que RECORTAR la cola sobrante, nunca estirar.

  · AUDIO DEL ORIGINAL ENCIMA (el de antes)
    Si los trozos vienen mudos. Wan reparte la accion por toda la duracion entera que le
    pediste, asi que hay que devolver cada trozo a su duracion exacta clavando el numero
    de fotogramas. Sin eso se pierden 5-7 centesimas por trozo y al final la voz va medio
    segundo por delante de la imagen."""
import json, os, subprocess, sys

carpeta = os.path.abspath(sys.argv[1])
buenos = os.path.abspath(sys.argv[2])
salida = sys.argv[3] if len(sys.argv) > 3 else os.path.join(carpeta, "REPLICA.mp4")
FPS = 30

def sh(*a):
    return subprocess.run(a, capture_output=True, text=True)

def dur(v):
    return float(sh("ffprobe", "-v", "error", "-show_entries", "format=duration",
                    "-of", "csv=p=0", v).stdout)

def tiene_audio(v):
    return bool(sh("ffprobe", "-v", "error", "-select_streams", "a:0",
                   "-show_entries", "stream=codec_type", "-of", "csv=p=0", v).stdout.strip())

tramos = json.load(open(os.path.join(carpeta, "tramos.json")))
final = os.path.join(carpeta, "_union")
os.makedirs(final, exist_ok=True)

primero = os.path.join(buenos, tramos[0]["nombre"] + ".mp4")
if not os.path.exists(primero):
    raise SystemExit(f"Falta {primero}")
VOZ_IA = tiene_audio(primero) and os.path.isdir(os.path.join(carpeta, "audios"))
print("MODO:", "voz de la IA (se queda el audio generado)" if VOZ_IA
      else "audio del original encima")

lista, total = [], 0
for t in tramos:
    src = os.path.join(buenos, t["nombre"] + ".mp4")
    if not os.path.exists(src):
        raise SystemExit(f"Falta {src}")
    N = round(t["dur"] * FPS)                 # fotogramas exactos que debe tener
    out = os.path.join(final, t["nombre"] + "_ok.mp4")

    if VOZ_IA:
        # recortar, nunca estirar: la voz ya esta en su sitio
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", src,
            "-vf", f"scale=1080:1920:flags=lanczos,fps={FPS},tpad=stop_mode=clone:stop_duration=1",
            "-frames:v", str(N), "-af", f"apad,atrim=0:{N/FPS:.3f},asetpts=N/SR/TB",
            "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-r", str(FPS),
            "-c:a", "aac", "-ar", "44100", "-ac", "2", "-y", out], check=True)
    else:
        factor = dur(src) / (N / FPS)
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", src,
            "-vf", (f"setpts=PTS/{factor:.6f},scale=1080:1920:flags=lanczos,fps={FPS},"
                    f"tpad=stop_mode=clone:stop_duration=1"),
            "-frames:v", str(N), "-an", "-c:v", "libx264", "-crf", "17",
            "-preset", "medium", "-r", str(FPS), "-y", out], check=True)

    total += N
    lista.append(out)
    print(f"{t['nombre']}: {N} fotogramas = {N/FPS:.3f} s  (objetivo {t['dur']})")

txt = os.path.join(final, "lista.txt")
# el concat de ffmpeg no traga las barras invertidas de Windows
open(txt, "w").write("".join(f"file '{p}'\n".replace("\\", "/") for p in lista))

if VOZ_IA:
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", txt, "-c:v", "copy", "-c:a", "aac", "-y", salida], check=True)
else:
    mudo = os.path.join(final, "unido.mp4")
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", txt, "-c", "copy", "-y", mudo], check=True)
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", mudo,
                    "-i", os.path.join(carpeta, "viral_full.mp4"),
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac",
                    "-shortest", "-y", salida], check=True)

orig = dur(os.path.join(carpeta, "viral_full.mp4"))
print(f"\n{salida}")
print(f"Replica {total/FPS:.3f} s · original {orig:.3f} s · desfase {total/FPS-orig:+.3f} s")
if abs(total / FPS - orig) > 0.15:
    print("OJO: mas de 0,15 s de desfase. Revisa las duraciones de tramos.json.")
