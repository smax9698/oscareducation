from django.contrib.auth.decorators import user_passes_test

import stats.models as models
import datetime

def user_is_superuser(function):
    return user_passes_test(lambda x: x.is_superuser)(function)

###################
# Access database #
###################

###################
#    Update       #
###################


def add_exam_done_by_student(user, exam_id):
    student = models.ExamStudent(user=user, exam=exam_id)
    student.save()


def add_skill_acquired_by_student(user, skill_id):
    student = models.ResourceStudent(date_acquired=datetime.datetime, user=user, skill=skill_id)
    student.save()


def add_authentication_by_student(user, start_date, end_date):
    student = models.AuthenticationStudent(user=user, date_accessed=start_date, end_of_session=end_date)
    student.save()


def add_resource_accessed_by_student(user, resource_id):
    student = models.ResourceStudent(resource=resource_id, user=user, when=datetime.datetime)
    student.save()

###################
#      Get        #
###################


def get_resources_accessed_by_student(student):
    accessed_by_ressources = {}

    query = models.ResourceStudent.objects.get(user=student)

    for item in query:
        if item.resource in accessed_by_ressources:
            accessed_by_ressources[item.resource] += 1
        else:
            accessed_by_ressources[item.resource] = 1

    return accessed_by_ressources


def get_number_of_authentication_by_student(student):
    query = models.AuthenticationStudent.objects.get(user=student)

    return len(query)


def get_authentication_info_by_student(student):
    return models.AuthenticationStudent.objects.get(user=student)


def get_skill_acquired_by_student(student):
    query = models.SkillStudent.objects.get(user=student)

    len(query)
