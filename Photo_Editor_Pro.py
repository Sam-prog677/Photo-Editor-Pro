#I still didn't 'upgrade' (haha, just let my code to be clearer) it yet, but I will
#when I have time... Please ignore that.

import os
import random
import re as rep
import sys
import time
import tkinter as tk
import tkinter.filedialog as tkFD
import winsound
from collections import Counter
from tkinter import *
from tkinter import Menu, Scrollbar, Text
from tkinter import messagebox as mbox
from tkinter import ttk

import itchat
import jieba.analyse
import PIL
from PIL import Image
from pyecharts import WordCloud
from removebg import RemoveBg
from skimage import data, io, transform

from functions.cut_funcs import *


class Notebook2(tk.Frame): # 继承Frame类的Notebook类
    def __init__(self, master=None,m=0,anchor=tk.NW, size=9,width=10,**kw):  
        tk.Frame.__init__(self, master,**kw)  
        self.tab1 = master #定义内部变量tab1
        self.m=m
        self.width=width
        self.size=size
        self.anchor=anchor
        self.s1=tk.TOP
        self.s2=tk.BOTTOM
        if (self.anchor in [tk.SW,tk.S,tk.SE]):
            self.s1=tk.BOTTOM
            self.s2=tk.TOP
        self.t=[]
        t=[]
        m2=self.m
        self.v=[]
        self.view=None
        self.pack(side=self.s2, fill=tk.BOTH, expand=1,ipady=1,pady=1,ipadx=1,padx=1)

        self.tab()


    def add(self,tab=None,text=''):
        global t,m2
        if (tab!=None):
            self.m=self.m+1
            m2=self.m
            def handler (self=self, i=self.m-1 ):
                self.select(i)
                self.select(i)
            
            if (self.anchor in [tk.NW,tk.N,tk.SW,tk.S]):
                self.button = tk.Button(self.tab, width=self.width,text=text, cursor='hand2',
                                        anchor=tk.S,
                                        font=('Arial', '%d'%self.size),
                                        command=handler,
                                        relief=FLAT,
                                        activebackground="white")
                self.t.append(self.button)
                t=self.t
                self.button.pack(side=tk.LEFT)
                self.v.append(tab)
                if (self.m==1):
                    self.select(0)


            if (self.anchor in [tk.NE,tk.SE]):
                self.button = tk.Button(self.tab, width=self.width,text=text, cursor='hand2',
                                        anchor=tk.S,
                                        font=('Arial','%d'%self.size),
                                        command=handler,
                                        relief=FLAT,
                                        activebackground="white")
                self.t.append(self.button)
                t=self.t
                self.button.pack(side=tk.RIGHT)
                self.v.append(tab)
                if (self.m==1):
                    self.select(0)


    def tab(self):
        self.tab=tk.Frame(self)
        if (self.anchor in [tk.N,tk.S]):
            self.tab.pack(side=self.s1)
        if (self.anchor in [tk.NW,tk.NE,tk.SW,tk.SE]):
            self.tab.pack(side=self.s1,fill=tk.X)

        
        for i in range(self.m):
            def handler (self=self, i=i ):
                self.select(i)
            self.button = tk.Button(self.tab, width=self.width,text='Tab%d'%i, cursor='hand2',
                                    anchor=tk.S,
                                    font=('Arial','%d'%self.size),
                                    command=handler,
                                    activebackground="white")
            self.t.append(self.button)
            t=self.t
            self.v.append(None)
            if (self.anchor in [tk.NW,tk.SW]) :
                self.button.pack(side=tk.LEFT)
            else:
                self.button.pack(side=tk.RIGHT)
            
        self.update()

         
    def frame(self):
        self.frame=tk.Frame(self,bd=2,
                            borderwidth=2,  #边框宽度
                            padx=1,  #部件x方向间距
                            pady=1, #部件y方向间距
                            )
        self.frame.pack(side=self.s2,fill=tk.BOTH, expand=1)         


    def select(self,x):
        global m2
        self.m=m2
        print(x)
        if (self.view!=None):
            self.view.pack_forget()
        for i in range(self.m):
            self.t[i]['relief']=tk.FLAT
            self.t[i]['anchor']=tk.S
            self.t[i]['bg']="#F0F0ED"
            
        self.t[x]['anchor']=tk.N
        self.t[x]['bg']='white'
        self.view=self.v[x]
        if (self.view!=None):
            self.view.pack(fill=tk.BOTH, expand=1)
        self.m=m2
        print(x)
        if (self.view!=None):
            self.view.pack_forget()
        for i in range(self.m):
            self.t[i]['relief']=tk.FLAT
            self.t[i]['anchor']=tk.S
            self.t[i]['bg']="#F0F0ED"
            
        self.t[x]['anchor']=tk.N
        self.t[x]['bg']='white'
        self.view=self.v[x]
        if (self.view!=None):
            self.view.pack(fill=tk.BOTH, expand=1)  


    def modify(self,x,tab=None,text=''):
        if (x>self.m-1):
            return
        if (tab!=None):
            self.v[x]=tab
        if (text!=''):
            self.t[x]['text']=text


