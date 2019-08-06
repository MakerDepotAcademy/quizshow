from tkinter import *

root = Tk()
root.attributes("-fullscreen", True)
canvas = Canvas(root, background="red", highlightthickness=0)
#canvas.pack(fill=BOTH, expand=True)

lable_1 = Label(root, text="Question")
lable_2 = Label(root, text="Answer")

lable_1.grid(row=0, column=0)
lable_2.grid(row=1, column=0)

root.mainloop()
