from django.apps import AppConfig
import subprocess
import os
import threading
from django.conf import settings

class KameraConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kamera'

    def ready(self):
        from kamera.models import Camera

        def start_ffmpeg(camera):
            # Har bir kamera uchun HLS papkasi
            stream_dir = os.path.join(settings.MEDIA_ROOT, f"hls/cam_{camera.id}")
            os.makedirs(stream_dir, exist_ok=True)

            # Chiqish fayli nomi: stream.m3u8
            output_path = os.path.join(stream_dir, "stream.m3u8")

            # RTSP URL
            rtsp_url = camera.rtsp_url()

            # ffmpeg buyrug‘i
            cmd = [
                "ffmpeg",
                "-i", rtsp_url,
                "-c:v", "libx264",
                "-preset", "veryfast",  # Tez ishlashi uchun
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

        # Barcha kameralar uchun streamni fon jarayonda ishga tushirish
        threading.Thread(target=start_all_cameras, daemon=True).start()




# from django.apps import AppConfig
# import subprocess
# import os

# class StreamappConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'streamapp'

#     def ready(self):
#         # Ffmpeg komandani ishga tushurish
#         ffmpeg_cmd = [
#             "ffmpeg",
#             "-i", "rtsp://admin:990507817a@192.168.200.5:554/stream",
#             "-c:v", "libx264",
#             "-f", "hls",
#             "-hls_time", "5",
#             "-hls_list_size", "6",
#             "-hls_flags", "delete_segments",
#             "media/hls/stream.m3u8"
#         ]

#         # HLS katalogi mavjud bo‘lmasa, yaratamiz
#         os.makedirs("media/hls/", exist_ok=True)

#         # Stream jarayonini ishga tushirish (agar hali yo‘q bo‘lsa)
#         try:
#             subprocess.Popen(ffmpeg_cmd)
#             print("🎥 FFMPEG kamerani yozishni boshladi.")
#         except Exception as e:
#             print("❌ FFMPEGni ishga tushirishda xatolik:", e)
