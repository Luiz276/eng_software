from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter.messagebox import askyesno
from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor
from mesa import Mesa
import os
from PIL import Image,ImageTk

class PlayerInterface(DogPlayerInterface):
    def __init__(self):
        self.main_window = Tk()
        self.fill_main_window()
        
        self.mesa = Mesa()
        self.game_state = 1
        self.update_gui(self.game_state)

        player_name = simpledialog.askstring(title='Player Indentification', prompt="Qual o seu nome?")
        self.dog_server_interface = DogActor()
        message = self.dog_server_interface.initialize(player_name, self)
        messagebox.showinfo(message=message)
        
        self.main_window.mainloop()
        
    def fill_main_window(self):
        self.main_window.title("Pife")              #titulo da janela
        self.main_window.geometry("1280x920")       #dimensão da janela
        self.main_window.resizable(False, False)    #Define se é possivel reajustar dimensões da janela
        self.main_window["bg"] = "darkgreen"            #cor da janela
        
        # Criação de 2 frames e organização da janela em um grid de 2 linhas e 1 coluna,
        # sendo que table_frame ocupa a linha superior e message_frame, a inferior
        self.table_frame = Frame(self.main_window, padx=100, pady=25, bg="darkgreen")
        self.table_frame.grid(row=0,column=0)

        # Frame que contém o botão de descarte
        self.message_frame = Frame(self.main_window, padx=0, pady=10, bg="darkgreen")
        self.message_frame.grid(row=1 , column=0)
        btn = Button(self.message_frame, text="Descartar", command=self.descartar)
        btn.pack(side='right')
        
        self.pasta = os.path.dirname(__file__)
        
        self.an_image = PhotoImage(file=self.pasta+"/images/yellow_square.png")
        self.bg_image = PhotoImage(file=self.pasta+"/images/background_square.png")
            
        self.board_view = []
        for y in range(9):
            a_column = []
            for x in range(7):
                if (((x == 4 or x == 0) and ((y % 3) == 1)) or ((x == 2) and (y == 3 or y == 5)) or (x == 6)):
                    aLabel = Label(self.table_frame, bd=0, image=self.an_image)
                    aLabel.bind("<Button-1>", lambda event, a_line=x, a_column=y: self.click(event, a_line, a_column))
                else:
                    aLabel = Label(self.table_frame, bd=0, image=self.bg_image)
                aLabel.grid(row=x, column=y)
                a_column.append(aLabel)
            self.board_view.append(a_column)
            
        # Criação de um menu para o programa
        # Criar a barra de menu (menubar) e adicionar à janela:
        self.menubar = Menu(self.main_window)
        self.menubar.option_add('*tearOff', FALSE)
        self.main_window['menu'] = self.menubar
        # Adicionar menu(s) à barra de menu:
        self.menu_file = Menu(self.menubar)
        self.menubar.add_cascade(menu=self.menu_file, label='File')
        # Adicionar itens de menu a cada menu adicionado à barra de menu:
        self.menu_file.add_command(label='start_match', command=self.start_match)
        self.menu_file.add_command(label='start_game', command=self.start_match)
        
    def click(self, event, line, column):
        print('CLICK', line, column)
        
    def start_match(self):
        print('start_match')
        match_status = self.mesa.getStatus()
        if match_status==1 or match_status==0:
            answer = askyesno('START', 'Deseja iniciar uma nova partida?')
            if answer:
                start_status = self.dog_server_interface.start_match(2)
                code = start_status.get_code()
                message = start_status.get_message()
                if code=="0" or code=="1":
                    messagebox.showinfo(message)
                else: #if code==2:
                    players = start_status.get_players()
                    local_player_id = start_status.get_local_id()
                    print("ELSE")
                    self.mesa.start_match(players, local_player_id)

                    game_state = self.mesa.getStatus()
                    self.update_gui(game_state)
        print("PARTIDA INICIADA")
        
    # def start_game(self):
    #     print('start_game')
        
    def receive_start(self, start_status):
        message = start_status.get_message()

        # -------------
        # Nosso jogo não possui reset
        # -------------
        # self.start_game()  #    use case reset game

        players = start_status.get_players()
        local_player_id = start_status.get_local_id()
        self.mesa.start_match(players, local_player_id)
        game_state = self.mesa.getStatus()
        self.update_gui(game_state)
        messagebox.showinfo(message=message)
    
    def descartar(self):
        print("Descartar")
    
    def getStatus(self):
        return self.game_state
    
    def update_gui(self, game_state: int):
        # Loop por trincas de cada jogador e pela mão do jogador local
        # Assim como por baralho e descarte
        naipes_eng = {
            'ouros': 'diamonds',
            'paus' : 'clubs',
            'espadas' : 'spades',
            'copas' : 'hearts'
        }
        numeros = {
            'A' : 'ace',
            '2' : '2',
            '3' : '3',
            '4' : '4',
            '5' : '5',
            '6' : '6',
            '7' : '7',
            '8' : '8',
            '9' : '9',
            '10' : '10',
            'J' : 'jack',
            'Q' : 'queen',
            'K' : 'king'
        }
        cartas_locais = self.mesa.local_player.getCartas()
        self.image = []
        for i in range(9):
            if i < len(cartas_locais):
                location = self.pasta+"/images/"+f"{numeros[cartas_locais[i].getNum()]}"+"_of_"+f"{naipes_eng[cartas_locais[i].getNaipe()]}"+".png"
                img = ImageTk.PhotoImage(Image.open(location).resize((117,117)))
            else:
                #location = self.an_image
                img = self.an_image
            #img.resize()
            self.board_view[i][6].configure(image=img)
            self.image.append(img)
            #self.main_window.update_idletasks()
            #self.board_view[i][6].update()
