import os
import unix2base62

file_name = os.getenv("FILE_NAME")
m3u8_url = os.getenv("M3U8_URL")
video_only = os.getenv("VIDEO_ONLY")
audio_only = os.getenv("AUDIO_ONLY")
use_ffmpeg = os.getenv("USE_FFMPEG")
referer = os.getenv("REFERER")
tc = os.getenv("TC")

output = "%s [%s]" % (file_name, unix2base62.timename())
# metadata = '-metadata:g encoding_tool="GA.00.00"'
http_header = '--http-header "User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0"'
s_referer = '--http-header "Referer=%s"' % (referer)

if use_ffmpeg == 'true':
  download_command = 'ffmpeg -hide_banner -i "%s" -c copy "DL/%s.ts"' % (m3u8_url, output)
else:
  if tc == 'true':
    download_command = 'streamlink --twitch-disable-hosting --twitch-disable-ads --twitch-disable-reruns --hls-live-restart --retry-streams 30 --stream-segment-threads 8 --force-progress %s %s -o "DL/%s.ts" "%s" audio_only,worst' % (http_header, s_referer, output, m3u8_url)
  else:
    download_command = 'streamlink --hls-live-restart --retry-open 30 --retry-streams 30 --retry-max 300 --stream-segment-threads 8 --force-progress %s %s -o "DL/%s.ts" "%s" 360p,best' % (http_header, s_referer, output, m3u8_url)
os.system(download_command)

if audio_only == 'true' and video_only == 'true':
  fix_command = 'sudo ffmpeg -hide_banner -i "DL/%s.ts" -c copy -map_metadata -1 -map_metadata:s -1 -movflags +faststart "UL/%s.mp4" -vn -c:a copy -map_metadata -1 -movflags +faststart "UL/%s.m4a"' % (output, output, output)
elif audio_only == 'true':
  fix_command = 'sudo ffmpeg -hide_banner -i "DL/%s.ts" -vn -c:a copy -map_metadata -1 -map_metadata:s -1 -movflags +faststart "UL/%s.m4a"' % (output, output)
elif video_only == 'true':
  fix_command = 'sudo ffmpeg -hide_banner -i "DL/%s.ts" -c copy -map_metadata -1 -map_metadata:s -1 -movflags +faststart "UL/%s.mp4"' % (output, output)
else:
  fix_command = 'sudo ffmpeg -hide_banner -i "DL/%s.ts" -vn -c:a copy -map_metadata -1 -map_metadata:s -1 -movflags +faststart "UL/%s.m4a"' % (output, output)

os.system(fix_command)
