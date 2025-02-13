
# This will import all the widgets
# and modules which are available in
# tkinter and ttk module
import threading
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
from tkinter import filedialog
import cantools
from pprint import pprint
import json
import tkinter as tk
from tkinter import ttk
import time
import can.interfaces.vector
from queue import Queue

bus = can.interface.Bus(interface ='vector', app_name='DCAN', channel=0, bitrate=500000)
# creates a Tk() object
master = tk.Tk()

is_on = False
First_Run = 0
CAN_ID = Queue(maxsize = 3000000000)
CAN_DLC = Queue(maxsize = 3000000000)
CAN_DATA = Queue(maxsize = 3000000000)
# sets the geometry of main 
# root window
master.geometry("1000x500")
master.resizable(0,0)
# function to open a new window 
# on a button click
Message_Add_Frame = tk.Frame(master, width=400, height=400, bg="#FFFFFF",borderwidth=2)
Message_Add_Frame.pack(expand= YES, padx=5, pady=5, side=tk.LEFT, fill=tk.Y)

#Add domains in trace
Message_Trace_Frame = tk.Frame(master, width=600, height=400, bg="#FFFFFF",borderwidth=2)
Message_Trace_Frame.pack(expand= YES,padx=6, pady=5, side=tk.LEFT, fill=tk.Y)
tabControl = ttk.Notebook(Message_Trace_Frame) 
Infor_Frame = tk.Frame(tabControl, width=600, height=400, bg="#FFFFFF",borderwidth=2)
Body_Frame = tk.Frame(tabControl, width=600, height=400, bg="#FFFFFF",borderwidth=2)
CH_Frame = tk.Frame(tabControl, width=600, height=400, bg="#FFFFFF",borderwidth=2)
PT_Frame = tk.Frame(tabControl, width=600, height=400, bg="#FFFFFF",borderwidth=2)
BA_Frame = tk.Frame(tabControl, width=600, height=400, bg="#FFFFFF",borderwidth=2)
DIAG_Frame = tk.Frame(tabControl, width=600, height=400, bg="#FFFFFF",borderwidth=2)
LEGACY_Frame = tk.Frame(tabControl, width=600, height=400, bg="#FFFFFF",borderwidth=2)
SAFETY_Frame = tk.Frame(tabControl, width=600, height=400, bg="#FFFFFF",borderwidth=2)
tabControl.add(Infor_Frame, text="INFOR")
tabControl.add(Body_Frame, text="BODY")
tabControl.add(CH_Frame, text="CH")
tabControl.add(PT_Frame, text="PT")
tabControl.add(BA_Frame, text="BA")
tabControl.add(DIAG_Frame, text="DIAG")
tabControl.add(LEGACY_Frame, text="SAFETY")
tabControl.add(SAFETY_Frame, text="LEGACY")

#Creat tree view
trv = ttk.Treeview(Infor_Frame, selectmode ='browse',height = 20)
trv.grid(row=1,column=1,padx=20,pady=20)
trv["columns"] = ("1", "2", "3")
trv['show'] = 'tree headings'
s=ttk.Style()
s.configure(trv,rowhieght=20)
s.configure(trv,height=20)
# width of columns and alignment 
trv.column("#0", width = 200, anchor ='c')
trv.column("1", width = 60, anchor ='c')
trv.column("2", width = 200, anchor ='c')
trv.column("3", width = 50, anchor ='c')
# Headings  
# respective columns
trv.heading("#0", text ="Name")
trv.heading("1", text ="ID")
trv.heading("2", text ="DATA")
trv.heading("3", text ="DLC")

tabControl.pack(expand= True, padx=5, pady=5, side=tk.LEFT, fill=tk.Y) 
Value_Dummy = {
    'INFOR_DBCPATH': '',
    'BODY_DBCPATH': '',
    'CH_DBCPATH': '',
    'PT_DBCPATH': '',
    'HV_DBCPATH': '',
    'DIAG_DBCPATH': '',
    'LEGACY_DBCPATH': '',
    'SAFETY_DBCPATH': '',
    'Process': 0,
    'Trace_sts':0,
}
with open('data.json', 'w') as file:
    json.dump(Value_Dummy, file, indent=4)

def Modify_DataJs(Object,Data):
    with open('data.json') as f:
        output_data = json.load(f)

    output_data[Object] = Data

    with open('data.json', 'w') as f:
        json.dump(output_data, f, indent=4)

def Read_DataJs(Object):
    with open('data.json') as f:
        output_data = json.load(f)
    return output_data[Object]

