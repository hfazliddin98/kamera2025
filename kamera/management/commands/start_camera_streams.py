import os
import platform
from django.core.management.base import BaseCommand
from django.conf import settings
from kamera.models import Camera

if platform.system() == "Windows":
    SUPERVISOR_DIR = "D:/github/kamera2025/supervisor_conf"
else:
    SUPERVISOR_DIR = "/etc/supervisor/conf.d"

OUTPUT_DIR = os.path.join(settings.MEDIA_ROOT, "hls")

class Command(BaseCommand):
    help = "Kameralar uchun supervisor .conf fayllarni yaratadi"

    def handle(self, *args, **kwargs):
        os.makedirs(SUPERVISOR_DIR, exist_ok=True)
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        cameras = Camera.objects.filter(is_active=True)

        for camera in cameras:
            stream_dir = os.path.join(OUTPUT_DIR, f"cam_{camera.id}")
            os.makedirs(stream_dir, exist_ok=True)

            m3u8_path = os.path.join(stream_dir, "stream.m3u8")
            log_file = os.path.join(stream_dir, "ffmpeg.log")
            rtsp = camera.rtsp_url()

            conf_content = f"""
[program:camera_{camera.id}]
command=ffmpeg -i {rtsp} -c:v libx264 -preset ultrafast -tune zerolatency -f hls -hls_time 5 -hls_list_size 3 -hls_flags delete_segments+omit_endlist {m3u8_path}
directory={stream_dir}
autostart=true
autorestart=true
stdout_logfile={log_file}
stderr_logfile={log_file}
redirect_stderr=true
stopasgroup=true
killasgroup=true
""".strip()

            conf_path = os.path.join(SUPERVISOR_DIR, f"camera_{camera.id}.conf")

            with open(conf_path, "w", encoding="utf-8", newline='\n') as f:
                f.write(conf_content)

            self.stdout.write(self.style.SUCCESS(f"✅ Yaratildi: {conf_path}"))
