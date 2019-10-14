#Gematria Calculator
# Violet S. Ravenwood
#Uses Mispar Hechrachi (plain addition without sofit forms)

from tkinter import *

#the dictionary

gem0 = {
    " " : 0,
    "-" : 0,
    "־" : 0,
    "׳" : 0,
    "״" : 0,
    "א" : 1,
    "ב" : 2,
    "ג" : 3,
    "ד" : 4,
    "ה" : 5,
    "ו" : 6,
    "ז" : 7,
    "ח" : 8,
    "ט" : 9,
    "י" : 10,
    "כ" : 20,
    "ל" : 30,
    "מ" : 40,
    "נ" : 50,
    "ס" : 60,
    "ע" : 70,
    "פ" : 80,
    "צ" : 90,
    "ק" : 100,
    "ר" : 200,
    "ש" : 300,
    "ת" : 400,
    "ך" : 20,
    "ם" : 40,
    "ן" : 50,
    "ף" : 80,
    "ץ" : 90,
    }

#Creates the window
window0 = Tk()
window0.title("Gematria Calculator")
window0.geometry("520x200")

#Creates Adjustable Text Variable
#Will later be updated when Gematria is calculated
result = StringVar()
result.set("Please input a Hebrew word (without niqqud)")
errormsg = StringVar()
errormsg.set("")

#Creates the text
txt0 = Label(window0, textvariable = result, font =("DejaVu Sans", 20), wraplength =  520)
txt0.grid(column=1, row=0)
txt_error = Label(window0, textvariable = errormsg , font =("DejaVu Sans", 8), wraplength =  520)
txt_error.grid(column=1, row=4)

#Creates the input field
inp0 = Entry(window0,width=20)
inp0.grid(column=1, row=1)
inp0.focus()


#calculate gematria
def calc():
    input0 = inp0.get()
    running_total = 0
    for x in input0:
        try:
            running_total += gem0[x]
        except:
            errormsg.set("Warning! Non-Hebrew Characters")
            continue
    #update text variable
    result.set("The Gematria of \"%s\" is %d" % (input0, running_total))
    



#creates the button
button0 = Button(window0, text="Calculate!", command = calc)
button0.grid(column=1, row=2)

window0.mainloop()