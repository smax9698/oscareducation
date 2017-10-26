from django.contrib.auth.decorators import user_passes_test

import models
from promotions.models import Lesson
from users.models import Student


def user_is_superuser(function):
    return user_passes_test(lambda x: x.is_superuser)(function)


###################
# Access database #
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
    query = models.SkillStudent.object.get(user=student)

    len(query)


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
