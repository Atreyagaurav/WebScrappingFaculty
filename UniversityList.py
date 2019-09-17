from urllib.parse import urljoin
import os.path
import threading
import enchant
import os
from bs4 import BeautifulSoup
import requests
import re
import pyperclip as pc
import time
import multiprocessing as mp
def getSoup(web):
	try:
		r=requests.get(web,timeout=(5,25))
		print(web+"::Retrived")
		return BeautifulSoup(r.text,'html.parser')
	except requests.exceptions.Timeout:
		print(web+"::Timeout")
		return None
def makeUniDirectory(Universities):
	curDirect=os.getcwd()
	os.chdir(curDirect+"/Data")
	for uni in Universities:
		web=Universities[uni]
		web=web.split('/')[-1]
		if not(os.path.exists(curDirect+"/Data/"+web)):
			os.mkdir(web)
	os.chdir(curDirect)
def giveUniPath(web):
	curDirect=os.getcwd()
	profList=[]
	os.chdir(curDirect+"/Data")
	uniAddress=get_base_url(web)
	web=uniAddress.split('/')[-1]
	if not(os.path.exists(curDirect+"/Data/"+web)):
		os.mkdir(curDirect+"/Data/"+web)
	os.chdir(curDirect)
	return (curDirect+"/Data/"+web)
def getProffList_File(uniAddress):
	curDirect=os.getcwd()
	profList=[]
	os.chdir(curDirect+"/Data")
	web=uniAddress.split('/')[-1]
	if (os.path.exists(curDirect+"/Data/"+web)):
		os.chdir(curDirect+"/Data/"+web)
		ProfFiles=iter(os.listdir(curDirect+"/profList"))
		for prof in ProfFiles:
			profList.append(Professor(prof))
	os.chdir(curDirect)
	return profList
def saveProfObj_Web(web,name):
	soup=getSoup(web)
	uniPath=giveUniPath(web)
	if soup==None:
		return None
	test=soup.find(['a','p','div','h2','h3','h4'],text=re.compile(r'Research Interests.*|Interests.*'))
	if test==None:
		Interests=None
	else:
		Interests=test.text
	try:
		test=test.find_next_siblings()[0]
		Interests+=test.text
	except:
		pass
	finally:
		test=soup.find('a',href=re.compile('mailto:.*'))
		if test!=None:
			email=test['href'][7:]
		else:
			test=soup.find(['a','p','div','h2','h3','h4'],text=re.compile(r'.*@.*[.].*'))
			if test!=None:
				email=test.text
			else:
				email=None
		uni=getWebsitesFromFile(os.getcwd()+"/Data/Universities.txt")
		uni={v: k for k, v in uni.items()}
		f=open(uniPath+"/"+name+".txt","wt")
		prop=(name,web,get_base_url(web),email,Interests)
		for p in prop:
			if p==None:
				f.write('\n')
			else:
				f.write(p+'\n')
		f.close()
		return uniPath+"/"+name+".txt"
def getCivilProgramSite(uni):
	webText= (uni+" Civil Engineering Graduate Programs").replace(" ","+")
	webText= webText.replace(",","%2C")
	webText="https://www.google.com/search?client=firefox-b-d&q="+webText
	r=requests.get(webText)
	soup=BeautifulSoup(r.text,'html.parser')
	sObj=soup.find_all('a',{'href':re.compile(r'http://www[.].*[.]edu|.*[.]edu')})
	if len(sObj)==0:
		print("a href didn't work")
	web=(sObj[0]['href'])
	web=web.replace(" › ","/")
	temp=re.match(r'.*(https*://.*[.]edu/.*)&.*',web)
	if temp:
		asdad=temp.groups()[0]
		asd=asdad.split('&')
		web=asd[0]
	elif(not(web.startswith('http://'))):
		web='http://'+web
	return web
def getUniversities():
	uni=[]
	r=requests.get("https://www.mastersportal.com/ranking-country/82/united-states.html")
	soup=BeautifulSoup(r.text,'html.parser')
	sObj=soup.find_all('td',{'data-title':'Universities'})
	for ob in sObj:
		uni.append(ob.text)
	return uni
def getWebsites(UniList,Display):
	uniWeb={}
	for uni in UniList:
		webText= uni.replace(" ","+")
		webText= webText.replace(",","%2C")
		webText="https://www.google.com/search?client=firefox-b-d&q="+webText
		#os.startfile(webText)
		r=requests.get(webText)
		soup=BeautifulSoup(r.text,'html.parser')
		sObj=soup.find_all('div',{'class':'BNeawe UPmit AP7Wnd'})
		uniWeb[uni]=sObj[0].text
		if(Display):
			print(uni+":"+uniWeb[uni])
	return uniWeb
