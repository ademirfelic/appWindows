from kivy.app import App
from kivy.lang import Builder
from botoes import *
from bannerColeta import *
import requests

class MyApp(App):

    loja = 'Matriz'

    def build(self):

        return Builder.load_file('main.kv')


    def listar_coletas(self):
        self.excluir_listagem()
        link = f'https://appbalanco-27229-default-rtdb.firebaseio.com/{self.loja}/.json?leitura=1'
        requisicao_dic = requests.get(link).json()
        for dados in requisicao_dic:
            nome = requisicao_dic[dados]['nome'].upper()
            for coletas in requisicao_dic[dados]['coletas']:
                leitura = int(requisicao_dic[dados]['coletas'][coletas]['leitura'])
                if leitura == 0:
                    qnt = len(requisicao_dic[dados]['coletas'][coletas]['coleta'].split(','))
                    self.root.ids['lista_coleta'].add_widget(BannerColeta(codigo = coletas, nome = nome, quantidade = qnt))


    def baixar_coleta(self, codigo, *args):
        link = f'https://appbalanco-27229-default-rtdb.firebaseio.com/{self.loja}/.json'
        requisicao_dic = requests.get(link).json()
        texto = ''
        for dados in requisicao_dic:
            for coletas in requisicao_dic[dados]['coletas']:
                if coletas == codigo:
                    coleta = requisicao_dic[dados]['coletas'][coletas]['coleta'].split(',')
                    for cod in coleta:
                        texto += f'{cod[1:]}                       1\n'

                    with open('../../coleta.txt', 'w') as arquivo:
                        arquivo.write(texto)
                    info = '{"leitura": "1"}'
                    requests.patch(f'https://appbalanco-27229-default-rtdb.firebaseio.com/{self.loja}/{dados}/coletas/{coletas}.json',data = info)
                    self.listar_coletas()



    def excluir_listagem(self):
        for item in list(self.root.ids['lista_coleta'].children):
            self.root.ids['lista_coleta'].remove_widget(item)



MyApp().run()