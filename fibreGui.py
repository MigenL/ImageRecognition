import ttk
import tkMessageBox
from fibreCheck import fibreVal
from Tkinter import *
from PIL import ImageTk,Image
from tkFileDialog   import askopenfilename



class VisibleImage:
   def __init__(self, win):
        photo = PhotoImage(file="teiath.png")
        l = Label(win, image=photo)
        l.photo = photo
        l.grid(column=5, row=0)

class SelectionTest :
    def callback(self):
        self.impimg=askopenfilename(initialdir = "/home/mlena/PY/",title = "Select file",
        filetypes = (("jpeg files","*.jpg"),("test","[A-Z][A-Z][A-Z]_[0-9][0-9][0-9][0-9]_[A-Z].jpg"),("all files","*.*")))
        self.status()

    def status(self):
        self.Filename = self.impimg[self.impimg.rfind("/")+1:len(self.impimg)]
        label1=ttk.Label(self.root)
        label1.config(text=self.Filename, width=12)
        label1.grid(column=4, row=3)
        label1.update_idletasks()








    def allstates(self):
        try:
            if str(self.rbuttons.get())!='1':
                self.check=[1,1,1,1,1,1,1,1,1]
                self.val='-i'


            else:
                self.val = '-c'
                self.check= [self.check_1.get(),self.check_2.get(),self.check_3.get(),
                 self.check_4.get(),self.check_5.get(),self.check_6.get(),self.check_7.get(),self.check_8.get(),self.check_9.get()]
        
            fibreVal(self.impimg,self.check,self.val)


        except:
             tkMessageBox.showerror("Error","No File is Selected")

    def cb_check(self):
        if str(self.rbuttons.get())!='1':
            self.check=[1,1,1,1,1,1,1,1,1]
            ttk.Checkbutton(self.root, text="Max Probability", variable=self.check_1, state=DISABLED).grid(column=1, row=1, sticky= W)
            ttk.Checkbutton(self.root, text="Contrast", variable=self.check_2, state=DISABLED).grid(column=2, row=1, sticky= W)
            ttk.Checkbutton(self.root, text="Homogeneity", variable=self.check_3, state=DISABLED).grid(column=3, row=1, sticky= W)
            ttk.Checkbutton(self.root, text="ASM", variable=self.check_4, state=DISABLED).grid(column=1, row=2, sticky= W)
            ttk.Checkbutton(self.root, text="Dissimilarity", variable=self.check_5, state=DISABLED).grid(column=2, row=2, sticky= W)
            ttk.Checkbutton(self.root, text="Energy", variable=self.check_6, state=DISABLED).grid(column=3, row=2, sticky= W)
            ttk.Checkbutton(self.root, text="Variance", variable=self.check_7, state=DISABLED).grid(column=1, row=3, sticky= W)
            ttk.Checkbutton(self.root, text="Correlation", variable=self.check_8, state=DISABLED).grid(column=2, row=3, sticky=W)
            ttk.Checkbutton(self.root, text="Entropy", variable=self.check_9, state=DISABLED).grid(column=3, row=3, sticky=W)
        else:
            ttk.Checkbutton(self.root, text="Max Probability", variable=self.check_1).grid(column=1, row=1, sticky= W)
            ttk.Checkbutton(self.root, text="Contrast", variable=self.check_2).grid(column=2, row=1, sticky= W)
            ttk.Checkbutton(self.root, text="Homogeneity", variable=self.check_3).grid(column=3, row=1, sticky= W)
            ttk.Checkbutton(self.root, text="ASM", variable=self.check_4).grid(column=1, row=2, sticky= W)
            ttk.Checkbutton(self.root, text="Dissimilarity", variable=self.check_5).grid(column=2, row=2, sticky= W)
            ttk.Checkbutton(self.root, text="Energy", variable=self.check_6).grid(column=3, row=2, sticky= W)
            ttk.Checkbutton(self.root, text="Variance", variable=self.check_7).grid(column=1, row=3, sticky= W)
            ttk.Checkbutton(self.root, text="Correlation", variable=self.check_8).grid(column=2, row=3, sticky= W)
            ttk.Checkbutton(self.root, text="Entropy", variable=self.check_9).grid(column=3, row=3, sticky= W)



    def __init__(self) :
        self.root = Tk()
        self.root.minsize(740, 300)
        self.root.maxsize(740,300)
        self.root.geometry("740x300+300+300")
        self.root.title("Fibre Check")
        self.root = ttk.Frame(self.root, padding=(9,9,9,9))
        self.frame = ttk.Frame(self.root, borderwidth=5, relief="groove", width=500, height=180)
        #self.label = ttk.Label(self.root, text='Full name:').grid(column=3, row=3, sticky= W)

        self.rbuttons = IntVar()
        self.details = IntVar()








        #create radious buttons to choose between install and compare images
        ttk.Radiobutton(self.root, text="Import Image", variable=self.rbuttons, command=self.cb_check, value= 0).grid(column=1, row=0)
        ttk.Radiobutton(self.root, text="Compare Image", variable=self.rbuttons, command=self.cb_check, state= ACTIVE, value=1).grid(column=2, row=0)
        # ttk.Radiobutton(self.root, text="Plot Prosses", variable=self.details,  value= 0).grid(column=1, row=5)
        # ttk.Radiobutton(self.root, text="Quiet", variable=self.details, state= ACTIVE, value=1).grid(column=0, row=5)




        self.check_1 = IntVar()
        self.check_2 = IntVar()
        self.check_3 = IntVar()
        self.check_4 = IntVar()
        self.check_5 = IntVar()
        self.check_6 = IntVar()
        self.check_7 = IntVar()
        self.check_8 = IntVar()
        self.check_9 = IntVar()



        ttk.Button(self.root, text='Quit', command=self.root.quit, style='Fun.TButton').grid(column=6, row=4)
        ttk.Button(self.root, text='RUN', command=self.allstates,  style='Fun.TButton').grid(column=5, row=4)
        ttk.Button(self.root,text='File Open', command=self.callback, style='Fun.TButton').grid(column=4, row=4)

        app = VisibleImage(self.root)
        self.root.grid(column=0, row=0, sticky=(N, S, E, W))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=3)
        self.root.columnconfigure(1, weight=3)
        self.root.columnconfigure(2, weight=3)
        self.root.columnconfigure(3, weight=1)
        self.root.columnconfigure(0, weight=0)
        self.root.columnconfigure(4, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.mainloop()


st = SelectionTest()
