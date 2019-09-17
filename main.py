from UniversityList import *
import threading
import tkinter as tk
class MainCanvas:
	def __init__(self,App):
		self.App=App
		self.Universities=getWebsitesFromFile("Universities.txt")
		self.UniversitiesList= tk.Listbox(self.App.MainWindow,height=10,width=40)
		self.Faculties=None
		self.FacultyList= tk.Listbox(self.App.MainWindow,height=10,width=40)
		self.Threads={}
		self.GrabberRunning=False
		i=1
		for uni in self.Universities:
			self.UniversitiesList.insert(i,uni)
			i+=1
		self.UniversitiesList.grid(row=0,column=0,rowspan=5)
		self.OpenUniBotton=tk.Button(self.App.MainWindow,text="Browse University",command=self.OpenUniversityWeb)
		self.OpenUniBotton.grid(row=1,column=1)
		self.OpenCivilWebBotton=tk.Button(self.App.MainWindow,text="Browse Civil Dept.",command=self.OpenCivilWeb)
		self.OpenCivilWebBotton.grid(row=2,column=1)
		self.LoadFacultyBotton=tk.Button(self.App.MainWindow,text="Load Faculty",command=self.LoadFacultyFromUni)
		self.LoadFacultyBotton.grid(row=3,column=1)
		self.FacultyList.grid(row=1,column=2,rowspan=5)
		self.GrabFacultyBotton=tk.Button(self.App.MainWindow,text="Run Faculty Grabber",command=self.GrabFacultyFromWeb)
		self.GrabFacultyBotton.grid(row=6,column=0)
		self.Notice=tk.StringVar()
		self.Notice.set('Welcome.. Browse through the Universities to find professors.')
		self.NoticeText=tk.Label(self.App.MainWindow,textvariable=self.Notice)
		self.NoticeText.grid(row=8,columnspan=3)
	def OpenUniversityWeb(self):
		index=(self.UniversitiesList.curselection()[0])
		web=list(self.Universities.values())[index]
		os.startfile(web)
	def OpenCivilWeb(self):
		index=(self.UniversitiesList.curselection()[0])
		uni=list(self.Universities.keys())[index]
		web=getCivilProgramSite(uni)
		os.startfile(web)
	def LoadFacultyFromUni(self):
		index=(self.UniversitiesList.curselection()[0])
		web=list(self.Universities.values())[index]
		self.Faculties=getProffList_File(web)
		self.UpdateFacultyList()
	def Grabbing(self):
		v=tk.StringVar()
		v.set("Grabber Running")
		self.GrabbingText=tk.Label(self.App.MainWindow,textvariable=v,anchor="w")
		self.GrabbingText.grid(row=7)
		i=1
		while self.GrabberRunning:
			v.set("Grabber Running"+"."*i)
			i+=1
			time.sleep(1)
			if (i>5):
				i=0
		self.GrabbingText.destroy()
	def GrabFacultyFromWeb(self):
		if self.GrabberRunning:
			self.GrabberRunning=False
			self.Threads['capture_Clipboard']._stop()
			self.Threads['Grabbing']._stop()
		else:
			self.Threads['capture_Clipboard']=threading.Thread(target=self.capture_Clipboard)
			self.Threads['capture_Clipboard'].daemon=True
			self.Threads['capture_Clipboard'].start()
			self.Threads['Grabbing']=threading.Thread(target=self.Grabbing)
			self.Threads['Grabbing'].daemon=True
			self.Threads['Grabbing'].start()
			self.GrabberRunning=True
	def capture_Clipboard(self):
		pc.copy('capture_Clipboard Running')
		prev_text = pc.paste()
		while self.GrabberRunning:
			try:
				new_text = pc.paste()
				if prev_text != new_text:
					if re.match(r'https*://.*[.]edu.*',new_text):
						print("Getting info from: "+new_text)
						self.Faculties= getProfessorList_Web(new_text,self)
						self.UpdateFacultyList()
						print("Grabbing Completed.\nWaiting for new.")
						self.Notice.set("Retrival Completed from :"+new_text)
			except Exception as e:
				self.Notice.set("Some Error Occured")
				print(e)
			prev_text = new_text
			time.sleep(1)
	def UpdateFacultyList(self):
		i=1
		self.FacultyList.delete(0,'end')
		for prof in self.Faculties:
			self.FacultyList.insert(i,prof.Name)
			i+=1
class MainApp:
	def __init__(self):
		self.MainWindow= tk.Tk()
		self.MainWindow.geometry("600x300")
		self.MainWindow.title("Browsing Through Universities")
		#self.MenuStripe= MainMenuStripe(self)
		self.Canvas=MainCanvas(self)
		self.MainWindow.mainloop()
if __name__=="__main__":
	App=MainApp()


