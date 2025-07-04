from django.shortcuts import render
from django.http import StreamingHttpResponse
import cv2
from django.shortcuts import render, get_object_or_404
from .models import Camera


# IP kamera URL (o‘zingizniki bilan almashtiring)
camera_url = "rtsp://admin:990507817a@192.168.200.5:554/h264"
cap = cv2.VideoCapture(camera_url)

def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def video_feed(request):
    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

def index(request):
    return render(request, 'kamera/index.html')

from django.shortcuts import render
from .models import Bino

def home(request):
    binolar = Bino.objects.prefetch_related('kameralar').all()
    return render(request, 'kamera/home.html', {'binolar': binolar})

def camera_detail(request, pk):
    camera = get_object_or_404(Camera, pk=pk)
    return render(request, 'kamera/camera_detail.html', {'camera': camera})

