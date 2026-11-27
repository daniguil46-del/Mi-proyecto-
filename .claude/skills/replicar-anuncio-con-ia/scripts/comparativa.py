"""Pone el anuncio original y la replica uno al lado del otro, para enseñarlo.
uso: python3 comparativa.py <original.mp4> <replica.mp4> [salida.mp4] [--sin-etiquetas]

Suena el audio de la REPLICA, que es lo que hay que juzgar. Si duran distinto, se
corta por el mas corto y se avisa."""
import os, subprocess, sys

args = [a for a in sys.argv[1:] if a != "--sin-etiquetas"]
etiquetas = "--sin-etiquetas" not in sys.argv
ORIG, REP = os.path.abspath(args[0]), os.path.abspath(args[1])
SALIDA = args[2] if len(args) > 2 else os.path.join(os.path.dirname(REP), "COMPARATIVA.mp4")

def sh(*a):
    return subprocess.run(a, capture_output=True, text=True)

def dur(v):
    return float(sh("ffprobe", "-v", "error", "-show_entries", "format=duration",
                    "-of", "csv=p=0", v).stdout or 0)

d1, d2 = dur(ORIG), dur(REP)
if abs(d1 - d2) > 0.3:
    print(f"OJO: el original dura {d1:.2f} s y la replica {d2:.2f} s. Se corta por el mas corto.")

def lado(idx, texto):
    c = f"[{idx}:v]scale=540:960:force_original_aspect_ratio=decrease," \
        f"pad=540:960:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1,setpts=PTS-STARTPTS"
    if etiquetas:
        c += (f",drawbox=x=0:y=0:w=540:h=64:color=black@0.55:t=fill"
              f",drawtext=text='{texto}':fontsize=30:fontcolor=white:"
              f"x=(w-text_w)/2:y=18")
    return c

filtro = (f"{lado(0,'ORIGINAL')}[a];{lado(1,'REPLICA')}[b];[a][b]hstack=inputs=2[v]")
r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", ORIG, "-i", REP,
                    "-filter_complex", filtro, "-map", "[v]", "-map", "1:a?",
                    "-t", f"{min(d1, d2):.3f}",
                    "-c:v", "libx264", "-crf", "20", "-preset", "medium",
                    "-c:a", "aac", "-y", SALIDA])
if r.returncode != 0:
    # algunos Mac no tienen fuente para drawtext: se repite sin etiquetas
    filtro = ("[0:v]scale=540:960:force_original_aspect_ratio=decrease,"
              "pad=540:960:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1,setpts=PTS-STARTPTS[a];"
              "[1:v]scale=540:960:force_original_aspect_ratio=decrease,"
              "pad=540:960:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1,setpts=PTS-STARTPTS[b];"
              "[a][b]hstack=inputs=2[v]")
    r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", ORIG, "-i", REP,
                        "-filter_complex", filtro, "-map", "[v]", "-map", "1:a?",
                        "-t", f"{min(d1, d2):.3f}",
                        "-c:v", "libx264", "-crf", "20", "-preset", "medium",
                        "-c:a", "aac", "-y", SALIDA])
if r.returncode != 0 or not os.path.exists(SALIDA):
    raise SystemExit("No se ha podido montar la comparativa.")
print("Comparativa →", SALIDA)
