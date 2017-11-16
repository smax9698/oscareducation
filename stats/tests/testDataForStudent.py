from django.test import TestCase

from examinations.models import TestStudent, Test
from promotions.models import Stage
from resources.models import Resource
from stats.models import ExamStudent, AuthenticationStudent, ResourceStudent
from stats.utils import *
from users.models import User, Student
from skills.models import Skill
from stats.StatsObject import get_stat_for_student


class RetrieveCorrectJSON(TestCase):
    def setUp(self):
        user = User.objects.create(username="username")
        user.save()
        student = Student.objects.create(user=user)
        student.save()
        self.student = student

        stage = Stage.objects.create(name="stage_name", short_name='sn', level=1)
        stage.save()
        lesson = Lesson.objects.create(name="lesson", stage=stage)
        lesson.save()
        lesson.students.add(student)

        # Defining a set of skills
        skills = []
        for i in range(6):
            skill = Skill.objects.create(code="skill" + str(i), name="skill" + str(i))
            skill.save()
            skills.append(skill)

        self.skills = skills

        # Defining an set of tests
        test1 = Test.objects.create(name="test1", lesson=lesson)
        test1.save()
        test1.skills.add(skills[0])
        test1.skills.add(skills[1])

        test2 = Test.objects.create(name="test2", lesson=lesson)
        test2.save()
        test2.skills.add(skills[0])
        test2.skills.add(skills[2])
        test2.skills.add(skills[3])

        test3 = Test.objects.create(name="test3", lesson=lesson)
        test3.save()
        test3.skills.add(skills[4])
        test3.skills.add(skills[5])

        # Defining the TestStudent (object we will look for)
        test_student1 = TestStudent.objects.create(student=student, test=test1, finished_at=datetime.date(2017, 9, 12))
        test_student1.save()
        test_student2 = TestStudent.objects.create(student=student, test=test2, finished_at=datetime.date(2017, 10, 11))
        test_student2.save()
        test_student3 = TestStudent.objects.create(student=student, test=test3, finished_at=datetime.date(2017, 11, 10))
        test_student3.save()

        result = {}
