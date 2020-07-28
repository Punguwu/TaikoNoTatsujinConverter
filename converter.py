# by pungu
# idk how to code help

from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from PIL import ImageTk, Image, ImageFilter, ImageEnhance
from pydub import AudioSegment
import os

root = Tk()

# makes paths for world and osu! song folder
path = os.path.expanduser('~')
path1 = os.path.join(path, 'AppData\\Local\\osu!\\Songs')
path2 = os.path.join(path, "AppData\\Roaming\\.minecraft\\saves\\Taiko no Tatsujin (MC Edition)"
                           "\\datapacks\\Taiko""\\data\\taiko\\functions")
path3 = os.path.join(path, "AppData\\Roaming\\.minecraft\\resourcepacks\\Taiko (Resources)\\assets\\minecraft\\sounds")


# gets file
def command1():
    filename = filedialog.askopenfilename(initialdir=path1, title='Select .osu File',
                                          filetypes=(("osu", "*.osu"), ("all files", "*.*")))
    e.delete(0, END)
    e.insert(0, str(filename).replace("/", "\\"))

    # sets image and text
    with open(filename, encoding="utf8") as file:
        data = file.read()
        base = os.path.basename(filename)

        try:
            bg = (data.partition("[Events]")[2].partition("0,0,")[2]).partition("\n")[0].split("\"")[1]
            bgdir = str(filename).replace(base, bg).replace("/", "\\")
        except IOError:
            bgdir = "resources/noimage.jpg"

        title = data.partition("Title:")[2].split("\n")[0]
        artist = data.partition("Artist:")[2].split("\n")[0]
        diff = data.partition("Version:")[2].split("\n")[0]

    canvas = Canvas(root, background='#24222a', height=165, width=490, highlightthickness=0)
    canvas.place(x=42, y=30)
    try:
        bg = Image.open(bgdir)
    except:
        bg = Image.open("resources/noimage.jpg")
    bg = bg.resize((612, 344), Image.ANTIALIAS)
    bg = bg.filter(ImageFilter.GaussianBlur(radius=2))
    enhance = ImageEnhance.Brightness(bg)
    enhanceimg = enhance.enhance(.75)
    canvas.image = ImageTk.PhotoImage(enhanceimg)
    canvas.create_image(245, 82, image=canvas.image, anchor='center')

    canvas.create_text(2, 100, text=title, font=('Aller', 25, 'bold'), fill='White', anchor='w')
    canvas.create_text(5, 130, text=artist, font=('Aller', 15, 'bold'), fill='White', anchor='w')
    canvas.create_text(5, 150, text=diff, font=('Aller', 10, 'bold'), fill='White', anchor='w')


# gets file
def command2():
    filename = filedialog.askdirectory(initialdir=path2, title='Select File')
    e1.delete(0, END)
    e1.insert(0, str(filename).replace("/", "\\"))


# gets file
def command3():
    filename = filedialog.askdirectory(initialdir=path3, title='Select File')
    e2.delete(0, END)
    e2.insert(0, str(filename).replace("/", "\\"))


# displays scale value in label
def command4(val):
    text4['text'] = round(float(val), 2)


