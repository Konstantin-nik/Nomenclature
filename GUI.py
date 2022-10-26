import tkinter as tk
import re
import random as rand


class MapLevel:

    def __init__(self, size, encoding, value, prev_level=None, prev_x=None, \
                 prev_y=None, changable_x=True, changable_y=True):
        self.size = size
        self.encoding = encoding
        self.position_x = (value - 1) % self.size
        self.position_y = (value - self.position_x) // self.size
        self.prev_level = prev_level
        self.changable_x = changable_x
        self.changable_y = changable_y
        self.prev_x = prev_x
        self.prev_y = prev_y

    def move_right(self):
        if self.changable_x:
            self.position_x += 1
            if self.position_x == self.size:
                if self.prev_level is not None:
                    self.prev_level.move_right()
                elif self.prev_x is not None:
                    self.prev_x.move_right()
                self.position_x = 0
        return self
    
    def move_left(self):
        if self.changable_x:
            self.position_x -= 1
            if self.position_x == -1:
                if self.prev_level:
                    self.prev_level.move_left()
                elif self.prev_x is not None:
                    self.prev_x.move_left()
                self.position_x = self.size - 1
        return self
    
    def move_up(self):
        if self.changable_y:
            self.position_y -= 1
            if self.position_y == -1:
                if self.prev_level is not None:
                        self.prev_level.move_up()
                elif self.prev_y is not None:
                    self.prev_y.move_up()   
                self.position_y = self.size - 1
        elif self.prev_y is not None:
            self.prev_y.move_up()
        return self
    
    def move_down(self):
        if self.changable_y:
            self.position_y += 1
            if self.position_y == self.size:
                if self.prev_level is not None:
                    self.prev_level.move_down()
                elif self.prev_y is not None:
                    self.prev_y.move_down()   
                self.position_y = 0
        elif self.prev_y is not None:
            self.prev_y.move_down()   
        return self

    def get_value(self):
        val = (self.position_x + 1) + (self.position_y) * self.size
        if self.encoding == 'A':
            return str(chr(val + ord('A') - 2))
        if self.encoding == 'ABCD':
            return str(chr(val + ord('А') - 1))
        if self.encoding == 'abcd':
            return str(chr(val + ord('а') - 1))
        return val

    

def print_levels(lvls):
    r = ''
    r += str(lvls[0].get_value())
    for lvl in lvls[1:]:
        r +=  '-' + str(lvl.get_value())
    return r


def generate(word):
    global ent
    data = re.split(' |-', word)
    ind = 0
    global millionka_l, millionka_n, sotka, pesyatka, dvatspyatka, karta
    karta = []
    for c in data:
        if ind == 0:
            millionka_l = MapLevel(1, 'A', (ord(c)-ord('A')+1), None, changable_x=False)
            d = millionka_l
        elif ind == 1:
            millionka_n = MapLevel(60, None, int(c), prev_level=millionka_l, \
                                   prev_y=millionka_l, changable_y=False)
            d = millionka_n
        elif ind == 2:
            sotka = MapLevel(12, None, int(c), prev_x=millionka_n, prev_y=millionka_l)
            d = sotka
        elif ind == 3:
            pesyatka = MapLevel(2, 'ABCD', (ord(c)-ord('А')+1), prev_level=sotka)
            d = pesyatka
        elif ind == 4:
            dvatspyatka = MapLevel(2, 'abcd', (ord(c)-ord('а')+1), prev_level=pesyatka)
            d = dvatspyatka
        elif ind == 5:
            desyatka = MapLevel(2, None, int(c), prev_level=dvatspyatka)
            d = desyatka
        karta.append(d)
        ind += 1
    ind -= 1 
    a5 =  print_levels(karta)
    d.move_right()
    a6 = print_levels(karta)
    d.move_up()
    a3 = print_levels(karta)
    d.move_left()
    a2 = print_levels(karta)
    d.move_left()
    a1 = print_levels(karta)
    d.move_down()
    a4 =  print_levels(karta)
    d.move_down()
    a7 =  print_levels(karta)
    d.move_right()
    a8 =  print_levels(karta)
    d.move_right()
    a9 =  print_levels(karta)
    return (a1, a2, a3, a4, a5, a6, a7, a8, a9)

