from flask import Flask, request, send_file, redirect
from pystyle import Colorate, Colors, System, Center, Write, Anime
from webbrowser import open_new as start
from socket import gethostname, gethostbyname
from os import listdir, chdir, name
from os.path import isfile



chronos = """

 .d8888b.  888                                                 
d88P  Y88b 888                                                 
888    888 888                                                 
888        88888b.  888d888 .d88b.  88888b.   .d88b.  .d8888b  
888        888 "88b 888P"  d88""88b 888 "88b d88""88b 88K      
888    888 888  888 888    888  888 888  888 888  888 "Y8888b. 
Y88b  d88P 888  888 888    Y88..88P 888  888 Y88..88P      X88 
 "Y8888P"  888  888 888     "Y88P"  888  888  "Y88P"   88888P' 
                                                               
                           by Miro                                         
                      
                      
                      
"""

banner = """
eee
"""

app = Flask("Chronos")


def run(host: str, port: int):
    return app.run(host, port)


def render(filename: str):
    with open(filename, mode='r', encoding='utf-8') as f:
        return f.read()

def ren(text: str, status_code: int = 200) -> tuple:
    print(f"Retourne {text} | Status code: {status_code}")
    return text, status_code


@app.route('/', methods=['GET'])
def main_route():
    return render('src/index.html')


@app.route('/upload', methods=['POST'])
def upload_route():
    try:
        f = request.files['file']
        if f.filename == '':
            return 'Aucun fichier sélectionné'
        f.save(f'database/{f.filename}')
        return redirect('/')
    except Exception as e:
        return f'error: {e}'


@app.route('/get/<filename>', methods=['GET'])
def get_route(filename):
    filename = f'database/{filename}'
    if isfile(filename):
        return send_file(filename, as_attachment=True)
    else:
        return "Fichier non trouvé !", 404



@app.route('/images/<image>', methods=['GET'])
def image_route(image):
    imagename = f'src/images/{image}'
    if isfile(imagename):
        return send_file(imagename, as_attachment=True)
    else:
        return send_file('db/chronos.jpg', as_attachment=True)



System.Clear()
System.Size(150, 40)
System.Title("Chronos")




def ui():
    System.Clear()
    print("\n"*2)
    print(Colorate.Diagonal(Colors.white_to_blue, Center.XCenter(chronos)))
    print("\n"*5)

def main():
    ui()

    hostname = gethostname()
    local_ip = gethostbyname(hostname)

    host = Write.Input("Entrez l'ip (appuiyez 'entré' pour l'adresse ip local) -> ",
                    Colors.white_to_blue, interval=0.005)
    if host == '':
        host = local_ip

    print()

    port = Write.Input("Entrez le port (appuiyez 'entré' pour '8080') -> ",
                    Colors.white_to_blue, interval=0.005)
    if port == '':
        port = "8080"
    try:
        port = int(port)
    except ValueError:
        Colorate.Error("Erreur! Le port doit être un chiffre.")
        return

    print('\n')

    Write.Input("Appuiyez 'entré' pour lancer le serveur !",
                    Colors.white_to_blue, interval=0.005)

    url = f"http://{host}:{port}/"
    start(url)
    ui()
    print(Colorate.Vertical(Colors.white_to_blue,
          f"   Lancé sur : {url}"))
    print(Colors.blue, end='')
    run(host=host, port=port)
    


if __name__ == '__main__':
    while True:
        main()
