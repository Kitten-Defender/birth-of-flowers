import tkinter
from tkinter import *
import random, string

#WitchNode
#A Program to create Feature-Geometric diagrams
#Creator: Samantha V. Bookholder


root = Tk()
root.title("WitchNode v1")
#root.iconbitmap(r"icon.ico") #use only if you have icon.ico in the root dir

#input section
inp = LabelFrame(root, text="Input", padx=5, pady=5)
inp.grid(row=0,column=0,sticky=N)

#canvas section
canvas = Canvas(root, width = 800, height = 700, bg = 'white')
canvas.grid(row=0,column=1)


##~~~~~~~~~~~~~~~~~~~~PLOT/DRAW~~~~~~~~~~~~~~~~~~~~###

#inputs a set of numbers, returns a tuple of each number rounded
def rr(*x):
    els = []
    for el in x:
        els.append(int(round(el)))
    return tuple(els)

#draws a line based on either four coordinates or two points
def line(p1, p2, ds=None):
    if ds:
        canvas.create_line(p1,p2, fill="#000000", width=8, dash=ds)
    else:
        canvas.create_line(p1,p2, fill="#000000", width=8)


def circle(center):
    pneg = ((center[0]-10),(center[1]-10))
    ppos = ((center[0]+10),(center[1]+10))
    canvas.create_oval(pneg,ppos, fill="#000000")

def seg(a,b): #draws a line with two dots at the end
    line(a,b)
    circle(a) #draws circles on ends of line
    circle(b)
    
#prints a line from the tuples of the line coordinates
def lineprint(m):
    line(m[0],m[1])

#draws two lines cutting off a node
def ddiv(line):
    #divides the line into two points
    p1,p2 = line
    #divides each point into two coordinates
    p1x,p1y,p2x,p2y = p1[0],p1[1],p2[0],p2[1]
    
    #finds midpoint y-val of the line
    zhang = p2y - p1y
    rawmid =  zhang / 2
    mid = p1y + rawmid #raw middle val + border/offset
    
    #defines the x-vals to to the sides of the midpoint
    #these are the start and end of each div
    m = 10 #distance between the two divs
    l = 50 #length of the divs
    line_upper_start = rr((p1x - (l/2)), (mid + m))
    line_upper_end = rr((p1x + (l/2)), (mid + m))
    line_lower_start = rr((p1x - (l/2)), (mid - m))
    line_lower_end = rr((p1x + (l/2)), (mid - m))
    line_upper = (line_upper_start,line_upper_end)
    line_lower = (line_lower_start,line_lower_end)
    lineprint(line_upper)
    lineprint(line_lower)


def txt(x,y,txt_a):
    canvas.create_text(x,y,fill="#000000",font="Sans 20", text=txt_a)


def draw_desc(p,feats):
    if type(feats) == str:
        txt(p[0], (p[1] + (100)),feats)
    elif type(feats) == list:
        i = 0
        while i < len(feats):
            txt(p[0], (p[1] + (100 + (60 * i))),feats[i])
            i += 1


def draw_all(parent,child,assim,feats1, feats2):
    canvas.delete("all") #clears canvas
    #these are the two lines for the phonemes
    #I define them in this roundabout way to make it easier for me to visually parse
    line1 = ((100,50),(100,450))
    line2 = ((450,50),(450,450))
    l1p1,l1p2 = line1
    l2p1,l2p2 = line2

    #draws line segments
    seg(l1p1,l1p2) #phon 1
    seg(l2p1,l2p2) #phon 2
    
    #writes text
    txt((l2p1[0] + 175),l2p1[1],parent)
    txt((l2p2[0] + 175),l2p2[1],child)
    
    #connecting dotted line for transfer from following phone
    if assim == "Regressive": #Regressive (change comes from letter after)
        line(l1p1,l2p2,1)
        ddiv(line1)   #draws breakers
    elif assim == "Progressive": #Progressive (change comes from letter before)
        line(l1p2,l2p1,1)
        ddiv(line2)
    elif assim == "None (Detatch 1st)":
        ddiv(line1)
    elif assim == "None (Detatch 2nd)":
        ddiv(line2)
    
    #prints Structural Description
    draw_desc(l1p2,feats1)
    draw_desc(l2p2,feats2)


###~~~~~~~~~~~~~~~~~~~~INPUT~~~~~~~~~~~~~~~~~~~~###

def lab(r,c,t):
    lab_a = Label(inp, text=t)
    lab_a.grid(row=r,column=c,padx=10, pady=2)
    return lab_a

def ent(r,c):
    ent_a = Entry(inp)
    ent_a.grid(row=r,column=c,padx=10, pady=2)
    return ent_a

def ask(r,c,offset,txt):
    l = lab(r,c,txt)
    e = ent((r+offset),c)
    return l,e

#Create a text box to get the parent node
labPN,entPN = ask(0,0,1,"Parent Node")

#create a text box to get the child node
labCN,entCN = ask(0,1,1,"Child Node")

#create a text box to get the Structural Description for the first phone
labSD1,entSD1 = ask(2,0,1,"SD 1 (comma-separated)")

#create a text box to get the Structural Description for the second phone
labSD2,entSD2 = ask(2,1,1,"SD 2 (comma-separated)")


#creates a label for the radio buttons
lab(4,0,"Type of Assimilation:")

#Creates radio buttons to determine Progressiveressive or Regressive assimilation
proreg_ops = StringVar(inp)
proreg_ops.set("Progressive") # default value

proreg_box = OptionMenu(inp, proreg_ops, "Progressive", "Regressive", "None (Detatch 1st)", "None (Detatch 2nd)")
proreg_box.grid(row=5, column=0)

#splits string of features into list of features
def feat_split(x):
    y = x
    if "," in x:
        if " " not in x:
            y = y.split(",")
        else:
            y = y.split(", ")
    elif " " in x:
        if "," not in x:
            y = y.split(" ")
    if " " not in x:
        if "," not in x:
            y = x
    return y

#returns the text entered in the text boxes
def alltogether():
    parent = entPN.get()
    child = entCN.get()
    assim = proreg_ops.get()
    feats1 = entSD1.get()
    feats1 = feat_split(feats1)
    feats2 = entSD2.get()
    feats2 = feat_split(feats2)
    draw_all(parent,child,assim,feats1, feats2)

def ran():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

gen = Button(inp, text="Generate", command=alltogether)
gen.grid(row=5,column=1, padx=10)

root.mainloop()