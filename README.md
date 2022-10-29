<h1>Automatic static website deployment using S3 and CodePipeline with a custom domain.</h1>

<h2> The contents below states the steps taken to deploy a static website that automatically changes when the source code is updated from a chosen git repository. </h2>

<h3>Create S3 bucket and configure it to host a static website. </h3>
Important steps
-	Ensure that the bucket is public
-	Write a bucket policy that grants s3:GetObject permission
-	Enter the file names for the home page and the error page.

<h3>Using AWS-CLI</h3>
Run
-	Aws s3 sync <local directory> <remote bucket> --acl public read
-	Use –dryrun flag to test what’s going to happen before the files are uploaded
-	Once command has been ran, verify the files has been uploaded on the console

Open the static website endpoint to test that the website is working
  
<h3>Create a pipeline to using CodePipeline</h3>
-	Mostly default settings and create a new service role.
-	You can chose whether to create new bucket to store pipeline artifacts or an existing bucket in the same region
-	Source stage to connect to Github(Version 2)
-	There will be a one-time setup verification for the connection.
-	Select repos that AWS can access
-	You should then be able to select repo and branch name within the Pipeline settings
-	Skip the build stage because I don’t need to build the files
-	Deploy Stage – Set S3 as the provider and select the bucket created for the static website
-	Tick “Extract file before deploy”
-	Review then create pipeline
  
Test the pipeline by changing the files locally then pushing to Github. 
The pipeline should get triggered and will show the same commit message entered on Github.

---------------------------------------------------------------------------  
Register a domain – the domain in this project is acquired from Route53. 
Once the domain has been verified, a hosted zone will be created. 


The next steps will then show how to add a custom domain to the static website
Access AWS ACM
-	Request a public certificate
-	Add both www and non-www in the fully qualified domain names
-	Choose DNS validation (recommended)
-	Click request
-	The status will then show ‘pending validation’
-	Click into the certificate and click create records in Route53. 
-	Check the hosted zone and the records should be added

Access CloudFront
-	Origin = s3 website path/endpoint
-	Alternate domain name (CNAME) – enter www and non-www
-	Custom SSL certificate – Add the certificate created from ACM
-	In default cache behaviour -> Viewer > Redirect HTTP to HTTPs.
-	Create distribution

Back to Route53
-	Create A record for www
-	Route traffic to Alias
-	Alias to Cloudfront Distribution
-	Create record
-	Repeat the same steps for non-www 

After a few minutes - Enter your domain in the browser, you should see your website showing as secure connection.

Remember that CloudFront is serving cache content. It will need to be invalidated to pull again from S3.

