import mysql.connector
from mysql.connector.locales.eng import client_error
import kivy
kivy.require('2.0.0')
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
import os
import mysql.connector
import tkinter as tk
import subprocess
import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from tkinter import filedialog
from kivy.uix.popup import Popup

# Abrir o arquivo .txt com a codificação correta
# No .txt estão as informações para conexão com o banco de dados
arquivo = open("bdds.txt", "r", encoding="utf-8")

# Criando um dicionário para armazenar as informações de login
informacoes_login = {}

# Lendo o conteúdo do arquivo
for linha in arquivo:
    # Removendo espaços em branco extras e quebras de linha
    linha = linha.strip()

    # Separando a chave e o valor
    chave, valor = linha.split('=')

    # Removendo as aspas simples em torno do valor
    valor = valor.strip("'")

    # Armazenando a informação no dicionário
    informacoes_login[chave] = valor

# Fechando o arquivo
arquivo.close()

# Acessando as informações de login individualmente
user = informacoes_login.get('user')
password = informacoes_login.get('password')
host = informacoes_login.get('host')
database = informacoes_login.get('database')
port = informacoes_login.get('port')

class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Conectando-se ao banco de dados
        cnx = mysql.connector.connect(user=user, password=password,
                                      host=host, database=database, port=port)

        # Criando um cursor para executar consultas
        cursor = cnx.cursor()

        # Executando uma consulta para obter os dados dos estados
        query = "SELECT nome FROM estados"
        cursor.execute(query)

        # Obtendo os resultados da consulta e converta-os em uma lista de strings
        resultados_estados = [str(row[0]) for row in cursor.fetchall()]

        # Fechando o cursor e a conexão
        cursor.close()
        cnx.close()

        # Criando um spinner para os estados
        spinner1 = Spinner(text='Estados', values=resultados_estados, size_hint=(0.4, 0.1), pos_hint={'center_x': 0.5, 'top': 0.9})

        # Criando um spinner para as cidades
        spinner2 = Spinner(text='Cidades', size_hint=(0.4, 0.1), pos_hint={'center_x': 0.5, 'top': 0.7})

        # Criando um spinner para aos loteamentos
        spinner3 = Spinner(text='Loteamentos', size_hint=(0.4, 0.1), pos_hint={'center_x': 0.5, 'top': 0.5})

        # Criando um spinner para as informações
        spinner4 = Spinner(text='Informações', size_hint=(0.4, 0.1), pos_hint={'center_x': 0.5, 'top': 0.3})

        # Criando um layout
        layout = FloatLayout()

        # Adicionando os spinners ao layout
        self.add_widget(spinner1)
        self.add_widget(spinner2)
        self.add_widget(spinner3)
        self.add_widget(spinner4)

        # Atualizando as opções do spinner2 quando uma opção do spinner1 for selecionada
        def update_spinner2_options(spinner, text1):
            if text1 != 'Estados':
                # Conectando-se ao banco de dados
                cnx = mysql.connector.connect(user=user, password=password,
                                      host=host, database=database, port=port)

                # Criando um cursor para executar consultas
                cursor = cnx.cursor()

                # Executando uma consulta para obter as cidades relacionadas ao estado selecionado
                query = """
                    SELECT cidades.nome
                    FROM cidades
                    INNER JOIN estados ON cidades.estado_id = estados.id
                    WHERE estados.nome = %s
                """
                estado = text1
                cursor.execute(query, (estado,))

                # Obtendo os resultados da consulta e converta-os em uma lista de strings
                resultados_cidades = [str(row[0]) for row in cursor.fetchall()]

                # Fechando o cursor e a conexão
                cursor.close()
                cnx.close()

                # Atualizando as opções do spinner2
                spinner2.values = resultados_cidades
                spinner2.text = 'Cidades'
        
        # Atualizando as opções do spinner3 quando uma opção do spinner2 for selecionada
        def update_spinner3_options(spinner, text2):
            if text2 != 'Cidades':
                # Conectando-se ao banco de dados
                cnx = mysql.connector.connect(user=user, password=password,
                                      host=host, database=database, port=port)

                # Criando um cursor para executar consultas
                cursor = cnx.cursor()

                # Executando uma consulta para obter as cidades relacionadas ao estado selecionado
                query = """
                    SELECT loteamentos.nome
                    FROM loteamentos
                    INNER JOIN cidades ON loteamentos.cidade_id = cidades.id
                    WHERE cidades.nome = %s
                """
                cidade = text2
                cursor.execute(query, (cidade,))

                # Obtendo os resultados da consulta e converta-os em uma lista de strings
                resultados_loteamentos = [str(row[0]) for row in cursor.fetchall()]

                # Fechando o cursor e a conexão
                cursor.close()
                cnx.close()

                # Atualizando as opções do spinner2
                spinner3.values = resultados_loteamentos
                spinner3.text = 'Loteamentos'

        # Atualizando as opções do spinner4 quando uma opção do spinner3 for selecionada
        def update_spinner4_options(spinner, text3):
            if text3 != 'Loteamentos':
                # Conectando-se ao banco de dados
                cnx = mysql.connector.connect(user=user, password=password,
                                  host=host, database=database, port=port)

                # Criando um cursor para executar consultas
                cursor = cnx.cursor()

                # Executando uma consulta para obter as informações relacionadas ao loteamento selecionado
                query = """
                    SELECT informacoes.nome
                    FROM informacoes
                    INNER JOIN loteamento_informacao ON loteamento_informacao.id_informacao = informacoes.id
                    INNER JOIN loteamentos ON loteamento_informacao.id_loteamento = loteamentos.id
                    WHERE loteamentos.nome = %s
                """
                global loteamento
                loteamento = text3
                cursor.execute(query, (loteamento,))

                # Obtendo os resultados da consulta e converta-os em uma lista de strings
                resultados_infos = [str(row[0]) for row in cursor.fetchall()]

                # Fechando o cursor e a conexão
                cursor.close()
                cnx.close()
                
                # Atualizando as opções do spinner4
                spinner4.values = resultados_infos
                spinner4.text = 'Informações'

        def on_spinner4_select(spinner, resultados_infos):
            # Criando um dicionário para mapear o resultado obtido dos spinners com a tela que será gerada 
            screen_mapping = {
                'água': Screen_Água,
                'ambiental': Screen_Ambiental,
                'art': Screen_ART,
                'asfalto': Screen_Asfalto,
                'cartório': Screen_Cartório,
                'certidão': Screen_Certidão,
                'certificado': Screen_Certificado,
                'cetesb': Screen_CETESB,
                'contrato': Screen_Contrato,
                'cronograma': Screen_Cronograma,
                'declaração': Screen_Declaração,
                'diretriz': Screen_Diretriz,
                'drenagem': Screen_Drenagem,
                'esgoto': Screen_Esgoto,
                'fotos': Screen_Fotos,
                'graprohab': Screen_GRAPROHAB,
                'igc': Screen_IGC,
                'incra': Screen_INCRA,
                'iphan': Screen_IPHAN,
                'jornal': Screen_Jornal,
                'laudo': Screen_Laudo,
                'localização': Screen_Localização,
                'matrículas': Screen_Matrículas,
                'memorial': Screen_Memorial,
                'perfil longitudinal': Screen_Perfil_Longitudinal,
                'perfil transversal': Screen_Perfil_Transversal,
                'planialtimétrico': Screen_Planialtimétrico,
                'prefeitura': Screen_Prefeitura,
                'procuração': Screen_Procuração,
                'protocolos': Screen_Protocolos,
                'requerimentos': Screen_Requerimentos,
                'sinalização': Screen_Sinalização,
            }

            # Verificando se resultados_infos está no mapeamento, senão, usa Screen_Urbanístico
            screen_class = screen_mapping.get(resultados_infos, Screen_Urbanístico)

            resetar_widgets(self)

            # Criando uma tela com base nos resultados obrtidos dos spinners
            new_screen = screen_class(name='screen_' + resultados_infos.capitalize())


            # Adicionando a nova tela ao gerenciador de telas
            self.manager.add_widget(new_screen)

            # Mudando para a nova tela
            self.manager.current = new_screen.name

        # Adicionar um evento aos spinners para chamar a função de atualização quando uma opção for selecionada
        spinner1.bind(text=update_spinner2_options)
        spinner2.bind(text=update_spinner3_options)
        spinner3.bind(text=update_spinner4_options)
        spinner4.bind(text=on_spinner4_select)
    
        def resetar_widgets(self, *args):
            # Redefinir os valores iniciais dos spinners
            spinner1.text = 'Estados'
            spinner2.text = 'Cidades'
            spinner3.text = 'Loteamentos'
            spinner4.text = 'Informações'

