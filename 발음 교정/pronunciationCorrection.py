#-*- coding:utf-8 -*-
import urllib3
import json
import base64

openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/Pronunciation"
accessKey = "api키"
audioFilePath = "audio/test6.wav"
languageCode = "english"

#녹음된 음성파일의 제시 문장입니다. 
#API 요청 시 script가 포함되지 않는 경우 비원어민 영어 음성인식을 수행한 이후 인식 결과에 대한 발음평가 점수를 제공합니다.
#API 정확도가 집나가서 이거 있으면 0.0 점 나오는 거였음
script = "when shall i pay for it now or at check out time."
 
file = open(audioFilePath, "rb")
audioContents = base64.b64encode(file.read()).decode("utf8")
file.close()
 
requestJson = {
    "access_key": accessKey,
    "argument": {
        "language_code": languageCode,
        #"script": script,
        "audio": audioContents
    }
}
 
http = urllib3.PoolManager()

response = http.request(
    "POST",
    openApiURL,
    headers={"Content-Type": "application/json; charset=UTF-8"},
    body=json.dumps(requestJson)
)

 
print("[responseCode] " + str(response.status))
print("[responBody]")
print(str(response.data,"utf-8"))