import requests

from pathlib import Path
def download(url,name,tipo):

    response = requests.get(url)
    arq = str(name) + tipo
    with open(arq,'wb') as f:
            f.write(response.content)
    f.close()
    caminho = arq
    print(caminho)
    tamanho = Path(caminho).stat().st_size
    print(tamanho)
    if tamanho == 0:
        print("Download falhou, tentando novamente")
        download(url,name,tipo)
    print('Download completo')

def deleta(path):
    import os
    dir = os.listdir(path)
    print(dir)
    for file in dir:
            os.remove(path+'/'+file)