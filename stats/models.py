# encoding: utf-8

from django.contrib.auth.models import User
from django.db import models

from examinations import models as model_examination
from resources import models as model_resource
from skills import models as model_skill


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
    ressource : ressouce id
    user : student id
    """
    resource = models.ForeignKey(model_resource.Resource)
    user = models.ForeignKey(User)
    when = models.DateTimeField(auto_now_add=True)


class AuthenticationStudent(models.Model):
    """
    A record is saved on this table each time
    a student access to the application

    user : foreign key to User table
    date_accessed : date time when the student log in
    end_of_session : date time when the student log out
    """
    user = models.ForeignKey(User)
    date_accessed = models.DateTimeField(auto_now_add=True)
    end_of_session = models.DateTimeField()


class SkillStudent(models.Model):
    """
    when a student master a skill. The date is recorded on this table

    date_acquired : date time of the acquired skill
    user :  student id (foreign key)
    skill : skill id (foreign key)
    """
    date_acquired = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    skill = models.ForeignKey(model_skill.Skill)


class ExamStudent(models.Model):
    """
    each time a student make an exam, a record will be saved on this table
    user : student id (foreign key)
    exam : exam id (foreign key)
    """
    user = models.ForeignKey(User)
    exam = models.ForeignKey(model_examination.TestStudent)


class ExamStudentSkill(models.Model):
    """
    skills tested when doing an exam
    skill_student : skill_student id (foreign key)
    skill : skil id (foreign key)
    """
    skill_student = models.ForeignKey(ExamStudent)
    skill = models.ForeignKey(model_skill.Skill)
