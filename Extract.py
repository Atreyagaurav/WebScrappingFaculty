import os
import pandas
def getProfInfo(ProfFile):
	f=open(ProfFile)
	lines=f.readlines()
	f.close()
	return lines
curDirect=os.getcwd()
os.chdir(curDirect+"/Data")
UniFiles=iter(os.listdir(curDirect+"/Data"))
data={'Name':[],'Profile Link':[],'Department Website':[],'E-mail':[],'Interests':[]}
for unifile in UniFiles:
	os.chdir(curDirect+"/Data/"+unifile)
	ProfFiles=iter(os.listdir(curDirect+"/Data/"+unifile))
	for prof in ProfFiles:
		info=getProfInfo(prof)
		print("Scanning:"+unifile+"/"+prof)
		# if len(info)<4:
		# 	for i in range(4-len(info)):
		# 		info.append('')
		data['Name'].append(info[0][:-1])
		data['Profile Link'].append(info[1][:-1])
		data['Department Website'].append(info[2][:-1])
		data['E-mail'].append(info[3][:-1])
		data['Interests'].append(info[4][:-1])
df=pandas.DataFrame(data)
os.chdir(curDirect)
df.to_csv("profList.csv")