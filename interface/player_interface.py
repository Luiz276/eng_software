from tkinter import *

class PlayerInterface:
    def __init__(self):
        self.main_window = Tk()
        self.fill_main_window()
        self.main_window.mainloop()
        
    def fill_main_window(self):
        self.main_window.title("Pife")              #titulo da janela
        self.main_window.geometry("1280x900")       #dimensão da janela
        self.main_window.resizable(False, False)    #Define se é possivel reajustar dimensões da janela
        self.main_window["bg"] = "darkgreen"            #cor da janela
        
        # Criação de 2 frames e organização da janela em um grid de 2 linhas e 1 coluna,
        # sendo que table_frame ocupa a linha superior e message_frame, a inferior
        self.table_frame = Frame(self.main_window, padx=100, pady=25, bg="darkgreen")
        self.table_frame.grid(row=0,column=0)
        # self.message_frame = Frame(self.main_window, padx=0, pady=10, bg="darkgreen")
        # self.message_frame.grid(row=1 , column=0)
        
        self.an_image = PhotoImage(file="images/yellow_square.png")
        self.bg_image = PhotoImage(file="images/background_square.png")
            
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
        self.menu_file.add_command(label='Iniciar jogo', command=self.start_match)
        self.menu_file.add_command(label='restaurar estado inicial', command=self.start_game)
        
    def click(self, event, line, column):
        print('CLICK', line, column)
        
    def start_match(self):
        print('start_match')
        
    def start_game(self):
        print('start_game')
