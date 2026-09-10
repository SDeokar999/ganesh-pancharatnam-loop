# Builds a static-image video from your Ganpati image + AI-generated audio.
# The image is held still for the entire length of the audio track.
#
# Usage: drop your image at image\ganpati.(jpg|png) and your audio at
# audio\pancharatnam.(mp3|wav|m4a), then run:
#   .\scripts\make-video.ps1

$ffmpeg = python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())" 2>$null
if (-not $ffmpeg) { $ffmpeg = "ffmpeg" }  # fall back to PATH if the pip package isn't installed here

$root = Split-Path $PSScriptRoot -Parent
$image = Get-ChildItem (Join-Path $root "image") -Include *.jpg,*.jpeg,*.png -File | Select-Object -First 1
$audio = Get-ChildItem (Join-Path $root "audio") -Include *.mp3,*.wav,*.m4a,*.aac -File | Select-Object -First 1

if (-not $image) { Write-Error "No image found in image\ — add a .jpg/.png first."; exit 1 }
if (-not $audio)  { Write-Error "No audio found in audio\ — add your AI-generated track first."; exit 1 }

Write-Output "Image: $($image.Name)"
Write-Output "Audio: $($audio.Name)"

$out = Join-Path $root "video\loop.mp4"

& $ffmpeg -y -loop 1 -i $image.FullName -i $audio.FullName `
  -c:v libx264 -tune stillimage -crf 23 -preset medium `
  -c:a aac -b:a 192k -pix_fmt yuv420p -shortest `
  "$out"

Write-Output "---"
Get-Item $out | Select-Object Name, @{N='SizeMB';E={[math]::Round($_.Length/1MB,2)}}
