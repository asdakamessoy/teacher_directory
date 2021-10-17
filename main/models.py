# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import uuid

from django.db import models


class Teacher(models.Model):
    """
    Teacher model

    """

    first_name = models.TextField(max_length=100)
    last_name = models.TextField(max_length=100)
    # saving it in a specific path
    profile_picture = models.ImageField(upload_to="images", blank=True, null=True)
    phone_number = models.TextField(max_length=15, null=True, default=None)
    email = models.EmailField(blank=True, unique=True, default=None, null=True)
    # assuming room number is varchar
    room_number = models.TextField(max_length=10)
    code = models.TextField(max_length=20)
    # reference_number
    reference_number = models.CharField(
        default=uuid.uuid4,
        editable=False,
        max_length=100,
        null=True,
        blank=True,
        unique=True,
    )

    def can_add_new_subject(self):
        """
        Check if teacher has capacity of getting new subject

        :return:
        """
        # get all active allocated course
        course_allocated_count = CourseAllocation.objects.filter(
            teacher=self, subject__is_active=True
        ).count()
        return course_allocated_count < CourseAllocation.MAX_SUBJECT_COUNT

    def __str__(self):
        return f"{self.first_name}"


class Subject(models.Model):
    """
    Subject model

    """

    name = models.TextField(max_length=100)
    # this way we can deactivate a subject
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"


class CourseAllocation(models.Model):
    """
    Course Allocation Details

    Subject with it's active associated teacher

    """

    # can get it as a config variable
    MAX_SUBJECT_COUNT = 5

    # course might have no teacher assigned
    teacher = models.ForeignKey(
        "main.Teacher", on_delete=models.PROTECT, blank=True, null=True
    )
    subject = models.ForeignKey("main.Subject", on_delete=models.PROTECT)
    # we can add interval to it as well
    end_date = models.DateField(null=True, blank=True)
    start_date = models.DateField(default=datetime.date.today())


    def __str__(self):
        return f"{self.teacher.first_name} -- {self.subject.name}"
