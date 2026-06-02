import boto3
import os
from botocore.exceptions import NoCredentialsError

class S3Storage:
    def __init__(self):
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )
        self.bucket_name = os.getenv('AWS_S3_BUCKET')

    def upload_file(self, file_obj, filename):
        try:
            self.s3.upload_fileobj(
                file_obj,
                self.bucket_name,
                filename,
                ExtraArgs={'ACL': 'public-read'}
            )
            return f"https://{self.bucket_name}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{filename}"
        except NoCredentialsError:
            print("Credentials not available")
            return None
        except Exception as e:
            print(f"Error uploading to S3: {e}")
            return None

storage = S3Storage()