def printGenerated(key):
    lab1['text'], lab2['text'], lab3['text'], lab4['text'], lab5['text'], lab6['text'], \
                  lab7['text'], lab8['text'], lab9['text'] = generate(key)

def onLabelClick(lab):
    if lab['text'] != '':
        printGenerated(lab['text'])

check = None
test = None
clickNumOnCheck = 0
specialFont = ('Droid Sans Mono', 18)
def startCheck():
    global check, frm, frm2, ent, but, lab1, lab2, lab3, lab4, lab5, lab6, lab7, \
           lab8, lab9, test, screenHeight
    if check is not None:
        check.destroy()
    if test is not None:
        test.destroy()
    check = tk.Toplevel()

    check.title("Номенклатура - Проверка")
    check.geometry(f"600x450+850+{int((screenHeight-450)/2)}")
    check.minsize(500, 350)
    check.resizable(width='false', height='false')

    frm2 = tk.Frame(check)
    ent = tk.Entry(frm2, justify='center')
    ent.bind('<Return>', lambda event: printGenerated(ent.get()))
    ent.pack(side = 'left', ipadx=3, ipady=2)
    but = tk.Button(frm2, text='Генерация', command=lambda: printGenerated(ent.get()))
    but.pack(side = 'left', ipadx=5, padx=10)
    frm2.pack(pady=(10, 0))

    frm = tk.Frame(check, width=500, height=480)
    frm.pack(fill='both', expand=1, padx=10, pady=10)
    frm.columnconfigure(0, weight=1)
    frm.columnconfigure(1, weight=1)
    frm.columnconfigure(2, weight=1)
    frm.rowconfigure(0, weight=1)
    frm.rowconfigure(1, weight=1)
    frm.rowconfigure(2, weight=1)

    lab1 = tk.Label(frm, font=specialFont)
    lab1.bind("<Button-1>", lambda e: onLabelClick(lab1))
    lab1.grid(row=0, column=0)

    lab2 = tk.Label(frm, font=specialFont)
    lab2.bind("<Button-1>", lambda e: onLabelClick(lab2))
    lab2.grid(row=0, column=1)

    lab3 = tk.Label(frm, font=specialFont)
    lab3.bind("<Button-1>", lambda e: onLabelClick(lab3))
    lab3.grid(row=0, column=2)

    lab4 = tk.Label(frm, font=specialFont)
    lab4.bind("<Button-1>", lambda e: onLabelClick(lab4))
    lab4.grid(row=1, column=0)

    lab5 = tk.Label(frm, font=specialFont)
    lab5.bind("<Button-1>", lambda e: onLabelClick(lab5))
    lab5.grid(row=1, column=1)

    lab6 = tk.Label(frm, font=specialFont)
    lab6.bind("<Button-1>", lambda e: onLabelClick(lab6))
    lab6.grid(row=1, column=2)

    lab7 = tk.Label(frm, font=specialFont)
    lab7.bind("<Button-1>", lambda e: onLabelClick(lab7))
    lab7.grid(row=2, column=0)

    lab8 = tk.Label(frm, font=specialFont)
    lab8.bind("<Button-1>", lambda e: onLabelClick(lab8))
    lab8.grid(row=2, column=1)

    lab9 = tk.Label(frm, font=specialFont)
    lab9.bind("<Button-1>", lambda e: onLabelClick(lab9))
    lab9.grid(row=2, column=2)


def testEntry(entry, key):
    word = entry.get().strip()
    if word == '':
        entry['bg'] = 'white'
    elif word == key:
        entry['bg'] = 'lightgreen'
    else:
        entry['bg'] = 'red'


def checkTest():
    ind = 0
    key1, key2, key3, key4, key5, key6, key7, key8, key9 = generate(key)
    testEntry(entry1, key1)
    testEntry(entry2, key2)
    testEntry(entry3, key3)
    testEntry(entry4, key4)
    testEntry(entry5, key5)
    testEntry(entry6, key6)
    testEntry(entry7, key7)
    testEntry(entry8, key8)
    testEntry(entry9, key9)
    