root = tk.Tk()
root.iconbitmap("./pictures/icon.ico")
root.title("Photo Editor Pro")
root.minsize(900,700)
path = ()
rpath = ()
choose = False
text=StringVar()
text2 = StringVar()
text3 = StringVar()

def getway():
    global text
    filename = tkFD.askopenfilename()
    text.set(filename)
    path = text.get()
    if path != (''):
        global rpath
        rpath = path
        global choose
        choose = True

def getwaytab2():
    global text2
    filename = tkFD.askopenfilename()
    text2.set(filename)
    global path2
    path2 = text2.get()
    if path2 != (''):
        global rpath2
        rpath2 = path2
        global choose2
        choose2 = True

def getwaytab3():
    global text3
    filename = tkFD.askopenfilename()
    text3.set(filename)
    global path3
    path3 = text3.get()
    if path3 != (''):
        global rpath3
        rpath3 = path3
        global choose3
        choose3 = True

def close(tab,index):
    global t,m2
    index = t.pop(index)
    index.destroy()
    tab.destroy()
    m2-=1

def cut2(image_name):
    global choose
    global stbg,statusbar
    statusbar['text'] = 'Cutting Picture...'
    statusbar.update()
    #to make sure is it the type of file that can be cut
    if image_name == '':
        image_name = text.get()
        print(image_name+'done1')
    print(image_name+'done')
    if '.jpg'in image_name or '.jpeg'in image_name or '.png'in image_name or '.gif'in image_name or '.ico'in image_name:
        try:
            image = PIL.Image.open(image_name)
            image = fill_image(image)
            image_list = cut_image(image)
            save_images(image_list, image_name)
            statusbar['text'] = 'Picture Cut Successfully'
            statusbar.update()
        except FileNotFoundError:
            statusbar['text'] = 'File Not Found'
            statusbar.update()
    else:
        statusbar['text'] = 'Failed to Cut Picture'
        statusbar.update()
    time.sleep(2.0)
    statusbar['text'] = 'Ready'
    statusbar.update()

def loginAndSend():
    statusbar['text'] = 'Sending Pictures to Wechat(To File Transfer)...'
    statusbar.update()
    itchat.auto_login(hotReload=True)
    itchat.send("Sending pictures from Photo Editor Pro...(Total 9 pictures)",toUserName="filehelper")
    for i in range(1,11):
        itchat.send_image("./output/output"+str(i)+".png",toUserName="filehelper")
        statusbar['text'] = 'Sending The '+str(i)+"th Picture..."
        statusbar.update()
    itchat.send("Done.",toUserName="filehelper")
    statusbar['text'] = 'Pictures Sended.'
    statusbar.update()
    time.sleep(2.0)
    statusbar['text'] = 'Ready'
    statusbar.update()

