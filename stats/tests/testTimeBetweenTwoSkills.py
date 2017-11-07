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

        diff1 = datetime.date(2017, 6, 27) - datetime.date(2016, 3, 13)
        self.result = diff1.days * 24 + (diff1.seconds / 3600)
        diff2 = datetime.date(2016, 3, 13) - datetime.date(2015, 4, 23)
        self.result1 = diff2.days * 24 + (diff2.seconds / 3600)
        diff3 = datetime.date(2015, 4, 23) - datetime.date(2010, 10, 27)
        self.result2 = diff3.days * 24 + (diff3.seconds / 3600)

    def test_time_between_two_skills(self):
        time = TimeBetweenTwoSkills(self.student)
        self.assertEquals(time.data[str(self.skill_student2.skill).split(' ')[0]], 0)
        self.assertEquals(time.data[str(self.skill_student1.skill).split(' ')[0]], self.result2)
        self.assertEquals(time.data[str(self.skill_student.skill).split(' ')[0]], self.result1)
        self.assertEquals(time.data[str(self.skill_student3.skill).split(' ')[0]], self.result)

    def test_no_skills_acquired(self):
        time = TimeBetweenTwoSkills(self.student1)
        self.assertEquals(time.data, {})
