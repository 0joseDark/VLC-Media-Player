import os
import ctypes
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import vlc

# Indicar o caminho completo para o libvlc.dll
libvlc_path = r'C:\Users\jose\Documents\libvlc\libvlc.dll'

# Verificar se o ficheiro libvlc.dll existe no caminho fornecido
if not os.path.exists(libvlc_path):
    raise FileNotFoundError(f'O ficheiro libvlc.dll não foi encontrado em: {libvlc_path}')

# Carregar a biblioteca manualmente
ctypes.CDLL(libvlc_path)

# Classe principal para o media player
class VLCPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("VLC Media Player")  # Título da janela
        self.root.geometry("500x200")  # Tamanho da janela

        # Criar uma instância do VLC
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        # Variável para armazenar o caminho do ficheiro ou URL
        self.media_path = None

        # Menu
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Abrir Ficheiro", command=self.open_file)
        filemenu.add_command(label="Abrir URL", command=self.open_url)
        filemenu.add_separator()
        filemenu.add_command(label="Sair", command=self.exit_player)
        menubar.add_cascade(label="Ficheiro", menu=filemenu)
        self.root.config(menu=menubar)

        # Botões
        self.play_button = tk.Button(self.root, text="Ligar", command=self.play_media)
        self.play_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.stop_button = tk.Button(self.root, text="Desligar", command=self.stop_media)
        self.stop_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.exit_button = tk.Button(self.root, text="Sair", command=self.exit_player)
        self.exit_button.pack(side=tk.LEFT, padx=10, pady=10)

    # Função para abrir ficheiro local
    def open_file(self):
        self.media_path = filedialog.askopenfilename(title="Escolha um ficheiro",
                                                     filetypes=(("Todos os ficheiros", "*.*"),
                                                                ("Ficheiros de vídeo", "*.mp4;*.avi;*.mkv"),
                                                                ("Ficheiros de áudio", "*.mp3;*.wav")))
        if self.media_path:
            self.play_button.config(state=tk.NORMAL)

    # Função para abrir uma URL de stream
    def open_url(self):
        self.media_path = simpledialog.askstring("URL Stream", "Introduza o URL do stream:")
        if self.media_path:
            self.play_button.config(state=tk.NORMAL)

    # Função para tocar o ficheiro ou URL
    def play_media(self):
        if self.media_path:
            # Carregar o media no VLC player
            media = self.instance.media_new(self.media_path)
            self.player.set_media(media)
            self.player.play()

    # Função para parar o media
    def stop_media(self):
        self.player.stop()

    # Função para sair do player
    def exit_player(self):
        self.player.stop()
        self.root.quit()

# Função principal para iniciar a aplicação
def main():
    root = tk.Tk()
    app = VLCPlayer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
