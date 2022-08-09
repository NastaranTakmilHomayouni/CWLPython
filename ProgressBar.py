from tkinter import *
from tkinter.ttk import *
import time
#step=1
#total=100
#ch=1
#n_channels=76
window = Tk()
window.geometry("350x150+500+250")
f1 = Frame(window, height=50, width=50)
f1.pack()
progress_var = DoubleVar()
#bar = Progressbar(window, orient=HORIZONTAL,variable=progress_var, length=300)
bar =Progressbar(window, orient=HORIZONTAL, length=300)
bar.pack(pady=10)
step=0
lim1=1116
lim2=1116
residual = lim2 - lim1 + 1
message = ''
n_channels = 76
total = n_channels * lim2 * 2

#def Progress(step,total,ch,n_channels):
for i in range(100):
    step=step+1
    time.sleep(0.5)
    steptostr = str((step / total) * 100)
    bar['value']+=step/total*100

    #progress_var.set(step/total*100)
    #steptostr = str((5 / 100) * 100)
    text = StringVar()
    #text.set("Applying Changes ( Channel " + str(1) + "/" + str(76) + ") Total Progress" + steptostr + "%")
    #taskLabel = Label(window, textvariable=text).pack()
    #window.after(1000, Progress)
    window.update_idletasks()
    #window.mainloop()
#Progress(5,100,1,76)
#window.after(1000, Progress(5,100,1,76))

#Progress(8,100,1,76)
#Progress(9,100,1,76)

window.mainloop()
