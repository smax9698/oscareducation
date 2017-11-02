import datetime

from django.test import TestCase

from examinations.models import TestStudent, Test
from promotions.models import Lesson, Stage
from skills.models import Skill
from stats.models import ExamStudent, ExamStudentSkill
from stats.utils import get_latest_test_succeeded
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
        self.test1 = Test.objects.create(name="test1", lesson=self.lesson1)
        self.test2 = Test.objects.create(name="test2", lesson=self.lesson1)

        self.test.save()
        self.test1.save()
        self.test2.save()

        test_student1 = TestStudent.objects.create(student=self.student, finished=True, test=self.test1,
                                                   started_at=datetime.date(2016, 3, 13),
                                                   finished_at=datetime.date(2016, 3, 20))
        test_student2 = TestStudent.objects.create(student=self.student, finished=False, test=self.test,
                                                   started_at=datetime.date(2015, 3, 13),
                                                   finished_at=datetime.date(2015, 4, 02))
        test_student3 = TestStudent.objects.create(student=self.student1, finished=True, test=self.test2,
                                                   started_at=datetime.date(2017, 10, 13),
                                                   finished_at=datetime.date(2017, 10, 27))
        test_student4 = TestStudent.objects.create(student=self.student1, finished=False, test=self.test,
                                                   started_at=datetime.date(2017, 3, 13),
                                                   finished_at=datetime.date(2017, 6, 13))

        test_student1.save()
        test_student2.save()
        test_student3.save()
        test_student4.save()

        exam1 = ExamStudent.objects.create(student=self.student, exam=test_student1, succeeded=True)
        exam2 = ExamStudent.objects.create(student=self.student, exam=test_student2, succeeded=False)
        exam3 = ExamStudent.objects.create(student=self.student1, exam=test_student3, succeeded=True)
        exam4 = ExamStudent.objects.create(student=self.student1, exam=test_student4, succeeded=False)

        exam1.save()
        exam2.save()
        exam3.save()
        exam4.save()

        exam_skill1 = ExamStudentSkill.objects.create(skill=skill1, skill_student=exam1)
        exam_skill2 = ExamStudentSkill.objects.create(skill=skill2, skill_student=exam2)
        exam_skill3 = ExamStudentSkill.objects.create(skill=skill3, skill_student=exam3)
        exam_skill4 = ExamStudentSkill.objects.create(skill=skill4, skill_student=exam4)

        exam_skill1.save()
        exam_skill2.save()
        exam_skill3.save()
        exam_skill4.save()

    def test_get_latest_test_succeeded(self):
        self.assertEquals(get_latest_test_succeeded(self.student, self.lesson1), self.test1)
        self.assertEquals(get_latest_test_succeeded(self.student1, self.lesson1), self.test2)

    def test_when_no_test(self):
        self.assertEquals(get_latest_test_succeeded(self.student2, self.lesson1), None)