def Database_Window():
    # Toplevel object which will 
    # be treated as a new window
    newWindow = Toplevel(master)
    global INFOR_PATH
    # sets the title of the
    # Toplevel widget
    newWindow.title("New Window")
 
    # sets the geometry of toplevel
    newWindow.geometry("700x400")

    def Infor_DBC():
        filename = filedialog.askopenfilename(initialdir = "/",
                                            title = "Select a File",
                                            filetypes = (("Text files",
                                                            "*.dbc*"),
                                                        ("all files",
                                                            "*.*")))    
        Infor_LinkFile.config(text = filename)
        Modify_DataJs("INFOR_DBCPATH",filename)
    def BODY_DBC():
        filename = filedialog.askopenfilename(initialdir = "/",
                                            title = "Select a File",
                                            filetypes = (("Text files",
                                                            "*.dbc*"),
                                                        ("all files",
                                                            "*.*")))     
        Body_LinkFile.config(text = filename)
        Modify_DataJs("Body_DBCPATH",filename)
    def CH_DBC():
        filename = filedialog.askopenfilename(initialdir = "/",
                                            title = "Select a File",
                                            filetypes = (("Text files",
                                                            "*.dbc*"),
                                                        ("all files",
                                                            "*.*")))    
        CH_LinkFile.config(text = filename)  
        Modify_DataJs("CH_DBCPATH",filename)   
    def PT_DBC():
        filename = filedialog.askopenfilename(initialdir = "/",
                                            title = "Select a File",
                                            filetypes = (("Text files",
                                                            "*.dbc*"),
                                                        ("all files",
                                                            "*.*")))   
        PT_LinkFile.config(text = filename) 
        Modify_DataJs("PT_DBCPATH",filename)
    def HV_DBC():
        filename = filedialog.askopenfilename(initialdir = "/",
                                            title = "Select a File",
                                            filetypes = (("Text files",
                                                            "*.dbc*"),
                                                        ("all files",
                                                            "*.*")))   
        HV_LinkFile.config(text = filename) 
        Modify_DataJs("HV_DBCPATH",filename)
    def DIAG_DBC():
        filename = filedialog.askopenfilename(initialdir = "/",
                                            title = "Select a File",
                                            filetypes = (("Text files",
                                                            "*.dbc*"),
                                                        ("all files",
                                                            "*.*")))     
        DIAG_LinkFile.config(text = filename)     
        Modify_DataJs("DIAG_DBCPATH",filename)
    def LEGACY_DBC():
        filename = filedialog.askopenfilename(initialdir = "/",
                                            title = "Select a File",
                                            filetypes = (("Text files",
                                                            "*.dbc*"),
                                                        ("all files",
                                                            "*.*")))  
        LEGACY_LinkFile.config(text = filename) 
        Modify_DataJs("LEGACY_DBCPATH",filename)
    def SAFETY_DBC():
        filename = filedialog.askopenfilename(initialdir = "/",
                                            title = "Select a File",
                                            filetypes = (("Text files",
                                                            "*.dbc*"),
                                                        ("all files",
                                                            "*.*")))   
        SAFETY_LinkFile.config(text = filename) 
        Modify_DataJs("SAFETY_DBCPATH",filename)
    # A Label widget to show in toplevel
    Infor_Label = Label(newWindow, text ="INFOR BUS",)
    Infor_Label.place(relx = 0.1, rely = 0.1,anchor = 'center')
    Infor_LinkFile = Label(newWindow, width = 70,borderwidth=1,relief="solid",background = "white")
    Infor_LinkFile.place(relx = 0.5, rely = 0.1,anchor = 'center')
    Infor_BntFile = Button(newWindow,text = "Select",command= Infor_DBC)
    Infor_BntFile.place(relx = 0.9, rely = 0.1,anchor = 'center')

    Body_Label = Label(newWindow, text ="BODY BUS")
    Body_Label.place(relx = 0.1, rely = 0.2,anchor = 'center')
    Body_LinkFile = Label(newWindow, width = 70,borderwidth=1,relief="solid",background = "white")
    Body_LinkFile.place(relx = 0.5, rely = 0.2,anchor = 'center')
    Body_BntFile = Button(newWindow,text = "Select",command = BODY_DBC)
    Body_BntFile.place(relx = 0.9, rely = 0.2,anchor = 'center')

    CH_Label = Label(newWindow, text ="CH BUS")
    CH_Label.place(relx = 0.1, rely = 0.3,anchor = 'center')
    CH_LinkFile = Label(newWindow, width = 70,borderwidth=1,relief="solid",background = "white")
    CH_LinkFile.place(relx = 0.5, rely = 0.3,anchor = 'center')
    CH_BntFile = Button(newWindow,text = "Select", command= CH_DBC)
    CH_BntFile.place(relx = 0.9, rely = 0.3,anchor = 'center')

    PT_Label = Label(newWindow, text ="PT BUS")
    PT_Label.place(relx = 0.1, rely = 0.4,anchor = 'center')
    PT_LinkFile = Label(newWindow, width = 70,borderwidth=1,relief="solid",background = "white")
    PT_LinkFile.place(relx = 0.5, rely = 0.4,anchor = 'center')
    PT_BntFile = Button(newWindow,text = "Select",command= PT_DBC)
    PT_BntFile.place(relx = 0.9, rely = 0.4,anchor = 'center')

    HV_Label = Label(newWindow, text ="HV BUS")
    HV_Label.place(relx = 0.1, rely = 0.5,anchor = 'center')
    HV_LinkFile = Label(newWindow, width = 70,borderwidth=1,relief="solid",background = "white")
    HV_LinkFile.place(relx = 0.5, rely = 0.5,anchor = 'center')
    HV_BntFile = Button(newWindow,text = "Select",command = HV_DBC)
    HV_BntFile.place(relx = 0.9, rely = 0.5,anchor = 'center')

    DIAG_Label = Label(newWindow, text ="DIAG BUS")
    DIAG_Label.place(relx = 0.1, rely = 0.6,anchor = 'center')
    DIAG_LinkFile = Label(newWindow, width = 70,borderwidth=1,relief="solid",background = "white")
    DIAG_LinkFile.place(relx = 0.5, rely = 0.6,anchor = 'center')
    DIAG_BntFile = Button(newWindow,text = "Select",command = DIAG_DBC)
    DIAG_BntFile.place(relx = 0.9, rely = 0.6,anchor = 'center')

    LEGACY_Label = Label(newWindow, text ="LEGACY BUS")
    LEGACY_Label.place(relx = 0.1, rely = 0.7,anchor = 'center')
    LEGACY_LinkFile = Label(newWindow, width = 70,borderwidth=1,relief="solid",background = "white")
    LEGACY_LinkFile.place(relx = 0.5, rely = 0.7,anchor = 'center')
    LEGACY_BntFile = Button(newWindow,text = "Select",command= LEGACY_DBC)
    LEGACY_BntFile.place(relx = 0.9, rely = 0.7,anchor = 'center')

    SAFETY_Label = Label(newWindow, text ="SAFETY BUS")
    SAFETY_Label.place(relx = 0.1, rely = 0.8,anchor = 'center')
    SAFETY_LinkFile = Label(newWindow, width = 70,borderwidth=1,relief="solid",background = "white")
    SAFETY_LinkFile.place(relx = 0.5, rely = 0.8,anchor = 'center')
    SAFETY_BntFile = Button(newWindow,text = "Select",command = SAFETY_DBC)
    SAFETY_BntFile.place(relx = 0.9, rely = 0.8,anchor = 'center')

