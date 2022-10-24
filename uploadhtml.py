import boto3
import os


s3 = boto3.client('s3')

response = s3.list_buckets()
print("Here is a list of all the buckets in your account.")
for bucket in response['Buckets']:
         print('BucketName: {}'.format(bucket['Name']))

bucket_name = input(str("Which bucket would you like to upload files to?\n"))
fileName = ['app.js','error.html','index.html','styles.css']
 
for file in fileName:
    data = open(file)
    s3.put_object(
        Body=data,
        Bucket=bucket_name,
        Key=file,
        ContentType='text/html'
    )