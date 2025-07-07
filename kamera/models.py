from django.db import models

class Bino(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Camera(models.Model):
    bino = models.ForeignKey(Bino, on_delete=models.CASCADE, related_name='kameralar')
    name = models.CharField(max_length=100)
    port = models.IntegerField(default=554)
    ip = models.CharField(max_length=100)
    chanel = models.CharField(max_length=100)
    username = models.CharField(max_length=50, default='admin')
    password = models.CharField(max_length=50, default='990507817a')
    youtube = models.BooleanField(default=False)
    link = models.CharField(max_length=500, blank=True)


    def rtsp_url(self):
        base_url = f"{self.ip}:{self.port}/Streaming/Channels/{self.chanel}/"
        if self.username and self.password:
            return f"rtsp://{self.username}:{self.password}@{base_url}"
        else:
            return f"rtsp://{base_url}"


    def __str__(self):
        return f"{self.bino.name} - {self.name}"