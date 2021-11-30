import json
import boto3 as boto

BUCKET = 'fa-afonso-images'
REGION = 'us-east-1'

s3 = boto.resource('s3')
client = boto.client('rekognition', region_name=REGION)


def detect_face():
    faces = client.index_faces(
        CollectionId='faces',
        DetectionAttributes=['DEFAULT'],
        ExternalImageId='temp_image',
        Image=dict(S3Object=dict(
            Bucket=BUCKET,
            Name='temp_sent_image.png'
        ))
    )

    faces_ids = list()
    face_records = faces.get('FaceRecords')
    for face in face_records:
        real_face = face.get('Face')
        faces_ids.append(real_face.get('FaceId'))

    return faces_ids


detected_faces = detect_face()
print(detected_faces)
