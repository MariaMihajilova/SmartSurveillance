import cv2
from django.http import StreamingHttpResponse
from django.shortcuts import render

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
