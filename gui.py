import threading
from tkcalendar import Calendar, DateEntry
from tkinter import ttk, Tk, Entry, Label, Text, END, Frame, RIGHT, Y, StringVar, Spinbox, Button
from monitor import *
from manualMonitor import *

class Gui:
    #init the Gui details
    def __init__(self):
        self.service = ""
        self.change  = False
        self.m = monitor()
        self.manu = manualMonitor()
        self.window = Tk()
        self.frameMonitor = Frame(self.window)
        self.frameManual = Frame(self.window)
        self.window.title("monitor")
        self.window.geometry("600x600")
        self.window.configure(bg="lightgray")
        self.time_text = Entry(self.frameMonitor)
        self.time=""
        self.stop_thread = True
        ttk.Button(self.window, text="monitor", width=10, command=self.monitorShow).place(x=2, y=4)
        ttk.Button(self.window, text="manual", width=10, command=self.manualShow).place(x=100, y=4)
        #date
        self.date_start_entry = DateEntry(self.frameManual)
        self.date_end_entry = DateEntry(self.frameManual)
        self.date_start = self.date_start_entry.get()
        self.date_end = self.date_end_entry.get()
        #time
        self.hourstr_start=StringVar(self.frameManual,'10')
        self.hour_start = Spinbox(self.frameManual,from_=0,to=23,wrap=True,textvariable=self.hourstr_start,width=2,state="readonly").place(x=355, y=10)
        self.minstr_start=StringVar(self.frameManual,'30')
        self.min_start = Spinbox(self.frameManual,from_=0,to=59,wrap=True,textvariable=self.minstr_start,width=2,state="readonly").place(x=385, y=10)
        self.secstr_start=StringVar(self.frameManual,'10')
        self.sec_start = Spinbox(self.frameManual,from_=0,to=59,wrap=True,textvariable=self.secstr_start,width=2,state="readonly").place(x=415, y=10)
        self.hourstr_end=StringVar(self.frameManual,'10')
        self.hour_end = Spinbox(self.frameManual,from_=0,to=23,wrap=True,textvariable=self.hourstr_end,width=2,state="readonly").place(x=355, y=30)
        self.minstr_end=StringVar(self.frameManual,'30')
        self.min_end = Spinbox(self.frameManual,from_=0,to=59,wrap=True,textvariable=self.minstr_end,width=2,state="readonly").place(x=385, y=30)
        self.secstr_end=StringVar(self.frameManual,'10')
        self.sec_end = Spinbox(self.frameManual,from_=0,to=59,wrap=True,textvariable=self.secstr_end,width=2,state="readonly").place(x=415, y=30)
        # scrollbar
        self.scrollbar = ttk.Scrollbar(self.window)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.window.mainloop()

    #present the monitor screen and details
    def monitorShow(self):
        self.frameManual.pack_forget()
        self.frameMonitor.pack(side="top", expand=True, fill="both")
        self.msg_label1 = Text(self.frameMonitor)
        self.msg_label1.place(x=10, y=30, width=570, height=560)
        self.msg_label1.config(state="disabled")
        self.scrollbar.configure(command=self.msg_label1.yview)
        if self.service!="":
            self.change = True
            self.print(self.service)
        self.time_button = Label(self.frameMonitor, text="enter time in sec:")
        self.time_button.place(x=200, y=8)
        self.time_button.config(font=("Ariel", 8))
        self.time_text.place(x=300, y=8)
        if self.change:
            ttk.Button(self.frameMonitor, text="exit", width=10, command=self.exit).place(x=430, y=5)
        else:
            Button(self.frameMonitor, text="ok", width=7, command=self.monitor).place(x=430, y=5)

    #running 3 threads in parallel: of start-time, of income warnings, of income info to show
    def monitor(self):
        self.time = int(self.time_text.get())
        threading.Thread(target=self.start).start()
        threading.Thread(target=self.warning).start()
        threading.Thread(target=self.recv).start()
        ttk.Button(self.frameMonitor, text="exit", width=10, command=self.exit).place(x=430, y=5)

    #open a new window with warning msg if there's changes in files
    def warning(self):
        i = 0
        while self.stop_thread:
            if len(self.m.warning) != 0:
                if i == 0:
                    print("dd")
                    w = Tk()
                    w.geometry("300x300")
                    w.title("warning")
                    l = Label(w, text="You've been attacked!!!")
                    l.config(font=("Courier", 14))
                    l.pack()
                    Button(w, text="Quit", command=w.destroy).pack()
                    i += 1
                w.mainloop()

    #exit and stop the program
    def exit(self):
        self.stop_thread = False
        self.m.stopMonitor()
        exit(0)

    #start the monitor
    def start(self):
        self.m.start(self.time)

    #present the screen of manualShow button
    def manualShow(self):
        self.frameMonitor.pack_forget()
        self.msg_label = Text(self.frameManual)
        self.msg_label.place(x=10, y=50, width=570, height=530)
        self.msg_label.config(state="disabled")
        self.frameManual.pack(side="top", expand=True, fill="both")
        self.start_time = Label(self.frameManual, text="enter start time:")
        self.start_time.place(x=170, y=10)
        self.start_time.config(font=("Ariel", 8))
        self.end_time = Label(self.frameManual, text="enter end time:")
        self.end_time.place(x=170, y=30)
        self.end_time.config(font=("Ariel", 8))
        self.date_start_entry.place(x=255, y=10)
        self.date_end_entry.place(x=255, y=30)
        ttk.Button(self.frameManual, text="ok", width=7, command=self.manual).place(x=450, y=15)

    #take care for input values of manualMonitor and send it to startManual
    def manual(self):
        datestart = self.date_start_entry.get()
        size = datestart.find("/",3)
        datestart=datestart[0:size+1]+"20"+datestart[size+1:len(datestart)]
        hourstart = self.hourstr_start.get()
        minstart = self.minstr_start.get()
        secstart = self.secstr_start.get()
        start = datestart + ' ' +  hourstart+":"+minstart+":"+secstart
        dateend = self.date_end_entry.get()
        size = dateend.find("/",3)
        dateend=dateend[0:size+1]+"20"+dateend[size+1:len(dateend)]
        hourend = self.hourstr_end.get()
        minend= self.minstr_end.get()
        secend = self.secstr_end.get()
        end = dateend +' ' +hourend+":"+minend+":"+secend
        print(start,end)
        threading.Thread(target=self.startManual,args=(start,end)).start()

    #send the inputs to manualMonitor
    def startManual(self,start,end):
        s = self.manu.start(start,end)
        if s!=None:
         self.msg_label.config(state='normal')
         self.msg_label.insert('end', s)
         self.msg_label.yview('end')
         self.msg_label.insert('end', "\n")
         self.msg_label.config(state='disable')

    #insert the service values to the fields
    def recvManual(self):
            if len(self.m.listOfServices) != 0:
                temp = self.m.listOfServices.pop(0)
                self.service+=temp
                self.service+="\n"
                self.print(temp)
    #print the input text in the Gui screen
    def print(self, mes):
        self.msg_label1.config(state='normal')
        self.msg_label1.insert('end', mes)
        self.msg_label1.yview('end')
        self.msg_label1.insert('end', "\n")
        self.msg_label1.config(state='disable')
    #send the service list to print func for printing
    def recv(self):
        while self.stop_thread:
            if len(self.m.listOfServices) != 0:
                temp = self.m.listOfServices.pop(0)
                self.service+=temp
                self.service+="\n"
                self.print(temp)

if __name__ == '__main__':
    i = Gui()