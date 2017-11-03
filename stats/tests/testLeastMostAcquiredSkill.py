import random

from django.test import TestCase
from django.utils import timezone

from promotions.models import Stage, Lesson
from skills.models import Skill, StudentSkill
from stats.StatsObject import LeastMasteredSkill, MostMasteredSkill
from users.models import User, Student


class TestLeastSkillAcquired(TestCase):
    def setUp(self):
        number_of_student = 100
        number_of_skills = 100

        students_list = []
        students_list2 = []
        skills_list = []

        stage = Stage.objects.create(name="stage", short_name="s", level=1)
        stage_no_student_acquired_skills = Stage.objects.create(name="stage_nas", short_name="snas", level=1)
        stage_no_student_acquired_skills.save()
        stage.save()

        lesson = Lesson.objects.create(name="lesson", stage=stage)
        lesson_no_acquired_skill = Lesson.objects.create(name="lesson2", stage=stage_no_student_acquired_skills)
        lesson2 = Lesson.objects.create(name="lesson2", stage=stage)
        lesson.save()
        lesson_no_acquired_skill.save()
        lesson2.save()

        for i in range(0, number_of_student):
            user = User.objects.create(username="username" + str(i))
            user2 = User.objects.create(username="usernameV2" + str(i))
            student = Student.objects.create(user=user)
            student2 = Student.objects.create(user=user2)
            student.save()
            student2.save()
            lesson.students.add(student)
            lesson2.students.add(student2)
            students_list.append(student)
            students_list2.append(student2)

        for i in range(0, number_of_skills):
            gen_name = "skill" + str(i)
            gen_name2 = gen_name + "v2"
            skill = Skill.objects.create(code=gen_name, name=gen_name)
            skill2 = Skill.objects.create(code=gen_name2, name=gen_name2)
            skill.save()
            skill2.save()
            stage.skills.add(skill)
            stage_no_student_acquired_skills.skills.add(skill2)
            skills_list.append(skill)

        random.seed()

        max_skill, skill_obj_max = None, None
        min_skill, skill_obj_min = None, None

        max_skill2, skill_obj_max2 = None, None
        min_skill2, skill_obj_min2 = None, None

        for skill in skills_list:
            count, count2 = 0, 0
            for student in students_list:
                if random.randint(0, 1) == 1:
                    skill_student = StudentSkill.objects.create(student=student, skill=skill, acquired=timezone.now())
                    skill_student.save()
                    count += 1
            for student in students_list2:
                if random.randint(0, 1) == 1:
                    skill_student = StudentSkill.objects.create(student=student, skill=skill, acquired=timezone.now())
                    skill_student.save()
                    count2 += 1

            if max_skill is None or count > max_skill:
                max_skill = count
                skill_obj_max = skill
            if min_skill is None or count < min_skill:
                min_skill = count
                skill_obj_min = skill

            if max_skill2 is None or count2 > max_skill2:
                max_skill2 = count2
                skill_obj_max2 = skill
            if min_skill2 is None or count2 < min_skill2:
                min_skill2 = count2
                skill_obj_min2 = skill

        self.expected_min_skill = skill_obj_min
        self.expected_max_skill = skill_obj_max

        self.expected_min_skill_lesson2 = skill_obj_min2
        self.expected_max_skill_lesson2 = skill_obj_max2

        self.lesson = lesson
        self.lesson2 = lesson2
        self.lesson_no_acquired_skill = lesson_no_acquired_skill

    def test_least_skill_acquired(self):
        least_lesson1 = LeastMasteredSkill(self.lesson).data
        least_lesson2 = LeastMasteredSkill(self.lesson2).data
        self.assertEquals(least_lesson1, self.expected_min_skill)
        self.assertEquals(least_lesson2, self.expected_min_skill_lesson2)

    def test_most_skill_acquired(self):
        most_lesson1 = MostMasteredSkill(self.lesson).data
        most_lesson2 = MostMasteredSkill(self.lesson2).data
        self.assertEquals(most_lesson1, self.expected_max_skill)
        self.assertEquals(most_lesson2, self.expected_max_skill_lesson2)

    def test_when_no_skill_is_acquired_in_stage(self):
        most_none = MostMasteredSkill(self.lesson_no_acquired_skill).data
        least_none = LeastMasteredSkill(self.lesson_no_acquired_skill).data
        self.assertEquals(most_none, None)
        self.assertEquals(least_none, None)
