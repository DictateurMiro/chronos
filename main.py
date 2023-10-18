from flask import Flask, request, send_file, redirect, jsonify
from pystyle import Colorate, Colors, System, Center, Write, Anime
from webbrowser import open_new as start
from socket import gethostname, gethostbyname
from os import listdir, chdir, name
from os.path import isfile, getsize, join

import psutil
import math



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
        return send_file('images/chronos.jpg', as_attachment=True)

@app.route('/list-files', methods=['GET'])
def list_files():
    directory_path = 'database'
    files = listdir(directory_path)
    file_info = {}
    
    total_size = 0
    for file in files:
        file_path = join(directory_path, file)
        file_size = getsize(file_path)
        total_size += file_size
        file_info[file] = convert_size(file_size)

        
    disk_info = psutil.disk_usage('/')
    free_space = disk_info.free
    total_space = disk_info.total
    used_space = total_space - free_space
    percent_used = (used_space / total_space) * 100
    percent_no_used = 100 - percent_used
    
    total_space_gb = total_space / (1024 ** 3)
    free_space_gb = free_space / (1024 ** 3)
    
    return jsonify({
        'files': file_info,
        'total_size': f"{total_space_gb:.2f} Go",
        'free_space': f"{free_space_gb:.2f} Go",
        'total_space': f"{total_space} octets",
        'percent_used': f"{percent_used:.2f}%",
        'percent_no_used': f"{percent_no_used:.2f}%"
    })

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("octets", "Ko", "Mo", "Go", "To", "Po", "Eo", "Zo", "Yo")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"


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