def cut_new():
    global cut_tab,tabControl,word_text,t
    if len(t)<=8:
        global stbg,statusbar
        statusbar['text'] = 'Ready'
        statusbar.update()
        cut_tab = Frame(tabControl)
        tabControl.add(cut_tab,text="Cut Photos")

        lb = ttk.Label(cut_tab,text="Cut Photos",font=("Arial",30))
        lb.place(x=100,y=50)
        tip3_tt = ("No photos to choose when using Wechat-Moments?\nDon't worry, just choose one picture and cut it to nine photos right here!")
        tip3_lb = ttk.Label(cut_tab,text=tip3_tt,wraplength=500,font=("Arial",13),justify = 'left')   
        tip3_lb.place(x=100,y=120)
        word_text = ttk.Entry(cut_tab,background = 'white',width = 25,textvariable = text)
        word_text.place(x=100,y=210)
        chbt = Button(cut_tab,text="Choose Photo",command=getway,relief=GROOVE,cursor='hand2')
        chbt.place(x=350,y=209)
        cut_bt = Button(cut_tab,text="Cut Photo",command=lambda : cut2(rpath or text.get()),relief=GROOVE,cursor='hand2')
        cut_bt.place(x=350,y=250)#effect picture
        send_bt = Button(cut_tab,text="Send to\nWechat",command=loginAndSend,relief=GROOVE,cursor='hand2')
        send_bt.place(x=100,y=250)
        efplb = ttk.Label(cut_tab,text="Tip for You:\nYou can choose pictures that are colorful and have lots of things to cut. Don't choose pictures with only one or two things.",font=("Arial",13),wraplength=500,justify='left')
        efplb.place(x=100,y=350)
        copy = ttk.Label(cut_tab,text="Copy Right © 2019-2020 Sam Tech.co.,Inc.",font=("Arial",10))
        copy.place(x=1000,y=700)
        cut_tab.update()

def removebg(picture):
    global stbg,statusbar
    statusbar['text'] = 'Removing Background...'
    statusbar.update()
    rmbg = RemoveBg("V9TBQtaer***************(your_secret_number)", "error.log")
    rmbg.remove_background_from_img_file(picture)
    statusbar['text'] = 'Removed Background Successfully'
    statusbar.update()
    time.sleep(1.0)
    statusbar['text'] = 'Ready'
    statusbar.update()

def rescale(picture,x):
    '''A moudle to resize the images. Used to the "Photo Zoom".
    Uses the skimage package. Needs to input image. Needs pictures that are PNG or GIF.'''
    global stbg,statusbar
    statusbar['text'] = 'Resacling Picture...'
    statusbar.update()
    try:
        img = io.imread(picture)
    except:
        statusbar['text'] = 'Unknown Type of Picture. Please Enter Pictures With PNG or GIF Type.'
        statusbar.update()
        return "NEED_PNG"
    else:
        _type=type(img)
        print(_type)
        new_img = transform.rescale(img,[float(x),float(x)])
        output=picture
        print(output[0:output.rfind('.',1)])
        print(output[output.rfind('.',1):])
        input_type=output[output.rfind('.',1):]
        output=output[0:output.rfind('.',1)]
        output+="_resized_"+str(x)+"x"
        output+=input_type
        io.imsave(output,new_img)
        statusbar['text'] = 'Rescaled Picture Successfully'
        statusbar.update()
    time.sleep(2.0)
    statusbar['text'] = 'Ready'
    statusbar.update()

# 将counter拆分成两个list
def counter2list(counter):
    keyList,valueList = [],[]
    for c in counter:
        keyList.append(c[0])
        valueList.append(c[1])
    return keyList,valueList

# 使用jieba提取关键词并计算权重
def extractTag(content,tagsList):
    keyList,valueList = [],[]
    if content:
        tags = jieba.analyse.extract_tags(content, topK=100, withWeight=True)
        for tex, widget in tags:
            tagsList[tex] += int(widget*10000)

def drawWorldCloud(content,count):
    name = random.randint(0,9999)
    outputFile = './'+str(name)+'.html'
    cloud = WordCloud('', width=1000, height=600, title_pos='center')
    cloud.add(
        ' ',content,count,
        shape='cardioid',
        background_color='white',
        max_words=200 
    )
    cloud.render(outputFile)

def wordCloudMaker(txt=None):
    '''WordCloud maker. Needs to give the text that will turn to wordcloud.
    Uses pyecharts as the main maker. \n
    Param txt: the text file that needs to make wordcloud.
    Used in "Cloud Maker".'''
    c = Counter()   #建一个容器
    filePath = txt   #分析的文档路径
    with open(filePath) as file_object:
        contents = file_object.read()
        extractTag(contents, c)

    contentList,countList = counter2list(c.most_common(1000))
    drawWorldCloud(contentList, countList)

