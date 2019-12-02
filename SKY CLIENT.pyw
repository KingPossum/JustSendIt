#! /usr/bin/env python
#
# GUI module generated by PAGE version 4.9
# In conjunction with Tcl version 8.6
#    Feb 05, 2018 08:51:29 PM

import threading #for use in download/progressbar function
import socket #for networking
import base64 #for encoding/decoding data sent across the network
import sys #imported by PAGE for use in GUI
import tkinter as tk #shit man idk
import math #do i even use math?

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

try:
    import ttk
    py3 = 0
except ImportError:
    import tkinter.ttk as ttk
    py3 = 1

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = Tk()
    top = New_Toplevel_1 (root)
    root.mainloop()

w = None
def create_New_Toplevel_1(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = Toplevel (root)
    top = New_Toplevel_1 (w)
    return (w, top)

def destroy_New_Toplevel_1():
    global w
    w.destroy()
    w = None

class New_Toplevel_1:
            
    global host
    global port
    global s
    host = "192.168.254.199"
    port = 55435
    s = socket.socket()
    def __init__(self, top=None):

        s.connect((host, port))
        info = s.recv(15360)
        info = info.decode()
        if info[:5] == "NAMES":
            info = info[6:].split("\n")
            
        def onSelect(event):
            try:
                s.connect(host, port)
            except:
                listVal = int(event.widget.curselection()[0])
                filename = info[listVal] #FILENAME
                self.head, self.sep, self.tail = filename.partition("...") # seperates filename from filesize, only head and tail are used
                self.finTail = self.tail.split("ZZ")[0] #converted filesize
                self.rawTail = self.tail.split("ZZ")[1] #raw filesize
                self.Label1.configure(font=("Terminal", 23), text=self.finTail)

         
       
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85' 
        _ana2color = '#d9d9d9' # X11 color: 'gray85' 
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("466x286+650+150")
        top.title("Sky Client v1.0")
        top.configure(background="#d9d9d9")
        top.configure(height="354")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")
        top.configure(width="493")



        self.Scrolledlistbox2 = ScrolledListBox(top)
        self.Scrolledlistbox2.place(relx=0.0, rely=0.0, relheight=1.0
                , relwidth=0.47)
        self.Scrolledlistbox2.configure(background="white")
        self.Scrolledlistbox2.configure(disabledforeground="#a3a3a3")
        self.Scrolledlistbox2.configure(font="TkFixedFont")
        self.Scrolledlistbox2.configure(foreground="black")
        self.Scrolledlistbox2.configure(highlightbackground="#d9d9d9")
        self.Scrolledlistbox2.configure(highlightcolor="#d9d9d9")
        self.Scrolledlistbox2.configure(selectbackground="#c4c4c4")
        self.Scrolledlistbox2.configure(selectforeground="black")
        self.Scrolledlistbox2.configure(width=10)
        
        filenames = []
        filesizes = []
        for entry in info:    
            self.ehead, self.esep, self.etail = entry.partition("...")
            self.Scrolledlistbox2.insert(tk.END, self.ehead)
            filenames.append(self.ehead)
            filesizes.append(self.etail)
        self.Scrolledlistbox2.bind("<<ListboxSelect>>", onSelect)
        
        self.TProgressbar1 = ttk.Progressbar(top)
        self.TProgressbar1.place(relx=0.49, rely=0.90, relwidth=0.49
                , relheight=0.0, height=22)
        

        self.Label1 = Label(top)
        self.Label1.place(relx=0.49, rely=0.1, height=100, width=224)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(activeforeground="black")
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(highlightbackground="#d9d9d9")
        self.Label1.configure(highlightcolor="black")
        self.Label1.configure(font=("Terminal", 23), text='''ROM
get!''')
        
        self.TButton1 = ttk.Button(top, text='''Download''', command = self.threadStarter)
        self.TButton1.place(relx=0.6, rely=0.52, height=55, width=126)
        self.TButton1.configure(takefocus="")
        
    def downloadFile(self, event=None):
        self.TProgressbar1['maximum'] = int(self.rawTail)
        pval = 0
        s.send(self.head.encode())
        self.data = s.recv(1024)
        self.data = self.data.decode()
        if self.data[:6] == "EXISTS":
            self.fileSize = int(self.data[6:])
            s.send(str.encode("OK"))
            self.f = open('new_'+self.head,'wb')
            self.data = s.recv(3000000) #was 8192
            pval = pval + len(self.data)
            self.TProgressbar1['value'] = pval
            self.TProgressbar1.update_idletasks()
            self.totalRecv = len(self.data)
            self.f.write(self.data)
            while self.totalRecv < self.fileSize:
                self.data = s.recv(11264)
                pval = pval + len(self.data)
                self.TProgressbar1['value'] = pval
                self.TProgressbar1.update_idletasks()
                self.totalRecv += len(self.data)
                self.f.write(self.data)
                #print( format((self.totalRecv/float(self.fileSize))*100, '0.2f') + "%")
            self.TProgressbar1['maximum'] = 0
            self.TProgressbar1['value'] = 0
            self.TProgressbar1.update_idletasks()
            self.f.close()  
    
    def threadStarter(self): #starts the downloadFile thread when download button is pressed.
        t = threading.Thread(target=self.downloadFile)
        t.start()




# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''

    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)

        #self.configure(yscrollcommand=_autoscroll(vsb),
        #    xscrollcommand=_autoscroll(hsb))
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))

        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        # Copy geometry methods of master  (taken from ScrolledText.py)
        if py3:
            methods = Pack.__dict__.keys() | Grid.__dict__.keys() \
                  | Place.__dict__.keys()
        else:
            methods = Pack.__dict__.keys() + Grid.__dict__.keys() \
                  + Place.__dict__.keys()

        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)

def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        return func(cls, container, **kw)
    return wrapped

class ScrolledListBox(AutoScroll, Listbox):
    '''A standard Tkinter Text widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        Listbox.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)
if __name__ == '__main__':        
    vp_start_gui()