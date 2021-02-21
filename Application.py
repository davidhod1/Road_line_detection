import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import cv2
import PIL.Image, PIL.ImageTk
import linedetection as ld
from CaptureVideo import Video

class LineApp():
    def __init__(self, master=None):
        self.master = master

        self.videoSource = "TestVideos/challenge.mp4"
        self.videoSizeX = 1000
        self.videoSizeY = 500

        self.video = Video(self.videoSource)

        self.tabController = ttk.Notebook(master)

        self.originalTab = self.addTab("Original Video")
        self.colorMaskTab = self.addTab("Color Mask")
        self.grayTab = self.addTab("Grayscale")
        self.cannyTab = self.addTab("Canny")
        self.roiTab = self.addTab("ROI")
        self.finalTab = self.addTab("Final Video")
        self.settingsTab = self.addTab("Settings")


        self.tabController.pack(expand=1, fill='both')

        button = tk.Button(self.settingsTab, text="Upload video", command=self.UploadAction)
        button.pack()


        self.originalCanvas = tk.Canvas(self.originalTab, width=self.videoSizeX, height=self.videoSizeY)
        self.originalCanvas.pack(pady = 100)

        self.roiCanvas = tk.Canvas(self.roiTab, width=self.videoSizeX, height=self.videoSizeY)
        self.roiCanvas.pack(pady=100)

        self.colorMaskCanvas = tk.Canvas(self.colorMaskTab, width=self.videoSizeX, height=self.videoSizeY)
        self.colorMaskCanvas.pack(pady = 100)

        self.grayCanvas = tk.Canvas(self.grayTab, width=self.videoSizeX, height=self.videoSizeY)
        self.grayCanvas.pack(pady=100)

        self.cannyCanvas = tk.Canvas(self.cannyTab, width=self.videoSizeX, height=self.videoSizeY)
        self.cannyCanvas.pack(pady=100)

        self.finalCanvas = tk.Canvas(self.finalTab, width=self.videoSizeX, height=self.videoSizeY)
        self.finalCanvas.pack(pady=100)


        self.delay = 15

        self.loadVideo()

        self.master.mainloop()

    def UploadAction(self, event=None):
        filename = filedialog.askopenfilename()
        self.videoSource = filename
        self.video = Video(self.videoSource)
        print('Selected:', filename)

    def addTab(self, name):
        tab = ttk.Frame(self.tabController)
        self.tabController.add(tab,text = name)
        return tab

    def loadVideo(self):


        index = self.tabController.index("current")
        if index == 0:
            ret, frame = self.video.getFrame()
            if ret:
                image = cv2.resize(frame, dsize=(self.videoSizeX, self.videoSizeY))
                self.photoOriginal = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)))
                self.originalCanvas.create_image(0, 0, image=self.photoOriginal, anchor=tk.NW)
        if index == 1:
            ret, frame = self.video.getFrame()
            if ret:
                image = cv2.resize(frame, dsize=(self.videoSizeX, self.videoSizeY))
                imgMasked,_,_,_,_ = ld.processImage(image)
                self.photoColorMask = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv2.cvtColor(imgMasked, cv2.COLOR_BGR2RGB)))
                self.colorMaskCanvas.create_image(0, 0, image=self.photoColorMask, anchor=tk.NW)
        if index == 2:
            ret, frame = self.video.getFrame()
            if ret:
                image = cv2.resize(frame, dsize=(self.videoSizeX, self.videoSizeY))
                _,grayImage,_,_,_ = ld.processImage(image)
                self.photoGray = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv2.cvtColor(grayImage, cv2.COLOR_BGR2RGB)))
                self.grayCanvas.create_image(0, 0, image=self.photoGray, anchor=tk.NW)
        if index == 3:
            ret, frame = self.video.getFrame()
            if ret:
                image = cv2.resize(frame, dsize=(self.videoSizeX, self.videoSizeY))
                _,_,cannyImage,_,_ = ld.processImage(image)
                self.photoGray = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv2.cvtColor(cannyImage, cv2.COLOR_BGR2RGB)))
                self.cannyCanvas.create_image(0, 0, image=self.photoGray, anchor=tk.NW)
        if index == 4:
            ret, frame = self.video.getFrame()
            if ret:
                image = cv2.resize(frame, dsize=(self.videoSizeX, self.videoSizeY))
                _,_,_,roiImage,_ = ld.processImage(image)
                self.photoGray = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv2.cvtColor(roiImage, cv2.COLOR_BGR2RGB)))
                self.roiCanvas.create_image(0, 0, image=self.photoGray, anchor=tk.NW)
        if index == 5:
            ret, frame = self.video.getFrame()
            if ret:
                image = cv2.resize(frame, dsize=(self.videoSizeX, self.videoSizeY))
                _,_,_,_,output = ld.processImage(image)
                self.photoGray = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv2.cvtColor(output, cv2.COLOR_BGR2RGB)))
                self.finalCanvas.create_image(0, 0, image=self.photoGray, anchor=tk.NW)

        self.master.after(self.delay, self.loadVideo)





