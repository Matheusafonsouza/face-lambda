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


def compare_faces(faces):
    result = list()
    for face in faces:
        result.append(client.search_faces(
            CollectionId='faces',
            FaceId=face,
            FaceMatchThreshold=80,
            MaxFaces=10
        ))
    return result


detected_faces = detect_face()
compared_faces = compare_faces(detected_faces)
print(json.dumps(compared_faces, indent=4))