class ScreenBase(Screen):
    # Criação das funções e botões das telas
    def __init__(self, id_informacoes, **kwargs):
        super().__init__(**kwargs)
        self.file_chooser = None
        self.id_informacoes = id_informacoes

        # Botão para escolher um arquivo do explorador de arquivos
        open_button = Button(text='Escolher Arquivo', size_hint=(.2, .1), pos_hint={'x':.1, 'y':.6})
        open_button.bind(on_press=lambda x: self.open_file())
        self.add_widget(open_button)

        self.file_chooser = Button(text='Nenhum arquivo selecionado', size_hint=(.8, .1), pos_hint={'x':.1, 'y':.4})
        self.add_widget(self.file_chooser)

        # Botão para salvar o arquivo escolhido no banco de dados
        save_button = Button(text='Salvar no Banco de Dados', size_hint=(.5, .1), pos_hint={'x':.25, 'y':.2})
        save_button.bind(on_press=lambda x: self.save_to_database(self.file_chooser.text, 'pdf'))
        self.add_widget(save_button)

        # Botão para mostrar os arquivos já salvos no banco de dados
        file_list_button = Button(text='Listar arquivos salvos', size_hint=(.5, .1), pos_hint={'x':.25, 'y':.05})
        file_list_button.bind(on_press=lambda x: self.file_list())
        self.add_widget(file_list_button)

    # Função para 
    def open_file(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        self.file_chooser.text = file_path

    # Função para salvar o arquivo no banco de dados
    def save_to_database(self, filepath, file_type):
        global loteamento
        id_informacoes = 33
        if filepath == 'Nenhum arquivo selecionado':
            return

        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        cursor = connection.cursor()

        with open(filepath, 'rb') as file:
            data = file.read()
            filename = filepath.split("/")[-1] # get the filename from the full path
            sql1 = '''SELECT loteamento_informacao.id
            FROM loteamento_informacao 
            Join loteamentos ON loteamento_informacao.id_loteamento = loteamentos.id
            WHERE loteamentos.nome = %s AND id_informacao = %s'''
            cursor.execute(sql1, (loteamento, id_informacoes))

            resultado = cursor.fetchone()
            id_loteamento_informacao = resultado
            valor = id_loteamento_informacao[0]

            # Insira o arquivo na tabela 'arquivos' com o valor recuperado de 'id_loteamento_informacao'
            sql = "INSERT INTO arquivos (id_loteamento_informacao, nome_arquivo, tipo_arquivo, conteudo) VALUES (%s, %s, %s, %s)"

            cursor.execute(sql, (str(valor), filename, file_type, data))

            # Faça o commit da transação
            connection.commit()

        # Feche o cursor e a conexão com o banco de dados
        cursor.close()
        connection.close()
        self.show_popup()
    
    # Função que mostra os arquivos que já estão no banco de dados
    def file_list(self):
        global loteamento
        id_informacoes = 33

        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        cursor = connection.cursor()

        sql1 = '''SELECT loteamento_informacao.id
        FROM loteamento_informacao 
        Join loteamentos ON loteamento_informacao.id_loteamento = loteamentos.id
        WHERE loteamentos.nome = %s AND id_informacao = %s'''
        cursor.execute(sql1, (loteamento, id_informacoes))

        resultado = cursor.fetchone()
        id_loteamento_informacao = resultado
        valor = id_loteamento_informacao[0]

        cursor.close()
        connection.close()

        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        cursor = connection.cursor()
        sql = '''SELECT nome_arquivo FROM arquivos WHERE id_loteamento_informacao = %s'''
        cursor.execute(sql, ((valor,)))
        results = cursor.fetchall()
        connection.close()

        popup_content = BoxLayout(orientation='vertical')
        for result in results:
            filename = result[0]
            button = Button(text=filename, size_hint_y=None, height=40)
            button.bind(on_press=lambda x: self.open_pdf(filename))
            popup_content.add_widget(button)

        popup = Popup(title='Lista de arquivos', content=popup_content, size_hint=(None, None), size=(400, 400))
        popup.open()

    # Função para abrir o arquivo .pdf do banco de dados
    def open_pdf(self, filename):
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        cursor = connection.cursor()
        cursor.execute("SELECT conteudo FROM arquivos WHERE nome_arquivo = %s", (filename,))
        file_content = cursor.fetchone()[0]
        connection.close()

        file_path = 'temp.pdf'
        with open(file_path, 'wb') as file:
            file.write(file_content)
        os.startfile(file_path)

    # Função que cria um popup para melhor visualização dos arquivos salvos no banco de dados
    def show_popup(self):
        content = Label(text="Salvo com sucesso!")
        popup = Popup(title="Sucesso", content=content, size_hint=(None, None), size=(200, 200))
        popup.open()

# Criação das telas utilizando o conceito de herança

class Screen_Água(ScreenBase):
    def __init__(self, **kwargs):
        super().__init__(id_informacoes=1, **kwargs)

class Screen_Ambiental(ScreenBase):
    def __init__(self, **kwargs):
        super().__init__(id_informacoes=2, **kwargs)

class Screen_ART(ScreenBase):
    def __init__(self, **kwargs):
        super().__init__(id_informacoes=3, **kwargs)

class Screen_Asfalto(ScreenBase):
    def __init__(self, **kwargs):
        super().__init__(id_informacoes=4, **kwargs)

class Screen_Cartório(ScreenBase):
    def __init__(self, **kwargs):
        super().__init__(id_informacoes=5, **kwargs)

class Screen_Certidão(ScreenBase):
    def __init__(self, **kwargs):
        super().__init__(id_informacoes=6, **kwargs)

class Screen_Certificado(ScreenBase):
    def __init__(self, **kwargs):
        super().__init__(id_informacoes=7, **kwargs)

class Screen_CETESB(ScreenBase):
    def __init__(self, **kwargs):
        super().__init__(id_informacoes=8, **kwargs)

class Screen_Contrato(ScreenBase):
    def __init__(self, **kwargs):
        super().__init__(id_informacoes=9, **kwargs)

class Screen_Cronograma(ScreenBase):
    def __init__(self, **kwargs):
        super().__init__(id_informacoes=10, **kwargs)

class Screen_Declaração(ScreenBase):
    def __init__(self, **kwargs):
        super().__init__(id_informacoes=11, **kwargs)

class Screen_Diretriz(ScreenBase):
    def __init__(self, **kwargs):
        super().__init__(id_informacoes=12, **kwargs)

class Screen_Drenagem(ScreenBase):
    def __init__(self, **kwargs):
        super().__init__(id_informacoes=13, **kwargs)

class Screen_Esgoto(ScreenBase):
    def __init__(self, **kwargs):
        super().__init__(id_informacoes=14, **kwargs)

class Screen_Fotos(ScreenBase):
    def __init__(self, **kwargs):
        super().__init__(id_informacoes=15, **kwargs)

class Screen_GRAPROHAB(ScreenBase):
    def __init__(self, **kwargs):
        super().__init__(id_informacoes=16, **kwargs)

class Screen_IGC(ScreenBase):
    def __init__(self, **kwargs):
        super().__init__(id_informacoes=17, **kwargs)

class Screen_INCRA(ScreenBase):
    def __init__(self, **kwargs):
        super().__init__(id_informacoes=18, **kwargs)

class Screen_IPHAN(ScreenBase):
    def __init__(self, **kwargs):
        super().__init__(id_informacoes=19, **kwargs)

class Screen_Jornal(ScreenBase):
    def __init__(self, **kwargs):
        super().__init__(id_informacoes=20, **kwargs)

class Screen_Laudo(ScreenBase):
    def __init__(self, **kwargs):
        super().__init__(id_informacoes=21, **kwargs)

class Screen_Localização(ScreenBase):
    def __init__(self, **kwargs):
        super().__init__(id_informacoes=22, **kwargs)

class Screen_Matrículas(ScreenBase):
    def __init__(self, **kwargs):
        super().__init__(id_informacoes=23, **kwargs)

class Screen_Memorial(ScreenBase):
    def __init__(self, **kwargs):
        super().__init__(id_informacoes=24, **kwargs)

class Screen_Perfil_Longitudinal(ScreenBase):
    def __init__(self, **kwargs):
        super().__init__(id_informacoes=25, **kwargs)

class Screen_Perfil_Transversal(ScreenBase):
    def __init__(self, **kwargs):
        super().__init__(id_informacoes=26, **kwargs)

class Screen_Planialtimétrico(ScreenBase):
    def __init__(self, **kwargs):
        super().__init__(id_informacoes=27, **kwargs)

class Screen_Prefeitura(ScreenBase):
    def __init__(self, **kwargs):
        super().__init__(id_informacoes=28, **kwargs)

class Screen_Procuração(ScreenBase):
    def __init__(self, **kwargs):
        super().__init__(id_informacoes=29, **kwargs)

class Screen_Protocolos(ScreenBase):
    def __init__(self, **kwargs):
        super().__init__(id_informacoes=30, **kwargs)

class Screen_Requerimentos(ScreenBase):
    def __init__(self, **kwargs):
        super().__init__(id_informacoes=31, **kwargs)

class Screen_Sinalização(ScreenBase):
    def __init__(self, **kwargs):
        super().__init__(id_informacoes=32, **kwargs) 

class Screen_Urbanístico(ScreenBase):
    def __init__(self, **kwargs):
        super().__init__(id_informacoes=33, **kwargs)

class Banco_de_dados_Villa(App):
    def build(self):
        # Criando o gerenciador de telas
        screen_manager = ScreenManager()

        # Adicionando as telas ao gerenciador de telas
        config_screen = SecondScreen(name='config')
        screens = {
            'Água': Screen_Água,
            'Ambiental': Screen_Ambiental,
            'ART': Screen_ART,
            'Asfalto': Screen_Asfalto,
            'Cartório': Screen_Cartório,
            'Certidão': Screen_Certidão,
            'Certificado': Screen_Certificado,
            'CETESB': Screen_CETESB,
            'Contrato': Screen_Contrato,
            'Cronograma': Screen_Cronograma,
            'Declaração': Screen_Declaração,
            'Diretriz': Screen_Diretriz,
            'Drenagem': Screen_Drenagem,
            'Esgoto': Screen_Esgoto,
            'Fotos': Screen_Fotos,
            'GRAPROHAB': Screen_GRAPROHAB,
            'IGC': Screen_IGC,
            'INCRA': Screen_INCRA,
            'IPHAN': Screen_IPHAN,
            'Jornal': Screen_Jornal,
            'Laudo': Screen_Laudo,
            'Localização': Screen_Localização,
            'Matrículas': Screen_Matrículas,
            'Memorial': Screen_Memorial,
            'Perfil_Longitudinal': Screen_Perfil_Longitudinal,
            'Perfil_Transversal': Screen_Perfil_Transversal,
            'Planialtimétrico': Screen_Planialtimétrico,
            'Prefeitura': Screen_Prefeitura,
            'Procuração': Screen_Procuração,
            'Protocolos': Screen_Protocolos,
            'Requerimentos': Screen_Requerimentos,
            'Sinalização': Screen_Sinalização,
            'Urbanístico': Screen_Urbanístico
        }

        # Adicionando as telas ao gerenciador de telas
        screen_manager.add_widget(config_screen)
        for screen_name, screen_class in screens.items():
            screen_instance = screen_class(name=f'screen_{screen_name}')
            screen_manager.add_widget(screen_instance)

        return screen_manager

if __name__ == '__main__':
    Banco_de_dados_Villa().run()