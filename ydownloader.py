import tkinter as tk
from pytube import YouTube
from tkinter import messagebox
from PIL import ImageTk, Image
import requests as rq
from io import BytesIO

window = tk.Tk(className=" Youtube downloader")
window.geometry("400x400")

SAVE_PATH = "C:\\Users\\yahia\\Downloads"

def loadInfo(event):
	title = ""
	link = entry.get()
	try:
		yt = YouTube(link)
		title = yt.title
	except:
		title = ""

	global label2
	label2['text'] = title
	loadImg(link)

	return title

def getEntry():
	link = entry.get()
	choice = variable.get().lower()
	title = ""
	try:
		yt = YouTube(link)
		
		if choice == "mp3":
			stream = yt.streams.filter(only_audio=True).first()
		else:
			stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
		
		stream.download(SAVE_PATH, filename=yt.title+"."+choice)
		title = yt.title
		tk.messagebox.showinfo("showinfo", "Successfully downloaded")
	except:
		tk.messagebox.showerror("showerror", "Error")
	
	return title

def loadImg(link):
	global img
	try:
		img_url = YouTube(link).thumbnail_url
		response = rq.get(img_url)
		img_data = response.content
		image = Image.open(BytesIO(img_data))
		image = image.resize((80, 80), Image.ANTIALIAS)
		img = ImageTk.PhotoImage(image)
		panel['image'] = img
	except:
		panel['image'] = ""

#input, label, button
label = tk.Label(window,
	text="Enter Video link : ",
    width=25,
    height=2,
    fg="black",
    font=("Arial", 19),
)
label.pack()

OPTIONS = ["MP3","MP4"]
variable = tk.StringVar(window)
variable.set(OPTIONS[0])

entry = tk.Entry(window, bd =5, width=25)
entry.bind('<KeyRelease>',loadInfo)
entry.pack()

choice = tk.OptionMenu(window, variable, *OPTIONS)
choice.pack()
btn = tk.Button(window, text = "Go", command = getEntry)
btn.pack()

#video info
label2 = tk.Label(window,
	text="",
	width=0,
	height=10,
	fg="black",
	font=("Arial", 12))
label2.pack()
img = ""
panel = tk.Label(window, image=img)
panel.pack(side="bottom", fill="both", expand="yes")

window.resizable(False, False)
window.mainloop()
			

