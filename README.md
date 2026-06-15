# PlayPoint Auto-Timestamp 🎵🎯

Este repositório contém ferramentas em Python criadas para automatizar a geração de **timestamps precisos** em áudios de hinos (arquivos MP3) baseando-se em suas letras/cifras oficiais. 

O objetivo principal é permitir que os usuários cliquem em qualquer frase ou acorde de uma cifra e o áudio comece a tocar exatamente naquele instante, eliminando centenas de horas de trabalho de marcação manual.

---

## 🚀 Abordagem idealizada

Transcrição e Mapeamento Difuso (`transcript-map.py`)
Utiliza o modelo **`faster-whisper`** (estado da arte em transcrição de áudio) combinado com algoritmos de correspondência flexível (**`rapidfuzz`**).
* **Como funciona:** 1. O Whisper processa o MP3 (mesmo com instrumentos ou ruídos de fundo) e gera uma transcrição com **timestamps no nível da palavra** (*word-level timestamps*).
  2. Como a transcrição gerada pela IA pode conter pequenas variações ou erros fonéticos em relação ao hinário oficial, o script usa correspondência difusa (*fuzzy matching*) para cruzar o texto da IA com o texto oficial da cifra.
  3. Ele injeta os tempos corretos nas frases oficiais com base nas palavras correspondentes encontradas pela IA.
* **Ideal para:** Áudios complexos (com órgãos, percussão, coros ou ruídos) e casos onde a precisão humana na fala/canto varia sutilmente do papel.

Transcrição + Mapeamento Difuso
Bash
python transcript-map.py --audio hino.mp3 --texto letra.txt --saida playpoint_whisper.json
Comportamento esperado: O faster-whisper fará a leitura fonética do áudio gerando marcações milimétricas palavra por palavra. Em seguida, o algoritmo difuso associará essas palavras às linhas oficiais do seu arquivo de texto, gerando o arquivo JSON final estruturado.

📄 Formato do Arquivo de Saída (JSON)
Ambos os scripts exportam o resultado no formato padronizado abaixo, facilitando a importação direta para o banco de dados do seu site:

JSON
[
  {
    "linha_id": 1,
    "texto": "Grandioso és Tu, Senhor",
    "tempo_inicio": "00:00:12.450",
    "tempo_fim": "00:00:16.890"
  },
  {
    "linha_id": 2,
    "texto": "Ao ver a Tua criação",
    "tempo_inicio": "00:00:17.100",
    "tempo_fim": "00:00:21.320"
  }
]

---

## 🛠️ Pré-requisitos e Instalação

### Dependências de Sistema
Para que as bibliotecas de áudio e alinhamento funcionem corretamente, é necessário ter o `FFmpeg` instalado no sistema operacional.

* **Ubuntu/Debian:** `sudo apt install -y ffmpeg espeak`
* **Windows/Mac:** Certifique-se de instalar o `ffmpeg` e adicioná-lo às variáveis de ambiente do sistema.

### Instalação das Bibliotecas Python

Recomenda-se o uso de um ambiente virtual para isolar as dependências do projeto.

1. **Crie e ative um ambiente virtual:**
   ```bash
   # No Linux/macOS:
   python3 -m venv venv
   source venv/bin/activate

   # No Windows:
   python -m venv venv
   .\venv\Scripts\activate
   ```

2. **Instale as dependências:**
   O projeto utiliza um arquivo `requirements.txt` para gerenciar as dependências.
   ```bash
   pip install -r requirements.txt
   ```


