import json
import boto3
import os
import urllib.parse
# 이 파일은 S3에 업로드된 이미지를 TexTract를 이용하여 문자 추출 후
# 문자를 Translate 기능을 이용하여 한국어로 번역한 텍스트 파일을 
# 새로운 버킷에 전송하는 내용이다.
s3 = boto3.client('s3')
textract= boto3.client('textract')
translate = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)
def getTextractData(bucketName, documentKey):
    print('Loading getTextractData')
    # Call Amazon Textract
    response = textract.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': bucketName,
                'Name': documentKey
            }
        })
        
    detectedText = ''

    # Print detected text
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            detectedText += item['Text'] + '\n'
            
    return detectedText
def writeTextractToS3File(textractData, bucketName, createdS3Document):
    print('Loading writeTextractToS3File')
    generateFilePath = os.path.splitext(createdS3Document)[0] + '.txt'
    s3.put_object(Body=textractData, Bucket=bucketName, Key=generateFilePath)
    print('Generated ' + generateFilePath)
    
def lambda_handler(event, context):
    print("시작 ")
    #bucket = record['s3']['bucket']['name']
    #key = urllib.parse.unquote_plus
    bucket = event['Records'][0]['s3']['bucket']['name'] # 저장소이름 
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8') # 파일이름 
    print("bucket name :",bucket)
    print("bucket key :", key)
    try:
        detectedText=getTextractData(bucket,key)
        #bucket = "useast1s3textupload"
        result = translate.translate_text(Text=detectedText,
            SourceLanguageCode="en", TargetLanguageCode="ko")
        print('TranslatedText: ' + result.get('TranslatedText'))
        print('SourceLanguageCode: ' + result.get('SourceLanguageCode'))
        print('TargetLanguageCode: ' + result.get('TargetLanguageCode'))
        bucket = "useast1s3textupload"
        writeTextractToS3File(result.get('TranslatedText'),bucket,key)
        return 'Processing Done!'
               
    except Exception as e:
        print(e)