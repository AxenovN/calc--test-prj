import socket
from calculator import sum
from config import CONTROLLER_SOCKET

def handle_request(request):
    """Обрабатывает HTTP запрос и возвращает ответ."""
    lines = request.splitlines()
    if len(lines) > 0:
        # Получаем первую строку запроса
        request_line = lines[0]
        method, path, _ = request_line.split()

        # Проверяем, что это GET запрос
        if method == 'GET':
            # Проверяем, соответствует ли путь нужному endpoint
            if path.startswith('/sum/'):
                # Извлекаем параметры a и b из пути
                try:
                    _, a, b = path.split('/')
                    a = float(a)
                    b = float(b)
                    result = sum(a, b)
                    # Изначально ИИ дал такую строку (см. ниже)
                    # response_body = f"Сумма {a} и {b} равна {result}"
                    # ... но я ее заменил на эту
                    response_body = f"{result}"
                    response_status = 'HTTP/1.1 200 OK'
                except (ValueError, IndexError):
                    response_body = "Ошибка: Неверные параметры."
                    response_status = 'HTTP/1.1 400 Bad Request'
            else:
                response_body = "Я Calculator, и я получил запрос. Он не sum."
                response_status = 'HTTP/1.1 404 Not Found'

            # Формируем ответ
            response_headers = 'Content-Type: text/plain; charset=utf-8\n'
            response_headers += f'Content-Length: {len(response_body)}\n\n'
            return f"{response_status}\n{response_headers}{response_body}"
    return "HTTP/1.1 400 Bad Request\n\n"

def run_server():
    """Запускает HTTP сервер на порту."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', CONTROLLER_SOCKET))
    server_socket.listen(5)
    print(f"Сервер запущен на порту {CONTROLLER_SOCKET}...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Подключение от {addr}")
        request_data = client_socket.recv(1024).decode('utf-8')
        print(f"Получен запрос:\n{request_data}")

        response = handle_request(request_data)
        
        client_socket.sendall(response.encode('utf-8'))
        client_socket.close()

if __name__ == "__main__":
    run_server()
