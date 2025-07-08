from django.db import models


class Bino(models.Model):
    name = models.CharField("Bino nomi", max_length=100)

    def __str__(self):
        return self.name


class Camera(models.Model):
    bino = models.ForeignKey(Bino, on_delete=models.CASCADE, related_name='kameralar', verbose_name="Bino")
    name = models.CharField("Kamera nomi", max_length=100)
    ip = models.GenericIPAddressField("IP manzil", protocol='both', default='192.168.0.1')
    port = models.PositiveIntegerField("RTSP port", default=554)
    chanel = models.CharField("Kanal raqami", max_length=100, default=101)
    username = models.CharField("Foydalanuvchi nomi", max_length=50, default='admin')
    password = models.CharField("Parol", max_length=50, default='990507817a')
    youtube = models.BooleanField("YouTube'ga uzatilsinmi?", default=False)
    link = models.URLField("YouTube havola", max_length=500, blank=True)
    is_active = models.BooleanField("Faolmi?", default=True)

    class Meta:
        verbose_name = "Kamera"
        verbose_name_plural = "Kameralar"

    def rtsp_url(self):
        """
        RTSP oqim manzilini hosil qiladi.
        """
        base_url = f"{self.ip}:{self.port}/Streaming/Channels/{self.chanel}/"
        if self.username and self.password:
            return f"rtsp://{self.username}:{self.password}@{base_url}"
        return f"rtsp://{base_url}"

    def stream_url(self):
        """
        HLS fayli manzili (nginx bilan ishlatish uchun).
        """
        return f"/hls/cam_{self.id}/stream.m3u8"

    def __str__(self):
        return f"{self.bino.name} - {self.name}"