def generateKey(ind):
    global key
    key = ''
    keyComponents = []
    keyComponents.append(str(chr(ord('A') + rand.randint(1, ord('V')-ord('A')) - 1)))
    if ind >= 1:
        keyComponents.append(str(rand.randint(1, 60)))
    if ind == 2:
        keyComponents.append(str(rand.randint(1, 36)))
    if ind >= 3:
        keyComponents.append(str(rand.randint(1, 144)))
    if ind >= 4:
        keyComponents.append(str(chr(ord('А') + rand.randint(1, 4) - 1)))
    if ind >= 5:
        keyComponents.append(str(chr(ord('а') + rand.randint(1, 4) - 1)))
    if ind >= 6:
        keyComponents.append(str(rand.randint(1, 4)))
    key = '-'.join(keyComponents)
    testMain()
    
clickNumOnTest = 0
key = ''
def startTest():
    global key, test, testModeFrame, testMainFrame, entry1, entry2, entry3, entry4, \
           entry5, entry6, entry7, entry8, entry9, check, screenHeight
    if test is not None:
        test.destroy()
    if check is not None:
        check.destroy()
    test = tk.Toplevel()
    
    test.title("Номенклатура - Тест")
    test.geometry(f"600x450+850+{int((screenHeight-450)/2)}")
    test.minsize(500, 350)
    test.resizable(width='false', height='false')

    testModeFrame = tk.Frame(test)
    
    tk.Label(testModeFrame, text='Выберите масштаб карты:', font=specialFont).pack(pady=(50,0))
    
    testModeScaleFrame = tk.Frame(testModeFrame)
    testModeScaleFrame.columnconfigure(0, weight=1)
    testModeScaleFrame.columnconfigure(1, weight=1)
    testModeScaleFrame.columnconfigure(2, weight=1)
    #testModeScaleFrame.rowconfigure(0, weight=1)
    #testModeScaleFrame.rowconfigure(1, weight=1)
    
    choice1 = tk.Button(testModeScaleFrame, text='1:1000000', width=10, height=2, \
                        font=specialFont, command=lambda: generateKey(1))
    choice1.grid(row=0, column=0, pady=(50, 9), ipady=8, ipadx=3)

    choice2 = tk.Button(testModeScaleFrame, text='1:200000', width=10, height=2, \
                        font=specialFont, command=lambda: generateKey(2))
    choice2.grid(row=1, column=0, ipady=10, ipadx=3)

    choice3 = tk.Button(testModeScaleFrame, text='1:100000', width=10, height=2, \
                        font=specialFont, command=lambda: generateKey(3))
    choice3.grid(row=0, column=1, pady=(50, 9), ipady=8, ipadx=3)

    choice4 = tk.Button(testModeScaleFrame, text='1:50000', width=10, height=2, \
                        font=specialFont, command=lambda: generateKey(4))
    choice4.grid(row=1, column=1, ipady=10, ipadx=3)

    choice5 = tk.Button(testModeScaleFrame, text='1:25000', width=10, height=2, \
                        font=specialFont, command=lambda: generateKey(5))
    choice5.grid(row=0, column=2, pady=(50, 9), ipady=8, ipadx=3)

    choice6 = tk.Button(testModeScaleFrame, text='1:10000', width=10, height=2, \
                        font=specialFont, command=lambda: generateKey(6))
    choice6.grid(row=1, column=2, ipady=10, ipadx=3)
    
    testModeScaleFrame.pack(fill='both', padx=40, pady=(0, 20))
    
    testModeFrame.pack(fill='both')

