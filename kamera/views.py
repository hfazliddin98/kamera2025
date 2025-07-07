from django.shortcuts import render, get_object_or_404
from .models import Camera
from .models import Bino

def home(request):
    binolar = Bino.objects.prefetch_related('kameralar').all()
    return render(request, 'kamera/home.html', {'binolar': binolar})

def camera_detail(request, pk):
    camera = get_object_or_404(Camera, pk=pk)
    return render(request, 'kamera/camera_detail.html', {'camera': camera})



