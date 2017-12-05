from django.test import TestCase

from examinations.models import TestStudent, Test
from promotions.models import Stage
from resources.models import Resource
from stats.models import ExamStudent, AuthenticationStudent, ResourceStudent
from stats.utils import *
from users.models import User, Student
from skills.models import Skill

import datetime

# Create your tests here.


class UpdateExamDoneByStudent(TestCase):
    def setUp(self):
        user = User.objects.create(username="username")
        student = Student.objects.create(user=user)
        student.save()
        self.student = student

        stage = Stage.objects.create(name="stage one", level=1)
        stage.save()

        lesson = Lesson.objects.create(name="lesson one", stage=stage)
        lesson.save()

        test_one = Test.objects.create(type="skills", name="test one", lesson=lesson)
        test_one.save()

        test_two = Test.objects.create(type="skills", name="test two", lesson=lesson)
        test_two.save()

        test_student_one = TestStudent.objects.create(student=student, test=test_one)
        test_student_one.save()

        test_student_two = TestStudent.objects.create(student=student, test=test_two)
        test_student_two.save()
        self.test_student_one = test_student_one
        self.test_student_two = test_student_two

    def test_when_no_row_insert_one(self):
        add_exam_done_by_student(self.student, self.test_student_one)
        result_query = ExamStudent.objects.filter(student=self.student)
        self.assertEqual(len(result_query), 1)

    def test_when_already_one_not_deleted(self):
        add_exam_done_by_student(self.student, self.test_student_one)
        add_exam_done_by_student(self.student, self.test_student_two)
        result_query = ExamStudent.objects.filter(student=self.student)

        exam_student_one_expected = ExamStudent(student=self.student, exam=self.test_student_one)
        exam_student_two_expected = ExamStudent(student=self.student, exam=self.test_student_two)

        self.assertIn(exam_student_one_expected, result_query)
        self.assertIn(exam_student_two_expected, result_query)


class UpdateSkillAcquiredByStudent(TestCase):
    def setUp(self):
        user = User.objects.create(username="username")
        student = Student.objects.create(user=user)
        student.save()
        self.student = student

        skill_one = Skill.objects.create(code="skill one")
        skill_one.save()
        self.skill_one = skill_one

        skill_two = Skill.objects.create(code="skill two")
        skill_two.save()
        self.skill_two = skill_two

    def test_when_no_row_insert_one(self):
        add_skill_acquired_by_student(self.student, self.skill_one)
        result_query = StudentSkill.objects.filter(student=self.student)
        self.assertEqual(len(result_query), 1)

    def test_when_already_one_not_deleted(self):
        add_skill_acquired_by_student(self.student, self.skill_one)
        add_skill_acquired_by_student(self.student, self.skill_two)
        result_query = StudentSkill.objects.filter(student=self.student)

        skill_expected_one = StudentSkill.objects.create(student=self.student, skill=self.skill_one)
        skill_expected_two = StudentSkill.objects.create(student=self.student, skill=self.skill_two)

        self.assertIn(skill_expected_one, result_query)
        self.assertIn(skill_expected_two, result_query)


class UpdateAuthenticationByStudent(TestCase):
    def setUp(self):
        user = User.objects.create(username="username")
        user.save()
        self.user = user
        student = Student.objects.create(user=user)
        student.save()
        self.student = student

        date_one = datetime.date(2017, 10, 26)
        self.date_one = date_one
        date_two = datetime.date(2017, 11, 10)
        self.date_two = date_two

    def test_when_no_row_insert_one(self):
        add_authentication_by_student(self.user, self.date_one)
        result_query = AuthenticationStudent.objects.filter(student=self.student)
        self.assertEqual(len(result_query), 1)
        self.assertEqual(result_query[0].end_of_session.date(), self.date_one)

    def test_when_already_one_not_deleted(self):
        add_authentication_by_student(self.user, self.date_one)
        add_authentication_by_student(self.user, self.date_two)

        result_query = AuthenticationStudent.objects.filter(student=self.student)

        self.assertEqual(len(result_query), 2)
        self.assertEqual(result_query[0].end_of_session.date(), self.date_one)
        self.assertEqual(result_query[1].end_of_session.date(), self.date_two)


class UpdateResourceAccessed(TestCase):
    def setUp(self):
        user = User.objects.create(username="username")
        student = Student.objects.create(user=user)
        student.save()
        self.student = student

        resource_one = Resource.objects.create(content={'name': 'resource one'})
        resource_one.save()
        resource_two = Resource.objects.create(content={'name': 'resource two'})
        resource_two.save()
        self.resource_one = resource_one
        self.resource_two = resource_two

    def test_when_no_row_insert_one(self):
        add_resource_accessed_by_student(student=self.student, resource_id=self.resource_one)
        result_query = ResourceStudent.objects.filter(student=self.student)
        self.assertEqual(len(result_query), 1)

    def test_when_already_one_not_deleted(self):
        add_resource_accessed_by_student(self.student, self.resource_one)
        add_resource_accessed_by_student(self.student, self.resource_two)

        result_query = ResourceStudent.objects.filter(student=self.student)

        self.assertEqual(len(result_query), 2)
        self.assertEqual(result_query[0].resource, self.resource_one)
        self.assertEqual(result_query[1].resource, self.resource_two)
