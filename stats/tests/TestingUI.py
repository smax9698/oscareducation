from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User

from selenium import webdriver

from users.models import Professor
from promotions.models import Lesson, Stage


class GeneralUITest(StaticLiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Firefox()
        self.selenium.implicitly_wait(10)
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
        self.selenium.find_element_by_link_text("Statistiques").click()
