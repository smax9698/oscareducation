import random

from django.test import TestCase
from django.utils import timezone

from promotions.models import Stage, Lesson
from skills.models import Skill, StudentSkill
from stats.utils import least_mastered_skill, most_mastered_skill
from users.models import User, Student


class TestLeastSkillAcquired(TestCase):
    def setUp(self):
        number_of_student = 100
        number_of_skills = 71

        students_list = []
        skills_list = []

        stage = Stage.objects.create(name="stage", short_name="s", level=1)
        stage.save()

        lesson = Lesson.objects.create(name="lesson", stage=stage)
        lesson.save()

        for i in range(0, number_of_student):
            user = User.objects.create(username="username" + str(i))
            student = Student.objects.create(user=user)
            student.save()
            lesson.students.add(student)
            students_list.append(student)

        for i in range(0, number_of_skills):
            gen_name = "skill" + str(i)
            skill = Skill.objects.create(code=gen_name, name=gen_name)
            skill.save()
            stage.skills.add(skill)
            skills_list.append(skill)

        random.seed()

        max_skill, skill_obj_max = None, None
        min_skill, skill_obj_min = None, None

        for skill in skills_list:
            count = 0
            for student in students_list:
                if random.randint(0, 1) == 1:
                    skill_student = StudentSkill.objects.create(student=student, skill=skill, acquired=timezone.now())
                    skill_student.save()
                    count += 1

            if max_skill is None or count > max_skill:
                max_skill = count
                skill_obj_max = skill
            if min_skill is None or count < min_skill:
                min_skill = count
                skill_obj_min = skill

        self.expected_min_skill = skill_obj_min
        self.expected_max_skill = skill_obj_max
        self.lesson = lesson

    def test_least_skill_acquired(self):
        self.assertEquals(least_mastered_skill(self.lesson, lambda: True), self.expected_min_skill)

    def test_most_skill_acquired(self):
        self.assertEquals(most_mastered_skill(self.lesson, lambda: True), self.expected_max_skill)
