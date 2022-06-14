import tkinter as tk
# import PyPDF2
from PIL import Image, ImageTk
# import imgEnc.encryption

root = tk.Tk()

canvas = tk.Canvas(root, width=600, height=500)
canvas.grid(columnspan=3, rowspan=3)

img = Image.open('apple.png')
img = ImageTk.PhotoImage(img)
img_label = tk.Label(image=img)
img_label.image = img
img_label.grid(column=1, row=0)

instr = tk.Label(
    root, text="Click on 'Encrypt' to encrypt the above image", font="Raleway")
instr.grid(columnspan=3, column=0, row=1)

button_text = tk.StringVar()
enc_btn = tk.Button(root, textvariable=button_text, command=lambda: imgEnc.encryption.encrypt(),
                    font="Raleway", bg="#000000", fg="white", height=2, width=15)
button_text.set("Encrypt")
enc_btn.grid(column=1, row=2)

root.mainloop()
