from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.uix.image import Image
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDToolbar

class ConversorApp(MDApp):
    # Mudar base de E/S de dados do conversor
    def flip(self):
        if self.state == 0:
            self.state = 1
            self.toolbar.title = 'Decimal para binário'
            self.entrada.hint_text = 'Digite um número decimal'
            self.entrada.text = ''
            self.saida.text = ''
            self.texto.text = ''
        else:
            self.state = 0
            self.toolbar.title = 'Binário para decimal'
            self.entrada.hint_text = 'Digite um número binário'
            self.entrada.text = ''
            self.saida.text = ''
            self.texto.text = ''
    
    #---------------------------------------------------------

    # Converter (gerar saída)
    def converter(self, argumentos):
        # Substituir ',' na entrada do usuário por '.' (impedir ValueError)
        if ',' in self.entrada.text:
            self.entrada.text = self.entrada.text.replace(',', '.')
        try:
            if '.' not in self.entrada.text:
                # Conversor binário para decimal
                if self.state == 0:
                    resultado = int(self.entrada.text, 2)
                    self.saida.text = str(resultado)
                    self.texto.text = 'Em decimal é:'
                else:
                    # Conversor decimal para binário
                    resultado = bin(int(self.entrada.text))[2:]
                    self.saida.text = resultado
                    self.texto.text = 'Em binário é:'
            else:
                # Conversor números fracionários
                inteiro, fracionario = self.entrada.text.split('.')

                # Binário (fracionário) para decimal
                if self.state == 0:
                    inteiro = int(inteiro, 2)
                    x = 0
                    for indice, digito in enumerate(fracionario):
                        x += int(digito)*2**(-(indice + 1))
                    self.texto.text = 'Em decimal é:'
                    self.saida.text = str(inteiro + x)
                
                # Decimal (fracionário) para binário
                else:
                    casas_decimais = 10
                    inteiro = bin(int(inteiro))[2:]
                    fracionario = float('0.' + fracionario)
                    x = []
                    for i in range(casas_decimais):
                        if fracionario * 2 < 1:
                            x.append('0')
                            fracionario *= 2
                        elif fracionario * 2 > 1:
                            x.append('1')
                            fracionario = fracionario * 2 - 1
                        elif fracionario * 2 == 1.0:
                            x.append('1')
                            break
                    self.texto.text = 'Em binário é:'
                    self.saida.text = inteiro + '.' + ''.join(x)
        except ValueError:
            self.saida.text = ''
            if self.state == 0:
                self.texto.text = 'Por favor, digite um número binário válido!'
            else:
                self.texto.text = 'Por favor, digite um número decimal válido!'

    #---------------------------------------------------------

    # Construtor da tela
    def build(self):
        self.theme_cls.primary_palette = 'BlueGray'
        tela = MDScreen()
        # Estado inicial da tela (binário para decimal)
        self.state = 0
        
        # Barra de Ferramentas (título do app; ícone flip())
        self.toolbar = MDToolbar(title='Binário para decimal')
        self.toolbar.pos_hint = {'top': 1}
        self.toolbar.right_action_items = [
            ['rotate-3d-variant', lambda x: self.flip()]
        ]
        tela.add_widget(self.toolbar)

    #---------------------------------------------------------

        # Logo APP
        tela.add_widget(Image(
            source='logo.png',
            pos_hint = {'center_x': 0.5, 'center_y': 0.7}
        ))

    #---------------------------------------------------------

        # Entrada do usuário
        self.entrada = MDTextField(
            hint_text='Digite um número binário',
            halign='center',
            size_hint = (0.8, 1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.45},
            font_size = 22
        )
        tela.add_widget(self.entrada)

    #---------------------------------------------------------

        # Texto de saída (label 1)
        self.texto = MDLabel(
            halign='center',
            pos_hint = {'center_x': 0.5, 'center_y': 0.35},
            theme_text_color = 'Secondary'
        )
        tela.add_widget(self.texto)

        # Texto de saída (label 2)
        self.saida = MDLabel(
            halign='center',
            pos_hint = {'center_x': 0.5, 'center_y': 0.3},
            theme_text_color = 'Primary',
            font_style = 'H5'
        )
        tela.add_widget(self.saida)

    #---------------------------------------------------------

        # Botão de converter
        tela.add_widget(MDFillRoundFlatButton(
            text = 'CONVERTER',
            font_size = 17,
            pos_hint = {'center_x': 0.5, 'center_y': 0.15},
            on_press = self.converter
        ))
        
    #---------------------------------------------------------

        # Abrir tela
        return tela

# Rodar App
if __name__ == '__main__':
    ConversorApp().run()