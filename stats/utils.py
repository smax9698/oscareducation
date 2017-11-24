import datetime
import pytz
from django.contrib.auth.decorators import user_passes_test

import stats.models as models
from promotions.models import Lesson
from skills.models import StudentSkill
from users.models import Student


def user_is_superuser(function):
    return user_passes_test(lambda x: x.is_superuser)(function)


###################
# Access database #
###################

###################
#    Update       #
###################


def add_exam_done_by_student(student, exam_id):
    """
    Each time a student is done with an exam we use this method to add the field in the table ExamStudent

    Keyword arguments:
    student -- the student who passed the exam
    exam_id -- id of the finished exam

    """
    new_entry = models.ExamStudent(student=student, exam=exam_id)
    new_entry.save()


def add_skill_acquired_by_student(student, skill_id):
    """
    Each time a student acquires a skill we use this method to add the field in the table SkillStudent

    Keyword arguments:
    student -- the student who acquired the skill
    skill_id -- id of the mastered skill
    status -- status of the mastering level of the skill (unmastered, in progress, mastered)

    """
    new_entry = StudentSkill(student=student, skill=skill_id, acquired=datetime.datetime.now(tz=pytz.utc))
    new_entry.save()


def add_authentication_by_student(user, end_date):
    """
    Each time a student logs in we use this method to add the field in the table AuthenticationStudent

    Keyword arguments:
    student -- student who logged in
    start_date -- date object in the same form as datetime.datetime, which times the beginning of the session
    end_date -- date object in the same form as datetime.datetime, which times the end of the session

    """
    student = Student.objects.filter(user=user)[0]
    new_entry = models.AuthenticationStudent(student=student, end_of_session=end_date)
    new_entry.save()


def add_resource_accessed_by_student(student, resource_id):
    """
    Each time a student access to a particular resource we use this method to add the field in the table ResourceStudent

    Keyword arguments:
    student -- student who accessed the resource
    resource_id -- id of the resource
    """
    new_entry = models.ResourceStudent(resource=resource_id, student=student)
    new_entry.save()


###################
#      Get        #
###################

def get_students_by_professor(professor):
    """
    Returns all students of all classes that the professor have

    :param professor: Professor object
    :return: a list with all students related to a professor
    """
    query = Lesson.objects.filter(professors=professor)
    students_dico = {}

    for item in query:
        students = Student.objects.filter(lesson=item)
        for student in students:
            if str(student) not in students_dico:
                yield student
                students_dico[str(student)] = True


def get_login_stats_by_professor(startDate,endDate, userKind):
    """
    Returns all login stats objects fulfilling the filtering criteria

    :param startDate: timedate
    :param endDate: timedate
    """
    print(userKind)
    if startDate != '':
        if endDate != '': # filter with both
            allLogins = models.LoginStats.objects.filter(when__lte=endDate).filter(when__gte=startDate).filter(user_kind__in=userKind)
        else: # filter with only startDate
            allLogins = models.LoginStats.objects.filter(when__gte=startDate).filter(user_kind__in=userKind)
    else:
        if endDate != '': # filter with only end
            allLogins = models.LoginStats.objects.filter(when__lte=endDate).filter(user_kind__in=userKind)
        else: # no filter
            allLogins = models.LoginStats.objects.filter(user_kind__in=userKind)

    for item in allLogins:
        yield [item.user, item.user_kind, item.when]

def get_res_students_by_professor(startDate,endDate):
    """
    Returns all resource student objects fulfilling the filtering criteria

    :param startDate: timedate
    :param endDate: timedate
    """
    if startDate != '':
        if endDate != '': # filter with both
            allLogins = models.ResourceStudent.objects.filter(when__lte=endDate).filter(when__gte=startDate)
        else: # filter with only startDate
            allLogins = models.ResourceStudent.objects.filter(when__gte=startDate)
    else:
        if endDate != '': # filter with only end
            allLogins = models.ResourceStudent.objects.filter(when__lte=endDate)
        else: # no filter
            allLogins = models.ResourceStudent.objects.all()

    for item in allLogins:
        yield [item.resource, item.student, item.when]

def get_auth_students_by_professor(startDate,endDate):
    """
    Returns all authentication student objects fulfilling the filtering criteria

    :param startDate: timedate
    :param endDate: timedate
    """
    if startDate != '':
        if endDate != '': # filter with both
            allLogins = models.AuthenticationStudent.objects.filter(date_accessed__lte=endDate).filter(date_accessed__gte=startDate)
        else: # filter with only startDate
            allLogins = models.AuthenticationStudent.objects.filter(date_accessed__gte=startDate)
    else:
        if endDate != '': # filter with only end
            allLogins = models.AuthenticationStudent.objects.filter(date_accessed__lte=endDate)
        else: # no filter
            allLogins = models.AuthenticationStudent.objects.all()

    for item in allLogins:
        yield [item.student, item.date_accessed, item.end_of_session]

def get_exam_students_by_professor():
    """
    Returns all authentication student objects fulfilling the filtering criteria

    """
    allLogins = models.ExamStudent.objects.all()

    for item in allLogins:
        yield [item.student, item.exam, item.succeeded]

def get_exam_students_skill_by_professor():
    """
    Returns all authentication student objects fulfilling the filtering criteria

    """
    allLogins = models.ExamStudentSkill.objects.all()

    for item in allLogins:
        yield [item.skill_student, item.skill]
