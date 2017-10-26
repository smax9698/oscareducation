from django.test import TestCase

from examinations.models import TestStudent, Test
from promotions.models import Lesson, Stage
from stats.models import ExamStudent
from stats.utils import *
from users.models import User, Student


# Create your tests here.


class TestUpdateExamDoneByStudent(TestCase):
    def setUp(self):
        user = User.objects.create(username="username")
        student = Student.objects.create(user=user)
        student.save()
        self.student = student

        stage_one = Stage.objects.create(name="stage one", level=1)
        stage_one.save()

        lesson_one = Lesson.objects.create(name="lesson one", stage=stage_one)
        lesson_one.save()

        test_one = Test.objects.create(type="skills", name="test one", lesson=lesson_one)
        test_one.save()

        test_student_one = TestStudent.objects.create(student=student, test=test_one)
        test_student_one.save()
        self.test_student_one = test_student_one

    def test_when_no_row_insert_new(self):
        add_exam_done_by_student(self.student.user, self.test_student_one)
        result_query = list(ExamStudent.objects.filter(user=self.student.user, exam=self.test_student_one))
        self.assertEqual(len(result_query), 1)
        self.assertEqual(result_query[0].user, self.student.user)
        self.assertEqual(result_query[0].exam, self.test_student_one)
