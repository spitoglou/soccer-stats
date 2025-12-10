# import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

message = Mail(
    from_email="s.pitoglou@csl.gr",
    to_emails="spitoglou@gmail.com",
    subject="Sending with Twilio SendGrid is Fun Γειά!..",
    html_content="<strong>and easy to do anywhere, even with Python</strong>",
)
try:
    sg = SendGridAPIClient("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")
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.args)
