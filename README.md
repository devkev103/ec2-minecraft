# EC2 Minecraft #

Welcome to the repository for creating an EC2 Minecraft server! This guide assumes you are completely new to EC2 and AWS in general. Lets get started!

## First Steps: Creating an S3 Bucket ##

Create an AWS account and login. Once logged in, change your region (top right-hand corner) to be as close as possible to where you live. This will reduce latency for your connection to the server.

Go to the CloudFormation Service - this is where we will be creating the infrastructre we need. 

Create Stack -> Select Upload Template -> Choose file "s3-bucket-creation.json"

Fill in a stack name of "Creation-of-S3-[BUCKET NAME]"

The only parameter is BucketName. Fill this in with an **all lowercase** name. Next -> Next -> Submit.

Once that is done creating, make your way over to the S3 service and check out your new bucket. In your new bucket upload the folders "cloudformation" and "lambda". In the end you will have something like this 

<img src="./images/s3-uploaded-folders.PNG"  width="600" height="300">

Before heading to the next step, copy the URL object for `top.json` and save it for a later step, should be something like this `https://devkev103-minecraft-ohio.s3.us-east-2.amazonaws.com/cloudformation/top.json`

## Creating a Key Pair ##

Go into the EC2 Service and look for `Key Pair`. Create a new key pair with options `RSA` and `.ppk` with whatever name you want. **Do not** lose or share this!! This is how you will access your server with SSH.

## Creating the VPC and EC2 ##

Head back over to CloudFormation, and paste the copied URL into the parameter field "Amazon S3 URL"

## How Much Will This Cost me? ##

https://instances.vantage.sh/

## Side Note ##

I know a lot of we could use the CLI instead, but I chose not to do this for simplicity sake.



AUTH Server: https://authserver.mojang.com/