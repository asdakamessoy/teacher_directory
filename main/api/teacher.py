import datetime
import string
import zipfile

from django.contrib import messages
from django.http import HttpResponseNotFound
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render

from main.models import Teacher, CourseAllocation
from main.utils.course_allocation import add_new_course
from main.utils.decorators.authorized import authorized_access
from main.utils.importer import get_data_from_upload, random_string
from main.utils.subject import get_subject_by_name
from main.utils.teacher import get_teacher_from_email

MAX_RESULT_SET = 10


def determine_offset_range(page=1):
    offset = int(page or 1) - 1
    if offset < 0:
        offset = 0

    offset = offset * MAX_RESULT_SET
    limit = offset + MAX_RESULT_SET
    return offset, limit


@authorized_access(user_types=["authorized_user"])
def list_all(request, *args, **kwargs):
    """
    List all teachers

    Endpoint: /api/v1/teacher/all/?page=<page number>&first_name=ABC&last_name=ABC&email=

    :param request:
    :return:
    """
    offset, limit = determine_offset_range(page=request.GET.get("page"))
    query = Teacher.objects.all()
    if request.GET.get("email"):
        query = query.filter(email__contains=request.GET.get("email"))
    if request.GET.get("first_name"):
        query = query.filter(first_name__contains=request.GET.get("first_name"))
    if request.GET.get("last_name"):
        query = query.filter(last_name__contains=request.GET.get("last_name"))
    query = query.all()[offset:limit]
    return JsonResponse(
        {
            "teachers": [
                dict(
                    reference_number=teacher.reference_number,
                    first_name=teacher.first_name,
                    last_name=teacher.last_name,
                    email=teacher.email,
                )
                for teacher in query
            ],
            "teachers_count": query.count(),
        }
    )


@authorized_access(user_types=["authorized_user"])
def read(request, *args, **kwargs):
    """
    View the details of a specific teacher.

    ** better to use reference_number rather

    Endpoint: /api/v1/teacher/?reference_number=ABC

    :param request:
    :return:
    """
    reference_number = request.GET.get("reference_number")
    response = HttpResponseNotFound()
    record = Teacher.objects.filter(reference_number=reference_number).first()
    allocated_subjects = CourseAllocation.objects.filter(
        teacher=record, subject__is_active=True
    )
    if record:
        response = JsonResponse(
            dict(
                first_name=record.first_name,
                last_name=record.last_name,
                email=record.email,
                profile_picture=record.profile_picture.url,
                phone_number=record.phone_number,
                room_number=record.room_number,
                code=record.code,
                active_courses=[
                    dict(
                        course_name=alloc_subject.subject.name,
                        start_date=alloc_subject.start_date,
                        end_date=alloc_subject.end_date,
                    )
                    for alloc_subject in allocated_subjects
                ],
            )
        )
    return response


@authorized_access(user_types=["authorized_user"])
def profile_upload(request, *args, **kwargs):
    """
    Upload teacher's profile

    Just keeping it simple

    Further enhancements can be doing this as a background task, keep number of failures and successful import cases
    and sending report ot a specific group of users via email

    :param request:
    :param args:
    :param kwargs:
    :return:
    """

    template = "profile_upload.html"
    # prompt is a context variable that can have different values      depending on their context
    prompt = {
        "order": "Order of the CSV should be <br/> "
        "First Name<br/>"
        "Last Name<br/>"
        "Profile picture<br/>"
        "Email Address<br/>"
        "Phone Number<br/>"
        "Room Number<br/>"
        "Subjects taught",
    }
    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES["file"]
    image_files = request.FILES["image_files"]
    folder_name = random_string(
        size=8, allowed=string.digits, prefix=datetime.date.today().strftime("%Y-%m-%d")
    )
    content_upload_path = "images/" + folder_name
    try:
        with zipfile.ZipFile(image_files, "r") as zip_ref:
            zip_ref.extractall(content_upload_path)
        if not csv_file.name.endswith(".csv"):
            messages.error(request, "File type not supported")
    except Exception as error:
        messages.error(request, error)
    data_dict, headers, errors = get_data_from_upload(
        csv_file,
        "csv",
        header_mapping={
            "First Name": "first_name",
            "Last Name": "last_name",
            "Profile picture": "profile_picture",
            "Email Address": "email",
            "Phone Number": "phone_number",
            "Room Number": "room_number",
            "Subjects taught": "subjects",
        },
    )
    for entry in data_dict:
        if entry.get("email"):
            teacher = get_teacher_from_email(
                entry["email"],
                create_teacher=True,
                content_upload_path=content_upload_path,
                **entry
            )
            if teacher:
                subject_list = entry.get("subjects", "").split(",")
                # add subjects
                for subject_name in subject_list:
                    subject_name = subject_name.strip()
                    subject = get_subject_by_name(
                        subject_name,
                        create_subject=True,
                        name=subject_name,
                        is_active=True,
                    )
                    if subject:
                        add_new_course(teacher, subject)

    return render(request, template, dict(order="Added successfully."))


def get_profile_picture(request, *args, **kwargs):
    """
    Profile picture preview

    Endpoint: /api/v1/teacher/profile_picture/?reference_number=ABC

    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    reference_number = request.GET.get("reference_number")
    record = Teacher.objects.filter(reference_number=reference_number).first()
    if record:
        with open(record.profile_picture.path, "rb") as fp:
            return HttpResponse(fp.read(), content_type="image/jpeg")
    return HttpResponseNotFound()