def remove_new():
    global re_tab,tabControl,word_text2,t,stbg,statusbar
    if len(t)<=8:
        global stbg,statusbar
        statusbar['text'] = 'Ready'
        statusbar.update()
        re_tab = Frame(tabControl)
        tabControl.add(re_tab,text="Remove Bg")
        lb3 = ttk.Label(re_tab,text="Remove Background",font=("Arial",30))
        lb3.place(x=100,y=50)
        tip3_tt = ("Want a clear photo with white background?\nDon't waste your money on the bla-bla website! Try out this! Free remove-bg and up to 50 photos per month!")
        tip3_lb = ttk.Label(re_tab,text=tip3_tt,wraplength=500,font=("Arial",13),justify = 'left')   
        tip3_lb.place(x=100,y=120)
        word_text2 = ttk.Entry(re_tab,background = 'white',width = 25,textvariable = text2)
        word_text2.place(x=100,y=210)
        chbt = Button(re_tab,text="Choose Photo",command=getwaytab2,relief=GROOVE,cursor='hand2')
        chbt.place(x=350,y=209)
        chbt.update()
        cut_bt = Button(re_tab,text="Remove\nBackground",command=lambda : removebg(rpath2 or text2.get()),relief=GROOVE,cursor='hand2')
        cut_bt.place(x=350,y=250)#effect picture
        efplb = ttk.Label(re_tab,text="Tip for You:\nYou may choose pictures with more bigger things, not a photo with things like stars or a lake.",font=("Arial",13),wraplength=500,justify='left')
        efplb.place(x=100,y=350)
        copy = ttk.Label(re_tab,text="Copy Right © 2019-2020 Sam Tech.co.,Inc.",font=("Arial",10))
        copy.place(x=1000,y=700)
        re_tab.update()

def rescale_new():
    global res_tab,tabControl,word_text3,t,stbg,statusbar,rpath3,text3
    if len(t)<=8:
        global stbg,statusbar
        statusbar['text'] = 'Ready'
        statusbar.update()
        res_tab = Frame(tabControl)
        tabControl.add(res_tab,text="Photo Zoom")
        lb3 = ttk.Label(res_tab,text="Photo Zoom",font=("Arial",30))
        lb3.place(x=100,y=50)
        tip3_tt = ("Want to rescale pictures but turned out to be messy?\nDon't worry, our Photo Zoom service will make your dream come true! You can make photos bigger(up to 4x) and it's free!\nWhat are you waiting for? Just do it!")
        tip3_lb = ttk.Label(res_tab,text=tip3_tt,wraplength=500,font=("Arial",13),justify = 'left')   
        tip3_lb.place(x=100,y=120)
        word_text3 = ttk.Entry(res_tab,background = 'white',width = 25,textvariable = text3)
        word_text3.place(x=100,y=220)
        chbt = Button(res_tab,text="Choose Photo",command=getwaytab3,relief=GROOVE,cursor='hand2')
        chbt.place(x=350,y=219)
        chbt.update()
        value = (0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0)
        cmb = ttk.Combobox(res_tab)
        cmb.place(x=100,y=280)
        cmb['value'] = value
        cmb.current(1)
        cmb.update()
        cut_bt = Button(res_tab,text="Rescale\nPicture",command=lambda : rescale(rpath3 or text3.get(),cmb.get()),relief=GROOVE,cursor='hand2')
        cut_bt.place(x=350,y=260)#effect picture
        efplb = ttk.Label(res_tab,text="Tip for You:\nYou may choose pictures with clear things, than it will turned out to be better after resizing.",font=("Arial",13),wraplength=500,justify='left')
        efplb.place(x=100,y=350)
        copy = ttk.Label(res_tab,text="Copy Right © 2019-2020 Sam Tech.co.,Inc.",font=("Arial",10))
        copy.place(x=1000,y=700)
        res_tab.update()
        time.sleep(1.0)
        statusbar['text'] = 'Ready'
        statusbar.update()
        res_tab.update()
    

def settings():
    global se_tab,t
    if len(t)<=8:
        global stbg,statusbar
        statusbar['text'] = 'Ready'
        statusbar.update()
        se_tab = ttk.Frame(tabControl)
        se_tab.update()
        tabControl.add(se_tab,text="Settings")
        lb = ttk.Label(se_tab,text="Settings",font=("Arial",30))
        lb.place(x=100,y=50)
        tip3_tt = ("Not done yet.")
        tip3_lb = ttk.Label(se_tab,text=tip3_tt,wraplength=500,font=("Arial",13),justify = 'left')   
        tip3_lb.place(x=100,y=120)
        copy = ttk.Label(se_tab,text="Copy Right © 2019-2020 Sam Tech.co.,Inc.",font=("Arial",10))
        copy.place(x=1000,y=700)
        se_tab.update()
        se_tab.update()

