- [EC2 Minecraft](#ec2-minecraft)
  - [First Steps: Creating an S3 Bucket](#first-steps-creating-an-s3-bucket)
  - [Creating a Key Pair](#creating-a-key-pair)
  - [Creating the VPC and EC2](#creating-the-vpc-and-ec2)
  - [Common Questions](#common-questions)
    - [How to Connect to the Minecraft Server](#how-to-connect-to-the-minecraft-server)
    - [How Much Will This Cost Me?](#how-much-will-this-cost-me)
    - [What is the Server Capacity?](#what-is-the-server-capacity)
    - [I Want to Completely Delete Everything](#i-want-to-completely-delete-everything)
    - [How Secure is this Server?](#how-secure-is-this-server)
  - [TODO!](#todo)


# EC2 Minecraft #

Welcome to the repository for creating an EC2 Minecraft server! This guide assumes you are completely new to EC2 and AWS in general. Lets get started!

## First Steps: Creating an S3 Bucket ##

Create an AWS account and login. Once logged in, change your region (top right-hand corner) to be as close as possible to where you live. This will reduce latency for your connection to the server.

Go to the CloudFormation Service - this is where we will be creating the infrastructre we need. 

Create Stack -> Select Upload Template -> Choose file "create-minecraft-s3-bucket.json"

Fill in a stack name of "Creation-of-S3-[BUCKET NAME]"

The only parameter is BucketName. Fill this in with an **all lowercase** name. Next -> Next -> Submit.

Once that is done creating, make your way over to the S3 service and check out your new bucket. In your new bucket upload the folders "cloudformation" and "lambda". In the end you will have something like this 

<img src="./images/s3-uploaded-folders.PNG"  width="600" height="300">

Before heading to the next step, copy the URL object for `top.json` and save it for a later step, should be something like this `https://devkev103-minecraft-ohio.s3.us-east-2.amazonaws.com/cloudformation/top.json`

## Creating a Key Pair ##

Go into the EC2 Service and look for `Key Pair`. Create a new key pair with options `RSA` and `.ppk` with whatever name you want. **Do not** lose or share this!! This is how you will access your server with SSH.

## Creating the VPC and EC2 ##

Head back over to CloudFormation, and paste the copied URL into the parameter field "Amazon S3 URL". Next -> Next -> Check the two "I acknowledge that AWS CloudFormation ..." -> Submit.

It will take approximately 5 minutes and then you will then have your minecraft server ready to go!

## Common Questions ##

### How to Connect to the Minecraft Server ##

You will need the public IP address for the EC2 instance you created. In the Minecraft launcher, you will use the servers's public IP address as "Server Address". You can find the server's public IP address in the EC2 console under `Public IPv4 address`

### How Much Will This Cost Me? ###

The instance running will cost you [approximately $0.09 per hour](https://aws.amazon.com/ec2/pricing/on-demand/). **When you are done playing on the server, shut it down to save money.**

### What is the Server Capacity? ###

From my experience, two people at one time played fine on the server. I have never tried more than two.

### I Want to Completely Delete Everything ###

Head over to the CloudFormation Service in the region you created your stack. And delete the root of the stack, this will delete **most** resouces provisioned by this CloudFormation stack.

By default, this stack keeps the EBS volumes so you can't accidently delete your world. In the VPC service, Route Table section, it will also fail to delete this as well because it is the main route table for the minecraft VPC. You can get around this by deleting it by hand and delete the CloudFormation Stack again.

### How Secure is this Server? ###

If you fill out `<YOUR PUBLIC IP>/32` in the CloudFormation template, only you can get to this server either for SSH'ing or connecting with the Minecraft launcher.

## TODO! ##

* add way to deploy with cli/powershell
* add a mechanism to shutoff/turn on instance
* configure better security practices for IAM - Least Privilege Strategy
* setup EC2 connect