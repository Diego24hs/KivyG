from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFillRoundFlatButton, MDRectangleFlatIconButton, MDIconButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.graphics import Line
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget

class MyTextInput(MDTextField):
    def __init__(self, next_widget=None, **kwargs):
        super().__init__(**kwargs)
        self.next_widget = next_widget
        self.bind(on_text_validate=self.on_enter)

    def on_enter(self, *args):
        if self.next_widget:
            self.next_widget.focus = True

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.spacing = 10
        self.padding = 10
        self.total = 0.0

        layout = MDBoxLayout(orientation='vertical', spacing=15)

        hex_color = "#191970"           
        # Cria a barra de ferramentas e adiciona ao layout
        self.toolbar = MDTopAppBar(title="Gasto Certo")
        self.toolbar.md_bg_color = hex_color
        self.toolbar.specific_text_color = (1, 1, 1, 1) 
        
        # Cria o navigation drawer e adiciona à tela
        nav_drawer = MDNavigationDrawer()
        
        # Define a cor de fundo do navigation drawer como transparente
        nav_drawer.md_bg_color = (1, 1, 1, 0)
        
        # Cria um botão para alternar o tema e adiciona ao navigation drawer
        self.theme_toggle_button = MDRectangleFlatIconButton(text="Alternar Tema",
                                                             icon="theme-light-dark", 
                                                             on_release=self.toggle_theme)
        self.theme_toggle_button.md_bg_color = (0, 0, 0, 1)
        self.theme_toggle_button.icon_color = (1, 1, 1, 1)
        self.theme_toggle_button.text_color = (1, 1, 1, 1)
        nav_drawer.add_widget(self.theme_toggle_button)
        
        self.add_widget(nav_drawer)
        
        # Define os itens de ação à esquerda da barra de ferramentas para abrir/fechar o navigation drawer quando pressionado
        self.toolbar.left_action_items = [["menu", lambda x: nav_drawer.set_state("toggle")]]
        
        layout.add_widget(self.toolbar)            


        self.limit_input = MyTextInput(multiline=False, hint_text='Limite de gastos')
        layout.add_widget(self.limit_input)

        self.product_name_input = MyTextInput(multiline=False, hint_text='Nome do produto')
        layout.add_widget(self.product_name_input)

        self.product_value_input = MyTextInput(multiline=False, hint_text='Valor do produto')
        layout.add_widget(self.product_value_input)

        self.product_quantity_input = MyTextInput(multiline=False, hint_text='Quantidade')
        layout.add_widget(self.product_quantity_input)

       
      # Definindo os atributos next_widget depois que todos os campos de entrada tiverem sido preenchidos
        self.product_name_input.next_widget = self.product_value_input
        self.product_value_input.next_widget = self.product_quantity_input
        
        hex_color = "#6A5ACD"
        add_product_button = MDRectangleFlatIconButton(text='Adicionar produto',
        icon='cart', 
        icon_color=(1,1,1,1), 
        md_bg_color= hex_color, 
        text_color=(1,1,1,1), 
        pos_hint={'center_x': .5, 'y': .5}, 
        size_hint_x=None, 
        size_hint_y=None, 
        height=50, 
        width=200, 
        halign='center')
        
        add_product_button.bind(on_press=self.add_product)
        layout.add_widget(add_product_button)
        
        hex_color = "#6A5ACD"
        view_products_button = MDRectangleFlatIconButton(text='Visualizar produtos',
        icon='eye',
        icon_color=(1,1,1,1),
        md_bg_color=hex_color , 
        text_color=(1,1,1,1),
        pos_hint={'center_x': .5, 'y': .4}, 
        size_hint_x=None, 
        size_hint_y=None, 
        height=50, 
        width=200, 
        halign='center')
        
        view_products_button.bind(on_press=self.view_products)
        layout.add_widget(view_products_button)
        
        hex_color = "#6A5ACD"
        finish_purchase_button = MDRectangleFlatIconButton(text='Finalizar compra',
        icon='thumb-up',
        icon_color=(1,1,1,1), 
        md_bg_color=hex_color, 
        text_color=(1,1,1,1), 
        pos_hint={'center_x': .5, 'y': .3}, 
        size_hint_x=None, 
        size_hint_y=None, 
        height=50, 
        width=200, 
        halign='center')        
        
        finish_purchase_button.bind(on_press=self.finish_purchase)
        layout.add_widget(finish_purchase_button)
        
                
        self.total_label = MDLabel(text='Valor total: R$0.00', 
        pos_hint={'center_x': .5, 'y': 0.1},  
        height=50, width=200, 
        halign='center')
        
        layout.add_widget(self.total_label)
        
        self.products = []
        
        self.add_widget(layout)
        
        
        
    def toggle_theme(self, *args):
        app = MDApp.get_running_app()
        if app.theme_cls.theme_style == "Light":
            app.theme_cls.theme_style = "Dark"
            self.theme_toggle_button.md_bg_color = (1, 1, 1, 1)
            self.theme_toggle_button.text_color = (0, 0, 0, 1)
            self.theme_toggle_button.icon_color = (0, 0, 0, 1)
           
        else:
            app.theme_cls.theme_style = "Light"
            self.theme_toggle_button.md_bg_color = (0, 0, 0, 1)
            self.theme_toggle_button.text_color = (1, 1, 1, 1)
            self.theme_toggle_button.icon_color = (1, 1, 1, 1)
      
    def add_product(self, instance):
        if not all([self.product_name_input.text, self.product_value_input.text, self.product_quantity_input.text]):
            dialog = MDDialog(title='Atenção', text='Por favor, preencha todos os campos antes de adicionar um produto.')
            dialog.open()
            return

        try:
            float(self.product_value_input.text.replace(',', '.'))
            value_is_valid = True
        except ValueError:
            value_is_valid = False

        if not (value_is_valid and self.product_quantity_input.text.isdigit()):
            dialog = MDDialog(title='Atenção', text='Por favor, insira apenas números nos campos de valor e quantidade.')
            dialog.open()
            return

        product_name = self.product_name_input.text
        product_value = float(self.product_value_input.text.replace(',', '.'))
        product_quantity = int(self.product_quantity_input.text)

        self.products.append({
            'name': product_name,
            'value': product_value,
            'quantity': product_quantity
        })
    
        total_value = sum([product['value'] * product['quantity'] for product in self.products])
    
        self.product_name_input.text = ''
        self.product_value_input.text = ''
        self.product_quantity_input.text = ''
        
        if self.limit_input.text:
            limit_value = float(self.limit_input.text)
            if total_value > limit_value:
                dialog = MDDialog(title='Atenção', text=f'O valor total ultrapassou o limite de R${limit_value:.2f}')
                dialog.open()
        
        self.total_label.text = f'Valor total: R${total_value:.2f}'
        
    def view_products(self, instance):
        self.manager.current = 'products'
            
    def finish_purchase(self, instance):
        total_value = sum([product['value'] * product['quantity'] for product in self.products])
        dialog = MDDialog(title='Compra finalizada', text=f'Valor total da compra: R${total_value:.2f}')
        dialog.open()
        self.products = []
        self.total_label.text = 'Valor total: R$0.00'
    
    def open_menu(self):
        self.menu.open()       
      