#cut 函数

def welcome_():
    global tabControl
    tab1 = tk.Frame(tabControl)  #增加新选项卡
    tabControl.add(tab1,text='Welcome')

    welcome = ttk.Label(tab1,text="Welcome to Photo Editor",font=("Arial",40))
    welcome.place(x=100,y=50)
    welcome_text = ("This is a photo editor tool.\nWe are tring to make photo-edit easier."
                    "You can remove background and cut your photos in 9 pieces here.")

    welcome_text_lb = ttk.Label(tab1,text=welcome_text,font=("Arial",13),wraplength = 500,justify = 'left')
    welcome_text_lb.place(x=100,y=150)

    tip = ttk.Label(tab1,text="Edit Your Photos",font=("Arial",20))
    tip.place(x=100,y=230)

    tip_text = ("We can give you lots of things. More tools are in the mood to get in to the app."
                "If you think we can do anything better, please tell us in the message box.")

    tip_lb = ttk.Label(tab1,text=tip_text,font=("Arial",13),wraplength=500,justify='left')
    tip_lb.place(x=100,y=280)

    tip2 = ttk.Label(tab1,text="Start Editing!",font=("Arial",20))
    tip2.place(x=100,y=360)

    tip2_text = ("Since you know how to use our app, it is time to get started! Find out the fun"
                " when you are editing your photos! Hope you have a good time while using our app.")
    tip2_lb = ttk.Label(tab1,text=tip2_text,font=("Arial",13),wraplength=500,justify='left')
    tip2_lb.place(x=100,y=420)

    copy = ttk.Label(tab1,text="Copy Right © 2019-2020 Sam Tech.co.,Inc.",font=("Arial",10))
    copy.place(x=1000,y=700)
    print("go")
    tab1.update()
tabControl=Notebook2(root,anchor=tk.NE)
tab1 = tk.Frame(tabControl)  #增加新选项卡
tabControl.add(tab1,text='Welcome',)
lb = Label(root,bg="dimgrey",text='')
lb.place(x=0,y=0,height=1000,width=50)
cutimg = PhotoImage(file="./pictures/cut.GIF")
cut = Button(root,image=cutimg,relief=FLAT,bg="dimgrey",cursor='hand2',activebackground="dimgrey",command=cut_new)
cut.place(x=6,y=80)
cutlb = Label(root,text="Cut\nPhotos",fg="white",bg="dimgrey",font=("Arial",7))
cutlb.place(x=6,y=115)
reimg = PhotoImage(file="./pictures/remove.GIF")
re = Button(root,image=reimg,relief=FLAT,bg="dimgrey",cursor='hand2',activebackground="dimgrey",command=remove_new)
re.place(x=6,y=140)
relb = Label(root,text="Remove\nBg",fg="white",bg="dimgrey",font=("Arial",7))
relb.place(x=5,y=175)
seimg = PhotoImage(file="./pictures/settings.GIF")
settingsbt = Button(root,image=seimg,relief=FLAT,bg="dimgrey",command=settings,cursor='hand2',activebackground='dimgrey')
settingsbt.place(x=6,y=270)
selb = Label(root,text="Settings",fg="white",bg="dimgrey",font=("Arial",7))
selb.place(x=5,y=305)
zoimg = PhotoImage(file="./pictures/zoomin.GIF")
zo = Button(root,image=zoimg,relief=FLAT,bg="dimgrey",cursor='hand2',activebackground="dimgrey",command=rescale_new)
zo.place(x=6,y=210)
zolb = Label(root,text=" Photo\n Zoom",fg="white",bg="dimgrey",font=("Arial",7))
zolb.place(x=5,y=245)
iconimg = PhotoImage(file="./pictures/icon.GIF")
iconbt = Button(root,image=iconimg,relief=FLAT,bg='dimgrey',cursor='hand2',command=welcome_,activebackground='dimgrey')
iconbt.place(x=6,y=10)
root.minsize(900,700)

