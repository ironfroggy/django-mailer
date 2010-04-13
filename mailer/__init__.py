VERSION = (0, 2, 0, "dev", 1)

def get_version():
    if VERSION[3] == "final":
        return "%s.%s.%s" % (VERSION[0], VERSION[1], VERSION[2])
    elif VERSION[3] == "dev":
        return "%s.%s.%s%s%s" % (VERSION[0], VERSION[1], VERSION[2], VERSION[3], VERSION[4])
    else:
        return "%s.%s.%s%s" % (VERSION[0], VERSION[1], VERSION[2], VERSION[3])

__version__ = get_version()


PRIORITY_MAPPING = {
    "high": "1",
    "medium": "2",
    "low": "3",
    "deferred": "4",
}


# replacement for django.core.mail.send_mail


def send_mail(subject, message, from_email, recipient_list, priority="medium",
              fail_silently=False, auth_user=None, auth_password=None, headers=None):
    from django.utils.encoding import force_unicode
    from mailer.models import Message
    
    priority = PRIORITY_MAPPING[priority]
    
    # need to do this in case subject used lazy version of ugettext
    subject = force_unicode(subject)
    message = force_unicode(message)
    
    if len(subject) > 100:
        subject = u"%s..." % subject[:97]
    
    for to_address in recipient_list:
        message_obj = Message(
            to_address=to_address,
            from_address=from_email,
            subject=subject,
            message_body=message,
            priority=priority)
        if headers:
            for name, value in headers.items():
                message_obj.headers[name] = value
        message_obj.save()


def send_html_mail(subject, message, message_html, from_email, recipient_list,
                   priority="medium", fail_silently=False, auth_user=None,
                   auth_password=None, headers=None):
    """
    Function to queue HTML e-mails
    """
    from django.utils.encoding import force_unicode
    from mailer.models import Message
    
    priority = PRIORITY_MAPPING[priority]
    
    # need to do this in case subject used lazy version of ugettext
    subject = force_unicode(subject)
    
    for to_address in recipient_list:
        message_obj = Message(to_address=to_address,
                from_address=from_email,
                subject=subject,
                message_body=message,
                message_body_html=message_html,
                priority=priority)
        if headers:
            for name, value in headers.items():
                message_obj.headers[name] = value
        message_obj.save()


def mail_admins(subject, message, fail_silently=False, priority="medium", headers=None):
    from django.utils.encoding import force_unicode
    from django.conf import settings
    from mailer.models import Message
    
    priority = PRIORITY_MAPPING[priority]
    
    subject = settings.EMAIL_SUBJECT_PREFIX + force_unicode(subject)
    message = force_unicode(message)
    
    if len(subject) > 100:
        subject = u"%s..." % subject[:97]
    
    for name, to_address in settings.ADMINS:
        message_obj = Message(to_address=to_address,
                from_address=settings.SERVER_EMAIL,
                subject=subject,
                message_body=message,
                priority=priority)
        if headers:
            for name, value in headers.items():
                message_obj.headers[name] = value
        message_obj.save()


def mail_managers(subject, message, fail_silently=False, priority="medium", headers=None):
    from django.utils.encoding import force_unicode
    from django.conf import settings
    from mailer.models import Message
    
    priority = PRIORITY_MAPPING[priority]
    
    subject = settings.EMAIL_SUBJECT_PREFIX + force_unicode(subject)
    message = force_unicode(message)
    
    if len(subject) > 100:
        subject = u"%s..." % subject[:97]
    
    for name, to_address in settings.MANAGERS:
        message_obj = Message(to_address=to_address,
                from_address=settings.SERVER_EMAIL,
                subject=subject,
                message_body=message,
                priority=priority)
        if headers:
            for name, value in headers.items():
                message_obj.headers[name] = value
        message_obj.save()
