from UniversityList import *
import csv
def append_to_file(data):
    with open("results.txt","a+") as ffile:
        ffile.write(",".join(data)+"\n")

with open("profList.csv","rt") as csv_file:
    file_data= csv.reader(csv_file, delimiter=',')
    data={'Name':[],'Profile Link':[],'University':[],'E-mail':[],'Interests':[]}
    myInterests=re.compile(r'.*[Ss]teel [Ss]tructure.*|.*[Bb]ridge [Ss]tructure.*|.*[Rr]einforced [Cc]oncret.*')
    check=""
    x=True
    for info in file_data:
        if x:
            x=False
            continue
        try:
            link=info[2].strip()
            soup=getSoup(link)
            if soup:
                x=soup.find_all(text=myInterests)
                if x:
                    stri=''
                    for y in x:
                        stri+=y.string
                    stri=stri.replace('\n','; ')
                    if(stri==check):
                        continue
                    else:
                        check=stri
                    print("-"*20+'\n'+"MATCH FOUND"+'\n'+stri+'\n'+"-"*20)
                    data['Name'].append(info[1].strip())
                    data['Profile Link'].append(info[2].strip())
                    data['University'].append(info[3].strip())
                    data['E-mail'].append(info[4].strip())
                    data['Interests'].append(stri)
                    append_to_file((info[1].strip(),info[2].strip(),info[3].strip(),info[4].strip(),stri))
        except:
            pass