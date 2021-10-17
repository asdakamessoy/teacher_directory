"""teacher_directory URL Configuration """

from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import re_path

from main.api import teacher


urlpatterns = [
    url(r"^admin/", admin.site.urls),
]


TEACHER_API = (
    re_path(
        r"^v1/teacher/all/",
        teacher.list_all,
        name="teacher-list",
    ),
    re_path(
        r"^v1/teacher/read/",
        teacher.read,
        name="teacher-view",
    ),
    re_path(
        r"^v1/teacher/upload-csv/",
        teacher.profile_upload,
        name="teacher-profile-upload",
    ),
    re_path(
        r"^v1/teacher/profile-picture/",
        teacher.get_profile_picture,
        name="teacher-profile-picture",
    ),
)

urlpatterns.extend(TEACHER_API)
