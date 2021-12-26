import tkinter as tk
from pytube import YouTube, Playlist
from tkinter import messagebox
from PIL import ImageTk, Image
import requests as rq
from io import BytesIO
import os
import re

window = tk.Tk(className=" Youtube downloader")
window.geometry("400x400")
SAVE_PATH = "C:\\Users\\yahia\\Downloads"

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

def loadInfo(event):
	global label2
	link = entry.get()
	list = link.split("list")
	try:
		if len(list) == 2: #checking if it's a playlist
			pl = Playlist(link)
			title = "Playlist containing " + str(len(pl)) + " songs"
		else: # or if it's a single video
			yt = YouTube(link)
			title = yt.title
			#obj = dir(yt)
			#getattr(yt, obj[len(obj)-1])
	except:
		title = ""

	label2['text'] = title
	loadImg(link)
	return

def downloadVideo(link, choice, path=SAVE_PATH):
	yt = YouTube(link)
	if choice == "mp3":
		stream = yt.streams.filter(only_audio=True).first()
	else:
		stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
	subtitle = re.sub('[/\:*?"<>|]',  '',  yt.title) #removing not allowed characters
	stream.download(path, filename=subtitle+"."+choice)
	title = yt.title
	return title

def getEntry():
	link = entry.get()
	choice = variable.get().lower()
	title = ""
	list = link.split("list")
	if len(list) == 2:
		pl = Playlist(link)
		yt = YouTube(pl[0])
		try:
			path = os.path.join(SAVE_PATH, yt.author)
			if os.path.isdir(path) == False:
				os.mkdir(path)
			for index, video in enumerate(pl):
				try:
					title = downloadVideo(pl[index], choice, path)
					print(index, title, pl[index])
				except:
					pass
			tk.messagebox.showinfo("showinfo", "Playlist successfully downloaded")
		except:
			tk.messagebox.showerror("showerror", "Error")
			
	else:
		try:
			title = downloadVideo(link, choice)
			tk.messagebox.showinfo("showinfo", "Successfully downloaded")
		except Exception as e:
			print(e)
			tk.messagebox.showerror("showerror", "Error")
	
	return

#input, label, button
label = tk.Label(window, text="Enter Video link : ", width=25, height=2, fg="black", font=("Arial", 19))
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
label2 = tk.Label(window, text="", width=0, height=10, fg="black", font=("Arial", 12))
label2.pack()
img = ""
panel = tk.Label(window, image=img)
panel.pack(side="bottom", fill="both", expand="yes")

window.resizable(False, False)
window.mainloop()