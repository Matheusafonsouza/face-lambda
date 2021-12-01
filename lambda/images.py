import boto3 as boto

BUCKET = 'fa-afonso-images'
REGION = 'us-east-1'

s3 = boto.resource('s3')
client = boto.client('rekognition', region_name=REGION)


def list_images():
    images = list()
    bucket = s3.Bucket(BUCKET)

    for image in bucket.objects.all():
        images.append(image.key)
    print(images)
    return images


def index_collection(images):
    try:
        client.describe_collection(CollectionId='faces')
    except Exception:
        client.create_collection(CollectionId='faces')

    for image in images:
        response = client.index_faces(
            CollectionId='faces',
            DetectionAttributes=[],
            ExternalImageId=image[:-4],
            Image=dict(S3Object=dict(
                Bucket=BUCKET,
                Name=image
            ))
        )


images = list_images()
index_collection(images)
