from django.test import TestCase
from skills.models import Skill, Section, CodeR
from stats.StatsObject import get_all_uaa_for_lesson, get_skills_for_uaa
from stats.utils import *
from promotions.models import Stage


class TestUAAFunctions(TestCase):
    def setUp(self):
        self.section1 = Section.objects.create(name="section one")
        self.section1.save()
        self.section2 = Section.objects.create(name="section two")
        self.section2.save()

        self.skill1 = Skill.objects.create(code="skill1", name="skill1")
        self.skill2 = Skill.objects.create(code="skill2", name="skill2")
        self.skill3 = Skill.objects.create(code="skill3", name="skill3")
        self.skill4 = Skill.objects.create(code="skill4", name="skill4")

        self.skill1.save()
        self.skill2.save()
        self.skill3.save()
        self.skill4.save()

        stage = Stage.objects.create(id='1', name="stage one", level=1)
        stage.save()
        stage.skills.add(self.skill1)
        stage.skills.add(self.skill2)
        stage.skills.add(self.skill3)
        stage.skills.add(self.skill4)

        self.lesson = Lesson.objects.create(name="lesson one", stage=stage)
        self.lesson.save()

        CodeR.objects.create(id='1', section=self.section1, name="uaa1", skill=[self.skill3, self.skill2, self.skill1])
        CodeR.objects.create(id='2', section=self.section2, name="uaa2", skill=[self.skill2])
        CodeR.objects.create(id='3', section=self.section2, name="uaa3", skill=[self.skill1])

    def test_get_all_UAA(self):
        self.assertEquals([self.section1, self.section2], get_all_uaa_for_lesson(self.lesson))

    def test_get_skills(self):
        self.assertEquals([self.skill1, self.skill2, self.skill3], get_skills_for_uaa(self.section1))
        self.assertEquals([self.skill1,self.skill2], get_skills_for_uaa(self.section2))