def testMain():
    global key, test, testModeFrame, testMainFrame, entry1, entry2, entry3, entry4, entry5, \
           entry6, entry7, entry8, entry9, check, screenHeight
    if test is not None:
        test.destroy()
    if check is not None:
        check.destroy()
    test = tk.Toplevel()

    test.title("Номенклатура - Тест")
    test.geometry(f"600x450+850+{int((screenHeight-450)/2)}")
    test.minsize(500, 350)
    test.resizable(width='false', height='false')
    
    testMainFrame = tk.Frame(test)
    testMainFrame.columnconfigure(0, weight=1)
    testMainFrame.columnconfigure(1, weight=1)
    testMainFrame.columnconfigure(2, weight=1)
    testMainFrame.rowconfigure(0, weight=1)
    testMainFrame.rowconfigure(1, weight=1)
    testMainFrame.rowconfigure(2, weight=1)
    
    entry1 = tk.Entry(testMainFrame, justify='center', width=15, font=specialFont)
    entry1.bind('<Return>',  lambda event: checkTest())
    entry1.grid(row=0, column=0, ipady=66)

    entry2 = tk.Entry(testMainFrame, justify='center', width=15, font=specialFont)
    entry2.bind('<Return>',  lambda event: checkTest())
    entry2.grid(row=0, column=1, ipady=66)

    entry3 = tk.Entry(testMainFrame, justify='center', width=15, font=specialFont)
    entry3.bind('<Return>',  lambda event: checkTest())
    entry3.grid(row=0, column=2, ipady=66)

    entry4 = tk.Entry(testMainFrame, justify='center', width=15, font=specialFont)
    entry4.bind('<Return>',  lambda event: checkTest())
    entry4.grid(row=1, column=0, ipady=66)

    entry5 = tk.Entry(testMainFrame, justify='center', width=15, font=specialFont)
    entry5.delete(0, 'end')
    entry5.insert(0, key)
    entry5.grid(row=1, column=1, ipady=66)

    entry6 = tk.Entry(testMainFrame, justify='center', width=15, font=specialFont)
    entry6.bind('<Return>',  lambda event: checkTest())
    entry6.grid(row=1, column=2, ipady=66)

    entry7 = tk.Entry(testMainFrame, justify='center', width=15, font=specialFont)
    entry7.bind('<Return>',  lambda event: checkTest())
    entry7.grid(row=2, column=0, ipady=66)

    entry8 = tk.Entry(testMainFrame, justify='center', width=15, font=specialFont)
    entry8.bind('<Return>',  lambda event: checkTest())
    entry8.grid(row=2, column=1, ipady=66)

    entry9 = tk.Entry(testMainFrame, justify='center', width=15, font=specialFont)
    entry9.bind('<Return>',  lambda event: checkTest())
    entry9.grid(row=2, column=2, ipady=66)

    testMainFrame.pack(fill='both')


def in_close(signum = None, frame = None):
    # Here you can attempt to gently exit your application.
    pass

def main():
    #root = tk.Tk()
    #root.attributes('-alpha', 0.0)
    menu = tk.Tk()

    global screenWidth, screenHeight
    menu.title("Номенклатура")
    screenWidth = menu.winfo_screenwidth()
    screenHeight = menu.winfo_screenheight()
    menu.geometry(f"500x350+300+{int((screenHeight-350)/2)}")
    menu.minsize(500, 350)
    menu.resizable(width='false', height='false')
    menu.overrideredirect(0)
    menu['bg'] = 'white'
    menu.tk_setPalette(background='white')#, foreground='black', activeBackground='black', activeForeground=mycolor2)

    mainFrame = tk.Frame(menu)

    tk.Label(mainFrame, text='Номенклатура', font=('Droid Sans Mono', 18)).pack(pady=(25, 0))

    checkModeButton = tk.Button(mainFrame, text='Режим проверки', \
                                width=30, height=2, command=startCheck)
    checkModeButton.pack(side='top', expand=1, pady=(40, 3))

    testModeButton = tk.Button(mainFrame, text='Режим теста', \
                               width=30, height=2, command=startTest)
    testModeButton.pack(side='top', expand=1, pady=(0, 3))
    
    statisticButton = tk.Button(mainFrame, text='Статистика', \
                               width=30, height=2)
    statisticButton.pack(side='top', expand=1, pady=(0, 3))

    exitButton = tk.Button(mainFrame, text='Выход', width=20, height=2, \
                           command = lambda: menu.destroy())
    exitButton.pack(pady=(70,0))

    mainFrame.pack(fill='both')

    menu.mainloop()

if __name__ == "__main__":
    main()
