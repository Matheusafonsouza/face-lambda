import json
import boto3 as boto

BUCKET = 'fa-afonso-images'
WEBSITE_BUCKET = 'fa-afonso-website'
REGION = 'us-east-1'


class FaceRecognition:
    def __init__(self):
        self.s3 = boto.resource('s3')
        self.rck = boto.client('rekognition', region_name=REGION)

        self.faces = self.detect_face()
        self.data = self.compare_faces()
        print(json.dumps(self.data, indent=4))
        self.publish_data()

    def detect_face(self):
        faces = self.rck.index_faces(
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

    def compare_faces(self):
        result = list()
        for face in self.faces:
            result.append(self.rck.search_faces(
                CollectionId='faces',
                FaceId=face,
                FaceMatchThreshold=80,
                MaxFaces=10
            ))
        return self.parse_data(result)

    def parse_data(self, detected_faces):
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

    def publish_data(self):
        file = self.s3.Object(WEBSITE_BUCKET, 'data.json')
        file.put(Body=json.dumps(self.data))
        self.remove_files()

    def remove_files(self):
        self.rck.delete_faces(
            CollectionId='faces',
            FaceIds=self.faces
        )


FaceRecognition()
