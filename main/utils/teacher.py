import os

from main.models import Teacher


def get_teacher_from_email(
    registered_email, create_teacher=False, content_upload_path=None, **kwargs
):
    """
    Get Teacher from email

    :param registered_email:
    :param create_teacher: Boolean indicating if a new teacher should be created
    :param content_upload_path: path on which profile pictures are stored
    :param kwargs: kwargs should be as per column name

    :returns: teachers
    """
    teacher = None
    if not content_upload_path:
        content_upload_path = "images"
    if registered_email:
        teacher = Teacher.objects.filter(email=registered_email).first()

    if registered_email and not teacher and create_teacher:
        # Remove any keys which won't map
        defaults = {
            key: value for key, value in kwargs.items() if hasattr(Teacher, key)
        }
        profile_picture = f"{content_upload_path}/{kwargs.get('profile_picture')}"
        if not os.path.isfile(profile_picture):
            profile_picture = f"images/default_image.jpeg"
        defaults["profile_picture"] = profile_picture
        teacher = Teacher(**defaults)
        teacher.save()

    return teacher
