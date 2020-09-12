import json
import boto3
import os
import uuid
# 이 코드는 s3에 텍스트가 업로드 되는 이벤트가 발생하면,
# 받은 파일을 디코딩 하는 과정을 거쳐 string type 형태로 만들고
# string type의 내용을 AWS Polly 를 이용하여 텍스트를 음성으로 변환시킨다.
# 텍스트를 음성으로 변환 후 변환된 파일을 S3에 저장한다. 
s3 = boto3.client('s3')
translate = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)
def lambda_handler(event, context):
    #post_id = str(uuid.uuid4())
    #output=os.path.join('/tmp/',post_id)
    try:
        for record in event['Records']:
            # 버켓 네임을 받음
            bucket = record['s3']['bucket']['name']
            # 파일 Key를 받음
            key = record['s3']['object']['key']
            mp3filename= key
            print("bucket name :",bucket)
            print("bucket key :", key)
            response = s3.get_object(Bucket=bucket, Key=key)
            #emailcontent = response['Body'].read()
            #print("email:",emailcontent)
            emailcontent = response['Body'].read().decode('utf-8')
            #emailcontent = response['Body'].read().encode('utf-8')
            print("data:",emailcontent)
            
            print(type(emailcontent))
            #encoded = emailcontent.encode('utf-8')
            #print("enoded :",encoded)
            polly = boto3.client('polly')
            post_id = str(uuid.uuid4())
            response = polly.synthesize_speech(
            Text=emailcontent,
            OutputFormat="mp3",
            VoiceId="Seoyeon")
            stream=response.get("AudioStream")
            
            #s3.put_object(Body=textractData, Bucket=bucket, Key=generateFilePath)
            output=os.path.join('/tmp/',post_id)
            with open(output, 'wb') as f:
                data2 = stream.read()
                f.write(data2)
      
            bucketname ="useast1s3textupload"
            keyreplace =key.replace(".txt","")
            s3.upload_file('/tmp/'+post_id,bucketname,keyreplace+'.mp3')
    except Exception as e:
        print(e)
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')