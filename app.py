from flask import Flask, url_for, request, redirect
import datetime

app = Flask(__name__)

@app.route("/web")
def web():
    return """<!doctype html> \
        <html> \
            <body> \
               <h1>web-сервер на flask</h1> \
               <a href="/author">author</a> \
               <a href="/info">info</a> \
               <a href="/counter">counter</a> \
            </body> \
        </html>"""

@app.route("/info")
def info():
    return redirect("/author")

@app.route("/author")
def author():
    name = "Филиппов Денис Макисмович"
    group = "ФБИ-33"
    faculty = "Бизнес-информатика"
    return f"""<!doctype html>
        <html>
            <body>
                <p>Студент: {name}</p>
                <p>Группа: {group}</p>
                <p>Факультет: {faculty}</p>
                <a href="/web">web</a>
                <a href="/info">info</a>
            </body>
        </html>"""

count = 0

@app.route('/counter')
def counter():
    global count
    count += 1
    time = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")  # ИСПРАВЛЕНО!
    url = request.url
    client_ip = request.remote_addr
    return f'''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: {count}
        <hr>
        Дата и время: {time}<br>
        Запрошенный адрес: {url}<br>
        Ваш IP-адрес: {client_ip}<br>
        <a href="/web">На главную</a>
    </body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)