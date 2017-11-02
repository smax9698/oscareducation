import datetime

import pytz
from django.test import TestCase
from django.utils import timezone

from promotions.models import Stage, Lesson
from skills.models import Skill, StudentSkill
from stats.utils import get_latest_skill_acquired
from users.models import User, Student


class TestLatestSkillAcquired(TestCase):
    def setUp(self):
        user = User.objects.create(username="username")
        self.student1 = Student.objects.create(user=user)

        user2 = User.objects.create(username="username2")
        self.student2 = Student.objects.create(user=user2)

        user3 = User.objects.create(username="user_3")
        self.student3 = Student.objects.create(user=user3)

        self.student1.save()
        self.student2.save()
        self.student3.save()

        stage = Stage.objects.create(name="stage_name", short_name='sn', level=1)
        stage2 = Stage.objects.create(name="stage_name2", short_name='sn2', level=1)

        stage.save()
        stage2.save()

        self.lesson1 = Lesson.objects.create(name="my_lesson", stage=stage)
        self.lesson2 = Lesson.objects.create(name="my_lesson2", stage=stage2)

        self.lesson1.save()
        self.lesson2.save()

        self.lesson1.students.add(self.student1)
        self.lesson2.students.add(self.student2)

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

        stage2.skills.add(skill1)
        stage2.skills.add(skill2)
        stage2.skills.add(skill3)
        stage2.skills.add(skill4)

        student_skill1 = StudentSkill.objects.create(student=self.student1, skill=skill1,
                                                     acquired=datetime.datetime(2016, 11, 12, tzinfo=pytz.utc))
        student_skill2 = StudentSkill.objects.create(student=self.student1, skill=skill2,
                                                     acquired=datetime.datetime(2016, 11, 29, 5, 32, 24, 2236,
                                                                                tzinfo=pytz.utc))
        student_skill3 = StudentSkill.objects.create(student=self.student1, skill=skill3,
                                                     acquired=datetime.datetime(2016, 11, 29, 5, 32, 23, 2235,
                                                                                tzinfo=pytz.utc))
        student_skill4 = StudentSkill.objects.create(student=self.student1, skill=skill4,
                                                     acquired=datetime.date(2016, 11, 28))

        student2_skill1 = StudentSkill.objects.create(student=self.student2, skill=skill1,
                                                      acquired=datetime.datetime(2016, 11, 11, 11, 11, 11, 1112,
                                                                                 tzinfo=pytz.utc))
        student2_skill2 = StudentSkill.objects.create(student=self.student2, skill=skill2,
                                                      acquired=datetime.datetime(2016, 11, 11, 11, 11, 11, 1111,
                                                                                 tzinfo=pytz.utc))
        student2_skill3 = StudentSkill.objects.create(student=self.student2, skill=skill3,
                                                      acquired=datetime.datetime(2016, 11, 10, tzinfo=pytz.utc))
        student2_skill4 = StudentSkill.objects.create(student=self.student2, skill=skill4,
                                                      acquired=datetime.datetime(2016, 11, 9, tzinfo=pytz.utc))

        student_skill1.save()
        student_skill2.save()
        student_skill3.save()
        student_skill4.save()

        student2_skill1.save()
        student2_skill2.save()
        student2_skill3.save()
        student2_skill4.save()

        self.expected_latest_skill_student1 = skill2
        self.expected_latest_skill_student2 = skill1

        old_stage_student = Stage.object.create(name="old_stage", short_name="os", level=1)

        for i in range(0, 20):
            skill = Skill.objects.create(code="code" + str(i), name="name" + str(i))
            skill.save()
            old_stage_student.skills.add(skill)
            skill_student = StudentSkill.objects.create(student=self.student1, skill=skill,
                                                        acquired=timezone.now())
            skill_student2 = StudentSkill.objects.create(student=self.student2, skill=skill,
                                                         acquired=timezone.now())
            skill_student.save()
            skill_student2.save()

    def test_correct_skill_queried(self):
        self.assertEquals(get_latest_skill_acquired(self.student1, self.lesson1), self.expected_latest_skill_student1)
        self.assertEquals(get_latest_skill_acquired(self.student2, self.lesson2), self.expected_latest_skill_student2)

    def test_when_no_skills_acquired(self):
        self.assertEquals(get_latest_skill_acquired(self.student3, self.lesson2), None)
        self.assertEquals(get_latest_skill_acquired(self.student3, self.lesson1), None)
