import subprocess
from pathlib import Path
import imageio_ffmpeg

root = Path(__file__).resolve().parent.parent
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

src = root / "image" / "source" / "ganesh-murti-idol.jpg"
out = root / "image" / "ganesha-16x9.jpg"

nirmala_bold = "C:/Windows/Fonts/NirmalaB.ttf".replace(":", "\\:")
arial_bold = "C:/Windows/Fonts/arialbd.ttf".replace(":", "\\:")

filter_complex = (
    "[0:v]scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,"
    "eq=brightness=-0.14:contrast=1.08:saturation=0.85[base];"
    "[base]drawbox=x=0:y=470:w=1280:h=250:color=black@0.50:t=fill[boxed];"
    f"[boxed]drawtext=fontfile='{nirmala_bold}':text='गणेश पंचरत्न':"
    "fontcolor=0xE8C55A:fontsize=68:x=60:y=500:shadowcolor=black@0.9:shadowx=2:shadowy=2[t1];"
    f"[t1]drawtext=fontfile='{arial_bold}':text='PEACE  ·  PROSPERITY  ·  PROTECTION':"
    "fontcolor=0xE8C55A:fontsize=26:x=64:y=600:shadowcolor=black@0.9:shadowx=1:shadowy=1[out]"
)

cmd = [
    ffmpeg, "-y", "-i", str(src),
    "-filter_complex", filter_complex,
    "-map", "[out]", "-frames:v", "1", "-q:v", "2",
    str(out),
]

result = subprocess.run(cmd, capture_output=True, text=True)
print(result.stderr[-2000:])
print("OK" if result.returncode == 0 else f"FAILED ({result.returncode})")
