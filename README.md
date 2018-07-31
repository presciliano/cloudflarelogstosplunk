# CloudflareLogsToSplunk
AWS Lambda function to get Cloudflare Enterprise Log Share logs and send them to Splunk HTTP Event Collector 

## Pre-requisites
1. Get the ID of the Cloudflare zone (available in the Cloudflare Control Panel -> Overview, Domain Summary)
2. Create a Cloudflare user with log access (the feature Enterprise Log Share is available in Enterprise accounts)
3. Configure the Splunk HEC
4. Determine the desired interval between the logs collection (default -> 30 minutes)

## Setup
1. Create a new AWS Lambda Function: Author from scratch, Runtime Python 3.6
2. Edit code inline and copy the contents of the file (lambda_function.py) from this repository
3. Add the following Environment variables and their values
  - CLOUDFLARE_ZONE_ID
  - CLOUDFLARE_EMAIL
  - CLOUDFLARE_AUTH_KEY 
  - SPLUNK_TOKEN
  - SPLUNK_HOST
  - TIME_OFFSET
  - TIME_INTERVAL
4. Add a Cloudwatch Events trigger with a schedule expression accordingly to your desired collection frequency, e.g. `rate(30 minutes`
5. Enable the trigger
