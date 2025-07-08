# kamera/apps.py

from django.apps import AppConfig
import subprocess
import os
import threading
from django.conf import settings

class KameraConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kamera'

    def ready(self):
        # Kodni faqat bitta ishga tushishida chaqilishiga chek qo'yamiz
        if os.environ.get('RUN_MAIN') != 'true':
            return

        from kamera.models import Camera

        def start_ffmpeg(camera):
            stream_dir = os.path.join(settings.MEDIA_ROOT, f"hls/cam_{camera.id}")
            os.makedirs(stream_dir, exist_ok=True)
            output_path = os.path.join(stream_dir, "stream.m3u8")
            rtsp_url = camera.rtsp_url()

            cmd = [
                "ffmpeg",
                "-rtsp_transport", "tcp",
                "-i", rtsp_url,
                "-vcodec", "libx264",
                "-acodec", "aac",
                "-preset", "veryfast",
                "-f", "hls",
                "-hls_time", "5",
                "-hls_list_size", "6",
                "-hls_flags", "delete_segments+omit_endlist",
                output_path
            ]

            try:
                subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"✅ Kamera ishga tushdi: {camera.name} ({camera.ip})")
            except Exception as e:
                print(f"❌ Xatolik: {camera.name} uchun ffmpeg ishlamadi:\n{e}")

        def start_all_cameras():
            try:
                cameras = Camera.objects.all()
                for camera in cameras:
                    threading.Thread(target=start_ffmpeg, args=(camera,), daemon=True).start()
            except Exception as e:
                print("❌ Kameralarni ishga tushirishda xatolik:", e)

        # Fon jarayonda barcha kameralarni boshlaymiz
        threading.Thread(target=start_all_cameras, daemon=True).start()
