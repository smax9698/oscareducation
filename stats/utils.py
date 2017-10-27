from django.contrib.auth.decorators import user_passes_test

import stats.models as models
from promotions.models import Lesson
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
    new_entry = models.SkillStudent(student=student, skill=skill_id, progress="mastered")
    new_entry.save()


def add_authentication_by_student(student, end_date):
    """
    Each time a student logs in we use this method to add the field in the table AuthenticationStudent

    Keyword arguments:
    student -- student who logged in
    start_date -- date object in the same form as datetime.datetime, which times the beginning of the session
    end_date -- date object in the same form as datetime.datetime, which times the end of the session

    """
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


def get_resources_accessed_by_student(student):
    accessed_by_ressources = {}

    query = models.ResourceStudent.objects.get(student=student)

    for item in query:
        if item.resource in accessed_by_ressources:
            accessed_by_ressources[item.resource] += 1
        else:
            accessed_by_ressources[item.resource] = 1

    return accessed_by_ressources


def get_number_of_authentication_by_student(student):
    query = models.AuthenticationStudent.objects.get(student=student)

    return len(query)


def get_authentication_info_by_student(student):
    return models.AuthenticationStudent.objects.get(student=student)


def get_skill_acquired_by_student(student):
    query = models.SkillStudent.objects.get(student=student)

    return len(query)


def get_number_succeeded_exam_by_student(student):
    query = models.ExamStudent.objects.get(student=student, succeeded=True)

    return len(query)


def get_exam_by_student(student):
    query = models.ExamStudent.objects.get(student=student)
    # TODO find exam_id


def get_time_spent_on_exam(exam):
    """exam : examination.TestStudent"""
    return exam.finished_at - exam.started_at


def get_skill_status(skillStudent):
    return skillStudent.progress


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
