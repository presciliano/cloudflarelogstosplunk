import os
from botocore.vendored import requests
import json
import datetime

CLOUDFLARE_ZONE_ID = os.getenv('CLOUDFLARE_ZONE_ID')
CLOUDFLARE_EMAIL = os.getenv('CLOUDFLARE_EMAIL')
CLOUDFLARE_AUTH_KEY = os.getenv('CLOUDFLARE_AUTH_KEY')
SPLUNK_TOKEN = os.getenv('SPLUNK_TOKEN')
SPLUNK_HOST = os.getenv('SPLUNK_HOST')
TIME_OFFSET = os.getenv('TIME_OFFSET', 10)
TIME_INTERVAL = os.getenv('TIME_INTERVAL', 30)

def lambda_handler(event, context):
    
    # Definition of start and end times
    now = datetime.datetime.utcnow()
    timeoffset = int(TIME_OFFSET) * (-1)
    timeinterval = (int(TIME_INTERVAL) + int(TIME_OFFSET)) * (-1)
    start_date = now + datetime.timedelta(minutes=timeinterval)
    start_date = start_date.isoformat("T") + "Z"
    end_date = now + datetime.timedelta(minutes=timeoffset)
    end_date = end_date.isoformat("T") + "Z"
    
    print('Searching for logs between {} and {}'.format(start_date,end_date))

    #Format Cloudflare Enterprise Log Share Request
    cloudflare_headers = {'X-Auth-Email': CLOUDFLARE_EMAIL,
                          'X-Auth-Key': CLOUDFLARE_AUTH_KEY,
                          'Content-Type': 'application/json'}
    
    cloudflare_url = 'https://api.cloudflare.com/client/v4/zones/' + CLOUDFLARE_ZONE_ID + '/logs/received?start=' + str(start_date) + '&end=' + str(end_date)
    cloudflare_request = requests.get(cloudflare_url, headers=cloudflare_headers)
    
    cloudflare_response = cloudflare_request.text.splitlines()
    
    if len(cloudflare_response)>0:
        
        print('Sending {} events'.format(len(cloudflare_response)))
        
        #Format Splunk HEC Request
        splunk_headers = {'Authorization': 'Splunk ' + SPLUNK_TOKEN}
        splunk_url = 'https://' + SPLUNK_HOST + '/services/collector'
        
        splunk_batch = ""
        for line in cloudflare_response:
            splunk_data = '{"sourcetype": "cflogshare", "event":' + str(line) + '}\n'
            splunk_batch += splunk_data
        
        splunk_request = requests.post(splunk_url, headers=splunk_headers, data=splunk_batch)
        print('Splunk HEC Response: {}'.format(splunk_request.text))

    else:
        print('No events found')    
