import json
import boto3 as boto

BUCKET = 'fa-afonso-images'
WEBSITE_BUCKET = 'fa-afonso-website'
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


def parse_data(detected_faces):
    parsed_response = list()
    for face in detected_faces:
        match = face.get('FaceMatches')
        if not match:
            continue
        parsed_response.append(dict(
            name=match[0].get('Face').get('ExternalImageId'),
            face_id=match[0].get('Face').get('FaceId'),
            similarity=round(match[0].get('Similarity'), 2)
        ))
    return parsed_response


def publish_data(parsed_data):
    file = s3.Object(WEBSITE_BUCKET, 'data.json')
    file.put(Body=json.dumps(parsed_data))


def remove_files(detected_faces):
    client.delete_faces(
        CollectionId='faces',
        FaceIds=detected_faces
    )


detected_faces = detect_face()
compared_faces = compare_faces(detected_faces)
parsed_compared_faces = parse_data(compared_faces)
print(json.dumps(parsed_compared_faces, indent=4))
publish_data(parsed_compared_faces)
remove_files(detected_faces)
