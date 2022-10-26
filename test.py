import tkinter as tk

root = tk.Tk()
root.geometry("600x450+450+100")

check1 = tk.Checkbutton(root, text='Hello', onvalue=1)
check1.pack()
check2 = tk.Checkbutton(root, text='Hello 2', onvalue=2)
check2.pack()
check3 = tk.Checkbutton(root, text='Hello 3', onvalue=3)
check3.pack()
check4 = tk.Checkbutton(root, text='Hello 4', onvalue=4)
check4.pack()
check5 = tk.Checkbutton(root, text='Hello 5', onvalue=5)
check5.pack()

root.mainloop()
