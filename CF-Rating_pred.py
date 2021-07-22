#!/usr/bin/env python
# coding: utf-8

# In[7]:


from tkinter import *
from tkinter.ttk import *
import matplotlib.pyplot as plt
import urllib.request
from sklearn.model_selection import train_test_split
import numpy as np
import urllib, ast
import math
import validators, requests
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)


# In[8]:


def cal():
    url = "https://codeforces.com/api/contest.ratingChanges?contestId="+str(n1.get())
    try:
        file = urllib.request.urlopen(url)
        old = [] #stores old ratings
        new = [] #stores new ratings
        for line in file:
            dic = line.decode("utf-8")
            dic = ast.literal_eval(dic)
            l = dic.get("result")
            for i in l:
                o = i.get("oldRating")
                old.append(o)
                n = i.get('newRating')
                new.append(n)
        train_x, valid_x, train_y, valid_y = train_test_split(old, new, test_size=0.3, random_state = 42)
        # Testing for best polynomial function
        per = []
        for i in range(1,20):
            weights = np.polyfit(train_x, train_y, i)
            # Generating model with the given weights
            model = np.poly1d(weights)
            # Prediction on validation set
            pred = model(valid_x)
            perc = 0
            for i in range(len(pred)):
                perc+=abs(pred[i]-valid_y[i])/valid_y[i]
            per.append(perc/len(pred))
        fig = Figure(figsize = (5, 5),dpi = 100)
        plot1 = fig.add_subplot(111)
        weights1 = np.polyfit(train_x, train_y, 1+per.index(min(per)))
        model1 = np.poly1d(weights1)
        if int(n2.get()) >=min(old) and int(n2.get())<= max(old):
            myText.set(math.ceil(model1(int(n2.get()))))
        else:
            myText.set(int(n2.get()))
        pred1 = model1(valid_x)
        xp = np.linspace(min(valid_x),max(valid_x))
        pred_plot = model1(xp)
        plot1.scatter(valid_x, valid_y, facecolor='Red', edgecolor='k', alpha=0.1)
        plot1.plot(xp, pred_plot)
        canvas = FigureCanvasTkAgg(fig,master = window)
        canvas.draw()
        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().grid(row=5,column=1, ipadx=20, ipady=10)

        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas,window)
        toolbar.update()

        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().pack()
    except urllib.error.HTTPError as e:
        x = "HTTP Error "+str(e.code)
        myText.set(x)


# In[9]:


window = Tk()
myText=StringVar()
style = Style()
style.configure('W.TButton', font = ('Helvetica', 10, 'bold'), foreground = 'blue', background='#fff',borderwidth=18)
window.geometry("500x500")
window.title(" CF Rating Predictor")
Label(master=window, text="Contest Code",font=('Helvetica', 10), foreground = '#000000', background='gold').grid(row=0, sticky=W,padx=7)
Label(master=window, text="Old Rating",font=('Helvetica', 10), foreground = '#000000', background='gold').grid(row=1, sticky=W, ipadx=9,padx=7)
Label(master=window, text="New Rating:",font=('Helvetica', 10), foreground = '#000000', background='gold').grid(row=2, sticky=W,ipadx=5,padx=7)
result=Label(master=window, text="", textvariable=myText,font=('Helvetica', 12,'bold','underline'), foreground = 'red').grid(row=2, column=1)
n1 = Entry(window)
n2 = Entry(window)
n1.grid(row=0, column=1, pady = 5)
n2.grid(row=1, column=1, pady = 5)
b = Button(master=window, text="Ready", command = cal,style = 'W.TButton')
b.grid(row=3, column=2,columnspan=2, rowspan=2,sticky=W+E+N+S, padx=1, pady=1)
mainloop()


# In[ ]:





# In[ ]:





# In[ ]:




