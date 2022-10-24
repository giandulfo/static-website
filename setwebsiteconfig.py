import boto3

s3 = boto3.client('s3')
response = s3.list_buckets()
print("Here is a list of all the buckets in your account.")
for bucket in response['Buckets']:
         print('BucketName: {}'.format(bucket['Name']))


bucket_name = input(str("Which bucket would you like to set static website hosting to?\n"))


s3.put_bucket_website(
     Bucket=bucket_name,
     WebsiteConfiguration={
     'ErrorDocument': {'Key': 'error.html'},
     'IndexDocument': {'Suffix': 'index.html'},
    }
 )