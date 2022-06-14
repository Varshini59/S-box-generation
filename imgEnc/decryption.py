import numpy as np
import csv
from PIL import Image
from PIL import Image as im
from numpy import asarray
import numpy as np
import generator.sbox
import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()


def showCipherImage():
    img = Image.open('birdCipher.png')
    img = img.resize((300, 200))
    print(img.format)
    print(img.size)
    img = ImageTk.PhotoImage(img)
    img_label = tk.Label(image=img)
    img_label.image = img
    img_label.grid(column=1, row=1)

    instr = tk.Label(
        root, text="Click on 'Decrypt' to decrypt the above image", font=("Raleway", 13))
    instr.grid(columnspan=3, column=0, row=2)

    dec_btn_text = tk.StringVar()
    dec_btn = tk.Button(root, textvariable=dec_btn_text, command=lambda: decrypt(),
                        font=("Raleway", 13), bg="#000000", fg="white", height=2, width=12)
    dec_btn_text.set("Decrypt")
    dec_btn.grid(column=1, row=3)


rec_btn_text = tk.StringVar()

rec_btn = tk.Button(root, textvariable=rec_btn_text, command=lambda: showCipherImage(),
                    font=("Raleway", 13), bg="#000000", fg="white", height=2, width=12)
rec_btn_text.set("Receive")
rec_btn.grid(column=1, row=0)


def decrypt():
    sbox96 = []
    AES = []

    with open('source.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    for i in range(0, 16):
        AES.append(list(map(int, data[i])))

    def addToMainSbox(sbox32):
        for i in range(0, len(sbox32)):
            sbox96.append(sbox32[i])

    t1 = generator.sbox.getRowShuffled(AES)
    with open("out2.csv", "a", newline="") as f:
        writer = csv.writer(f)
        for i in range(0, len(t1)):
            writer.writerows(t1[i])

    addToMainSbox(t1)
    t2 = generator.sbox.getColShuffled(AES)
    addToMainSbox(t2)
    t3 = generator.sbox.getRowColShuffled(AES)
    addToMainSbox(t3)

    def xor(message, iv):
        arr = []
        for i in range(0, len(message)):
            arr.append(message[i] ^ iv[i])
        return arr

    data = []

    with open('imgsize.txt', "r") as f:
        rowLen = int(f.readline())
        colLen = int(f.readline())
        zLen = int(f.readline())

    with open('cipher.csv', newline='') as f:
        reader = csv.reader(f)
        cipher = list(reader)

    cipher2 = []
    for i in range(0, len(cipher)):
        cipher2.append(list(map(int, cipher[i])))

    roundkeys = []
    iv = []
    with open('iv.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            iv.append(int(row[0]))

    content = np.genfromtxt('keys.txt', delimiter=',',
                            dtype=None, encoding='UTF-8')

    for row in content:
        roundkeys.append(row.split())

    message = []
    blocksOfMessage = cipher2

    idx = 0
    sboxIndices = []
    with open('indices.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            sboxIndices.append(int(row[0]))

    arr = []
    for i in range(0, len(cipher2)):
        arr = cipher2[i]

        for j in range(0, 8):
            roundkey = [int(i) for i in roundkeys[j]]
            sbox = np.array(sbox96[sboxIndices[idx]])
            sbox = sbox.flatten()
            tempArr = xor(arr, sbox)
            arr = xor(tempArr, roundkey)
            arr = xor(arr, iv)
            idx += 1
        iv = cipher2[i]
        message.append(arr)
    # print(message)
    message = np.array(message)
    message = message.flatten()

    np.savetxt("pt.csv",
               message,
               delimiter=",",
               fmt='%d')

    with open('pt.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    data = np.array(data)
    data = data.flatten()

    data = list(map(int, data))

    t1 = []
    x = 0
    for i in range(0, rowLen):
        t2 = []
        for j in range(0, colLen):
            t3 = []
            if zLen != 0:
                for k in range(0, zLen):
                    t3.append(256-data[x])
                    x += 1
                t2.append(t3)
            else:
                t2.append(256-data[x])
                x += 1

        t1.append(t2)

    t1 = np.array(t1)
    try:
        data = Image.fromarray((t1 * 255).astype(np.uint8))
    except:
        data = Image.fromarray(t1)

    data.save('birdConv.png')
    print("converted!!!")

    instr = tk.Label(
        root, text="Decrypted!", font=("Raleway", 13))
    instr.grid(columnspan=3, column=0, row=4)

    img2 = Image.open('birdConv.png')
    img2 = img2.resize((300, 200))
    img2 = ImageTk.PhotoImage(img2)
    img_label2 = tk.Label(image=img2)
    img_label2.image = img2
    img_label2.grid(column=1, row=5)


canvas = tk.Canvas(root, width=600, height=400)
canvas.grid(columnspan=3, rowspan=3)

root.mainloop()
