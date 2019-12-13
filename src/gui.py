import tkinter as tk
import cv2
from PIL import Image, ImageTk
from tkinter import filedialog

width, height = 800, 600
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


def stream():
    global display1
    global display2
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    image = Image.fromarray(image)
    image = ImageTk.PhotoImage(image)
    if display2 is not None:
        display2.destroy()
    if display1 is None:
        display1 = tk.Label(root)
        display1.config(bd='5')
        display1.place(x=50, y=250)
        display1.image = image
        display1.configure(image=image)
        display1.after(10, stream)
        output = tk.Label(root, text='Output Text: ', font='Helvetica', bg='#202020', fg='white')
        output.place(x=1120, y=250)
    else:
        display1.image = image
        display1.configure(image=image)
        display1.after(10, stream)
        output = tk.Label(root, text='Output Text: ', font='Helvetica', bg='#202020', fg='white')
        output.place(x=1120, y=250)


def upload():
    global display1
    global display2
    path = filedialog.askopenfilename()
    if len(path) > 0:
        image = cv2.imread(path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = image.resize((500, 500), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)
        if display1 is not None:
            display1.destroy()
        if display2 is None:
            display2 = tk.Label(image=image)
            display2.image = image
            display2.place(x=50, y=250)
            output = tk.Label(root, text='Output Text: ', font='Helvetica', bg='#202020', fg='white')
            output.place(x=700, y=250)
        else:
            display2.configure(image=image)
            display2.image = image
            output = tk.Label(root, text='Output Text: ', font='Helvetica', bg='#202020', fg='white')
            output.place(x=700, y=250)


root = tk.Tk()
root.geometry('1920x1080')
root.resizable(True, True)
root.bind('<Escape>', lambda e: root.quit())
root.title('Sign Language Recognition')
root.configure(background='#202020')

title = tk.Label(root, text='Sign Language Recognition', font='Helvetica', bg='#202020', fg='white')
title.place(x=650, y=50)

stream_video = tk.Button(root, bg='white', text='Stream', command=stream)
stream_video.config(width=50)
stream_video.place(x=50, y=150)

upload_image = tk.Button(root, bg='white', text='Upload', command=upload)
upload_image.config(width=50)
upload_image.place(x=600, y=150)

process_image = tk.Button(root, bg='white', text='Process', command=upload)
process_image.config(width=50)
process_image.place(x=1120, y=150)

display1 = None
display2 = None

root.mainloop()
cap.release()
