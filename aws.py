import io
import os
import boto3
import requests as requests

allowed_extensions = ['jpeg', 'png', 'webp', 'img']

def is_file_allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

s3_client = boto3.client('s3', aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID'],
                             aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY'],
                         )

def generate_urls(image_datas:[], key:str):
    index = 0
    urls = []
    for data in image_datas:
        try:
            curr_key = key + str(index)
            print(curr_key)
            s3_client.upload_fileobj(data, "rec-man-bucket", curr_key)
            urls.append(f"https://rec-man-bucket.s3.amazonaws.com/{curr_key}")
            index += 1
        except Exception as e:
            print("Something Happened: ", e)
            raise e
    return urls

#https://<bucket_name>.s3.amazonaws.com/<filename>.<extension>
"""
test_data = requests.get('https://www.google.de/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png').content
print(os.environ)
print(generate_urls([io.BytesIO(test_data)], "somethingelse"))'"
"""