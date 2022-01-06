import socket
import threading
from tkinter import *
import tkinter
from tkinter import simpledialog

class Chat:
    def __init__(self):
        HOST = '127.0.0.1'
        PORT = 55556
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))
        login = Tk()
        login.withdraw()

        self.janela_carregada = False
        self.ativo = True

        self.nome = simpledialog.askstring('Nome', 'Digite seu Nome:', parent=login)
        self.sala = simpledialog.askstring('Sala', 'Digite a sala que deseja entrar: ', parent=login)
        thread = threading.Thread(target=self.connect)
        thread.start()
        self.janela()

    def janela(self):
        self.root = Tk()
        self.root.geometry('800x800')
        self.root.title('Chat')

        self.caixa_texto = Text(self.root)
        self.caixa_texto.place(relx=0.05, rely=0.01, width=700, height=600 )
        self.root.mainloop()

        self.enviaMensagem = Entry(self.root)
        self.enviaMensagem.place(relx=0.05, rely=0.8, width=500, height=20 )

        self.button = Button(self.root, text='Enviar',command=self.enviarMensagem)
        self.button.place(relx=0.7, rely=0.8, width=100, height=20)
        self.root.protocol("WM_DELETE_WINDOW", self.fechar)

    def fechar(self):
        self.root.destroy()
        self.client.close()

    def connect(self):
        while True:
            receber = self.client.recv(1024)
            if receber == b'SALA':
                self.client.send(self.sala.decode())
                self.client.send(self.nome.decode())
            else:
                try:
                    self.caixa_texto.insert('end', receber.encode())
                except:
                    pass

    def enviarMensagem(self):
        mensagem = self.enviaMensagem.get()
        self.client.send(mensagem.encode())
chat = Chat()