def conversion():
    osupath = e.get()
    multiplier = round(mult.get(), 2)
    functionpath = e1.get()
    soundpath = e2.get()
    sound = var.get()

    try:
        with open(osupath, encoding="utf8") as file:
            newchart = os.path.join(functionpath, "chart.mcfunction")
            newchart = open(newchart, 'w+')
            data = file.read()
            base = os.path.basename(osupath)

            # gets slider stuff
            sv = data.partition("SliderMultiplier:")[2].split("\n")[0]
            timingpoints = data.partition("[TimingPoints]")[2]
            timingpoints = timingpoints.partition('\n\n')[0].split('\n')
            del timingpoints[0]
            lc1 = len(timingpoints)
            timinglist = []
            i = 0
            while i < lc1:
                bpm = timingpoints[i].split(',')[1]
                timingtick = str(round(float(timingpoints[i].split(',')[0])))
                if float(bpm) > 0:
                    bpm = str(round(60000 / float(bpm)))
                    timinglist.append(timingtick + ',' + bpm)

                i = i + 1
            listcount = len(timinglist)
            bpm = timinglist[0].split(',')[1]

            # sound
            if sound == 1:
                mp3 = data.partition("AudioFilename: ")[2].split("\n")[0]
                mp3path = str(osupath).replace(base, mp3).replace("/", "\\")
                audio = os.path.join(soundpath, "audio.ogg")
                AudioSegment.from_mp3(mp3path).export(audio, format='ogg')

            # title and artist
            title = data.partition("Title:")[2].split("\n")[0].replace('"', '\\"')
            artist = data.partition("Artist:")[2].split("\n")[0].replace('"', '\\"')

            # scroll speed and other stuff
            tpspeed = str((multiplier * .275))
            start = str(round((1 / multiplier) * 52))
            # writes stuff in file
            newchart.write('scoreboard players add @p chart 1\nexecute as @e[tag=note] at @s run tp @s ~ ~ ~-' + tpspeed
                           + '\nexecute if score @p chart matches ' + start +
                           ' as @p at @s run playsound minecraft:song master @s ~ ~ ~ .5 1 '
                           '.5\ntitle @p actionbar [{"text":"Now Playing: "'
                           ',"color":"white","bold":false,"italic":false,'
                           '"underlined":false,"strikethrough":false,"obfuscated":false},{"text":"' + title + ' - ' +
                           artist + '","color":"yellow''","bold":true,"italic":false,"underlined":false,"strikethrough"'
                                    ':false,"obfuscated":false},''{"text":" Score: ","color":"white","bold":false,"ital'
                                    'ic":false,"underlined":false,"striketh''rough":false,"obfuscated":false},{"score":'
                                    '{"name":"@p","objective":"score"},"color":"yellow''","bold":false,"italic":false,'
                                    '"underlined":false,"strikethrough":false,"obfuscated":false},''{"text":" Combo: "'
                                    ',"color":"white","bold":false,"italic":false,"underlined":false,"striketh''rough"'
                                    ':false,"obfuscated":false},{"score":{"name":"@p","objective":"combo"},"color":"ye'
                                    'llow''","bold":false,"italic":false,"underlined":false,"strikethrough":false,"ob'
                                    'fuscated"'':false}]\n')

            objects = data.partition("[HitObjects]")[2]
            lc = int(len(objects.split("\n"))) - 2
            i = 1

            # conversion
            while i <= lc:
                objectsline = objects.split("\n")[i]
                tick = objectsline.split(",")[2]
                ticks = round(int(tick) / 50 + 1)
                type1 = int(objectsline.split(",")[3])
                hitsound = int(objectsline.split(",")[4])

                i1 = 0

                try:
                    while float(timinglist[i1].split(',')[0]) > float(tick):
                        bpm = timinglist[i1].split(',')[1]
                        i1 = i1 + 1
                except IndexError:
                    bpm = timinglist[i1 - 1].split(',')[1]

                if type1 > 12:
                    type1 = int(str(type1)[1])

                # converts type number to type
                typedict = {
                    0: 'slider',
                    1: 'hitcircle',
                    2: 'slider',
                    3: 'hitcircle',
                    4: 'slider',
                    5: 'hitcircle',
                    6: 'slider',
                    7: 'hitcircle',
                    8: 'slider',
                    9: 'hitcircle',
                    10: 'slider',
                    11: 'hitcircle',
                    12: 'spinner'
                }

                type1 = typedict[type1]
                # converts hitsound number to type
                hitsounddict = {
                    0: 'don',
                    2: 'ka',
                    4: 'bigdon',
                    6: 'bigka',
                    8: 'ka',
                    10: 'ka',
                    12: 'bigka',
                    14: 'bigka'
                }
                hitsound = hitsounddict[hitsound]

                # converts to taiko
                idkwhattocallthis = {
                    'hitcircle': {
                        'don': 'don',
                        'ka': 'ka',
                        'bigdon': 'bigdon',
                        'bigka': 'bigka'
                    },
                    'slider': {
                        'don': 'slider',
                        'ka': 'slider',
                        'bigdon': 'bigslider',
                        'bigka': 'bigslider'
                    },
                    'spinner': {
                        'don': 'spinner',
                        'ka': 'spinner',
                        'bigdon': 'spinner',
                        'bigka': 'spinner'
                    }
                }

                type1 = (idkwhattocallthis[type1][hitsound])

                # prints commands on .mcfuntion file
                if type1 == 'don':
                    newchart.write("execute if score @p chart matches " + str(ticks) +
                                   " run summon armor_stand 18 8 16 {Invisible:1b,Tags:[\"note\",\"don\"],Pose:{Head:"
                                   "[0f,90f,0f]},ArmorItems:[{},{},{},{id:\"minecraft:diamond_hoe\",Count:1b,tag:"
                                   "{Unbreakable:1b,Damage:1}}]}\n")
                elif type1 == 'ka':
                    newchart.write("execute if score @p chart matches " + str(ticks) +
                                   " run summon armor_stand 18 8 16 {Invisible:1b,Tags:[\"note\",\"ka\"],"
                                   "Pose:{Head:[0f,90f,0f]},ArmorItems:[{},{},{},{id:\"minecraft:diamond_hoe\","
                                   "Count:1b,tag:{Unbreakable:1b,Damage:2}}]}\n")
                elif type1 == 'bigdon':
                    newchart.write("execute if score @p chart matches " + str(ticks) +
                                   " run summon armor_stand 18 8 16 {Invisible:1b,Tags:[\"note\",\"don\",\"big\"],"
                                   "Pose:{Head:[0f,90f,0f]},ArmorItems:[{},{},{},{id:\"minecraft:diamond_hoe\","
                                   "Count:1b,tag:{Unbreakable:1b,Damage:6}}]}\n")
                elif type1 == 'bigka':
                    newchart.write("execute if score @p chart matches " + str(ticks) +
                                   " run summon armor_stand 18 8 16 {Invisible:1b,Tags:[\"note\",\"ka\",\"big\"],Pose:"
                                   "{Head:[0f,90f,0f]},ArmorItems:[{},{},{},{id:\"minecraft:diamond_hoe\",Count:1b,tag:"
                                   "{Unbreakable:1b,Damage:7}}]}\n")
                elif type1 == 'slider':
                    sliderrepeat = objectsline.split(',')[6]
                    sliderlength = objectsline.split(',')[7]
                    slidertick = round(
                        (round((600 * (float(sliderlength) * float(sliderrepeat)) / (float(bpm) * float(sv))))
                         + float(tick)) / 50 + 1)

                    newchart.write("execute if score @p chart matches " + str(ticks) +
                                   " run summon armor_stand 18 8 16 {Invisible:1b,Tags:[\"note\",\"slider\",\"big\"],"
                                   "Pose:{Head:[0f,90f,0f]},ArmorItems:[{},{},{},{id:\"minecraft:diamond_hoe\",Count:1b"
                                   ",tag:{Unbreakable:1b,Damage:11}}]}\nexecute if score @p chart matches " +
                                   str(ticks + 1) + ".." + str(slidertick - 1) +
                                   " run summon armor_stand 18 8 16 {Invisible:1b,Tags:[\"note\",\"slider\",\"big\"],"
                                   "Pose:{Head:[0f,90f,0f]},ArmorItems:[{},{},{},{id:\"minecraft:diamond_hoe\","
                                   "Count:1b,tag:{Unbreakable:1b,Damage:9}}]}\nexecute if score @p chart matches "
                                   + str(slidertick) +
                                   " run summon armor_stand 18 8 16 {Invisible:1b,Tags:[\"note\",\"slider\",\"big\"],"
                                   "Pose:{Head:[0f,90f,0f]},ArmorItems:[{},{},{},{id:\"minecraft:diamond_hoe\","
                                   "Count:1b,tag:{Unbreakable:1b,Damage:10}}]}\n")
                elif type1 == 'bigslider':
                    sliderrepeat = objectsline.split(',')[6]
                    sliderlength = objectsline.split(',')[7]
                    slidertick = round(
                        (round((600 * (float(sliderlength) * float(sliderrepeat)) / (float(bpm) * float(sv))))
                         + float(tick)) / 50 + 1)

                    newchart.write("execute if score @p chart matches " + str(ticks) +
                                   " run summon armor_stand 18 8 16 {Invisible:1b,Tags:[\"note\",\"slider\",\"big\"],"
                                   "Pose:{Head:[0f,90f,0f]},ArmorItems:[{},{},{},{id:\"minecraft:diamond_hoe\",Count:1b"
                                   ",tag:{Unbreakable:1b,Damage:11}}]}\nexecute if score @p chart matches " +
                                   str(ticks + 1) + ".." + str(slidertick - 1) +
                                   " run summon armor_stand 18 8 16 {Invisible:1b,Tags:[\"note\",\"slider\",\"big\"],"
                                   "Pose:{Head:[0f,90f,0f]},ArmorItems:[{},{},{},{id:\"minecraft:diamond_hoe\","
                                   "Count:1b,tag:{Unbreakable:1b,Damage:9}}]}\nexecute if score @p chart matches "
                                   + str(slidertick) +
                                   " run summon armor_stand 18 8 16 {Invisible:1b,Tags:[\"note\",\"slider\",\"big\"],"
                                   "Pose:{Head:[0f,90f,0f]},ArmorItems:[{},{},{},{id:\"minecraft:diamond_hoe\","
                                   "Count:1b,tag:{Unbreakable:1b,Damage:10}}]}\n")
                elif type1 == 'spinner':
                    spinnerticks = objectsline.split(',')[5]
                    spinnerend = round(int(spinnerticks) / 50 + 1)
                    spinnerticks = round(((int(spinnerticks) - int(tick)) * .007))
                    newchart.write("execute if score @p chart matches " + str(ticks) +
                                   " run summon armor_stand 18 8 16 {Invisible:1b,Tags:[\"note\",\"balloon\"]"
                                   ",Pose:{Head:[0f,90f,0f]},ArmorItems:[{},{},{},{id:\"minecraft:diamond_hoe\",Count:"
                                   "1b,tag:{Unbreakable:1b,Damage:12}}]}\nexecute if score @p chart matches " + str(
                        ticks) + " run scoreboard players set @e[tag=balloon,limit=1] spinner " + str(spinnerticks) +
                                   "\nexecute if score @p chart matches " + str(spinnerend) +
                                   " run scoreboard players set @p spinner 0\n")

                i = i + 1

        text5['text'] = "Success!"
        text5.configure(foreground="#30E829")
    except IOError:
        text5['text'] = "Failure! :c"
        text5.configure(foreground="#FF3333")


