from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from loguru import logger


def send_mail(
    from_email='s.pitoglou@csl.gr',
    to_emails='spitoglou@gmail.com',
    subject='Test Subject',
    html_content='<strong>Content</strong>'
):
    message = Mail(
        from_email=from_email,
        to_emails=to_emails,
        subject=subject,
        html_content=html_content)
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        logger.info(response.status_code)
        logger.info(response.body)
        logger.info(response.headers)
    except Exception as e:
        logger.error(e.args)


if __name__ == '__main__':
    send_mail()
