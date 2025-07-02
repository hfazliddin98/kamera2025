from django.core.management.base import BaseCommand
from kamera.models import Camera
import os
import subprocess
import threading
from django.conf import settings

def start_ffmpeg(camera):
    stream_dir = os.path.join(settings.MEDIA_ROOT, f"hls/cam_{camera.id}")
    os.makedirs(stream_dir, exist_ok=True)
    output_path = os.path.join(stream_dir, "stream.m3u8")
    rtsp_url = camera.rtsp_url()

    cmd = [
        "ffmpeg",
        "-i", rtsp_url,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-f", "hls",
        "-hls_time", "5",
        "-hls_list_size", "6",
        "-hls_flags", "delete_segments+omit_endlist",
        output_path
    ]

    try:
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"✅ {camera.bino.name} - {camera.name} stream boshlandi")
    except Exception as e:
        print(f"❌ Xatolik: {camera.bino.name} - {camera.name} -> {e}")

class Command(BaseCommand):
    help = 'Barcha kameralar uchun ffmpeg orqali streamlarni ishga tushiradi'

    def handle(self, *args, **kwargs):
        cameras = Camera.objects.all()
        for camera in cameras:
            threading.Thread(target=start_ffmpeg, args=(camera,), daemon=True).start()