# ui stuff
w1 = Canvas(root, background='#24222a', height=200, width=500, highlightthickness=0)
w1.place(x=37, y=25)

w = Canvas(root, background='#302e38', height=200, width=500, highlightthickness=0)
w.place(x=37, y=200)

text = Label(root, text=" Enter .osu File Location: ", background='#302e38', font=('Aller', 10), fg='#BDB9BD')
text.place(x=40, y=210)

button = Button(root, text="...", foreground='#BDB9BD', bd=0, command=command1, font=('Aller', 8, 'bold'),
                background='#24222a', pady=.0001)
button.place(x=510, y=212)

e = Entry(root, width=44, highlightcolor='white', highlightthickness=0, foreground='black', bd=0, font=('Aller', 9),
          background='#18171c', fg='#BDB9BD')
e.insert(0, str(path1))
e.place(x=200, y=213)

text1 = Label(root, text=" Enter Path to Function Folder: ", background='#302e38', font=('Aller', 10), fg='#BDB9BD')
text1.place(x=40, y=230)

button1 = Button(root, text="...", foreground='#BDB9BD', bd=0, command=command2, font=('Aller', 8, 'bold'),
                 background='#24222a', pady=.0001)
button1.place(x=510, y=232)

e1 = Entry(root, width=40, highlightcolor='white', highlightthickness=0, foreground='black', bd=0, font=('Aller', 9),
           background='#18171c', fg='#BDB9BD')
