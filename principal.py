import arq
def envio_sidecar(update,vetor):
        cont=0
        for i in vetor:
            if i == 1:
                arq.download(vetor[cont+1],'midia/'+str(cont),'.jpeg')
                update.message.reply_photo(photo=open('midia/'+str(cont)+'.jpeg','rb'))
            elif i == 2:
                arq.download(vetor[cont+1],'midia/'+str(cont),'.mp4')
                update.message.reply_photo(video=open('midia/'+str(cont)+'.mp4','rb'))


            cont = cont+1
   

def envio_single_photo(update,vetor):
    arq.download(vetor,'midia/1','.jpeg')
    update.message.reply_photo(photo=open('midia/1.jpeg','rb'))

def envio_single_video(update,vetor):
    arq.download(vetor,'midia/1','.mp4')
    print("teste",vetor)
    update.message.reply_video(video=open('midia/1.mp4','rb'))