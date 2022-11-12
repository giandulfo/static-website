<h1>Automatic static website deployment using S3 and CodePipeline with a custom domain.</h1>

The contents below states the steps taken to deploy a static website that automatically changes when the source code is updated from a chosen git repository. 

<h3>Create S3 bucket and configure it to host a static website. </h3>
Important steps.
<ul>
  <li>Ensure that the bucket is public.</li>
  <li>Write a bucket policy that grants s3:GetObject permission.</li>
  <li>Enter the file names for the home page and the error page.</li>
</ul>

<h3>Using AWS-CLI</h3>
Run
<ul>
  <li>Aws s3 sync *local directory* *remote bucket* --acl public read.</li>
  <li>Use –dryrun flag to test what’s going to happen before the files are uploaded.</li>
  <li>Once command has been ran, verify the files has been uploaded on the console.</li>
</ul>

Open the static website endpoint to test that the website is working<br>
  
<h3>Create a pipeline to using CodePipeline</h3>
<ul>
  <li>Mostly default settings and create a new service role.</li>
  <li>You can choose whether to create new bucket to store pipeline artifacts or an existing bucket in the same region.</li>
  <li>Select repos that AWS can access.</li>
  <li>Source stage to connect to Github(Version 2).</li>

  <li>There will be a one-time setup verification for the connection.</li>
  <li>Select repos that AWS can access.</li>
  <li>You should then be able to select repo and branch name within the Pipeline settings.</li>
  <li>Skip the build stage because I don’t need to build the files.</li>

  <li>Deploy Stage – Set S3 as the provider and select the bucket created for the static website.</li>
  <li>Tick “Extract file before deploy”.</li>
  <li>Review then create pipeline.</li>
  <li>Fourth item</li>
</ul>
  
Test the pipeline by changing the files locally then pushing to Github.
The pipeline should get triggered and will show the same commit message entered on Github.

---------------------------------------------------------------------------  
Register a domain – the domain in this project is acquired from Route53. <br>
Once the domain has been verified, a hosted zone will be created. 


The next steps will then show how to add a custom domain to the static website.<br>
Access AWS ACM<br>
<ul>
  <li>Request a public certificate.</li>
  <li>Add both www and non-www in the fully qualified domain names.</li>
  <li>Choose DNS validation (recommended)</li>
  <li>Click request</li>
  <li>The status will then show ‘pending validation’</li>
  <li>Click into the certificate and click create records in Route53.</li>
  <li>Check the hosted zone and the records should be added</li>
</ul>

Access CloudFront<br>
<ul>
  <li>Origin = s3 website path/endpoint.</li>
  <li>Alternate domain name (CNAME) – enter www and non-www.</li>
  <li>Custom SSL certificate – Add the certificate created from ACM.</li>
  <li>In default cache behaviour -> Viewer > Redirect HTTP to HTTPs.</li>
  <li>Create distribution</li>
</ul>

Back to Route53<br>
<ul>
  <li>Create A record for www</li>
  <li>Route traffic to Alias</li>
  <li>Alias to Cloudfront Distribution</li>
  <li>Create record</li>
  <li>Repeat the same steps for non-www </li>
</ul>

After a few minutes - Enter your domain in the browser, you should see your website showing as secure connection.

Remember that CloudFront is serving cached content. It will need to be invalidated to pull again from S3.
-------------------------------------------------------------------------------------

<h2>Github action to invalidate a CloudFront distribution whenever source code changes.</h2>

Ensure that you have your secrets saved in the repository. <br>
REPONAME > Settings > Secrets 
You will need to set Secrets for the items below.  


```
DISTRIBUTION = EAFDQBR8EXAMPLE
AWS_ACCESS_KEY_ID
AWS_SECRETACCESS_KEY
```
This section of the yaml file indicates where the workflow will not run.
```
paths-ignore:
    - './README.md'
```   
Invalidate CloudFront

```
name: Invalidate Cloudfront on push
on:
  push:
    branches: [ "main" ]
    paths-ignore:
      - 'README.md'
  pull_request:
    branches: [ "main" ]
    paths-ignore:
      - 'README.md'

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: checkout
        uses: actions/checkout@master

      # Invalidate CloudFront (this action)
      - name: Invalidate CloudFront
        uses: chetan/invalidate-cloudfront-action@v2
        env:
          DISTRIBUTION: ${{ secrets.DISTRIBUTION }}
          PATHS: "/*"
          AWS_REGION: "eu-west-2"
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

-------------------------------------------------------------------------------------
<h2>Possible upgrades</h2>
<ul>
<li>Automate invalidation once a change is made - Completed - 29.10.22</li>
<p> Updated invalidation workflow to ignore README.md commits</p>
<li>Add a database to record hit counters</li>
<li>Serverless Contact form using Lambda and API Gateway</li>
</ul>

