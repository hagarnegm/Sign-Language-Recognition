import tkinter as tk, threading
import cv2
from commonfunctions import *
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from tkinter import filedialog
import imageio
import numpy as np
import preprocessing as pre
from features import *
import os
import openpyxl as op
# from xlutils.copy import copy
from xlrd import open_workbook
from classifiction import *
import csv


def stream():
    thread = threading.Thread(target=video, args=())
    thread.daemon = 1
    thread.start()


# def video():
#     global display1
#     global display2
#     global images
#
#     if display2 is not None:
#         display2.destroy()
#     cap = cv2.VideoCapture(0)
#
#     currentFrame = 0
#
#     while True:
#         # Capture frame-by-frame
#         ret, frame = cap.read()
#
#         # Handles the mirroring of the current frame
#         frame = cv2.flip(frame, 1)
#
#         # Our operations on the frame come here
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#
#         # Saves image of the current frame in jpg file
#         # name = 'frame' + str(currentFrame) + '.jpg'
#         # cv2.imwrite(name, frame)
#         images.append(gray)
#         # Display the resulting frame
#         cv2.imshow('frame', frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
#         # To stop duplicate images
#         currentFrame += 1
#
#     # When everything done, release the capture
#     cap.release()
#     cv2.destroyAllWindows()
#     fig = plt.figure(figsize=(50, 50))
#     diffr = []
#
#     # for i in range(len(images)):
#     #     images[i] = cv2.GaussianBlur(images[i], (5, 5), 0)
#     for i in range(0, len(images)):
#         # diff = cv2.absdiff(images[i], images[0])
#         # diff[diff <= 20] = 0
#         # diff[diff > 20] = 255
#         # diff = cv2.GaussianBlur(diff, (5, 5), 0)
#         img = pre.hand(images[i])
#         img = pre.extractTip(img)
#         diffr.append(img)
#         # diffr.append(diff)
#         # image=np.copy(images[i])
#         # image[diff==1]=images[i]
#         # image[diff == 0] = 0
#         # images[i]=image
#     columns = 5
#     rows = int(np.floor(len(diffr)/5))
#     for i in range(0, columns*rows):
#         print(diffr[i])
#         fig.add_subplot(rows, columns, i+1)
#         # images[i]=np.subtract(images[i],images[0])
#         plt.imshow(diffr[i])
#     print("here")
#     plt.show()
#     print("here2q")

def video():
    images = []
    video_name = filedialog.askopenfilename() # This is your video file path
    video = imageio.get_reader(video_name)

    vid = tk.Label()
    vid.config(width=800)
    vid.config(height=400)
    vid.pack()

    for image in video.iter_data():
        frame_image = ImageTk.PhotoImage(Image.fromarray(image))
        vid.config(image=frame_image)
        vid.image = frame_image
        images.append(image)

    z = []
    for i in range(len(images)):
        img1 = pre.hand(images[i])
        img2 = pre.extractTip(img1)
        z.append(img2)

    img3 = sum(z[:])
    hp,vp=pre.ZJF(img3)
    show_images([img3])


def photo():
    global display1
    global display2
    path = filedialog.askopenfilename()
    if len(path) > 0:
        image = cv2.imread(path)
        img = np.copy(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = image.resize((500, 500), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)
        if display1 is not None:
            display1.destroy()
        if display2 is None:
            display2 = tk.Label(image=image)
            display2.image = image
            display2.place(x=600, y=200)
        else:
            display2.configure(image=image)
            display2.image = image

        img = hand(img)
        img, centerh, centerv, original = cropPicture(img)
        img = extractFist(img)
        show_images([img])
        dist_trans, img_centroid, centroid = refpoint(img)
        dists = descriptor(img, centroid, 360)

        features = np.array(readFeatures())
        train_f = features[:, 1:]
        labels = features[:, 0]
        labels[labels == 'A'] = 1
        labels[labels == 'B'] = 2
        labels[labels == 'C'] = 3
        labels[labels == 'D'] = 4
        labels[labels == 'X'] = 6
        labels[labels == 'Y'] = 7
        labels[labels == 'O'] = 8
        classi = classify(train_f, labels, [dists])
        output(str(classi))


def output(text):
    out = tk.Text()
    out.insert('insert', text)
    out.place(x=50, y=700)


class GUI:

    def __init__(self, master):
        global output
        self.master = master
        master.title('Sign Language Recognition')
        master.configure(background='#40407a')
        master.geometry('1920x1080')
        master.resizable(True, True)

        self.title = tk.Label(root, text='Sign Language Recognition', font='Helvetica', bg='#40407a', fg='white')
        self.title.place(x=650, y=50)

        self.stream_video = tk.Button(root, bg='white', text='Video', command=stream)
        self.stream_video.config(width=50)
        self.stream_video.place(x=50, y=100)

        self.upload_image = tk.Button(root, bg='white', text='Photo', command=photo)
        self.upload_image.config(width=50)
        self.upload_image.place(x=600, y=100)

        self.process_image = tk.Button(root, bg='white', text='Process', command=photo)
        self.process_image.config(width=50)
        self.process_image.place(x=1120, y=100)

        self.output = tk.Label(root, text='Output Text: ', font='Helvetica', bg='#40407a', fg='white')
        self.output.place(x=50, y=700)


root = tk.Tk()
display1 = None
display2 = None
text = None
images = []
gui = GUI(root)
root.mainloop()

