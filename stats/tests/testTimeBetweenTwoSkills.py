import datetime

from django.test import TestCase

from skills.models import Skill, StudentSkill
from stats.utils import time_between_two_skills, time_between_two_last_skills
from users.models import Student, User


class TimeBetweenTwoSkills(TestCase):
    def setUp(self):
        self.skills = []
        self.diff_last = datetime.date(2017, 6, 27) - datetime.date(2016, 3, 13)
        self.diff = datetime.date(2015, 6, 13) - datetime.date(2010, 10, 27)

        user = User.objects.create(username="student1")
        self.student = Student.objects.create(user=user)
        self.student.save()

        for i in range(0, 4):
            gen_name = "skill" + str(i)

            skill = Skill.objects.create(code=gen_name, name=gen_name)
            skill.save()
            self.skills.append(skill)

        skill_student = StudentSkill.objects.create(student=self.student, skill=self.skills[0],
                                                    acquired=datetime.date(2016, 3, 13))
        skill_student.save()

        skill_student1 = StudentSkill.objects.create(student=self.student, skill=self.skills[1],
                                                     acquired=datetime.date(2015, 6, 13))
        skill_student1.save()

        skill_student2 = StudentSkill.objects.create(student=self.student, skill=self.skills[2],
                                                     acquired=datetime.date(2010, 10, 27))
        skill_student2.save()

        skill_student3 = StudentSkill.objects.create(student=self.student, skill=self.skills[3],
                                                     acquired=datetime.date(2017, 6, 27))
        skill_student3.save()

    def test_between_two_skills(self):
        self.assertEquals(time_between_two_skills(self.student, self.skills[1], self.skills[2]), self.diff)

    def test_between_two_last_skills(self):
        self.assertEquals(time_between_two_last_skills(self.student), self.diff_last)