welcome = Label(tab1,text="Welcome to Photo Editor",font=("Arial",40))
welcome.place(x=100,y=50)
welcome_text = ("This is a photo editor tool.\nWe are tring to make photo-edit easier."
                "You can remove background and cut your photos in 9 pieces here.")

welcome_text_lb = Label(tab1,text=welcome_text,font=("Arial",13),wraplength = 500,justify = 'left')
welcome_text_lb.place(x=100,y=150)

tip = Label(tab1,text="Edit Your Photos",font=("Arial",20))
tip.place(x=100,y=230)

tip_text = ("We can give you lots of things. More tools are in the mood to get in to the app."
            "If you think we can do anything better, please tell us in the message box.")

tip_lb = Label(tab1,text=tip_text,font=("Arial",13),wraplength=500,justify='left')
tip_lb.place(x=100,y=280)

tip2 = Label(tab1,text="Start Editing!",font=("Arial",20))
tip2.place(x=100,y=360)

tip2_text = ("Since you know how to use our app, it is time to get started! Find out the fun"
            " when you are editing your photos! Hope you have a good time while using our app.")
tip2_lb = Label(tab1,text=tip2_text,font=("Arial",13),wraplength=500,justify='left')
tip2_lb.place(x=100,y=420)
def callback():
    print("~被调用了~")

def _about():
    about = Toplevel()
    about.geometry("500x580")
    about.title("Photo Editor Pro - About")
    about_text = ("This is an app to help edit image files. Its author is Sam Zhang."
                "For remove background, this app uses the Removebg Api. For cut pictures,"
                "it uses code from the Zhihu Website. For the Gui building, we chose Python"
                " Tkinter as the Gui package.\n\nNow at here, I will say thank you to"
                "all the programmers that code the Removebg Api, thanks to the user on"
                "Zhihu for sharing the code, and all the programmers that made Tkinter, "
                "and thanks for Python this amazing thing.\n\nThis app is made by Sam."
                "Tech.co.,Inc. For more things, please look at the following.\n\n"
                "App Name: Photo Editor Pro\n\nCompany: Sam.Tech.co.,Inc.\n\nAuthor: Sam Zhang"
                "\n\nPost Date: 2019.10.1\n\nVersion: 1.1.0\n\nCompany Website: None\n\n"
                "Remove Background Api: Powered by the Removebg Api\n\nCode for Cut Pictures: "
                "Gived By a User on Zhihu\n\nGui: Powered By the Python Tkinter Gui Package\n\n"
                "App Type: Free\n\nFor more, please view the code.(Cutpro.py)")
    lb = Label(about,text=about_text,wraplength=450,font=("Arial",10),justify='left')
    lb.place(x=25,y=25)

 
mb = tk.Menubutton(root, text="File", relief=tk.FLAT,cursor='hand2')
mb.place(x=50,y=0)
mb2 = tk.Menubutton(root,text='Help',relief=FLAT,cursor='hand2')
mb2.place(x=85,y=0)
filemenu = tk.Menu(mb, tearoff=False)
filemenu.add_command(label="Exit", command=root.quit,font=("Arial",9),accelerator='Ctrl+E')
mb.config(menu = filemenu)
root.bind_all("<Control-e>", lambda event: root.quit())
root.bind_all("<Control-a>", lambda event: _about())
helpmenu = Menu(mb2,tearoff=False)
helpmenu.add_command(label='About',command=_about,font=("Arial",9),accelerator='Ctrl+A')
mb2.config(menu=helpmenu)
copy = Label(tab1,text="Copy Right © 2019-2020 Sam Tech.co.,Inc.",font=("Arial",10))
copy.place(x=1000,y=700)
tab1.update()
def GetSize(event):
    global statusbar
    root.update()
    statusbar.place(x=50,y=root.winfo_height()-20)
    statusbar.update()
    stbg.place(x=50,y=root.winfo_height()-20,height=30,width=3000)
stbg = tk.Label(root,text='',bg='Royalblue')
stbg.place(x=50,y=680,height=30,width=3000)
stbg.update()
statusbar = tk.Label(root,text='Ready',bg='Royalblue',anchor=SW)
statusbar.place(x=50,y=680)
root.bind('<Configure>', GetSize)
root.mainloop()
