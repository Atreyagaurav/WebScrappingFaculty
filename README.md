# WebScrappingFaculty
to collect faculty information from universities website
## More Information:
It is made so as to collect faculty information from web pages of universities. Although it tries to collect information like Name, web address, email and Research Interests, the last two part aren't completely successful yet.
I first tried to make everything automatic but it was hard to find the faculty website by itself, although the website of the department is easy to find. So now I have given that task to user.
## Prerequisites:
* A web browser. 
* Internet connection.
* Ms. Excel 
## How to Use
### To completely automate
* Edit the list of universities in file Universities.txt if you want. 
* Run UniversityList.py and wait till it is completed (will take a long time).
* Run Extract.py to collect the info into the profList.csv.
### To browse manually
* Open main.py
* Run Faculty Grabber : It'll run a endless loop where if you put any faculty website in clipboard it'll extract the info.
* Select any university
* Click Browse Civil Dept. button. It'll open the civil departmental website in your browser.
* Find the page with faculty information and copy the link into clipboard. (just click Ctrl + C)
* Now the grabber will extract information, see the information shown in console of the GUI for more info. 
* Open another website and copy link when one is complete.
## TODO:
* Make the "Load Faculty" button load the faculty information from memory.
* GUI to display professor inforamtion. Including Photo if possible.
* A collector to collect all the information in the data folder into an excel file. 
* Make the process completely automated if possible. 
* Make options for other departments except civil engineering.
