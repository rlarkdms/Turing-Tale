import requests

from bs4 import BeautifulSoup

import re

import boto3

import time


url1=requests.get("https://www.newsinlevels.com").text
#이 홈페이지에서 크롤링함.
soup=BeautifulSoup(url1, "html.parser")

key1=soup.find(attrs={'class':'news-block highlighted'})
key2=key1.find(attrs={'class':'img-wrap'})
key3=key2.find('a')['href']

url2=requests.get(key3).text

soup=BeautifulSoup(url2, "html.parser")
newstitle=str(soup.find(attrs={'class':'article-title'}))
news1=str(soup.find(attrs={'id':'nContent'}))
news1=re.sub('<.+?>','',news1,0).strip()

newstitle=re.sub('<.+?>','',newstitle,0).strip()

rep=""

realti=""

for i in range(16,len(news1)-56):
    rep=rep+news1[i]

for j in range(len(newstitle)-12):
    realti=realti+newstitle[j]

s3=boto3.client('s3',
    aws_access_key_id='',
    aws_secret_access_key='')


polly=boto3.Session(
    aws_access_key_id='',
    aws_secret_access_key='',
    region_name='us-east-1').client('polly')



response_woman=polly.synthesize_speech(
    Text=rep,
    OutputFormat="mp3",
    VoiceId="Joanna")

response_man=polly.synthesize_speech(
    Text=rep,
    OutputFormat="mp3",
    VoiceId="Joey")

stream_woman=response_woman.get("AudioStream")

stream_man=response_man.get("AudioStream")



realtimp3_woman=realti+"_woman.mp3"

realtimp3_man=realti+"_man.mp3"

print("rep :",type(rep))
rep_strip = rep.strip()
print("\n\n")
#print("rep_strip :",rep_strip)
Fix_Comma = '.'
rep_strip_len = len(rep_strip)
print("Len :",rep_strip_len)
Result_Text=""

count = 0
for i in range(rep_strip_len):
    if(i > 450):
        break
    #print("Count :",count)
    count+=1
    Result_Text+=rep_strip[i]
    if(count == 70):
        Result_Text+="\n"
        count=0

#print("Result_Text :",Result_Text)
Result_Text_Fix = Result_Text.strip()
#print("Result :",Result_Text_Fix)
with open('mp3/'+realtimp3_woman,'wb') as f:
    data=stream_woman.read()
    f.write(data)

with open('mp3/' + realtimp3_man, 'wb') as f:
    data = stream_man.read()
    f.write(data)

print("string realtl :",realti)
print("Type realti :",realti)
realtitxt=realti+".txt"



with open('txt/'+realtitxt,'w') as f:
    f.write(Result_Text_Fix)#이 부분에서 ubuntu에서는 'wb'로 실행해도 코드가 실행 되지만
#pycharm에서는 'w'로 실행해야 실행 가능함.

print("realtitxt :",realtitxt)
s3.upload_file('txt/'+realtitxt,'',realtitxt)
s3.upload_file('mp3/'+realtimp3_woman,'',realtimp3_woman)
s3.upload_file('mp3/'+realtimp3_man,'',realtimp3_man)
