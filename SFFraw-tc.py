import os
import unix2base62

file_name = os.getenv("FILE_NAME")
m3u8_url = os.getenv("M3U8_URL")
use_ffmpeg = os.getenv("USE_FFMPEG")
referer = os.getenv("REFERER")
cookies = os.getenv("TC_COOKIES")

output = "%s-[%s]" % (file_name, unix2base62.timename())
http_header = '--http-header "User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"'
http_cookie = '--http-cookie "%s"' % (cookies)
s_referer = '--http-header "Referer=%s"' % (referer)
new_m3u8_url = m3u8_url.replace("/132.68/media", "/138.96/media")

download_command = 'streamlink --stream-timeout 300 --stream-segment-attempts 300 --hls-playlist-reload-attempts 300 --hls-live-restart --retry-open 300 --retry-streams 30 --retry-max 600 --stream-segment-threads 8 --twitch-disable-hosting --twitch-disable-ads --twitch-disable-reruns --progress=force %s %s %s -o "DL/%s.ts" "%s" best' % (http_header, http_cookie, s_referer, output, m3u8_url)
os.system(download_command)
