from django.contrib.auth.decorators import user_passes_test

import models


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
