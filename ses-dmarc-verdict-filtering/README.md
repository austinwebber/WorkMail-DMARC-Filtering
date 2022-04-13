# Amazon SES DMARC Verdict Filtering

Integrating the filtering of emails depending on DMARC verdict in SES (and subsequently applies to all emails sent to all WorkMail organizations).

## Requirements:

1. Create a WorkMail organization using a domain of choice:

  https://docs.aws.amazon.com/workmail/latest/adminguide/add_new_organization.html
  https://docs.aws.amazon.com/workmail/latest/adminguide/add_domain.html

2. Create a test user in your WorkMail organization
3. Enable CloudWatch Logs on your WorkMail organization (for troubleshooting purposes)
4. A blank Lambda function using Python 3.9 or newer runtime
