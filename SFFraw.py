import os
import unix2base62

file_name = os.getenv("FILE_NAME")
m3u8_url = os.getenv("M3U8_URL")
use_ffmpeg = os.getenv("USE_FFMPEG")
referer = os.getenv("REFERER")

output = "%s-[%s]" % (file_name, unix2base62.timename())
http_header = '--http-header "User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0"'
s_referer = '--http-header "Referer=%s"' % (referer)

if use_ffmpeg == 'true':
  download_command = 'ffmpeg -hide_banner -i "%s" -c copy -map_metadata -1 -map_metadata:s -1 "DL/%s.ts"' % (m3u8_url, output)
else:
  download_command = 'streamlink --stream-timeout 300 --stream-segment-attempts 300 --hls-playlist-reload-attempts 300 --hls-live-restart --retry-open 300 --retry-streams 30 --retry-max 600 --stream-segment-threads 8 --twitch-disable-hosting --twitch-disable-ads --twitch-disable-reruns --force-progress %s %s -o "DL/%s.ts" "%s" best' % (http_header, s_referer, output, m3u8_url)
  
os.system(download_command)
