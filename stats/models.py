# encoding: utf-8

from django.contrib.auth.models import User
from django.db import models

from examinations import models as model_examination
from resources import models as model_resource
from skills import models as model_skill
from users.models import Student


# Create your models here.
class LoginStats(models.Model):
    user = models.ForeignKey(User)
    user_kind = models.CharField(max_length=255,
                                 choices=(('student', 'étudiant·e'), ('professor', 'Professeur'), ('admin', 'Admin')))
    when = models.DateTimeField(auto_now_add=True)


class ResourceStudent(models.Model):
    """
    Each time a student access to a particular resource, we store
    when : accessed date
    resource : resource id
    user : student id
    """
    resource = models.ForeignKey(model_resource.Resource)
    student = models.ForeignKey(Student)
    when = models.DateTimeField(auto_now_add=True)

    def __eq__(self, other):
        if other is None:
            return False
        return self.resource == other.resource and self.student == other.student


class AuthenticationStudent(models.Model):
    """
    A record is saved on this table each time
    a student access to the application

    user : foreign key to User table
    date_accessed : date time when the student log in
    end_of_session : date time when the student log out
    """
    student = models.ForeignKey(Student, default=None)
    date_accessed = models.DateTimeField(auto_now_add=True)
    end_of_session = models.DateTimeField(default=None, null=True)

    def __eq__(self, other):
        if other is None:
            return False
        return self.student == other.student and self.date_accessed == other.date_accessed \
               and self.end_of_session == other.end_of_session


class ExamStudent(models.Model):
    """
    each time a student make an exam, a record will be saved on this table
    user : student id (foreign key)
    exam : exam id (foreign key)
    succeeded : success of the exam
    """
    student = models.ForeignKey(Student, default=None)
    exam = models.ForeignKey(model_examination.TestStudent)
    succeeded = models.BooleanField(default=False)

    def __eq__(self, other):
        if other is None:
            return False
        return self.student == other.student and self.exam == other.exam and self.succeeded == other.succeeded


class ExamStudentSkill(models.Model):
    """
    skills tested when doing an exam
    skill_student : skill_student id (foreign key)
    skill : skil id (foreign key)
    """
    skill_student = models.ForeignKey(ExamStudent)
    skill = models.ForeignKey(model_skill.Skill)

    def __eq__(self, other):
        if other is None:
            return False
        return self.skill_student == other.skill_student and self.skill == other.skill
