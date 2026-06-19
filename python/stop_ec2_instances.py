import boto3
import os
 
ec2 = boto3.client('ec2')
 
TAG_KEY = os.environ.get('TAG_KEY', 'AutoSchedule')
TAG_VALUE = os.environ.get('TAG_VALUE', 'True')
 
def lambda_handler(event, context):
    print("--- Stopping EC2 instances process initiated ---")
    print(f"Looking for instances with tag '{TAG_KEY}':'{TAG_VALUE}'")
 
    filters = [
        {'Name': 'instance-state-name', 'Values': ['running']},
        {'Name': f'tag:{TAG_KEY}', 'Values': [TAG_VALUE]}
    ]
 
    instances_to_stop = []
    try:
        response = ec2.describe_instances(Filters=filters)
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                # In production, you might add extra checks here — e.g. exclude
                # instances in an Auto Scaling Group, or honor a "DoNotStop" tag.
                instances_to_stop.append(instance['InstanceId'])
 
        if instances_to_stop:
            print(f"Found {len(instances_to_stop)} instances to stop: {instances_to_stop}")
            ec2.stop_instances(InstanceIds=instances_to_stop)
            print("Successfully sent stop command to EC2 instances.")
        else:
            print("No running instances found with the specified tag.")
 
    except Exception as e:
        print(f"Error stopping EC2 instances: {e}")
        return {'statusCode': 500, 'body': f"Error stopping EC2 instances: {str(e)}"}
 
    print("--- EC2 instances stop process completed ---")
    return {'statusCode': 200, 'body': 'EC2 instance stop process completed.'}
