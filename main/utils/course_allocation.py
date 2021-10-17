from main.models import CourseAllocation


def add_new_course(teacher, subject):
    """
    Allocate new course to a teacher

    :param teacher:
    :param subject:
    :return:
    """
    result = False
    course_entry = None
    if subject.is_active and teacher.can_add_new_subject():
        course_entry, result = CourseAllocation.objects.get_or_create(
            subject=subject, teacher=teacher
        )
    return course_entry, result
