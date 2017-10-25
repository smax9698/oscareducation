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
    """
    Each time a student is done with an exam we use this method to add the field in the table ExamStudent

    Keyword arguments:
    user -- id of the user (who's normally a student)
    exam_id -- id of the finished exam

    """
    student = models.ExamStudent(user=user, exam=exam_id)
    student.save()


def add_skill_acquired_by_student(user, skill_id, status):
    """
    Each time a student acquires a skill we use this method to add the field in the table SkillStudent

    Keyword arguments:
    user -- id of the user (who's normally a student)
    skill_id -- id of the mastered skill
    status -- status of the mastering level of the skill (unmastered, in progress, mastered)

    """
    student = models.SkillStudent(date_acquired=datetime.datetime, user=user, skill=skill_id,)
    student.save()


def add_authentication_by_student(user, start_date, end_date):
    """
    Each time a student logs in we use this method to add the field in the table AuthenticationStudent

    Keyword arguments:
    user -- id of the user (who's normally a student)
    start_date -- date object in the same form as datetime.datetime, which times the beginning of the session
    end_date -- date object in the same form as datetime.datetime, which times the end of the session

    """
    student = models.AuthenticationStudent(user=user, date_accessed=start_date, end_of_session=end_date)
    student.save()


def add_resource_accessed_by_student(user, resource_id):
    """
    Each time a student access to a particular resource we use this method to add the field in the table ResourceStudent

    Keyword arguments:
    user -- id of the user (who's normally a student)
    resource_id -- id of the resource
    """
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

    return len(query)


def get_number_succeeded_exam_by_student(student):
    query = models.ExamStudent.object.get(user=student,succeeded=True)

    return len(query)


def get_exam_by_student(student):
    query = models.ExamStudent.object.get(user=student)
    #TODO find exam_id


def get_time_spent_on_exam(exam):
    """exam : examination.TestStudent"""
    return exam.finished_at - exam.started_at


def get_skill_status(skillStudent):
    return skillStudent.progress