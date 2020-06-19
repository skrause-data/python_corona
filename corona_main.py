# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 09:53:51 2020

@author: Tino Riebe, zusätzliche Autoren im Quelltext extra benannt
"""

BEVOELKERUNG = {'germany':83160000,'italy':60230000,'switzerland':8570000} 
LAENDERLIST  = ["germany","italy","switzerland"]

#%%
try:
    from tkinter import *
except:
    from Tkinter import *

import sys    

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter.filedialog as tkFileDialog

from time import sleep
import datetime
from datetime import date, timedelta

import api_import
import covid19api
import csv
#%%


class daten_laden:
    ''' Daten aus der Datenbank holen, testen ob ausreichend Werte vorhanden 
        sind, und das benötigte Lister erstellen bzw. Dummyliste'''
        
    germany=[]
    italy=[]
    switzerland=[]
    try:
        with open(r"D:\pyth\Projekt\germany.txt","x") as file:
            file.close()     
            germany=['2020-04-29,0']
    except:
        with open (r"D:\pyth\Projekt\germany.txt","rt") as file:
        
            reader=csv.reader(file, delimiter=',')
            for row in reader:
                germany.append(', '.join(row))
            file.close()
  
    
    try:
        with open(r"D:\pyth\Projekt\italy.txt","x") as file:
            file.close()     
            italy=['2020-04-29,0']
    except:
        with open (r"D:\pyth\Projekt\italy.txt","rt") as file:
        
            reader=csv.reader(file, delimiter=',')
            for row in reader:
                italy.append(', '.join(row))
            file.close()
       
        
    try:
        with open(r"D:\pyth\Projekt\switzerland.txt","x") as file:
            file.close()     
            switzerland=['2020-04-29,0']
    except:
        with open (r"D:\pyth\Projekt\switzerland.txt","rt") as file:
        
            reader=csv.reader(file, delimiter=',')
            for row in reader:
                switzerland.append(', '.join(row))
        
            file.close()

    
class save_Button(Button):
    ''' Daten in die Datenbank schreiben'''
    def save_new_data(self):
        l_info.config(text='Daten sichern')
        with open(r"D:\pyth\Projekt\germany.txt","w") as file:
            for i in range(0,len(germany)):
                file.write(germany[i])
                file.write('\n')
        file.close() 
        with open(r"D:\pyth\Projekt\italy.txt","w") as file:
            for i in range(0,len(italy)):
                file.write(italy[i])
                file.write('\n')
        file.close() 
        with open(r"D:\pyth\Projekt\switzerland.txt","w") as file:
            for i in range(0,len(switzerland)):
                file.write(switzerland[i])
                file.write('\n')
        file.close() 
  

class refresh_Button(Button):
    ''' neue Daten aus dem Internet ziehen, Übergabeparameter sind: 
        Länderliste und Datum des letzten Eintrags in der Datenbank,
        return-Werte: response-Code um Fehler abzufangen und neue Daten
        Da aktuell keine saubere Verbindung zur Datenbank vorliegt wird
        letzter Tage per Hand definiert
        +Stefan
    '''
    def refresh(self):
        
        
        l_info.config(text='Connecting to api',bg='white')
        sleep(1)
        
        ''' neue Daten holen'''
        
        lastday = date.today() - timedelta(days=7)
        lastday = str(lastday) + "T00:00:00Z"    


        germany = []

        new=covid19api.get_api("germany", lastday)
        html=new[1]
        list_api= new[0] 
  
        for i in range (0, len(list_api)):
            datestr = list_api[i]["Date"][0:10]
            germany += [datestr + ',' + str(list_api[i]["Cases"])]


        #Italien
        italy = []

        new=covid19api.get_api("italy", lastday)
        html=new[1]
        list_api= new[0] 
  
        for i in range (0, len(list_api)):
            datestr = list_api[i]["Date"][0:10]
            italy += [datestr + ',' + str(list_api[i]["Cases"])]
       
        #Schweiz    
    
        switzerland = []

        new=covid19api.get_api("switzerland", lastday)
        html=new[1]
        list_api= new[0] 
  
        for i in range (0, len(list_api)):
            datestr = list_api[i]["Date"][0:10]
            switzerland += [datestr + ',' + str(list_api[i]["Cases"])]
            
        l_warnung.config(text=[switzerland[1] + switzerland[2]])
       
       
def login(function):
   
    def function_wrapper(x):
        print(x)
        if x=='1':
            function(x)     
        else:
            l_info.config(text='Zugriff verweigert')
    return function_wrapper


def NewFile():
    ''' Möglichkeit neues Land hinzuzufügen, nur als Admin
    
    '''
    l_info.config(text='KONSOLENEINGABE',bg='green')
    
    class Passwort(Button):
        def action(self):
            pwd=Eing_pwd.get()
            return(pwd)
        
    admin=Tk()
    Label_pwd  = Label(admin,text='Passwort bitte:')
    Eing_pwd   = Entry(admin)
    Button_pwd = Passwort(admin,text='OK')
    Button_pwd['command']=Button_pwd.action
    Label_pwd.pack()
    Eing_pwd.pack()
    Button_pwd.pack()
    admin.mainloop()
        
    @login
    def zugriff(x):
        l_info.config(text='Zugriff erlaubt')
    zugriff(str(Button_pwd.action))
    
 

def OpenFile():
    ''' nicht belegt '''
    open_file= tkFileDialog.askopenfilename()
    fenster_name = tk.Label(fenster, text=open_file)
    open_file='k'
    return open_file

def plot(n='germany'):
    ''' Plot aktualiseren
        1. Versuch den alten Plot zu löschen
        2. neuen Plot erstellen und über Canvas an das Fenster übergeben
    '''
    try:
       canvas._tkcanvas.destroy()
    except:
        print('')
    fig = Figure(figsize = (9, 6), facecolor = "white")
    axis = fig.add_subplot(111)
    axis.plot(corona[n], "-r", label = n)
    axis.legend()
    axis.grid()
    canvas = FigureCanvasTkAgg(fig, master = fenster)
    canvas._tkcanvas.place( x=20, y=20, width=380, height =460) #side = tk.TOP, fill = tk.BOTH,expand = 1)
    return(fig)



def listbox_fuellen(land='germany'):
    '''
        Listbox füllen, Input ist das gewählte Land, Standard germany
        es werden Prozentwerte mitberechnet und ggf. eine Warnung ausgegeben
        +Rajan
    
    '''
    
    
    anzeige_listbox.delete(0,END)
    max_prozent=[]                   
    if land in corona:
        for n in range (1,len(corona[land])+1):
            if n>7:
                break
            prozent=round((corona[land][-n]/BEVOELKERUNG[land])*100,2)
            if prozent > 0.18:
                color = 'red'
            else:
                color = 'black' 
            prozentzuwachs=round((1-(corona[land][-(n+1)]/corona[land][-n]))*100,2)
            anzeige_listbox.insert(n-1,['Gesamt: %10d, Prozent: %2.2f, Zuwachs: %2.2f' %(int(corona[land][-n]),prozent,prozentzuwachs)])
            anzeige_listbox.itemconfig(n-1, fg=color)
            max_prozent.append(prozent)
        
        
    if max(max_prozent)>=0.2:
        l_info.config(text="Warnung, in " + land + ' sind mehr als 2% der Menschen infiziert!!! Ab in den Urlaub',bg='red')

    else:
        l_info.config(text='Alles noch i.O',bg='white')
       
    
#%% Daten holen, hier nur testweise, da Verbindung zur API nicht voll funktionsfähig

tmp=[]
#laenderlist = ["germany","italy","switzerland","france","spain","austria","netherlands"]
for i in range (0, len(LAENDERLIST) ):
    new=api_import.get_coronacases(LAENDERLIST[i])
    #new=api_corona.get_api('germany','2020-04-28T00:00:00Z')
    
    
    tmp.append(new)
corona={'germany':tmp[0],'italy':tmp[1],
        'switzerland':tmp[2]}


#%% Fenster

fenster = Tk()

fig=plot()

fenster_pos=[800,600,200,200]  # Größe und Lage des Fensters
fenster.title("Corona Fallzahlen")
fenster.wm_geometry("%dx%d+%d+%d" % (fenster_pos[0],fenster_pos[1],fenster_pos[2],fenster_pos[3]))
fenster.resizable(0,0)
fenster.transient()


b_exit          = Button(fenster, text="Beenden", command=fenster.destroy)

b_refresh       = refresh_Button(fenster, text="Refresh")
b_refresh['command']=b_refresh.refresh

b_speichern     = save_Button(fenster, text="Speichern")
b_speichern['command']= b_speichern.save_new_data
l_info          = Label(fenster, text='lfd. Infos')
l_warnung       = Label(fenster, text='akt.Meldungen',font=('Helvetica',8), fg='red')



#Listbox
anzeige_listbox=Listbox(width=60,height=10) #, yscrollcommand=scrollbar.set)
listbox_fuellen

# Pulldown
land = StringVar(fenster)
land.set(LAENDERLIST[0])
opt = OptionMenu(fenster, land, *LAENDERLIST)
opt.config(width=10, font=('Helvetica', 12))
opt.pack()

test_label = Label(text="", font=('Helvetica', 12), fg='red',)


''' verfolgen ob es in der Dropdownlist eine Änderung gab  '''
def callback(*args):
    
    land_select=land.get()
    listbox_fuellen(land.get())
    
    fig=plot(land.get())
    return fig
    
land.trace("w", callback)


# Filemenue
menu = Menu(fenster)
fenster.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=NewFile)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=fenster.destroy)


#%% Platzieren der Elemente

fenster.update()
width = fenster.winfo_width()  # 158
height = fenster.winfo_height()  # 174

''' 
adaptives Anpassen des Fensterinhalt an die aktuelle Fenstergröße noch 
nicht implementiert, daher Proportionalitätsfaktor=1 und Fenstergröße über 
resizable(0,0) festgesetzt
'''

prop=1


b_refresh.place(x=20/prop, y=500/prop, width=100/prop, height =50/prop)
b_speichern.place(x=140/prop, y=500/prop, width=100/prop, height =50/prop)
b_exit.place(x=260/prop, y=500/prop, width=100/prop, height =50/prop)
opt.place(x=420/prop, y=20/prop)
test_label.place(x=420/prop, y=60/prop)
anzeige_listbox.place(x=420/prop, y=100/prop)
l_info.place(x=20, y=580/prop, width=760/prop, height=20/prop)
l_warnung.place(x=420/prop, y=300/prop)
fenster.mainloop()