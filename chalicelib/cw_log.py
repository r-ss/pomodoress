from chalicelib.config import config
import boto3
import time

client = boto3.client('logs', region_name=config.AWS_REGION)

retention_period_in_days = 5

class CWLog:

    def set_groups():

        log_group = config.AWS_LOG_GROUP_NAME
        response = client.create_log_group(
            logGroupName=log_group,
            tags={
                'Type': 'backend',
                'RetentionPeriod': str(retention_period_in_days)
            }
        )

        # print(json.dumps(response, indent=4))

        response = client.put_retention_policy(
                logGroupName=log_group,
                retentionInDays=retention_period_in_days
        )

        # print(json.dumps(response, indent=4))

    def list_log_groups():

        response = client.describe_log_groups()

        # print(json.dumps(response, indent=4))

        for each_line in response['logGroups']:
            print(each_line)

    def create_log_stream():
        client.create_log_stream(
            logGroupName = config.AWS_LOG_GROUP_NAME,
            logStreamName = config.AWS_LOG_GENEGAL_STREAM_NAME
        )

    def send_cw_log(msg: str):

        if not config.AWS_LOGGING_ENABLED:
            return

        response = client.describe_log_streams(
            logGroupName = config.AWS_LOG_GROUP_NAME,
            logStreamNamePrefix = config.AWS_LOG_GENEGAL_STREAM_NAME
        )

        log_event = {
            'logGroupName': config.AWS_LOG_GROUP_NAME,
            'logStreamName': config.AWS_LOG_GENEGAL_STREAM_NAME,
            'logEvents': [
                {
                    'timestamp': int(round(time.time() * 1000)),
                    'message': msg
                },
            ],
        }

        if 'uploadSequenceToken' in response['logStreams'][0]:
            log_event.update({'sequenceToken': response['logStreams'][0] ['uploadSequenceToken']})

        response = client.put_log_events(**log_event)
