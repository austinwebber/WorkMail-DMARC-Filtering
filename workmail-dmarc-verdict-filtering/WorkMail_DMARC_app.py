import boto3
import email

def lambda_handler(event, context):

    workmail = boto3.client('workmailmessageflow', region_name='<REGION>')
    msg_id = event['messageId']
    raw_msg = workmail.get_raw_message_content(messageId=msg_id)

    parsed_msg = email.message_from_bytes(raw_msg['messageContent'].read())

    # Bounce email if DMARC verification fails
    if "dmarc=fail" in parsed_msg["Authentication-Results"]:
        print("DMARC failed, bouncing message")
        return {
          'actions' : [{
            'action' : {
              'type' : 'BOUNCE', # bounce email
              'parameters' : {
                'bounceMessage' : 'DMARC verification fail'
              }
            },
            'allRecipients': True
          }]
        }
    # Allow email if DMARC verification passes
    else:
        print("DMARC success, allowing message")
        return {
          'actions' : [{
            'action' : {
              'type' : 'DEFAULT', # allow email to be sent normally
            },
            'allRecipients': True
          }]
        }
