from shuttlelib.middleware.emailnotification import send_mail
import pandas as pd
import os


async def sendemailnotification(subject,htmlcontent):
    '''Send an email notification with the given subject and HTML content.
    Args:
        subject (str): The subject of the email.
        htmlcontent (str): The HTML content of the email.
    '''
    from_user = 'SRECoEDevSecOps@gruposantander.com'
    env_recipients=os.getenv("SRE_RECIPIENT_LIST")
    env_cc_recipients = os.getenv("SRE_CC_RECIPIENT_LIST")
    msg_to_user = env_recipients.split(",")
    msg_cc_user = env_cc_recipients.split(",")
    msg_subject = f'SHUTTLE-WARNINGS: {subject}'

    content = f"""
        {htmlcontent}

    """
    logger.info(f'Sending email with subject: {msg_subject} to {msg_to_user} with CC to {msg_cc_user}')
    await send_mail(msg_from=from_user,msg_to_user=msg_to_user,msg_cc_user=msg_cc_user,msg_subject=msg_subject,msg_content=content)