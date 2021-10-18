import psycopg2
import os
url = "postgres://kqgvesqibdfadi:dd7187fb30293722fbe1e69f8fb14e5b795723b1a71c15a9be9e86aca488bbf8@ec2-18-211-41-246.compute-1.amazonaws.com:5432/d4kni0qr398s83"


vetor =  url.split(":")
user = vetor[1].split("/")[2]
password = vetor[2].split("@")[0]
host = vetor[2].split("@")[1]
name = vetor[3].split("/")[1]



def logar(name,password,user,host):
    conn = psycopg2.connect(f"dbname={name} user={user} password={password} host={host} port=5432")

    return conn


def inserir(user_id,conta,update):
    conm = logar(name,password,user,host)
    cur = conm.cursor()
    try:
        cur.execute("INSERT INTO contas_usuarios (user_id,conta) VALUES (%s,%s)",(user_id,conta))
    except Exception as e:
        print(e)
        update.message.reply_text("Usuario ja cadastrado")

    else:
        conm.commit()
        update.message.reply_text("Dados Inseridos")
    finally:
        conm.close()

def remover(user_id):
    conm = logar(name,password,user,host)
    cur = conm.cursor()
    cur.execute("DELETE FROM contas_usuarios WHERE user_id = %s",(user_id,))
    conm.commit()
    conm.close()


def le_tabela(tabela):
    conm = logar(name,password,user,host)
    cur = conm.cursor()
    cur.execute("SELECT * FROM %s",(tabela,))
    conm.close()
    return cur.fetchall()


