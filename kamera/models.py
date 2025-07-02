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
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)


    def rtsp_url(self):
        if self.username and self.password:
            return f"rtsp://{self.username}:{self.password}@{self.ip}:{self.port}/Streaming/Channels/{self.chanel}/"
        else:
            return f"rtsp://{self.ip}:{self.port}/Streaming/Channels/101/"

    def __str__(self):
        return f"{self.bino.name} - {self.name}"