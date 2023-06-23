from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter.messagebox import askyesno
from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor
from mesa import Mesa
import os
from PIL import Image,ImageTk
import jsons
from baralho import Baralho

class PlayerInterface(DogPlayerInterface):
    def __init__(self):
        self.main_window = Tk()
        self.fill_main_window()
        
        self.mesa = Mesa()
        self.nova_trinca = []
        self.game_state = 1
        self.update_gui(self.game_state)
        self.a_move = {
            "trincas_baixadas" : [],
            "carta_descarte" : None,
            "comprou_baralho" : None,
            "baralho" : None,
            "match_status" : None
        }
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
        btn2 = Button(self.message_frame, text="Baixar Trinca", command=self.baixar)
        btn2.pack(side='right')
        self.turn_label = Label(self.message_frame, bd=0, text='AGUARDANDO INÍCIO')
        self.turn_label.pack(side='left')
        
        self.pasta = os.path.dirname(__file__)
        
        self.an_image = PhotoImage(file=self.pasta+"/images/yellow_square.png")
        self.bg_image = PhotoImage(file=self.pasta+"/images/background_square.png")
            
        self.board_view = []
        for y in range(10):
            a_column = []
            for x in range(7):
                if (((x == 4 or x == 0) and (y <9)) or ((x == 2) and (y == 3 or y == 5)) or (x == 6)):
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
        self.menu_file.add_command(label='start_match', command=self.start_match_and_send)
        #self.menu_file.add_command(label='start_game', command=self.start_match_and_send)
        
    def click(self, event, line, column):
        print('CLICK', line, column)
        if line == 2 and self.getStatus() == 2:
            print("compra")
            if column == 5:
                self.a_move["comprou_baralho"] = False
                self.mesa.comprou_baralho(self.mesa.local_player, False)
            elif column ==3:
                self.a_move["comprou_baralho"] = True
                self.mesa.comprou_baralho(self.mesa.local_player, True)
                print('baralho')
            self.game_state = 3
        elif line == 6:
            if self.getStatus() == 5:
                print('descarte')
                card = self.mesa.local_player.cartas[column]
                self.mesa.descartar_carta(self.mesa.local_player, card)
                self.a_move["carta_descarte"] = jsons.dump(card)
                self.game_state = 6
                self.nova_trinca = []
                self.dog_server_interface.send_move(self.a_move)
                #self.a_move["trincas_baixadas"] = []
                self.mesa.swap_turn()
            if self.getStatus() == 4:
                print('card baixar')
                self.nova_trinca.append(self.mesa.local_player.cartas[column])
                if len(self.nova_trinca) >= 3:
                    print('trinca')
                    valido = self.mesa.baixar_trinca(self.mesa.local_player, self.nova_trinca)
                    if valido:
                        print("trinca valida")
                        self.a_move["trincas_baixadas"].append(jsons.dump(self.nova_trinca))
                    self.nova_trinca = []
                    if self.mesa.getStatus() == 4:
                        self.end_game()
                    else:
                        self.game_state = 3
                #self.game_state = 4
        print(self.game_state)
        status = self.mesa.getStatus()
        self.update_gui(status)
    
    def end_game(self):
        self.game_state = 7
        self.update_gui(self.mesa.getStatus())
        self.a_move['match_status'] = 'end'
        self.dog_server_interface.send_move(self.a_move)
        messagebox.showinfo("FIM DE JOGO", "VOCÊ GANHOU")
        self.main_window.destroy()
        pass

    def start_match_and_send(self):
        if self.game_state == 1:
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
                        self.mesa.baralho = Baralho()

                        c_local = self.mesa.baralho.distribuir_cartas()
                        self.mesa.local_player.setCartas(c_local)
                        c_local_json = []
                        for carta in c_local:
                            c_local_json.append(jsons.dump(carta))
                        self.a_move['j1_mao'] = (c_local_json)
                        
                        c_remoto = self.mesa.baralho.distribuir_cartas()
                        self.mesa.remote_player.setCartas(c_remoto)
                        c_remoto_json = []
                        for carta in c_remoto:
                            c_remoto_json.append(jsons.dump(carta))
                        self.a_move['j2_mao'] = (c_remoto_json)
                        
                        self.mesa.start_match(players, local_player_id)
                        if self.mesa.getStatus() == 2:
                            self.game_state = 2
                            self.turn_label.configure(text='   SUA VEZ  ')
                            self.turn_label.pack(side='left')
                        elif self.mesa.getStatus() == 3:
                            self.game_state = 6
                            self.turn_label.configure(text='VEZ OPONENTE')
                            self.turn_label.pack(side='left')

            game_state = self.mesa.getStatus()
            self.update_gui(game_state)
            print("PARTIDA INICIADA")
            print("self.game_state = ", self.game_state)
            if game_state == 2 or game_state == 3:
                print("send")
                self.a_move['baralho'] = jsons.dump(self.mesa.baralho.getCartas())
                self.a_move['match_status'] = 'next'
                self.dog_server_interface.send_move(self.a_move)
            print("end")

    def start_match(self):
        if self.game_state == 1:
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
                        self.mesa.start_match(players, local_player_id)
                        if self.mesa.getStatus() == 2:
                            self.game_state = 2
                            self.turn_label.configure(text='   SUA VEZ  ')
                            self.turn_label.pack(side='left')
                        elif self.mesa.getStatus() == 3:
                            self.game_state = 6
                            self.turn_label.configure(text='VEZ OPONENTE')
                            self.turn_label.pack(side='left')

            status = self.mesa.getStatus()
            self.update_gui(status)
            print("PARTIDA INICIADA")
            print("self.game_state = ", self.game_state)
        
    def receive_start(self, start_status):
        #if self.getStatus() == 1:
            print("receive_start")
            message = start_status.get_message()

            # -------------
            # Nosso jogo não possui reset
            # -------------
            # self.start_game()  #    use case reset game

            players = start_status.get_players()
            print(players)
            local_player_id = start_status.get_local_id()
            self.mesa.start_match(players, local_player_id)
            status = self.mesa.getStatus()
            if self.mesa.getStatus() == 2:
                self.game_state = 2
                self.turn_label.configure(text='   SUA VEZ  ')
                self.turn_label.pack(side='left')
            elif self.mesa.getStatus() == 3:
                self.game_state = 6
                self.turn_label.configure(text='VEZ OPONENTE')
                self.turn_label.pack(side='left')
            self.update_gui(status)
            messagebox.showinfo(message=message)
    
    def receive_move(self, a_move):
        #return super().receive_move(a_move)
        print("receber")
        self.mesa.receive_move(a_move)
        self.game_state = 2
        match_state = self.mesa.getStatus()
        if match_state == 4:
            self.end_game()
        self.update_gui(match_state)
        self.a_move["trincas_baixadas"] = []

    def descartar(self):
        if self.game_state == 3 or self.game_state == 4:
            self.game_state = 5
            print("Descartar")
        status = self.mesa.getStatus()
        self.update_gui(status)

    def baixar(self):
        if self.game_state == 3 or self.game_state == 5:
            self.game_state = 4
            self.nova_trinca = []
            print("Baixar")
        status = self.mesa.getStatus()
        self.update_gui(status)
    
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
            '1' : 'ace',
            '2' : '2',
            '3' : '3',
            '4' : '4',
            '5' : '5',
            '6' : '6',
            '7' : '7',
            '8' : '8',
            '9' : '9',
            '10' : '10',
            '11' : 'jack',
            '12' : 'queen',
            '13' : 'king'
        }
        cartas_locais = self.mesa.local_player.getCartas()
        #print(cartas_locais)
        self.image = set()
        # loop das cartas do jogador local:
        for i in range(10):
            if i < len(cartas_locais):
                location = self.pasta+"/images/"+f"{numeros[str(cartas_locais[i].getNum())]}"+"_of_"+f"{naipes_eng[cartas_locais[i].getNaipe()]}"+".png"
                img = ImageTk.PhotoImage(Image.open(location).resize((117,117)))
            else:
                #location = self.an_image
                img = self.an_image
            #img.resize()
            self.board_view[i][6].configure(image=img)
            self.image.add(img)
            #self.main_window.update_idletasks()
            #self.board_view[i][6].update()
        # baralho
        #if game_state == 1 or (len(self.mesa.baralho.getCartas()) > 0 and self.mesa.baralho != None):
        location = self.pasta+"/images/"+"card_back"+".png"
        img = ImageTk.PhotoImage(Image.open(location).resize((117,117)))
        self.board_view[3][2].configure(image=img)
        self.image.add(img)

        if game_state != 1 and self.mesa != None:
            # descarte
            top = self.mesa.descarte.peek_top()
            if top:
                location = self.pasta+"/images/"+f"{numeros[str(top.getNum())]}"+"_of_"+f"{naipes_eng[top.getNaipe()]}"+".png"
                img = ImageTk.PhotoImage(Image.open(location).resize((117,117)))
            else:
                img = self.an_image
            # self.board_view[3][2].configure(image=img)
            # self.image.add(img)
            self.board_view[5][2].configure(image=img)
            self.image.add(img)
        
        #trincas
        cartas = []
        trincas_remotas = self.mesa.remote_player.getTrincas()
        for trinca in trincas_remotas:
            for carta in trinca.getCartas():
                cartas.append(carta)
        for i in range(len(cartas)):
            location = self.pasta+"/images/"+f"{numeros[str(cartas[i].getNum())]}"+"_of_"+f"{naipes_eng[cartas[i].getNaipe()]}"+".png"
            img = ImageTk.PhotoImage(Image.open(location).resize((117,117)))
            self.board_view[i][0].configure(image=img)
            self.image.add(img)

        cartas = []
        trincas_locais = self.mesa.local_player.getTrincas()
        for trinca in trincas_locais:
            for carta in trinca.getCartas():
                cartas.append(carta)
        for i in range(len(cartas)):
            location = self.pasta+"/images/"+f"{numeros[str(cartas[i].getNum())]}"+"_of_"+f"{naipes_eng[cartas[i].getNaipe()]}"+".png"
            img = ImageTk.PhotoImage(Image.open(location).resize((117,117)))
            self.board_view[i][4].configure(image=img)
            self.image.add(img)

        if self.game_state == 6:
            self.turn_label.configure(text = 'VEZ OPONENTE')
            self.turn_label.pack(side='left')
        else:
            self.turn_label.configure(text='   SUA VEZ  ')
            #self.turn_label.configure(text='VEZ OPONENTE')
            self.turn_label.pack(side='left')