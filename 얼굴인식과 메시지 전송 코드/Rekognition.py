import json
import boto3
import requests
import time
import io
# 이 코드는 AWS Rekognition과 Line Notify를 이용하는 코드입니다.
# 특정 버킷에 사용자의 이미지를 등록한 뒤, 라즈베리파이를 통해 업로드 되는 사진과
# 등록된 이미지를 비교하여 유사도가 특정 값 이하라면, 사용자에게 알림을 전송하여
# 외부인이 침입했음을 알려주고, 그 이미지를 전송합니다.
s3 = boto3.client('s3')


def compare_faces(source_bucket, source_key, target_bucket, target_key, threshold=80, region="us-east-1"):
    rekognition = boto3.client("rekognition", region)
    response = rekognition.compare_faces(
        SourceImage={
            'S3Object': {
                'Bucket': source_bucket,
                'Name': source_key,
            }
        },
        TargetImage={
            "S3Object": {
                "Bucket": target_bucket,
                "Name": target_key,
            }
        },
        SimilarityThreshold=threshold,
    )
    return response['SourceImageFace'], response['FaceMatches']


def lambda_handler(event, context):

    url = "https://notify-api.line.me/api/notify"
    token = " "
    headers = {'Authorization': 'Bearer ' + token}

    try:
        for record in event['Records']:
            filename = record['s3']['object']['key'] # S3 버킷에 들어온 파일 이름 
            bucket = record['s3']['bucket']['name'] # S3 버킷 이름 
            stand = [] # 빈 배열 
         
            for object in s3.list_objects(Bucket='rekognitionuseast1s3')['Contents']: # list_object : S3 버킷에서 파일 가져옴
                print("Object['Key'] :",object['Key'])
                source_face, matches = compare_faces('rekognitionuseast1s3', object['Key'], bucket, filename)
                if not matches:
                    print("if not matches 문 :",matches)
                else:
                    print("stand 에 match 정보 추가")
                    stand.append(matches) # 빈 배열에 match 정보 저장 

            file_byte_string = s3.get_object(Bucket=bucket, Key=filename)['Body'].read() # 새로 업로드 되는 사진 
            print("File name :",filename)
       
            
            if not stand: # 빈 배열이라면, 
                msg = {
                    "message": (None, "등록되지 않은 "),
                    "imageFile": file_byte_string
                }
                res = requests.post(url, headers=headers, files=msg) # 외부인 사진을 전송 Line으로
                # 여기서 rekognitionuseast1s3 버킷에 파일 업로드
                print("Decoded file upload !!! ")
                print("res.text :", res.text)
                orientbucket='rekognitionuseast1s3'
                connectedbucket ='rekogniitonoutsiderimagedb'
                copy_source = {
                    'Bucket':'rekogniitonoutsiderimagedb',
                    'Key':filename
                }
                s3.copy_object(Bucket=orientbucket ,CopySource=copy_source,Key=filename)


            else:
                print("else 문 Stand :",stand)
                print("여기부분")
                # print(match['Similarity'])

                msg = {
                    "message": (None, "외부인 아니고 등록된 사람입니다~~~~~ "),
                    "imageFile": file_byte_string
                }

                res = requests.post(url, headers=headers, files=msg) # 내부자를 사진으로 전송 
                print(res.text)

    except Exception as e:
        print(e)

    return "Thanks"