class ProductsScreen(Screen):
    def __init__(self, **kwargs):
        super(ProductsScreen, self).__init__(**kwargs)    
    
    def on_pre_enter(self):
        layout = GridLayout(cols=1, size_hint_y=None, spacing=30, padding=[20, 20])  # Adiciona espaçamento entre os itens e nas laterais
        layout.bind(minimum_height=layout.setter('height'))
        
        scrollview = ScrollView(bar_width=10, bar_color=(1, 1, 1, 0)) # a barra preta de scroll
        scrollview.add_widget(layout)
        
        # espaco do topo da janela
        spacer = Widget(size_hint_y=None, height=20)
        layout.add_widget(spacer)       
        
        for product in self.manager.get_screen('main').products: # a lista dos produtos e o botao de exclusao
            product_layout = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            total_value = product['value'] * product['quantity']
            label = MDLabel(text=f"{product['name']} - R${product['value']:.2f} x {product['quantity']} = R${total_value:.2f}")
            product_layout.add_widget(label)          
            delete_button = MDIconButton(icon='delete', pos_hint={"center_y": 0.5}, theme_text_color='Custom', text_color=(1, 0, 0, 1))
            delete_button.bind(on_press=lambda instance, product=product: self.delete_product(instance, product))
            product_layout.add_widget(delete_button)
            layout.add_widget(product_layout)           
            
            with layout.canvas: # linha para organização dos itens
                Line(points=[layout.x, layout.y + layout.height - 1, layout.x + layout.width, layout.y + layout.height - 1])
        spacer = Widget(size_hint_y=None, height=20)
        layout.add_widget(spacer)      
        
        hex_color = "#191970" 
        back_button = MDFillRoundFlatButton (text='Voltar',
                                            theme_text_color='Custom',
                                            text_color=(1, 1, 1, 1),
                                             md_bg_color=hex_color) # botão de voltar        
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)        
        self.add_widget(scrollview)    
    
    def on_leave(self):
        self.clear_widgets()    
    
    def delete_product(self, instance, product):
        main_screen = self.manager.get_screen('main')
        main_screen.products.remove(product)
        total_value = sum([product['value'] * product['quantity'] for product in main_screen.products])
        main_screen.total_label.text = f'Valor total: R${total_value:.2f}'    
        if not main_screen.products:
            dialog = MDDialog(title="Não a Produtos", text="A sua Lista de Produtos está Vazia.")
            dialog.open()    
        self.clear_widgets()
        self.on_pre_enter()     
    
    def go_back(self, instance):
        self.manager.current = 'main'
        
class Gasto_CertoApp(MDApp):
    def build(self):
        screen_manager = ScreenManager()
        
        main_screen = MainScreen(name='main')
        screen_manager.add_widget(main_screen)
        
        products_screen = ProductsScreen(name='products')
        screen_manager.add_widget(products_screen)
        
        return screen_manager
        
Gasto_CertoApp().run()