def getWebsitesFromFile(file):
	lines = [line.rstrip('\n') for line in open(file)]
	uniWeb={}
	for line in lines:
		var=line.split(';')
		if(not(var[1].startswith('http'))):
			var[1]='http://'+var[1]
		uniWeb[var[0]]=var[1]
	return uniWeb
def saveUniversities(UniList,file):
	f=open(file,"wt")
	for uni in UniList:
		f.write(UniList[uni]+"\n")
	f.close()
def get_base_url(web):
	ind=web.split("/")
	new=ind[:3]
	return '/'.join(new)
def getRelatedURLs(web,keys):
	urls=[]
	temp=re.match(r'.*(https*://.*[.]edu/.*)&.*',web)
	if temp:
		asdad=temp.groups()[0]
		asd=asdad.split('&')
		web=asd[0]
	elif(not(web.startswith('http://'))):
		web='http://'+web
	r=requests.get(web)
	soup=BeautifulSoup(r.text,'html.parser')
	sObj=soup.find_all('a',href=True)
	for ob in sObj:
		if(re.search(keys,ob['href'])):
			url=ob['href']
			if not(url.startswith('http')):
				url = urljoin(get_base_url(web), url)
			urls.append(url)
	return urls
def saveProfessorInfo(url):
	pass
	# r=requests.get(url)
	# soup=BeautifulSoup(r.text,'html.parser')
def getProfessorList_Web(url,AppCanvas):
	r=requests.get(url)
	web=get_base_url(url)
	link={}
	soup=BeautifulSoup(r.text,'html.parser')
	sObj=soup.find_all('a',href=True)
	for ob in sObj:
		if((len(ob.text.split(' '))==2 or len(ob.text.split(' '))==3) and isName(ob.text)):
			url=ob['href']
			if not(url.startswith('http')):
				url = urljoin(get_base_url(web), url)
			link[ob.text]=url
	profNames= RemoveOutliners(link)
	if profNames==None:
		return None
	profList=[]
	for profName in profNames:
		site=profNames[profName]
		fname=saveProfObj_Web(site,profName)
		if fname==None:
			continue
		AppCanvas.Notice.set("Found Professor: "+profName+"\nDetails Saved in Local Memory.")
		profList.append(Professor(fname))
	return profList
def isName(str):
	try:
		x= str.split(' ')
		if all(y[0].upper()==y[0] for y in x):
			return True
	except:
		return False
def collectUniInfo():
	websites=getWebsitesFromFile("Universities.txt")
	for uni in websites:
		try:
			collectProfessorSites(uni)
		except:
			pass
	# uniThreads=[]
	# for uni in websites:
	# 	x=threading.Thread(target=collectProfessorSites,args=(uni,))
	# 	x.start()
	# 	uniThreads.append(x)
	# 	time.sleep(5)
	# for thrd in threading.enumerate():
	# 	thrd.join()
def collectProfessorSites(uni):
	webText= (uni+" Civil Engineering Graduate Programs").replace(" ","+")
	webText= webText.replace(",","%2C")
	webText="https://www.google.com/search?client=firefox-b-d&q="+webText
	print("getting:"+webText)
	r=requests.get(webText)
	soup=BeautifulSoup(r.text,'html.parser')
	sObj=soup.find_all('a',{'href':re.compile(r'http://www[.].*[.]edu|.*[.]edu')})
	if len(sObj)==0:
		print("a href didn't work")
	web=(sObj[0]['href'])
	web=web.replace(" › ","/")
	print("getting:"+web)
	urls=getRelatedURLs(web,r'[Ff]aculty')
	if(len(urls)==0):
		return
	fname=get_base_url(urls[0]).split('/')
	if os.path.isfile("profList/"+fname[-1]+".txt"):
		print("Already scanned: "+uni)
		return
	lis=[]
	print("Universities Scanning: \t"+uni+"\n")
	actual=None
	for url in urls:
		print("getting:"+url)
		actual=getProfessorList(url)
		if actual==None:
			continue
		lis.append(actual)
		if(len(actual)>20):
			break
	if(len(lis)>1):
		n=len(lis[0])
		for data in lis:
			if(len(data)>n):
				actual=data
				n=len(data)
	saveDict(actual,"profList/"+fname[-1]+".txt")
	print("Results from"+uni+'\n')
	print(actual)
	print("\n")
def RemoveOutliners(givenDict):
	#Given Dict is the dictionary, where dissimilar links has to be removed.
	givenDict=removeEnglishWords(givenDict)
	newDict= {v: k for k, v in givenDict.items()}
	if (len(newDict)==0):
		return None
	Links=Node('Root',0)
	for ind in newDict:
		Links.AddMultiLayer(ind.split('/'))
	common=Links
	while(common.TotalChildrens>len(newDict)/2):
		common=common.getMainChild()
	if(common.Rank<4):
		return None
	leaves= common.Parent.getLeaves()
	finalDict={}
	for leaf in leaves:
		link=leaf.collectLeaf('/')
		link=link[5:]
		if(link in newDict):
			finalDict[newDict[link]]=link
	if(len(finalDict)<5):
		return None
	return finalDict
