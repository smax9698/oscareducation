from django.test import TestCase

from stats.models import AuthenticationStudent
from stats.StatsObject import NumberOfLogin
from users.models import User, Student


class RetrieveDataAuthentication(TestCase):
    def setUp(self):
        user = User.objects.create(username="pseudonym")
        student = Student.objects.create(user=user)
        student.save()

        user2 = User.objects.create(username="username")
        student_no_connexion = Student.objects.create(user=user2)
        student_no_connexion.save()

        self.student_already_connected = student
        self.student_not_connected_yet = student_no_connexion

        for i in range(0, 25):
            auth = AuthenticationStudent.objects.create(student=student)
            auth.save()

    def test_student_connected_for_more_than_zero_time(self):
        error_msg = "Query don't correctly retrieve authentication data when a student connect himself lot's of time"
        datas = NumberOfLogin(self.student_already_connected).data
        sum_log = 0
        for key in datas:
            if datas[key] > sum_log:
                sum_log = datas[key]
        self.assertEqual(sum_log, 25, error_msg)

    def test_student_not_connected_yet(self):
        error_msg = "Query don't correctly retrieve authentication when a student have no connexion data"
        datas = NumberOfLogin(self.student_not_connected_yet)
        sum_log = 0
        for key in datas:
            if datas[key] > sum_log:
                sum_log = datas[key]
        self.assertEqual(sum_log, 0, error_msg)
