import os
from django.core.management.base import BaseCommand

SUPERVISOR_DIR = "/etc/supervisor/conf.d"

class Command(BaseCommand):
    help = "Barcha kamera streamlarini to‘xtatadi va conf fayllarni o‘chiradi"

    def handle(self, *args, **kwargs):
        for file in os.listdir(SUPERVISOR_DIR):
            if file.startswith("camera_") and file.endswith(".conf"):
                program_name = file[:-5]
                os.system(f"sudo supervisorctl stop {program_name}")
                os.remove(os.path.join(SUPERVISOR_DIR, file))
                self.stdout.write(self.style.WARNING(f"🛑 To‘xtatildi va o‘chirildi: {program_name}"))

        os.system("sudo supervisorctl reread")
        os.system("sudo supervisorctl update")
        self.stdout.write(self.style.SUCCESS("🧹 Barcha kameralar to‘xtatildi va tozalandi"))
