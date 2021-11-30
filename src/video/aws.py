from dotenv import load_dotenv   
load_dotenv()   
from botocore.exceptions import ClientError
from boto3 import Session
import os

ACCESS_KEY = os.environ.get("ACCESS_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")
REGION_NAME = os.environ.get("REGION_NAME")
BUCKET_NAME = os.environ.get("BUCKET_NAME")

ses = Session(aws_access_key_id=ACCESS_KEY,
              aws_secret_access_key=SECRET_KEY,
              region_name=REGION_NAME)

s3 = ses.client('s3')

def getPresignedUrl(key=None):
    try:
        url = s3.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': BUCKET_NAME,
                'Key': key
            },
            ExpiresIn=600,
        )
        return url
    except ClientError as e:
        print(e)
        return None
