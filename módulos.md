Para este projeto, foram utilizados os seguintes módulos em Python:

### 1. **`os`**
   - **Função**: Este módulo oferece funções para interagir com o sistema operativo, como manipular ficheiros e diretórios.
   - **Uso no código**: Verifica se o ficheiro `libvlc.dll` existe, e também para verificar e manipular ficheiros XML.

### 2. **`ctypes`**
   - **Função**: Permite a interação com bibliotecas em C/C++ dentro do Python, permitindo carregar bibliotecas de sistema como a `libvlc.dll`.
   - **Uso no código**: Carrega manualmente a biblioteca `libvlc.dll`, necessária para interagir com o VLC.

### 3. **`tkinter`**
   - **Função**: É o módulo de interface gráfica (GUI) padrão em Python. Ele permite criar janelas, botões, caixas de texto, menus, e outros elementos de interface.
   - **Uso no código**: Cria a interface gráfica do player, com botões, caixa de texto, barra de volume, menus e interações com o rato (como copiar, cortar e colar).

### 4. **`filedialog`, `simpledialog`, `messagebox`** (parte de `tkinter`)
   - **Função**: São utilitários do módulo `tkinter` para interagir com o utilizador, abrindo caixas de diálogo para escolher ficheiros, introduzir URLs, e exibir mensagens de erro ou sucesso.
   - **Uso no código**:
     - `filedialog`: Usado para selecionar ficheiros locais de media.
     - `simpledialog`: Usado para pedir ao utilizador que insira uma URL.
     - `messagebox`: Usado para exibir mensagens informativas ou de erro.

### 5. **`xml.etree.ElementTree`**
   - **Função**: Fornece ferramentas para manipular ficheiros XML. Permite criar, modificar e ler dados em formato XML.
   - **Uso no código**: As URLs de stream são guardadas num ficheiro `urls.xml` e são lidas e gravadas usando este módulo. Cada URL é armazenada como um elemento `<url>` dentro da estrutura XML.

### 6. **`vlc`**
   - **Função**: É um módulo Python que fornece bindings para interagir com o VLC Media Player. Ele permite controlar o player, carregar ficheiros ou streams, e ajustar várias configurações, como o volume.
   - **Uso no código**: Permite criar uma instância do VLC, tocar ficheiros ou URLs, controlar o volume, parar a reprodução, etc. A biblioteca `libvlc.dll` do VLC precisa estar corretamente carregada para que este módulo funcione.

---

### Instalação dos Módulos:

1. **`vlc`**
   - Este módulo pode ser instalado com o `pip`:
     ```bash
     pip install python-vlc
     ```

2. **`tkinter`**
   - O `tkinter` geralmente já vem instalado por padrão com o Python. No entanto, se não estiver disponível no seu sistema, pode instalar:
     - **Windows**: Geralmente incluído na instalação do Python.
     - **Linux (Debian/Ubuntu)**:
       ```bash
       sudo apt-get install python3-tk
       ```

3. **`xml.etree.ElementTree`**
   - Este módulo é parte da biblioteca padrão do Python, portanto, não requer instalação adicional.

### Explicação do Funcionamento

- **os**: Garante que o ficheiro da biblioteca VLC está no local correto.
- **ctypes**: Carrega a biblioteca VLC para o Python.
- **tkinter**: Cria a interface gráfica com a qual o utilizador interage.
- **xml.etree.ElementTree**: Armazena e carrega as URLs em XML para que o utilizador possa reutilizá-las.
- **vlc**: Controla a reprodução de media, permitindo ao Python interagir diretamente com o VLC Media Player.