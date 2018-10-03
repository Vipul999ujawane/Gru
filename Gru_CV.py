import requests
import os
import sys
from bs4 import BeautifulSoup as bs
def cv_core(roll):
    invalid=open("CV\\invalid.pdf","r+")
    url = "https://erp.iitkgp.ac.in/TrainingPlacementSSO/AdmFilePDF.htm?path=/DATA/EXTERNAL/ARCHIVE/TRAINGANDPLACEMNT/STUDENT/"+roll+"/RESUME/1.pdf"
    token = open("SSO.gru","r")
    cookies=dict(ssoToken=str(token.read()))
    token.close()
    r=requests.get(url,cookies)
    print(len(r.content)==4108)
    if(len(r.content)==4108):
        data=input("Change SSOToken: ")
        token=open("SSO.gru","w")
        token.write(data)
        token.close()
        return
    if(r.content):
        print(r.content)
        file = open("CV\\"+roll+".pdf", "wb")
        file.write(r.content)
        file.close()
        print("File Written Successfully")

if __name__=="__main__":
    roll=sys.argv[1]
    cv_core(roll)