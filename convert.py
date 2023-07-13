import os
from pathlib import Path
from datetime import datetime
import chardet
import unicodedata
import re

def detectar_codificacao_arquivo(nome_arquivo):
    with open(nome_arquivo, 'rb') as arquivo:
        dados = arquivo.read()
        resultado = chardet.detect(dados)
        codificacao = resultado['encoding']
        print("codificação:", codificacao)
        return codificacao

def convert_srt_to_ttml(srt_file, ttml_file, language, log_file):
    try:
        codificacao = detectar_codificacao_arquivo(srt_file)
        with open(srt_file, 'r', encoding=codificacao) as srt:
            lines = srt.readlines()

        ttml_content = convert_to_ttml(lines, language)
        print("Lendo:", srt_file)

        with open(ttml_file, 'w', encoding='utf-8') as ttml:
            ttml.write(ttml_content)

        os.chmod(ttml_file, 0o775)
        print("Arquivo TTML convertido gerado:", ttml_file)

    except UnicodeDecodeError as e:
        with open(log_file, 'a') as log:
            log.write(f"Erro ao converter o arquivo: {srt_file}\n")
        print("Erro ao converter o arquivo:", srt_file)
        print("Detalhes do erro:", str(e))

def fix_accentuation(line):
    return ''.join(c for c in unicodedata.normalize('NFD', line) if unicodedata.category(c) != 'Mn')

def convert_to_ttml(lines, language):
    def convert_time_format(time_str):
        time_parts = time_str.replace(',', '.').split(' --> ')

        if len(time_parts) != 2:
            return None, None

        start_time_str, end_time_str = time_parts
        try:
            if start_time_str.startswith('-'):
                start_time = datetime.strptime(start_time_str[1:], '-%H:%M:%S.%f')
                end_time = datetime.strptime(end_time_str, '-%H:%M:%S.%f')

                start_seconds = -((start_time.hour * 3600) + (start_time.minute * 60) + start_time.second + (start_time.microsecond / 1000000))
                end_seconds = -((end_time.hour * 3600) + (end_time.minute * 60) + end_time.second + (end_time.microsecond / 1000000))
            else:
                start_time = datetime.strptime(start_time_str, '%H:%M:%S.%f')
                end_time = datetime.strptime(end_time_str, '%H:%M:%S.%f')

                start_seconds = (start_time.hour * 3600) + (start_time.minute * 60) + start_time.second + (start_time.microsecond / 1000000)
                end_seconds = (end_time.hour * 3600) + (end_time.minute * 60) + end_time.second + (end_time.microsecond / 1000000)

            return '{:.3f}'.format(start_seconds), '{:.3f}'.format(end_seconds)
        except ValueError:
            return None, None

    ttml_content = '''<?xml version="1.0" encoding="utf-8"?>
<tt xmlns="http://www.w3.org/ns/ttml" xmlns:ttp="http://www.w3.org/ns/ttml#parameter" ttp:timeBase="media" xmlns:tts="http://www.w3.org/ns/ttml#styling" xml:lang="{}" xmlns:ttm="http://www.w3.org/ns/ttml#metadata">
  <head>
    <metadata>
      <ttm:title></ttm:title>
    </metadata>
    <styling>
      <style xml:id="s0" tts:backgroundColor="red" tts:fontStyle="normal" tts:fontSize="36px" tts:fontFamily="arial" tts:color="white" />
    </styling>
    <layout>
      <region tts:extent="80% 40%" tts:origin="10% 10%" tts:displayAlign="before" tts:textAlign="start" xml:id="topLeft" />
      <region tts:extent="80% 40%" tts:origin="10% 30%" tts:displayAlign="center" tts:textAlign="start" xml:id="centerLeft" />
      <region tts:extent="80% 40%" tts:origin="10% 50%" tts:displayAlign="after" tts:textAlign="start" xml:id="bottomLeft" />
      <region tts:extent="80% 40%" tts:origin="10% 10%" tts:displayAlign="before" tts:textAlign="center" xml:id="topCenter" />
      <region tts:extent="80% 40%" tts:origin="10% 30%" tts:displayAlign="center" tts:textAlign="center" xml:id="centerСenter" />
      <region tts:extent="80% 40%" tts:origin="10% 50%" tts:displayAlign="after" tts:textAlign="center" xml:id="bottomCenter" />
      <region tts:extent="80% 40%" tts:origin="10% 10%" tts:displayAlign="before" tts:textAlign="end" xml:id="topRight" />
      <region tts:extent="80% 40%" tts:origin="10% 30%" tts:displayAlign="center" tts:textAlign="end" xml:id="centerRight" />
      <region tts:extent="80% 40%" tts:origin="10% 50%" tts:displayAlign="after" tts:textAlign="end" xml:id="bottomRight" />
    </layout>
  </head>
  <body style="s0">
    <div>\n'''.format(language)

    is_subtitle = False
    subtitle_counter = 0
    for line in lines:
        line = line.strip()

        if not line:
            if is_subtitle:
                ttml_content += '</p>\n'
                is_subtitle = False
        elif '-->' in line:
            if is_subtitle:
                ttml_content += '</p>\n'
            subtitle_counter += 1
            start, end = convert_time_format(line)
            ttml_content += f'      <p begin="{start}s" xml:id="p{subtitle_counter}" end="{end}s">'
            is_subtitle = True
        else:
            line = line.replace('{\\an8}', '')
            line = line.replace('<i><font face="proportionalSansSerif" color="rgba(255,255,255,255)">', '')
            line = re.sub(r'<[^>]*>', '', line)
            line = line.strip()
            if line and is_subtitle:
                ttml_content += f'{line}<br />'

    ttml_content += '''    </div>
  </body>
</tt>'''

    return ttml_content

def check_srt_files(root_directory, language, log_file):
    root_directory = Path(root_directory)

    for root, dirs, files in os.walk(root_directory):
        for file in files:
            if file.endswith('.srt'):
                srt_file = os.path.join(root, file)
                ttml_file = os.path.splitext(srt_file)[0] + '.ttml'
                convert_srt_to_ttml(srt_file, ttml_file, language, log_file)

root_directory = "/"
language = "pt"
log_file = "/"

check_srt_files(root_directory, language, log_file)

