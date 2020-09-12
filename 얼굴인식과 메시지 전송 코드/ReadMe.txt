[ Rekognition & Line Notify ]

사용하는 AWS 서비스 : Lambda - A, S3-A, S3-B , Rekognition 
SNS 서비스 : Line Notify

이 기능은 얼굴인식을 통해 등록되지 않은 사람이 감지되면 알림 메세지를 전달하는 내용입니다.

먼저 S3-A에 등록시킬 사용자의 이미지를 업로드 합니다.

그리고 S3-B 라는 버킷은 Lambda -A 와 연결해둡니다.

라즈베리파이를 통해 S3-B에 이미지가 업로드가 되면,

Lambda -A 가 동작합니다.

그 동작은 업로드된 이미지와 S3 -A 에 있는 이미지들을 

AWS Rekognition을 이용하여 하나씩 비교합니다.

비교 결과, 얼굴의 유사도가 특정 값 이하라면 이 결과와 이미지를

Line Notify를 통해 전달됩니다. 