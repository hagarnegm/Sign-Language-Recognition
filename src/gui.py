import tkinter as tk, threading
import cv2
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from tkinter import filedialog


def stream():
    thread = threading.Thread(target=video, args=())
    thread.daemon = 1
    thread.start()


def video():
    global display1
    global display2
    global images

    if display2 is not None:
        display2.destroy()

    vc = cv2.VideoCapture(0)

    plt.ion()

    if vc.isOpened():  # try to get the first frame
        is_capturing, frame = vc.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # makes the blues image look real colored
        # bg = remove_g_noise(frame)
        webcam_preview = plt.imshow(frame)

    else:
        is_capturing = False
    fig = plt.figure(figsize=(50, 50))
    columns = 10
    rows = 10
    for i in range(1, columns*rows +1):
        try:  # Lookout for a keyboardInterrupt to stop the script
            is_capturing, frame = vc.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # makes the blues image look real colored
            # webcam_preview.set_data(frame)
            # webcam_preview = plt.imshow(frame)
            fig.add_subplot(rows, columns, i)
            plt.imshow(frame)
            images.append(frame)

        except KeyboardInterrupt:
            vc.release()
    plt.show()
    # time = 1000
    # while cap.isOpened():
    #     # cap.set(cv2.CAP_PROP_POS_MSEC, time)
    #     ret, frame = cap.read()
    #     image = cv2.flip(frame, 1)
    #     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
    #     image = Image.fromarray(image)
    #     image = ImageTk.PhotoImage(image)
    #     # images.append(frame)
    #
    #     if display1 is None:
    #         display1 = tk.Label(root)
    #         display1.config(bd='5')
    #         display1.place(x=400, y=200)
    #         display1.image = image
    #         display1.configure(image=image)
    #         display1.after(10, video)
    #     else:
    #         display1.image = image
    #         display1.configure(image=image)
    #         display1.after(10, video)
    #
    #     if not ret:
    #         break
        # time += 1000
    # cap.release()


def photo():
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
            display2.place(x=600, y=200)
        else:
            display2.configure(image=image)
            display2.image = image


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

