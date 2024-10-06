import os
import ctypes
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

# Indicar o caminho completo para a libvlc.dll
libvlc_path = r'C:\Program Files\VideoLAN\VLC\libvlc.dll'

# Verificar se o ficheiro libvlc.dll existe no caminho fornecido
if not os.path.exists(libvlc_path):
    raise FileNotFoundError(f'O ficheiro libvlc.dll não foi encontrado em: {libvlc_path}')

# Carregar a biblioteca manualmente
ctypes.CDLL(libvlc_path)

# Agora importa a biblioteca vlc
import vlc

# Caminho do ficheiro de log onde as URLs serão armazenadas
log_file = "url.log"

# Função para gravar as URLs no ficheiro de log
def save_url_to_log(url):
    with open(log_file, "a") as f:
        f.write(url + "\n")

# Função para carregar URLs do ficheiro de log
def load_urls_from_log():
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            urls = f.readlines()
        return [url.strip() for url in urls]
    return []

# Classe principal para o media player
class VLCPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("VLC Media Player")
        self.root.geometry("500x300")  # Aumentar a altura para acomodar a barra de volume e o log

        # Definir opções de inicialização do VLC para desativar título de vídeo
        self.instance = vlc.Instance('--vout=glwin32', '--no-video-title-show')
        if not self.instance:
            raise Exception("Falha ao criar a instância do VLC")

        self.player = self.instance.media_player_new()

        # Variável para armazenar o caminho do ficheiro ou URL
        self.media_path = None

        # Carregar URLs do ficheiro de log
        self.saved_urls = load_urls_from_log()

        # Menu
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Abrir Ficheiro", command=self.open_file)
        filemenu.add_command(label="Abrir URL", command=self.open_url)
        filemenu.add_command(label="Reutilizar URL Guardado", command=self.reuse_url)
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

        # Adicionar a barra de volume
        self.volume_scale = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, label="Volume", command=self.set_volume)
        self.volume_scale.set(50)  # Volume padrão de 50%
        self.volume_scale.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

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
            # Guardar a URL no ficheiro de log
            save_url_to_log(self.media_path)
            self.play_button.config(state=tk.NORMAL)

    # Função para reutilizar uma URL guardada
    def reuse_url(self):
        if self.saved_urls:
            self.media_path = simpledialog.askstring("Escolha um URL", "Selecione um dos URLs guardados:\n" + "\n".join(self.saved_urls))
            if self.media_path:
                self.play_button.config(state=tk.NORMAL)
        else:
            messagebox.showinfo("Info", "Nenhuma URL guardada disponível.")

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

    # Função para ajustar o volume
    def set_volume(self, volume):
        volume = int(volume)
        self.player.audio_set_volume(volume)

# Função principal para iniciar a aplicação
def main():
    root = tk.Tk()
    app = VLCPlayer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
