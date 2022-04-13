# Amazon WorkMail DMARC Verdict Filtering

Integrating the filtering of emails depending on DMARC verdict in a WorkMail organization.

In order for this implementation to work, the Lambda function will need specific IAM permissions to call GetRawMessageContent action in the Amazon WorkMail Message Flow API, and I will outline how to complete this. 

## Requirements:

1. Create a WorkMail organization using a domain of choice:

    * https://docs.aws.amazon.com/workmail/latest/adminguide/add_new_organization.html
    * https://docs.aws.amazon.com/workmail/latest/adminguide/add_domain.html

2. Create a test user in your WorkMail organization
3. Enable CloudWatch Logs on your WorkMail organization (for troubleshooting purposes)
4. A blank Lambda function using Python 3.9 or newer runtime


## Implementation:

1. Copy the code from [WorkMail_DMARC_app.py](https://github.com/austinwebber/WorkMail-SES-DMARC/blob/main/workmail-dmarc-verdict-filtering/WorkMail_DMARC_app.py) in this repo

2. Paste the code into your blank Lambda function. **ENSURE to change the REGION in Line 6 to the region where your WorkMail organization exists (i.e. us-east-1)**

3. Deploy the changes to your Lambda. As compared to Solution 1 with SES, this solution does not have a great way to configure Lambda test events because we need a real messageID to execute the GetRawMessageContent in order to analyze the DMARC verdict of the email
  
4. In order for WorkMail to execute your Lambda function, use the following AWS CLI command to add permissions to your Lambda function (after adjusting the relevant placeholders):
  
  ```
aws --region REGION lambda add-permission --function-name LAMBDA_FUNCTION_NAME --statement-id AllowWorkMail --action "lambda:InvokeFunction" --principal workmail.REGION.amazonaws.com --source-arn arn:aws:workmail:REGION:AWS_ACCOUNT_ID:organization/WORKMAIL_ORGANIZATION_ID
  ```   
  
  * I found the above command in the AWS docs [here](https://docs.aws.amazon.com/workmail/latest/adminguide/lambda.html)
  
5. In order for your Lambda function to call the GetRawMessageContent API, create a new inline policy using the JSON below and attach it to your Lambda's IAM execution rule (ensure to update the policy to replace placeholders):
  
  ```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "workmailmessageflow:GetRawMessageContent"
            ],
            "Resource": "arn:aws:workmailmessageflow:<REGION>:<AWS ACCOUNT ID>:message/*",
            "Effect": "Allow"
        }
    ]
}
  ```
  
6. After configuring the above:

    -> Open WorkMail console
    -> Select your organization
    -> Select "Organization settings"
    -> Select "Inbound rules"
    -> Select "Create"
    -> Name the rule
    -> Set "Action" to "Run Lambda"
    -> Select your Lambda function
    -> Select the "Synchronous" slider
    -> Set "Rule timeout" to 1
    -> Set "Fallback action" to the desired action (i.e. if the Lambda times out or completely fails, what do you want to do with the email? This means we were unable to check if DMARC failed/passed for that individual email)
    -> For "Sender domains or addresses", either enter * or enter specific domains/emails you want your Lambda function to manually verify DMARC with (i.e. gmail.com)
    -> Select "Create"
  
7. Now, test your configuration by sending an email to your test user that you created earlier, and use CloudWatch Logs to verify the result from your Lambda function and from WorkMail

## Conclusion:

  * This solution was purely developed by myself, so there may be use cases or errors that are not handled. Test outside of production.

  * References I used to create this custom code and implementation:

    - https://docs.aws.amazon.com/workmail/latest/adminguide/lambda.html
    - https://docs.aws.amazon.com/workmail/latest/adminguide/lambda-content.html
    - https://docs.aws.amazon.com/workmail/latest/APIReference/API_messageflow_GetRawMessageContent.html
    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmailmessageflow.html
    - https://github.com/aws-samples/amazon-workmail-lambda-templates
