import Tkinter
import ttk
import ScrolledText as ST

def Show_Configs():

    root = Tkinter.Tk()
    root.title("Configuration")
    root.geometry("700x500+100+100")

    FrameA = Tkinter.Frame(root, bg='brown',width=450, height=200, padx=3, pady=3)
    FrameB = Tkinter.Frame(root, bg='yellow',width=450, height=200, padx=3, pady=3)
    
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)  

    FrameA.grid(row=0, sticky="ew")
    FrameB.grid(row=1, sticky="ew")  

    cfg_space = ST.ScrolledText(FrameA,
                             wrap = 'word',
                             width =30,
                             height = 10,
                             bg = 'beige')
    cfg_space.grid(row=0, column=0)
    cfg_space.insert('insert', "pile of text \n more text")

    fix_space = ST.ScrolledText(FrameA,
                             wrap = 'word',
                             width =30,
                             height = 10,
                             bg = 'beige')
    fix_space.grid(row=0, column=1)
    fix_space.insert('insert', "hello text \n more text")    

    clr_space = ST.ScrolledText(FrameB,
                             wrap = 'word',
                             width =30,
                             height = 10,
                             bg = 'beige')
    clr_space.grid(row=0, column=0)
    clr_space.insert('insert', "bottom text \n more text")   
    clr_space.config(state='disabled')        

    root.mainloop()

if __name__ == '__main__':

    Show_Configs()
