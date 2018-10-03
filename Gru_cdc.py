import requests
import os
from bs4 import BeautifulSoup as bs
file = open("invalid.html", "r+")
fileList=open("Gru_CDC_Company_List.html","w+")
fileList.write("<html><title>CDC List</title><body><table><Tr><Th>Code</Th><Th>Company</Th></Tr>")
for i in range(400):
    print(i)
    url = "https://erp.iitkgp.ac.in/TrainingPlacementSSO/TPJNFView.jsp?jnf_id=1&com_id="+str(i)+"&yop=2018-2019&user_type=SU"
    cookies=dict(ssoToken="9F3896DA01BE7BB86779FB7754A83291.worker22331A48BD9FDE9C46D55D49EE4DD2816.worker1AS0XGON5DN51NTEGTZTD3VIWDDN8F6ZT0RB7JFP7URWMBC6J2AI14BH35ISPDW8K")
    r=requests.get(url,cookies)
    print(len(r.content))
    if(len(r.content)==8192):
        continue
    file2=open("Data\\"+str(i)+".html","w+")
    #data=str(r.content).replace("\\n","")
    soup=bs(r.content,"html.parser")
    #print(soup.prettify())
    company=soup.findAll('td', align="center")
    company=str(company).replace("<td align=\"center\" class=\"header\">","").replace("</td>","")
    company=company[11:len(company)-1]
    print(company)
    fileList.write("<Tr><Td>"+str(i)+"</Td><Td><a href=\"file:///C:/Users/hp/Desktop/GRU_All/Data/"+str(i)+".html\" >"+company+"</a></Td></Tr>")
    file2.write(str(r.content.decode('cp1252')))
    file2.close()
fileList.write("</Table></Body></Html>")
fileList.close()
file.close()