def removeEnglishWords(dicti):
	d=enchant.Dict("en_US")
	rem=[]
	for val in dicti:
		wrds=val.split(' ')
		flag=True
		for wrd in wrds:
			if not(d.check(wrd.lower()) or wrd==wrd.upper()):
				flag=False
		if flag:
			rem.append(val)
	for al in rem:
		dicti.pop(al)
	return dicti
def saveDict(dict,file):
	if dict==None:
		return
	f=open(file,"wt")
	for uni in dict:
		f.write(uni+';'+dict[uni]+"\n")
	f.close()
def getSoup(web):
	try:
		r=requests.get(web,timeout=(5,25))
		print(web+"::Retrived")
		return BeautifulSoup(r.text,'html.parser')
	except requests.exceptions.Timeout:
		print(web+"::Timeout")
		return None
class Node:
	def __init__(self,val,parent=None,rnk=0):
		self.Value=val
		self.Parent=parent
		self.child=0
		self.Rank=rnk
		self.TotalChildrens=0
		self.childNodes=[]
	def AddMultiLayer(self,values):
		n=len(values)
		node=self.addNode(values[0])
		if n==1:
			return
		else:
			node.AddMultiLayer(values[1:])
		self.refresh()
	def addNode(self,val):
		if(self.hasChildValue(val)):
			return self.getChild(val)
		self.childNodes.append(Node(val,self,self.Rank+1))
		self.child+=1
		self.TotalChildrens+=1
		return self.childNodes[self.child-1]
	def removeNode(self,val):
		for i in range(self.child):
			if(self.childNodes[i].Value==val):
				self.TotalChildrens-=(self.childNodes[i].TotalChildrens+1)
				self.childNodes.pop(i)
	def refresh(self):
		num=self.child
		for childrens in self.childNodes:
			childrens.refresh()
			num+=childrens.TotalChildrens
		self.TotalChildrens=num
	def hasChildValue(self,val):
		for i in range(self.child):
			if(self.childNodes[i].Value==val):
				return True
		return False
	def getChild(self,val):
		for i in range(self.child):
			if(self.childNodes[i].Value==val):
				return self.childNodes[i]
	def show(self):
		print("Value="+self.Value)
		print("childNodes="+str(self.child))
		print("Total childNodes="+str(self.TotalChildrens))
	def showAll(self):
		self.show()
		for child in self.childNodes:
			child.showAll()
	def getMainChild(self):
		if self.child==0:
			return None
		child=self.childNodes[0]
		for i in range(self.child):
			max=self.childNodes[0].TotalChildrens
			if(self.childNodes[i].TotalChildrens>max):
				max=self.childNodes[i].TotalChildrens
				child=self.childNodes[i]
		return child
	def getLeaves(self,prev=[]):
		for i in range(self.child):
			if(self.childNodes[i].child==0):
				prev.append(self.childNodes[i])
			else:
				prev=self.childNodes[i].getLeaves(prev)
		return prev
	def CollectAll(self,deliminator=''):
		lis=[]
		leaves=self.getLeaves()
		for node in leaves:
			link=node.Value
			par=node.Parent
			r=node.Rank-self.Rank
			for i in range(r):
				link=par.Value+deliminator+link
				par=par.Parent
			lis.append(link)
		return lis
	def collectLeaf(self,deliminator=''):
		link=self.Value
		par=self.Parent
		r=self.Rank
		for i in range(r):
			link=par.Value+deliminator+link
			par=par.Parent
		return link
class Professor:
	def __init__(self,filename):
		f=open(filename)
		data=f.readlines()
		f.close()
		self.Name=data[0]
		self.WebAddress=data[1]
		self.University=data[2]
		self.email=data[3]
		self.Interests=data[4]
		self.Updated=True
		#self.getDataFromFile(filename)
class ProfList:
	def __init__(self):
		self.Universities=[]
		self.Professors={}
		curDirect=os.getcwd()
		os.chdir(curDirect+"/profList")
		UniFiles=iter(os.listdir(curDirect+"/profList"))
		os.chdir(curDirect)
		for unifile in UniFiles:
			self.Universities.append(unifile[:-4])
			f=open(unifile)
			indv=f.readlines()
			obj=[]
			count=0
			for prof in indv:
				data=prof.split(';')
				temp=Professor(data[0],data[1])
				if temp.Updated==False:
					count+=1
					if count==5:
						break
					continue
				else:
					count=0
				obj.append(temp)
			self.Professors[unifile[:-4]]=obj
		print(self.Professors)
if __name__=="__main__":
	collectUniInfo()
	#Profs=ProfList()
	#prof=Professor("Ana P. Barros","https://cee.duke.edu/faculty/ana-barros")