e1.insert(0, str(path2))
e1.place(x=228, y=233)

text2 = Label(root, text=" Enter Path to Sounds Folder: ", background='#302e38', font=('Aller', 10), fg='#BDB9BD')
text2.place(x=40, y=250)

button2 = Button(root, text="...", foreground='#BDB9BD', bd=0, command=command3, font=('Aller', 8, 'bold'),
                 background='#24222a', pady=.0001)
button2.place(x=510, y=252)

e2 = Entry(root, width=41, highlightcolor='white', highlightthickness=0, foreground='black', bd=0, font=('Aller', 9),
           background='#18171c', fg='#BDB9BD')
e2.insert(0, str(path3))
e2.place(x=221, y=253)

text2 = Label(root, text=" Scroll Speed Multiplier: ", background='#302e38', font=('Aller', 10), fg='#BDB9BD')
text2.place(x=40, y=275)

style = ttk.Style()
style.configure("Horizontal.TScale", background="#302e38")
mult = ttk.Scale(root, length=300, value=1, to=2, from_=0.01, orient=HORIZONTAL, style='Horizontal.TScale',
                 command=command4)
mult.place(x=225, y=275)

text4 = Label(root, width=4, highlightcolor='white', highlightthickness=0, foreground='black', bd=0, font=('Aller', 10),
              background='#18171c', fg='#BDB9BD', text=1.00)
text4.place(x=190, y=277)

img = Image.open("resources/button.png")
img = img.resize((200, 100), Image.ANTIALIAS)
img = ImageTk.PhotoImage(image=img)
button3 = Button(root, text="convert!", foreground='#BDB9BD', bd=0, command=conversion, font=('Aller', 20, 'bold'),
                 background='#302e38', pady=.0001, image=img, activebackground='#302e38')
button3.place(x=195, y=300)

text5 = Label(root, width=10, highlightthickness=0, foreground='black', bd=0, font=('Aller', 8),
              background='#302e38', fg='#BDB9BD')
text5.place(x=265, y=300)

var = IntVar()
box = Checkbutton(root, text="Convert .mp3 to \n.ogg (REQUIRES FFMPEG)", font=('Aller', 9), background='#302e38',
                  activebackground='#302e38', bd=0, fg='#BDB9BD', activeforeground='#BDB9BD',
                  selectcolor='#18171c', relief=FLAT, highlightthickness=0, variable=var)
box.place(x=45, y=300)

root.configure(background='#18171c')
root.title('Taiko to MC Converter')
root.iconbitmap('resources/icon.ico')
root.geometry("575x400")
root.resizable(width=False, height=False)

root.mainloop()
