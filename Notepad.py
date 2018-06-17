import tkinter
import os
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import time
import datetime
import _thread as thread

class Notepad:

    #variables
    __root = Tk()

    frame = Frame(__root)
    #default window width and height
    # dFont = tkinter..Font(family="Arial", size=30)
    __thisWidth = 500
    __thisHeight = 300
    __thisTextArea = Text(__root)
    __thisMenuBar = Menu(__root)
    __thisFileMenu = Menu(__thisMenuBar,tearoff=0)
    __thisEditMenu = Menu(__thisMenuBar,tearoff=0)
    __thisHelpMenu = Menu(__thisMenuBar,tearoff=0)
    __thisScrollBar = Scrollbar(__thisTextArea)
    # timerfield = Text(__root)
    timer_button = Button(__root, text="Start Typing")
    label = Label(__root, text="total character entered: 0")
    __file = None
    timer = 0
    paused = True
    totalCharEntered= 0
    speed =0
    textAreaContents = ""

    def __init__(self,**kwargs):
        #initialization
        #set icon
        try:
        		self.__root.wm_iconbitmap("Notepad.ico") #GOT TO FIX THIS ERROR (ICON)
        except:
        		pass

        #set window size (the default is 300x300)

        try:
            self.__thisWidth = kwargs['width']
        except KeyError:
            pass

        try:
            self.__thisHeight = kwargs['height']
        except KeyError:
            pass

        #set the window text
        self.__root.title("Untitled - Notepad")

        #center the window
        screenWidth = self.__root.winfo_screenwidth()
        screenHeight = self.__root.winfo_screenheight()

        left = (screenWidth / 2) - (self.__thisWidth / 2)
        top = (screenHeight / 2) - (self.__thisHeight /2)

        # self.__root.geometry('%dx%d+%d+%d' % (self.__thisWidth, self.__thisHeight, left, top))

        # self.__thisTextArea.winfo_screen()
        self.__thisTextArea.pack(fill=BOTH, expand=YES)
        #to make the textarea auto resizable
        self.__root.grid_rowconfigure(0,weight=1)
        self.__root.grid_columnconfigure(0,weight=1)

        #add controls (widget)

        # self.__thisTextArea.grid(sticky=N + E + S + W)

        self.__thisFileMenu.add_command(label="New",command=self.__newFile)
        self.__thisFileMenu.add_command(label="Open",command=self.__openFile)
        self.__thisFileMenu.add_command(label="Save",command=self.__saveFile)
        self.__thisFileMenu.add_separator()
        self.__thisFileMenu.add_command(label="Exit",command=self.__quitApplication)
        self.__thisMenuBar.add_cascade(label="File",menu=self.__thisFileMenu)

        self.__thisEditMenu.add_command(label="Cut",command=self.__cut)
        self.__thisEditMenu.add_command(label="Copy",command=self.__copy)
        self.__thisEditMenu.add_command(label="Paste",command=self.__paste)
        self.__thisMenuBar.add_cascade(label="Edit",menu=self.__thisEditMenu)

        self.__thisHelpMenu.add_command(label="About Notepad",command=self.__showAbout)
        self.__thisMenuBar.add_cascade(label="Help",menu=self.__thisHelpMenu)

        self.__root.config(menu=self.__thisMenuBar)

        # self.__thisScrollBar.pack(side=RIGHT,fill=Y)
        # self.__thisScrollBar.config(command=self.__thisTextArea.yview)
        # self.__thisTextArea.config(yscrollcommand=self.__thisScrollBar.set)

        # self.timerfield.pack(side=RIGHT,fill=Y)

        # self.label = tkinter.Label(text="")
        # self.label.pack()
        # thread.start_new_thread(self.update_button_time, (self,))
        self.timer_button.pack()
        self.timer_button.config(command = self.buttonClicked)
        self.update_button_time()
        self.label.pack()
        self.__thisTextArea.focus()
        self.__thisTextArea.bind("<Control-space>", self.pressCmdSpace)
        self.__thisTextArea.bind("<Key>", self.key)

    def __quitApplication(self):
        self.__root.destroy()
        #exit()

    def __showAbout(self):
        showinfo("Notepad","Created by: tmkakot, tinkumonikakoti@twitter.com")

    def __openFile(self):
        
        self.__file = askopenfilename(defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])

        if self.__file == "":
            #no file to open
            self.__file = None
        else:
            #try to open the file
            #set the window title
            self.__root.title(os.path.basename(self.__file) + " - Notepad")
            self.__thisTextArea.delete(1.0,END)

            file = open(self.__file,"r")

            self.__thisTextArea.insert(1.0,file.read())

            file.close()

        
    def __newFile(self):
        self.__root.title("Untitled - Notepad")
        self.__file = None
        self.__thisTextArea.delete(1.0,END)

    def __saveFile(self):

        if self.__file == None:
            #save as new file
            self.__file = asksaveasfilename(initialfile='Untitled.txt',defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])

            if self.__file == "":
                self.__file = None
            else:
                #try to save the file
                file = open(self.__file,"w")
                file.write(self.__thisTextArea.get(1.0,END))
                file.close()
                #change the window title
                self.__root.title(os.path.basename(self.__file) + " - Notepad")
                
            
        else:
            file = open(self.__file,"w")
            file.write(self.__thisTextArea.get(1.0,END))
            file.close()

    def __cut(self):
        self.__thisTextArea.event_generate("<<Cut>>")

    def __copy(self):
        self.__thisTextArea.event_generate("<<Copy>>")

    def __paste(self):
        self.__thisTextArea.event_generate("<<Paste>>")

    def run(self):
        #run main application
        self.__root.mainloop()

    def buttonClicked(self):
        if self.paused == True:
            self.paused = False
            self.timer_button.config(text= self.timer)
            # self.update_button_time
        else:
            self.paused =True
            self.timer_button.config(text = "paused " +"time: " + str(self.timer)+
                                           "  speed: " + "%.2f" % self.speed+ "WPM")


    def update_button_time(self):
        if self.paused== False :
            self.timer =self.timer+0.5
            if (self.timer > 0):
                self.speed = (self.totalCharEntered * 60) / (self.timer * 5)

            self.timer_button.config(text ="time: " + str(self.timer)+
                                           "  speed: " + "%.2f" % self.speed+"WPM")

        self.__root.after(500, self.update_button_time)

    def key(self, event):
        if(event.char >= ' ' and event.char <= '~'):
            self.paused = False
            if event.char != ' ':
                self.totalCharEntered +=1
            self.textAreaContents += event.char

        if(event.char == chr(8)):#backspace
            if not self.textAreaContents.endswith(' '):
                self.totalCharEntered -=1
        self.label.config(text ="total character entered: "+ str(self.totalCharEntered))

    def pressCmdSpace(self, event):
        self.paused = True
        self.timer_button.config(text="paused " + "time: " + str(self.timer) +
                                      "  speed: " + "%.2f" % self.speed + "WPM")


#run main application

notepad = Notepad(width=800,height=400)
notepad.run()


