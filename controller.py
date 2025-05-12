import socket
from calculator import sum
from config import CONTROLLER_SOCKET, FRONT_URL

def handle_request(request):
    """Обрабатывает HTTP запрос и возвращает ответ."""
    lines = request.splitlines()
    print(lines)
    if len(lines) > 0:
        print("len(lines) > 0")
        # Получаем первую строку запроса
        request_line = lines[0]
        print(request_line)
        print(len(request_line.split()))
        method, path, _ = request_line.split()
        print(method, path)

        # Проверяем, что это GET запрос
        if method == 'GET':
            print("Это метод GET")
            # Проверяем, соответствует ли путь нужному endpoint
            if path.startswith('/sum/'):
                print("Вижу sum")
                # Извлекаем параметры a и b из пути
                print("Пытаюсь извлечь числа а, б и вычислить результат")
                # print("... тест запуска метода sum: start")
                # a = float(1)
                # b = float(100)
                # result = sum(a, b)
                # print(f"... тест запуска метода sum: result is {result}")

                # print("... тест сплита path: start")
                # print(f"путь {path}<конец>")
                # print(f"содержит элементов: {len(path.split('/'))}")
                # k=0
                # for i in path.split('/'):
                #     k+=1
                #     print(f"{k} элемент: {i}")
                # print(f"... тест сплита path: done")
                
                try:
                    _, _, a, b = path.split('/')
                    a = float(a)
                    b = float(b)
                    print(f"Успешно извлек: a={a} and b={b}")
                    print("Запускаю метод sum")
                    result = sum(a, b)
                    print(f"Result of sum is {result}")
                    # Изначально ИИ дал такую строку (см. ниже)
                    # response_body = f"Сумма {a} и {b} равна {result}"
                    # ... но я ее заменил на эту
                    response_body = f"{result}"
                    response_status = 'HTTP/1.1 200 OK'
                except (ValueError, IndexError) as e:
                    print(f"Не смог извлечь числа и вычислить результат, т.к. ошибка: {e}")
                    response_body = "Ошибка: Неверные параметры."
                    response_status = 'HTTP/1.1 400 Bad Request'
            else:
                print("Не вижу sum. Возвращаю 404")
                response_body = "Я Calculator, и я получил запрос. Он не sum."
                response_status = 'HTTP/1.1 404 Not Found'

            # Формируем ответ
            response_headers = 'Content-Type: text/plain; charset=utf-8\n'
            response_headers += f'Access-Control-Allow-Origin: {FRONT_URL}\n'  # Добавляем заголовок CORS
            response_headers += f'Content-Length: {len(response_body)}\n\n'
            return f"{response_status}\n{response_headers}{response_body}"
        else:
            print("Это метод, отличный от GET")
            print("... я такие пока не умею обрабатывать => возвращаю 400")
    return "HTTP/1.1 400 Bad Request\n\n"

def run_server():
    """Запускает HTTP сервер на порту."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', CONTROLLER_SOCKET))
    server_socket.listen(5)
    print(f"Сервер запущен на порту {CONTROLLER_SOCKET}...")

    while True:
        print("====\nГотов принимать запрос...")
        client_socket, addr = server_socket.accept()
        print(f"Подключение от {addr}")
        request_data = client_socket.recv(1024).decode('utf-8')
        print(f"Получен запрос:\n{request_data}\n==== конец запроса ======\n")

        print("Запускаю обработку")
        response = handle_request(request_data)
        
        client_socket.sendall(response.encode('utf-8'))
        client_socket.close()

if __name__ == "__main__":
    run_server()
