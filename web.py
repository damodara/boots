from http.server import BaseHTTPRequestHandler, HTTPServer
import os

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Если запрос на корень, открываем contact.html
            self.path = '/contact.html'

        if self.path.endswith('.html'):
            # Обслуживаем HTML-страницу
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open(os.path.join('.', self.path.lstrip('/')), 'r', encoding='utf-8') as file:
                html_content = file.read()
            self.wfile.write(bytes(html_content, "utf-8"))
        elif self.path.startswith('/css/'):
            # Обслуживаем CSS-файлы
            file_path = os.path.join('.', self.path.lstrip('/'))
            try:
                self.send_response(200)
                self.send_header('Content-type', 'text/css')
                self.end_headers()
                with open(file_path, 'r', encoding='utf-8') as file:
                    self.wfile.write(bytes(file.read(), "utf-8"))
            except FileNotFoundError:
                self.send_error(404, "File Not Found")
        elif self.path.startswith('/js/'):
            # Обслуживаем JavaScript-файлы
            file_path = os.path.join('.', self.path.lstrip('/'))
            try:
                self.send_response(200)
                self.send_header('Content-type', 'text/javascript')
                self.end_headers()
                with open(file_path, 'r', encoding='utf-8') as file:
                    self.wfile.write(bytes(file.read(), "utf-8"))
            except FileNotFoundError:
                self.send_error(404, "File Not Found")
        elif self.path.startswith('/brand/'):
            # Обслуживаем изображения (включая SVG)
            file_path = os.path.join('.', self.path.lstrip('/'))
            try:
                self.send_response(200)
                if self.path.endswith('.svg'):
                    self.send_header('Content-type', 'image/svg+xml')
                else:
                    self.send_header('Content-type', 'image/png')  # Предположим, что изображения в формате PNG
                self.end_headers()
                with open(file_path, 'rb') as file:
                    self.wfile.write(file.read())
            except FileNotFoundError:
                self.send_error(404, "File Not Found")
        else:
            # Обрабатываем другие типы файлов (например, изображения или JavaScript)
            self.send_error(404, "Not Found")

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")