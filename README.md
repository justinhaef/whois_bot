# This is a repo in case anyone needs to create a quick public Webex Teams bot

## What you'll need

This bot will use AWS Lambda by way of the AWS Python Chalice library.  Chalice makes it very easy for you to deploy the Lambda function as well as the API Gateway. 

Good Resources for reference:
- https://realpython.com/aws-chalice-serverless-python/
- https://webexteamssdk.readthedocs.io/en/latest/user/quickstart.html
- https://github.com/aws/chalice

## Clone this repo

~~Be sure you use Python 3.6, can't use 3.7 as per AWS~~ Update - You can use 3.7 which is installed by default by HomeBrew, you just get warnings from the Chalice commands. 
You might need this command first `xcode-select --install` for mac users.
I also recommend you download [Microsoft VS Code](https://code.visualstudio.com)
Use [this guide](https://docs.python-guide.org/starting/install3/osx/) to install Homebrew and Pip. 
Next use [this guide](https://docs.python-guide.org/dev/virtualenvs/#lower-level-virtualenv) to install a virtual environment. (Optional)

Create an AWS Chalice project

Create a folder, name it whatever you'd like.  
1. `mkdir TeamsBot`
2. `cd TeamsBot`
3. `pip3 install chalice`
4. `chalice new-project TeamsBot`
5. `cd TeamsBot`
6. `git clone https://github.com/justinhaef/whois_bot.git`

Next, once you've cloned this repo and you've set it up in a virtual environment, run `pip install -r requirements.txt`.  

## You've got a little work to do

You need to create an AWS account, yes you'll need your credit card but don't worry, odds are you won't be charged a thing as the AWS free tier is amazing. 

You need to setup a file in your *home directory*, `.aws/config` and `.aws/credentials`.  


./aws/config

```key
[default]
output = json
region = us-east-1
```

.aws/credentials

```key
[default]
aws_access_key_id = ---AWS KEY---
aws_secret_access_key = ---AWS SECRET---
```

Also under your project's folder, *not your home directory* `.chalice/config.json` you'll need to add the following for the Webex Teams. 

config.json

```json
{
  "version": "2.0",
  "app_name": "TeamsBot",
  "stages": {
    "dev": {
      "api_gateway_stage": "api",
      "environment_variables": {
        "WEBEX_TEAMS_ACCESS_TOKEN": "---Webex Token---"
      }
    }
  }
}
```

## Change the logic if you'd like

The `app.py` has all the high level stuff and the `webexteams.py` file has the lower level, business logic stuff.  The `chalicelib/whois.json` file is where you can manually add in the info that you'd like the bot to give you back.  

## Publish

When you're happy with your lists, run `chalice deploy` and it will push to AWS.  Take note of the URL it gives you back. Should look something like this:

```shell
Creating deployment package.
Updating policy for IAM role: whois_bot-dev
Updating lambda function: whois_bot-dev
Updating rest API
Resources deployed:
  - Lambda ARN: arn:aws:lambda:us-east-1:1070648475659:function:whois_bot-dev
  - Rest API URL: https://b476bhfkduryi.execute-api.us-east-1.amazonaws.com/api/
```

## You are not done yet

Now you need to go to Webex Teams and create your bot's webhook. 

Just follow [this link](https://developer.webex.com/docs/api/v1/webhooks/create-a-webhook) and enter in the bot access token you got when you created it.  Enter the URL from above in the `targetUrl` field.  Then for the the simplest config, for both event and resource enter `all`.  __Be sure to change the `Authorization` toggle switch to off, so it doesn't use your personal token.__

Also [__UPDATE LINE #10 in app.py__](https://github.com/justinhaef/whois_bot/blob/075d3e5a5fef564dca6bbd80cdbcc9b83bf19060/app.py#L10), if you fail to do this you'll create a messaging loop!

## Finish

Once that is all done, you should have a working Webex Teams Bot hosted in AWS.  Every time you want to update your bot, make the changes in VS Code, save and upload using the `chalice deploy` command.  