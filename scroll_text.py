from Tkinter import *
from ttk import *
from ScrolledText import *


class c_ScrolledTextBox:

    def __init__(self, parent, height, width, row, col):
        self.area = ScrolledText(parent, wrap ='word', 
                             width = width,
                             height = height, relief='raised')
        self.area.grid(row=row,column=col, padx=5, pady=5)   
        self.area.insert('insert', "Hello me")

    def Add_Text(self, text):    
        self.area.insert('insert', text)

def Show_Configs():

    root = Tk()
    root.title("Configuration")
    root.geometry("700x500+100+100")

    s = Style()
    s.configure('Yellow.TFrame', background='yellow', borderwidth = 5, padding=15, relief='sunken')

    FrameA = Frame(width=450, height=200, style='Yellow.TFrame')
    FrameB = Frame(width=450, height=200)
    
    root.grid_rowconfigure(1, weight=1, pad=5)
    root.grid_columnconfigure(0, weight=1, pad=5)  

    FrameA.grid(row=0, sticky="ew")
    FrameB.grid(row=1, sticky="ew")  

    cfg_space = ScrolledText(FrameA,
                             wrap = 'word',
                             width =30,
                             height = 6,
                             bg = 'beige')
    cfg_space.grid(row=0, column=0, padx=5, pady=5)
    cfg_space.insert('insert', "pile of text \n more text")

    fix_space = ScrolledText(FrameA,
                             wrap = 'word',
                             width =30,
                             height = 6,
                             bg = 'beige')
    fix_space.grid(row=0, column=1)
    fix_space.insert('insert', "hello text \n more text")    

    clr_space = ScrolledText(FrameB,
                             wrap = 'word',
                             width =30,
                             height = 10,
                             bg = 'beige')
    clr_space.grid(row=0, column=0)
    clr_space.insert('insert', "bottom text \n more text")   
    clr_space.config(state='disabled')      

    seq_space = c_ScrolledTextBox(FrameA,6,30,1,0)
    seq_space.Add_Text("\nHello World")

    root.mainloop()

if __name__ == '__main__':

    Show_Configs()
