from django.test import TestCase

from users.models import User, Student


class TestLeastSkillAcquired(TestCase):
    def setUp(self):
        number_of_student = 60

        for i in range(0, number_of_student):
            user = User.objects.create(username="username" + str(i))
            student = Student.objects.create(user=user)
            student.save()
