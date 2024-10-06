import os
import ctypes
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import xml.etree.ElementTree as ET

# Indicar o caminho completo para a libvlc.dll
libvlc_path = r'C:\Program Files\VideoLAN\VLC\libvlc.dll'

# Verificar se o ficheiro libvlc.dll existe no caminho fornecido
if not os.path.exists(libvlc_path):
    raise FileNotFoundError(f'O ficheiro libvlc.dll não foi encontrado em: {libvlc_path}')

# Carregar a biblioteca manualmente
ctypes.CDLL(libvlc_path)

# Agora importa a biblioteca vlc
import vlc

# Caminho do ficheiro XML onde as URLs serão armazenadas
xml_file = "urls.xml"

# Função para gravar as URLs no ficheiro XML
def save_url_to_xml(url):
    if not os.path.exists(xml_file):
        root = ET.Element("urls")
        tree = ET.ElementTree(root)
        tree.write(xml_file)

    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Criar um novo elemento <url>
    url_element = ET.Element("url")
    url_element.text = url
    root.append(url_element)

    # Gravar as alterações no ficheiro XML
    tree.write(xml_file)

# Função para carregar URLs do ficheiro XML
def load_urls_from_xml():
    if os.path.exists(xml_file):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        return [url.text for url in root.findall("url")]
    return []

# Classe principal para o media player
class VLCPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("VLC Media Player")
        self.root.geometry("500x400")  # Aumentar a altura para acomodar a caixa de texto e a barra de volume

        # Definir opções de inicialização do VLC para desativar título de vídeo
        self.instance = vlc.Instance('--vout=glwin32', '--no-video-title-show')
        if not self.instance:
            raise Exception("Falha ao criar a instância do VLC")

        self.player = self.instance.media_player_new()

        # Variável para armazenar o caminho do ficheiro ou URL
        self.media_path = None

        # Carregar URLs do ficheiro XML
        self.saved_urls = load_urls_from_xml()

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

        # Caixa de texto para URLs
        self.url_text = tk.Text(self.root, height=5, width=50)
        self.url_text.pack(pady=10)

        # Adicionar o menu de contexto para copiar, cortar e colar
        self.create_context_menu()

        # Botão para memorizar URLs da caixa de texto
        self.save_url_button = tk.Button(self.root, text="Memorizar URLs", command=self.save_urls_from_text)
        self.save_url_button.pack(pady=5)

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

    # Função para criar o menu de contexto (copiar, cortar, colar)
    def create_context_menu(self):
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Copiar", command=self.copy_text)
        self.context_menu.add_command(label="Cortar", command=self.cut_text)
        self.context_menu.add_command(label="Colar", command=self.paste_text)

        # Associar o clique do botão direito para abrir o menu de contexto
        self.url_text.bind("<Button-3>", self.show_context_menu)

    # Função para exibir o menu de contexto
    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    # Função para copiar o texto selecionado
    def copy_text(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.url_text.get(tk.SEL_FIRST, tk.SEL_LAST))

    # Função para cortar o texto selecionado
    def cut_text(self):
        self.copy_text()
        self.url_text.delete(tk.SEL_FIRST, tk.SEL_LAST)

    # Função para colar o texto da área de transferência
    def paste_text(self):
        self.url_text.insert(tk.INSERT, self.root.clipboard_get())

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
            # Guardar a URL no ficheiro XML
            save_url_to_xml(self.media_path)
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

    # Função para memorizar as URLs da caixa de texto
    def save_urls_from_text(self):
        urls = self.url_text.get("1.0", tk.END).strip().split("\n")
        for url in urls:
            if url.strip():  # Ignorar linhas em branco
                save_url_to_xml(url.strip())
        self.saved_urls = load_urls_from_xml()  # Atualizar a lista de URLs guardadas
        messagebox.showinfo("Info", "As URLs foram memorizadas!")

# Função principal para iniciar a aplicação
def main():
    root = tk.Tk()
    app = VLCPlayer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
