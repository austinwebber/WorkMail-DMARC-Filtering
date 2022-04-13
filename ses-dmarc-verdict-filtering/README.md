# Amazon SES DMARC Verdict Filtering

Integrating the filtering of emails depending on DMARC verdict in SES (and subsequently applies to all emails sent to all WorkMail organizations).

## Requirements:

1. Create a WorkMail organization using a domain of choice:

    https://docs.aws.amazon.com/workmail/latest/adminguide/add_new_organization.html
    https://docs.aws.amazon.com/workmail/latest/adminguide/add_domain.html

2. Create a test user in your WorkMail organization
3. Enable CloudWatch Logs on your WorkMail organization (for troubleshooting purposes)
4. A blank Lambda function using Python 3.9 or newer runtime

## Implementation:

1. Copy the code from [SES_DMARC_app.py](https://github.com/austinwebber/WorkMail-DMARC-Filtering/blob/main/ses-dmarc-verdict-filtering/SES_DMARC_app.py) in this repo

2. Paste the code into your blank Lambda function, deploy the changes

3. (Optional) Create a test event with the name "DMARCsuccess" and use the following JSON listed [here](https://docs.aws.amazon.com/ses/latest/dg/receiving-email-action-lambda-event.html)

4. (Optional) Create an additional test event with the name "DMARCfail", use the same JSON as the previous test event, but change dmarcVerdict status to "FAIL" in the JSON.

5. (Optional) Test both of your test events, which should return disposition = "CONTINUE" for the first test event and disposition = "STOP_RULE_SET" for the second test event

6. Now that you've confirmed the Lambda function handles a test event as intended:

    -> Open SES console in the same region as the Lambda function
    -> Open the tab on the left side
    -> Select "Email receiving"
    -> Select the hyperlink on the "INBOUND_MAIL" rule set
    
    **WARNING**, please be cautious if changing these existing receipt rules as you could break inbound email if configured incorrectly

7. We will want to add an additional receipt rule to execute at position 1 to execute the Lambda function we just created. These steps are also outlined [here](https://docs.aws.amazon.com/ses/latest/dg/receiving-email-receipt-rules-console-walkthrough.html):

    -> Select "Create rule"
    -> Name the rule
    -> Select "Next"
    -> You can add a new recipient condition if you only want own DMARC filtering Lambda to run against specific recipient domains
    -> Select "Next"
    -> Select "Add new action"
    -> Select "Invoke AWS Lambda function"
    -> Select your Lambda function from earlier
    -> Select "RequestResponse invocation"
    -> Select "Next"
    -> Select "Create rule"
    -> Select "Add permissions" (if prompted)

8. Now, test your configuration by sending an email to your test user that you created earlier, and use CloudWatch Logs to verify the result from your Lambda function and from WorkMail

9. You can also use tools on the internet to test a spoofing email from gmail.com, yahoo.com, etc to confirm it is working as intended

The solution provided in this repo is a simple way to handle this in Python, but note AWS does have a public facing doc with a more complete solution in JavaScript:
https://docs.aws.amazon.com/ses/latest/dg/receiving-email-action-lambda-example-functions.html#receiving-email-action-lambda-example-functions-4

