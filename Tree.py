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
	def showTree(self):
		print(chr(195)+chr(196)*self.Rank+">"+(chr(196)*2)+"("+str(self.child)+"/"+str(self.TotalChildrens)+")"+("-"*3)+self.Value)
		for child in self.childNodes:
			child.showTree()
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
if __name__=="__main__":
	pass