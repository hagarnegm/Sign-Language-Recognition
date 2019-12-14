import tkinter as tk
import cv2
from PIL import Image, ImageTk
from tkinter import filedialog


def stream():
    global display1
    global display2
    global images
    width, height = 800, 600
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    ret, frame = cap.read()
    image = cv2.flip(frame, 1)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
    image = Image.fromarray(image)
    image = ImageTk.PhotoImage(image)
    images.append(frame)

    if display2 is not None:
        display2.destroy()

    if display1 is None:
        display1 = tk.Label(root)
        display1.config(bd='5')
        display1.place(x=600, y=150)
        display1.image = image
        display1.configure(image=image)
        display1.after(10, stream)
    else:
        display1.image = image
        display1.configure(image=image)
        display1.after(10, stream)

    cap.release()
    # time = 1000
    # while cap.isOpened():
    #     cap.set(cv2.CAP_PROP_POS_MSEC, time)
    #     images.append(frame)
    #     if not ret:
    #         break
    #     time += 1000




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
            display2.place(x=600, y=150)
        else:
            display2.configure(image=image)
            display2.image = image


class GUI:

    def __init__(self, master):
        self.master = master
        master.title('Sign Language Recognition')
        master.configure(background='#40407a')
        master.geometry('1920x1080')
        master.resizable(True, True)

        self.title = tk.Label(root, text='Sign Language Recognition', font='Helvetica', bg='#40407a', fg='white')
        self.title.place(x=650, y=50)

        self.stream_video = tk.Button(root, bg='white', text='Stream', command=stream)
        self.stream_video.config(width=50)
        self.stream_video.place(x=50, y=150)

        self.upload_image = tk.Button(root, bg='white', text='Upload', command=upload)
        self.upload_image.config(width=50)
        self.upload_image.place(x=50, y=200)

        self.process_image = tk.Button(root, bg='white', text='Process', command=upload)
        self.process_image.config(width=50)
        self.process_image.place(x=50, y=250)

        self.output = tk.Label(root, text='Output Text: ', font='Helvetica', bg='#40407a', fg='white')
        self.output.place(x=600, y=700)


root = tk.Tk()
display1 = None
display2 = None
images = []
gui = GUI(root)
root.mainloop()

