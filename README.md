# CloudflareLogsToSplunk
AWS Lambda function to get Cloudflare Enterprise Log Share logs and send them to Splunk HTTP Event Collector 

## Prerequisites
1. Get the ID of the Cloudflare zone (available in the Cloudflare Control Panel -> Overview, Domain Summary)
2. Create a Cloudflare user with log access (the feature Enterprise Log Share is available in Enterprise accounts)
3. Configure the Splunk HEC and set the sourcetype to `cflogshare`
4. Determine the desired interval between the logs collection (default -> 30 minutes)
5. Decide the list of fields you want in Splunk. Cloudflare will provide a list of default fields, but you can specify the entire list (please refer to the [documentation](https://support.cloudflare.com/hc/en-us/articles/216672448-Enterprise-Log-Share-Logpull-REST-API)), e.g. 
```
CacheCacheStatus,CacheResponseBytes,CacheResponseStatus,CacheTieredFill,ClientASN,ClientCountry,ClientDeviceType,ClientIP,ClientIPClass,ClientRequestBytes,ClientRequestHost,ClientRequestMethod,ClientRequestProtocol,ClientRequestReferer,ClientRequestURI,ClientRequestUserAgent,ClientSSLCipher,ClientSSLProtocol,ClientSrcPort,EdgeColoID,EdgeEndTimestamp,EdgePathingOp,EdgePathingSrc,EdgePathingStatus,EdgeRateLimitAction,EdgeRateLimitID,EdgeRequestHost,EdgeResponseBytes,EdgeResponseCompressionRatio,EdgeResponseContentType,EdgeResponseStatus,EdgeServerIP,EdgeStartTimestamp,OriginIP,OriginResponseBytes,OriginResponseHTTPExpires,OriginResponseHTTPLastModified,OriginResponseStatus,OriginResponseTime,OriginSSLProtocol,ParentRayID,RayID,SecurityLevel,WAFAction,WAFFlags,WAFMatchedVar,WAFProfile,WAFRuleID,WAFRuleMessage,WorkerCPUTime,WorkerStatus,WorkerSubrequest,WorkerSubrequestCount,ZoneID
``` 

## Setup
1. Create a new AWS Lambda Function: Author from scratch, Runtime Python 3.6, create a new role or use the `lambda_basic_execution`
2. Edit code inline and copy the contents of the file [lambda_function.py](lambda_function.py) from this repository
3. Add the following Environment variables and their [values](#prerequisites)
  - CLOUDFLARE_ZONE_ID
  - CLOUDFLARE_EMAIL
  - CLOUDFLARE_AUTH_KEY 
  - CLOUDFLARE_FIELDS: defaults to nothing, so only the default Cloudflare fields will be considered
  - SPLUNK_TOKEN
  - SPLUNK_HOST
  - TIME_OFFSET: defaults to 10
  - TIME_INTERVAL: defaults to 30
4. Add a Cloudwatch Events trigger with a schedule expression accordingly to your desired collection frequency, e.g. `rate(30 minutes`
5. Enable the trigger

## Logs
A sucessfull Lambda run will look like the following in the Cloudwatch Logs:
```
START RequestId: 81a9ee27-9979-11e8-8a12-d74937aaaaaa Version: $LATEST
Searching for logs between 2018-08-06T12:26:18.119359Z and 2018-08-06T12:56:18.119359Z
Sending request to Cloudflare API at https://api.cloudflare.com/client/v4/zones/aaaabbbbccccddddeeeeffffgggghhhh/logs/received?start=2018-08-06T12:26:18.119359Z&end=2018-08-06T12:56:18.119359Z&fields=
Sending 42 events
Sending request to Splunk HEC at https://hec-splunk-host.splunkcloud.com/services/collector
Splunk HEC Response: {"text":"Success","code":0}
END RequestId: 81a9ee27-9979-11e8-8a12-d74937aaaaaa
```

## Authors
- Presciliano Neto

## To do
- Treat request errors (e.g. API trothling limits) and wrong values in the required environment variables

## License
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details
