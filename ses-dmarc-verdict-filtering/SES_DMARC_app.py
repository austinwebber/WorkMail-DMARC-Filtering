import json

def lambda_handler(event, context):

    dmarc_verdict = (event['Records'][0]['ses']['receipt']['dmarcVerdict']['status'])

    # Allow email to continue as DMARC verdict is not FAIL
    if dmarc_verdict != "FAIL":
        print(dmarc_verdict)
        print("continue")
        return {
            "disposition" : "CONTINUE" # CONTINUE (goes to next rule and sends email to S3)
        }
    # Stop SES rule set as DMARC verdict is FAIL
    else:
        print(dmarc_verdict)
        print("stop rule set")
        return {
            "disposition" : "STOP_RULE_SET" # STOP_RULE_SET (stops processing the rule set and drops the email)
        }
