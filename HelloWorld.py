from Tkinter import *

class Application(Frame):
    def say_hi(self):
        print "hi there, everyone!"
    def say_ok(self):
        print "OK"

    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit
        self.QUIT.pack({"side": "left"})

        self.hi_there = Button(self)
        self.hi_there["text"] = "Hello"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack({"side": "left"})

        self.ok_there = Button(self, fg = "white", bg = "blue", text = "OK")
        self.ok_there["command"] = self.say_ok
        self.ok_there.pack({"side" : "left", "padx" : "10", "pady" : "10"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title("Hello World")
        self.master.minsize(100,200)
        self.pack()
        self.createWidgets()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()