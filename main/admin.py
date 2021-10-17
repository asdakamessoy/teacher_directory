# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.contrib import admin

# Register your models here.
from django.http.response import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe

from main.models import Teacher, Subject, CourseAllocation


class CourseAllocationInline(admin.TabularInline):
    """ CourseAllocationInline """

    model = CourseAllocation
    readonly_fields = (
        "subject_name",
        "start_date",
        "end_date",
        "course_status",
    )
    fields = (
        "subject_name",
        "start_date",
        "end_date",
        "course_status",
    )
    can_delete = False
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def subject_name(self, obj):
        return obj.subject.name

    def course_status(self, obj):
        status = "Active"
        if not obj.subject.is_active or (
            obj.end_date and obj.end_date < datetime.date.today()
        ):
            status = "Not Active"
        return status

    course_status.short_description = "Course Status"


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):

    list_display = [
        "first_name",
        "last_name",
        "email",
    ]
    search_fields = [
        "last_name",
        "first_name",
        "email",
    ]

    fields = (
        "profile_picture",
        "pic_thumb",
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "room_number",
        "code",
    )
    readonly_fields = ("pic_thumb",)

    inlines = [
        CourseAllocationInline,
    ]

    def __str__(self):
        """Literal name."""
        return self.first_name

    @mark_safe
    def pic_thumb(self, obj):
        from django.utils.html import escape

        url = f"{reverse('teacher-profile-picture')}?reference_number={obj.reference_number}"
        return '<img src="%s" style="width:100px; height: 100px;"/>' % escape(url)

    pic_thumb.short_description = "Profile Picture"
    pic_thumb.allow_tags = True


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):

    list_display = [
        "name",
    ]
    search_fields = [
        "name",
    ]
    fields = (
        "name",
        "is_active",
    )

    def __str__(self):
        """Literal name."""
        return self.name


@admin.register(CourseAllocation)
class CourseAllocationAdmin(admin.ModelAdmin):

    list_display = [
        "teacher",
        "subject",
        "course_status",
    ]
    readonly_fields = ("course_status",)

    def __str__(self):
        return f"{self.subject.name} - {self.teacher.first_name}"

    def course_status(self, obj):
        status = "Active"
        if not obj.subject.is_active or (
            obj.end_date and obj.end_date < datetime.date.today()
        ):
            status = "Not Active"
        return status

    course_status.short_description = "Status"
