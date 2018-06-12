import sys
import requests
import webbrowser
from datetime import timedelta, date
def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)

roll=sys.argv[1]
if roll == 'reset':
    url="https://erp.iitkgp.ac.in/StudentPerformanceV2/auth/authenticate.htm?rollno=15QBT0012&dob=01-01-2000"
    f=open("gru.txt","w+")
    result=requests.get(url)
    f.write(str(result.content))
    print("File Reset Successful")
    exit()
ystart=sys.argv[2]
yend=sys.argv[3]
url="https://erp.iitkgp.ac.in/StudentPerformanceV2/auth/authenticate.htm?rollno="+roll+"&dob="
start_dt = date(int(ystart),1, 1)
end_dt = date(int(yend), 12, 31)
dob=daterange(start_dt, end_dt)
f=open("gru.txt","r+")
c2=f.read()
flag=0
for dt in dob:
    date=dt.strftime("%d-%m-%Y")
    print(date,end='\r')
    result=requests.get(url+date)
    c=result.content
    if str(c)==c2:
        continue
    else:
        flag=1
        webbrowser.open(url+dt.strftime("%d-%m-%Y"))
        break
if flag==0:
    print("User Not Found")