import random

from django.test import TestCase
from django.utils import timezone

from skills.models import Skill, StudentSkill
from stats.utils import get_skill_acquired_by_student
from users.models import Student, User


class TestRetrieveAcquiredSkillStudent(TestCase):
    def setUp(self):
        user = User.objects.create(username="pseudonym")
        self.student = Student.objects.create(user=user)

        user2 = User.objects.create(username="username")
        self.student_no_skills_acquired = Student.objects.create(user=user2)

        self.student.save()
        self.student_no_skills_acquired.save()

        skill_list = []
        student_skill_acquired = 0

        for i in range(0, 25):
            gen_name = "skill" + str(i)

            skill = Skill.objects.create(code=gen_name, name=gen_name)
            skill.save()
            skill_list.append(skill)

        random.seed()

        for skill in skill_list:
            if random.randint(0, 1) == 1:
                student_skill_acquired += 1
                student_skill = StudentSkill.objects.create(student=self.student, skill=skill, acquired=timezone.now())
                student_skill.save()

        # Skill added in case of random always return 0

        skill = Skill.objects.create(name="my_skill", code="my_skill")
        skill.save()
        student_skill = StudentSkill.objects.create(student=self.student, skill=skill, acquired=timezone.now())
        student_skill.save()
        student_skill_acquired += 1

        self.expected_number_of_skill_acquired_by_student = student_skill_acquired

    def test_correct_number_skills_acquired_with_student_who_have_acquired_more_than_zero_skill(self):

        self.assertEqual(get_skill_acquired_by_student(self.student), self.expected_number_of_skill_acquired_by_student)

    def test_when_student_no_acquired_skill(self):
        self.assertEqual(get_skill_acquired_by_student(self.student_no_skills_acquired), 0)
