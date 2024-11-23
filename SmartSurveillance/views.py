import cv2
from django.http import StreamingHttpResponse
from django.shortcuts import render

def generate_frames():
    # Відкриваємо камеру
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        raise Exception("Не вдалося відкрити камеру")
      

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Перетворюємо кадр в JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # Відправка кадрів клієнту
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            # Невелика затримка для стабільності
            cv2.waitKey(1)

def video_feed(request):
    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

def index(request):
    return render(request, 'index.html')