from django.test import TestCase
from django.contrib.auth.models import User
from users.models import Professor, Student
from skills.models import Skill

'''  
    To run tests, make sure the oscar user in your DB has the can create DB option checked 
    Do a makemigrations and migrate to have the last version of the DB (professor criteria included) 
    If the migrate doesn't work, you're going to have to delete everything (DB and project included) and do 
    the whole installation again. 
    Once it's done, just do python manage.py tests (It's going to check every tests and the 3 from promotions 
    are failing but it has nothing to do with our work. 
'''

'''
class PermissionsTest(TestCase):
    def setUp(self):
        prof = User.objects.create(username="professor")
        print(User.get_username(prof))
        prof.set_password("1234")
        prof.save()
        self.prof = Professor.objects.create(user=prof)

        student = User.objects.create(username="student")
        student.set_password("1234")
        student.save()
        self.prof = Student.objects.create(user=student)

    # Create your tests here.
    def testMethod(self):
        test = 1
        self.assertEquals(test, 2) '''