# WorkMail/SES DMARC Filtering w/ AWS Lambda
Amazon WorkMail and SES DMARC Verdict Filtering using AWS Lambda with Python

Amazon WorkMail enforces inbound DMARC verification by default, however, if said domain owner has their DMARC policy set to none (i.e. gmail.com does this), then spoofing emails can pass into WorkMail user's inboxes without issues. You can use nslookup (on Windows computers) to verify the DMARC policy of such domains:

```
nslookup _dmarc.gmail.com
```

Output: "v=DMARC1; p=none; sp=quarantine; rua=mailto:mailauth-reports@google.com"

```
nslookup _dmarc.yahoo.com
```

Output: "v=DMARC1; p=reject; pct=100; rua=mailto:d@rua.agari.com; ruf=mailto:d@ruf.agari.com;"


As you see, spoofed emails sent from gmail.com will tell the receiving domain to take no action (p=none). On the other hand, spoofed emails sent from yahoo.com will tell the receiving domain to reject (p=reject) said spoofed emails that fail DMARC.

To address this, you can execute an AWS Lambda function to take action on incoming email depending on whether the DMARC verdict is fail or success. This theoretically decreases the amount of spoofing emails that your WorkMail users receive.

As WorkMail uses Amazon Simple Email Service (SES) for handling email, so there are 2 solutions to this I've created:

1. A Lambda function integrated in an SES receipt rule to execute at position 1, which would stop the SES INBOUND_MAIL rule set on the email if the DMARC verdict is fail (this would apply filtering to all WorkMail organizations by default)
2. A Lambda function integrated in WorkMail as an inbound rule to execute on all incoming email specific to the WorkMail organization (this would apply filtering to individual WorkMail organizations)

Solution 1 - [SES Receipt Rule w/ AWS Lambda](https://github.com/austinwebber/WorkMail-DMARC-Filtering/tree/main/ses-dmarc-verdict-filtering)

Solution 2 - [WorkMail Inbound Rule w/ AWS Lambda](https://github.com/austinwebber/WorkMail-DMARC-Filtering/tree/main/workmail-dmarc-verdict-filtering)