def Check_Routing():
    # Toplevel object which will 
    # be treated as a new window
    newWindow = Toplevel(master)
    
    # sets the title of the
    # Toplevel widget
    newWindow.title("New Window")
 
    # sets the geometry of toplevel
    newWindow.geometry("400x200")
    Run_BntFile = Button(newWindow,text = "Run")
    Run_BntFile.place(relx = 0.1, rely = 0.5,anchor = 'center')
    progressbar = ttk.Progressbar(newWindow)
    progressbar.place(relx = 0.5, rely = 0.5,anchor = 'center', width=200)
    progressbar.step(50)
    db = cantools.database.load_file(Read_DataJs("INFOR_DBCPATH"))
    print(db.messages)
# Creat menu bar
menubar = Menu(master)
filemenu = Menu(menubar, tearoff=0)
# filemenu.add_command(label="New", command=donothing)
# filemenu.add_command(label="Open", command=donothing)
filemenu.add_command(label="Database Setting", command=Database_Window)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=master.quit)
menubar.add_cascade(label="Setting", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
# helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="Check_Routing", command=Check_Routing)
menubar.add_cascade(label="Function", menu=helpmenu)

master.config(menu=menubar)
# mainloop, runs infinitely
def Run_Trace():
    global is_on  
    # Determine is on or off
    if is_on:
        Read_BntFile.config(image = off)
        is_on = False
        Clear_Data()
        Modify_DataJs("Trace_sts",is_on)
    else:       
        Read_BntFile.config(image = on)
        is_on = True
        Modify_DataJs("Trace_sts",is_on)
        t1 = threading.Thread(target=Get_Message, args=())
        t2 = threading.Thread(target=Display_Trace, args=())
        t1.start()
        t2.start()
        
on = PhotoImage(file = "play.png")
off = PhotoImage(file = "pause.png")

def Get_Message():
    if is_on == True:
        try:
            while True and is_on == True:
                message = bus.recv()

                if message is not None:
                    CAN_ID.put(message.arbitration_id)
                    CAN_DLC.put(message.dlc)
                    CAN_DATA.put(message.data[0])
        except KeyboardInterrupt:
            print("Stopped by user")
        master.after(1,Get_Message)
def Clear_Data():
    if is_on == False:    
        while CAN_ID.empty() == False:
            CAN_ID.get()
        while CAN_DLC.empty() == False:
            CAN_DLC.get()
        while CAN_DATA.empty() == False:
            CAN_DATA.get()        
        trv.delete(*trv.get_children())
        
def Display_Trace():
    if is_on == True:
        if CAN_ID.empty() == False:
            idd_to_check = CAN_ID.get()
            DLC = CAN_DLC.get()
            DATA = CAN_DATA.get()
            # print(idd_to_check)
            if trv.exists(idd_to_check) == False:
                trv.insert('','end',iid = idd_to_check ,values = (idd_to_check,DATA,DLC))  
            else:
                trv.item(idd_to_check,values = (idd_to_check,DATA,DLC))   
        master.after(1,Display_Trace)
        
Read_BntFile = Button(Message_Add_Frame,width=1,image = off,command = Run_Trace)
Read_BntFile.place(relx = 0.1, rely = 0.1,anchor = 'center')
mainloop()