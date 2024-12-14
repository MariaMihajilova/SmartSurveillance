import cv2
from django.http import StreamingHttpResponse
from django.shortcuts import render

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from SmartSurveillance.models import Screenshot
from django.core.files.base import ContentFile
import base64
import json
from datetime import datetime

# Глобальна змінна для збереження відкритої камери
camera = None

def generate_frames(camera_index):
    global camera

    # Закриваємо попередню камеру, якщо вона відкрита
    if camera is not None:
        camera.release()

    # Відкриваємо нову камеру
    camera = cv2.VideoCapture(camera_index)
    if not camera.isOpened():
        raise Exception(f"Не вдалося відкрити камеру {camera_index}")

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

def video_feed(request, camera_id=0):
    print(f"Отриманий camera_id: {camera_id}")
    return StreamingHttpResponse(
        generate_frames(camera_id), 
        content_type='multipart/x-mixed-replace; boundary=frame'
    )

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def save_screenshot(request):
    print(f"Скрін")
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            camera_id = data.get('camera_id')
            image_data = data.get('image')  # Баз64-дані зображення

            #if not (camera_id and image_data):
            #   return JsonResponse({'error': 'Camera ID or image data missing'}, status=400)

            # Перетворюємо base64 у файл
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            file_name = f"screenshot_{camera_id}_{int(datetime.now().timestamp())}.{ext}"
            image_file = ContentFile(base64.b64decode(imgstr), name=file_name)

            # Зберігаємо у базу даних
            screenshot = Screenshot(camera_id=camera_id, screenshot=image_file)
            screenshot.save()

            return JsonResponse({'message': 'Screenshot saved successfully'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)