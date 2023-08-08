import tkinter as tk
import tkinter.filedialog as fd
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.style import Style
from ttkbootstrap import utility
import datetime

class App(ttk.Frame):
    def __init__(self,master):
        super().__init__(master, padding=(20, 10))

        ttk.Style().configure("TButton", font="TkFixedFont 12")

        self.pack(fill=BOTH, expand=YES)

        
        # form header
        title_txt = "Sorveteria Sonho Real"
        ttk.Label(master=self, font="TkFixedFont 18", bootstyle="info", text=title_txt).pack(fill=Y)

        self.container = ttk.Frame(self)
        self.container.pack(fill=BOTH, expand=YES)

        self.create_left_frame()
        self.create_right_frame()
        self.create_cupom_fiscal()

    def add_item(self):
        _cbx_tipo = self.tipo_txt.get()
        _cbx_num = self.num_txt.get()
     
        iid = self.resultview.insert(
            parent='',
            index=END,            
            values=(_cbx_num, _cbx_tipo, self.calcula_preco(_cbx_num, _cbx_tipo))
        )
        self.resultview.selection_set(iid)
        self.resultview.see(iid)

    def calcula_preco(self, nb, tipo):
        TRADICIONAL = 8
        ESPECIAL = 9
        PRIMER = 12
        if 'Tradicional' in tipo:            
            if '1' in nb:
                retorno = TRADICIONAL * 1
            elif '2' in nb:
                retorno = TRADICIONAL * 2
            else:
                retorno = TRADICIONAL * 3
        elif tipo == 'Especial':
            if '1' in nb:
                retorno = ESPECIAL * 1
            elif '2' in nb:
                retorno = ESPECIAL * 2
            else:
                retorno = ESPECIAL * 3
        else:
            if '1' in nb:
                retorno = PRIMER * 1
            elif '2' in nb:
                retorno = PRIMER * 2
            else:
                retorno = PRIMER * 3
        return retorno
        


    def show_popup_menu(self, event):
        self.popup_menu.tk_popup(event.x_root, event.y_root, 0)

    def delete_item(self):
        selected_index = self.resultview.selection()
        if selected_index:
            self.resultview.delete(selected_index)


    def finaliza(self):
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        data_pedido = now.strftime("%y-%m-%d %H:%M:%S")
        total = []
        # exibe os valores no textfield recibo para impressão.
        for line in self.resultview.get_children():
            values = self.resultview.item(line, 'values')
            self.txtRecibo.insert(END, f"Sorvete {values[1]} com {values[0]} bola(s) -------------- Valor(RS): {values[2]}\n")
            total.append(int(values[2]))

        self.txtRecibo.insert(END, f'\nTotal (R$) ------------------------------------------------------------ {sum(total)}')
        
        # limpa o treeview
        for i in self.resultview.get_children():
            self.resultview.delete(i)
        
        self.btn_add.configure(state='disabled')
        self.btn_finaliza.configure(state='disabled')
 
    def print(self):
        self.btn_add.configure(state='enable')
        self.btn_finaliza.configure(state='enable')
        self.txtRecibo.delete('1.0', END)
        
        
    
    def create_left_frame(self):
        left_frame = ttk.Frame(self.container)
        left_frame.pack(fill=BOTH, expand=YES, side=LEFT)

        ttk.Label(left_frame,justify=LEFT, padding=(20, 20) ,text='Faça sua escolha', bootstyle='success').pack(anchor=W)

        ttk.Label(left_frame,justify=LEFT, padding=(20, 20) ,text='Escolha o tipo de sorvete', bootstyle='success').pack(fill=Y, anchor=W)
        self.tipo_txt = ttk.Combobox(left_frame, width=40)
        self.tipo_txt['values'] = ('Tradicional', 'Prime', 'Especial')
        self.tipo_txt.current(0)
        self.tipo_txt.pack(anchor=W, padx=20)

        ttk.Label(left_frame,justify=LEFT, padding=(20, 20) ,text='Escolha a quantidade de bolas', bootstyle='success').pack(fill=Y, anchor=W)
        self.num_txt = ttk.Combobox(left_frame,  width=40)
        self.num_txt['values'] = (1, 2, 3)
        self.num_txt.current(2)
        self.num_txt.pack(anchor=W, padx=20)

        self.btn_add = ttk.Button(left_frame, text="Adiciona >>", command=self.add_item)
        self.btn_add.pack(anchor=W, padx=20, pady=10)

    def create_right_frame(self):
        right_frame = ttk.Frame(self.container)
        right_frame.pack(fill=BOTH, expand=YES, side=RIGHT)

        ttk.Label(right_frame,justify=LEFT, padding=(0, 20) ,text='Escolha(s) do cliente', bootstyle='warning').pack(anchor=W)

        self.resultview = ttk.Treeview(
            master=right_frame,
            bootstyle=INFO,
            columns=[0, 1, 2],
            show=HEADINGS,
            selectmode='browse',
        )
        self.resultview.pack(anchor=W)

        self.resultview.heading(0, text='Nº Bolas', anchor=W)
        self.resultview.heading(1, text='Tipo de Sorvete', anchor=NW)
        self.resultview.heading(2, text='Valor(R$)', anchor=E)

        self.resultview.column(
            column=0, anchor=W, width=utility.scale_size(self, 100), stretch=False
        )
        self.resultview.column(
            column=1, anchor=NW, width=utility.scale_size(self, 200), stretch=False
        )
        self.resultview.column(
            column=2, anchor=E, width=utility.scale_size(self, 100), stretch=False
        )

        self.popup_menu = ttk.Menu(self.resultview, tearoff=0)
        self.popup_menu.add_command(label="Delete", command=self.delete_item)

        self.resultview.bind("<Button-3>", self.show_popup_menu)


        self.btn_finaliza = ttk.Button(right_frame, text="Concluir compra",bootstyle='danger', command=self.finaliza)
        self.btn_finaliza.pack(anchor=E,  pady=10, padx=5)

    def create_cupom_fiscal(self):
        cupom_frame = ttk.Frame(master=self, height=200)
        cupom_frame.pack(fill=BOTH, expand=YES)

        style = ttk.Style()
        self.txtRecibo = ttk.ScrolledText(
            master=cupom_frame,
            padx=5, pady=5,
            height=10,
            highlightcolor=style.colors.primary,
            highlightbackground=style.colors.border,
            highlightthickness=1,
            
            )
        self.txtRecibo.pack(fill=BOTH)

        btn_print = ttk.Button(cupom_frame, text="Imprimir", bootstyle='warning', command=self.print)
        btn_print.pack(anchor=E,  pady=10)

        
    def place_window_center(self):
        self.update_idletasks()
        w_height = self.winfo_height()
        w_width = self.winfo_width()
        s_height = self.winfo_screenheight()
        s_width = self.winfo_screenwidth()
        xpos = (s_width - w_width) // 2
        ypos = (s_height - w_height) // 2
        self.geometry(f'+{xpos}+{ypos}')

    place_window_center


if __name__ == "__main__":
    app = ttk.Window(title="Sorvete", themename="darkly", size=(800, 600),resizable=(False, False),)
    App(app)
    app.mainloop()
