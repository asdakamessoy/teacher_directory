from main.models import Subject


def get_subject_by_name(registered_name, create_subject=False, **kwargs):
    """
    Get Subject from name

    :param registered_name:
    :param create_subject: Boolean indicating if a new subject should be created
    :param kwargs: kwargs should be as per column name

    :returns: subject
    """
    subject = None
    if registered_name:
        subject = Subject.objects.filter(name__iexact=registered_name).first()

    if registered_name and not subject and create_subject:
        # Remove any keys which won't map
        defaults = {
            key: value for key, value in kwargs.items() if hasattr(Subject, key)
        }
        subject = Subject(**defaults)
        subject.save()
    return subject
