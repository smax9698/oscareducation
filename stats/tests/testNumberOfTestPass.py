import datetime

from django.test import TestCase

from examinations.models import TestStudent, Test
from promotions.models import Lesson, Stage
from skills.models import Skill
from stats.models import ExamStudent, ExamStudentSkill
from stats.utils import number_of_test_pass
from users.models import User, Student


class TestGetLatestTestSucceeded(TestCase):
    def setUp(self):
        user = User.objects.create(username="student1")
        user1 = User.objects.create(username="student2")
        user2 = User.objects.create(username="student3")

        self.student = Student.objects.create(user=user)
        self.student1 = Student.objects.create(user=user1)
        self.student2 = Student.objects.create(user=user2)

        self.student.save()
        self.student1.save()
        self.student2.save()

        stage = Stage.objects.create(name="stage_name", short_name='sn', level=1)
        stage.save()

        self.lesson1 = Lesson.objects.create(name="my_lesson", stage=stage)
        self.lesson1.save()

        self.lesson1.students.add(self.student)
        self.lesson1.students.add(self.student1)
        self.lesson1.students.add(self.student2)

        skill1 = Skill.objects.create(code="skill1", name="skill1")
        skill2 = Skill.objects.create(code="skill2", name="skill2")
        skill3 = Skill.objects.create(code="skill3", name="skill3")
        skill4 = Skill.objects.create(code="skill4", name="skill4")

        skill1.save()
        skill2.save()
        skill3.save()
        skill4.save()

        stage.skills.add(skill1)
        stage.skills.add(skill2)
        stage.skills.add(skill3)
        stage.skills.add(skill4)

        self.test = Test.objects.create(name="test0", lesson=self.lesson1)

        for i in range(0, 100):
            test_student = TestStudent.objects.create(student=self.student, finished=True, test=self.test,
                                                      started_at=datetime.date(2016, 3, 13),
                                                      finished_at=datetime.date(2016, 3, 20))
            exam = ExamStudent.objects.create(student=self.student, exam=test_student, succeeded=True)
            exam_skill = ExamStudentSkill.objects.create(skill=skill1, skill_student=exam)

            test_student.save()
            exam.save()
            exam_skill.save()

    def test_number_of_test_pass(self):
        self.assertEquals(number_of_test_pass(self.student, self.lesson1), 100)

    def test_no_test(self):
        self.assertEquals(number_of_test_pass(self.student1, self.lesson1), 0)
