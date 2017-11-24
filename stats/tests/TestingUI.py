import random
import datetime

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils import timezone
from selenium import webdriver

from examinations.models import Test, TestStudent, BaseTest
from promotions.models import Lesson, Stage
from skills.models import Skill, StudentSkill, Section, CodeR
from stats.models import ExamStudent, ExamStudentSkill
from users.models import Professor, Student


class GeneralUITest(StaticLiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Firefox()
        self.selenium.implicitly_wait(2)

        # Creation of the professor and setting up the database
        user = User.objects.create_user(username='prof', password='prof', email='prof@prof.com')
        user.save()
        prof = Professor.objects.create(user=user, is_pending=False)
        prof.save()
        self.prof = prof
        # Creating a class
        stage = Stage(name="test stage", level=1)
        stage.save()
        lesson = Lesson(name="Test", stage=stage)
        lesson.save()
        lesson.professors.add(prof)
        lesson.save()

        section = Section.objects.create(name="section")
        section.save()
        lesson.current_uaa = section.name
        lesson.save()

        skill_list = []
        self.student_list = []
        base_test_list = []
        self.codeR_list = []

        for i in range(0, 6):
            codeR = CodeR.objects.create(section=section, sub_code="UA"+str(i), name="name"+str(i))
            codeR.save()
            self.codeR_list.append(codeR)

        for i in range(0, 5):  # [0; 4[
            user = User.objects.create_user(username="student"+str(i))
            user.first_name = "student" + str(i)
            user.last_name = str(i) + "tneduts"
            user.email = "xxx_student" + str(i) + "_xxx@example.com"
            user.save()
            student = Student.objects.create(user=user)
            student.save()
            self.student_list.append(student)

        for i in range(0, 100):
            gen_name = "skill" + str(i)
            skill = Skill.objects.create(code=gen_name, name=gen_name)
            skill.save()
            stage.skills.add(skill)
            skill_list.append(skill)

        for i in range(0, 100):
            base_test = Test.objects.create(name="btest"+str(i), lesson=lesson, type="skills")
            base_test.save()
            base_test_list.append(base_test)

        random.seed()

        for skill in skill_list:
            for codeR in self.codeR_list:
                if random.randint(0,1) == 1:
                    codeR.skill.add(skill)

        for base_test in base_test_list:
            for skill in skill_list:
                if random.randint(0,1) == 1:
                    base_test.skills.add(skill)

        for skill in skill_list:
            for student in self.student_list:
                if random.randint(0, 1) == 1:
                    skill_student = StudentSkill.objects.create(student=student, skill=skill, acquired=timezone.now())
                    skill_student.save()

        for student in self.student_list:
            for base_test in base_test_list:
                if random.randint(0, 1) == 0:
                    test_student = TestStudent.objects.create(student=student, finished=True, test=base_test, started_at= timezone.now(), finished_at = timezone.now())
                    test_student.save()

        for student in self.student_list:
            lesson.students.add(student)

        super(GeneralUITest, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(GeneralUITest, self).tearDown()

    def go_to_stat_page(self):
        self.selenium.get("%s%s" % (self.live_server_url, "/accounts/usernamelogin/"))
        self.selenium.find_element_by_id("id_username").click()
        self.selenium.find_element_by_id("id_username").clear()
        self.selenium.find_element_by_id("id_username").send_keys("prof")
        self.selenium.find_element_by_css_selector("input.btn.btn-primary").click()
        self.selenium.find_element_by_id("id_password").click()
        self.selenium.find_element_by_id("id_password").clear()
        self.selenium.find_element_by_id("id_password").send_keys("prof")
        self.selenium.find_element_by_css_selector("input.btn.btn-primary").click()
        self.selenium.find_element_by_link_text("Test").click()
