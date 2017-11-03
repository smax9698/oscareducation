import datetime

from django.test import TestCase

from skills.models import Skill, StudentSkill
from stats.StatsObject import TimeBetweenTwoSkills
from users.models import Student, User


class TestTimeBetweenTwoSkills(TestCase):
    def setUp(self):
        self.skills = []

        user = User.objects.create(username="student1")
        user1 = User.objects.create(username="student2")
        self.student = Student.objects.create(user=user)
        self.student1 = Student.objects.create(user=user1)
        self.student.save()
        self.student1.save()

        for i in range(0, 4):
            gen_name = "skill" + str(i)

            skill = Skill.objects.create(code=gen_name, name=gen_name)
            skill.save()
            self.skills.append(skill)

        self.skill_student = StudentSkill.objects.create(student=self.student, skill=self.skills[0],
                                                         acquired=datetime.date(2016, 3, 13))
        self.skill_student.save()

        self.skill_student1 = StudentSkill.objects.create(student=self.student, skill=self.skills[1],
                                                          acquired=datetime.date(2015, 4, 23))
        self.skill_student1.save()

        self.skill_student2 = StudentSkill.objects.create(student=self.student, skill=self.skills[2],
                                                          acquired=datetime.date(2010, 10, 27))
        self.skill_student2.save()

        self.skill_student3 = StudentSkill.objects.create(student=self.student, skill=self.skills[3],
                                                          acquired=datetime.date(2017, 6, 27))
        self.skill_student3.save()

        self.diff1 = datetime.date(2017, 6, 27) - datetime.date(2016, 3, 13)
        self.diff2 = datetime.date(2016, 3, 13) - datetime.date(2015, 4, 23)
        self.diff3 = datetime.date(2015, 4, 23) - datetime.date(2010, 10, 27)

    def test_time_between_two_skills(self):
        time = TimeBetweenTwoSkills(self.student)
        self.assertEquals(time.data[str(self.skill_student2)], 0)
        self.assertEquals(time.data[str(self.skill_student1)], self.diff3)
        self.assertEquals(time.data[str(self.skill_student)], self.diff2)
        self.assertEquals(time.data[str(self.skill_student3)], self.diff1)

    def test_no_skills_acquired(self):
        time = TimeBetweenTwoSkills(self.student1)
        self.assertEquals(time.data, {})
