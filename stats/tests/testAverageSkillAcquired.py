import random

from django.test import TestCase
from django.utils import timezone

from promotions.models import Lesson, Stage
from skills.models import Skill, StudentSkill
from stats.utils import get_average_skill_acquired
from users.models import Student, User, Professor


class AverageSkillTest(TestCase):
    def setUp(self):

        students_list = []
        skills_list = []
        number_of_skills = 60
        number_of_student = 50

        count_skills_acquired = 0

        stage = Stage.objects.create(name="stage_name", short_name='sn', level=1)
        stage.save()

        self.lesson = Lesson.objects.create(name="LessonName", stage=stage)
        self.lesson.save()

        stage_no_skill = Stage.objects.create(name="LessonNoSkill", short_name="sns", level=2)
        stage_no_skill.save()

        stage_no_mastered = Stage.objects.create(name="stage", short_name="s", level=3)
        stage_no_mastered.save()

        self.lesson_empty_skill = Lesson.objects.create(name="lesson2", stage=stage_no_skill)
        self.lesson_empty_skill.save()

        self.lesson_no_student_mastered = Lesson.objects.create(name="hardLesson", stage=stage_no_mastered)
        self.lesson_no_student_mastered.save()

        self.lesson_no_student = Lesson.objects.create(name="LessonNoStudent", stage=stage_no_mastered)

        user = User.objects.create(username="prof")
        professor = Professor.objects.create(user=user)
        professor.save()

        self.lesson.professors.add(professor)
        self.lesson_no_student_mastered.professors.add(professor)

        for i in range(0, number_of_student):
            user = User.objects.create(username="testname" + str(i))
            student = Student.objects.create(user=user)
            student.save()
            self.lesson.students.add(student)
            self.lesson_empty_skill.students.add(student)
            self.lesson_no_student_mastered.students.add(student)
            students_list.append(student)

        for i in range(0, number_of_skills):
            gen_name = "skill" + str(i)
            skill = Skill.objects.create(code=gen_name, name=gen_name)
            skill_no = Skill.objects.create(code=gen_name + "v2", name=gen_name + "v2")
            skill.save()
            skill_no.save()
            stage.skills.add(skill)
            stage_no_mastered.skills.add(skill_no)
            skills_list.append(skill)

        random.seed()

        for student in students_list:
            for skill in skills_list:
                if random.randint(0, 1) == 1:
                    skill_student = StudentSkill.objects.create(student=student, skill=skill, acquired=timezone.now())
                    skill_student.save()
                    count_skills_acquired += 1

        self.avg_acquired_skills = (count_skills_acquired * 1.0) / number_of_student

    def test_when_acquired_skills(self):
        self.assertAlmostEqual(get_average_skill_acquired(self.lesson), self.avg_acquired_skills, delta=0.001)

    def test_when_no_skill_in_stage(self):
        self.assertEquals(get_average_skill_acquired(self.lesson_empty_skill), 0)

    def test_when_no_student_mastered_skills(self):
        self.assertEquals(get_average_skill_acquired(self.lesson_no_student_mastered), 0)

    def test_when_no_student_in_lesson(self):
        self.assertEquals(get_average_skill_acquired(self.lesson_no_student), None)
