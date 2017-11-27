from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from django.contrib.auth.models import User
from users.models import Professor
from selenium.webdriver.support.ui import Select

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import unittest
import time


class SuperUserUI(StaticLiveServerTestCase):
    def setUp(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk', "text/csv")

        self.selenium = webdriver.Firefox(profile)
        self.selenium.implicitly_wait(2)

        # Initialisation of
        user = User.objects.create_user(username='prof', password='prof', email='prof@prof.com')
        user.save()
        prof = Professor.objects.create(user=user, is_pending=False)
        prof.save()
        self.prof = prof

        super(SuperUserUI, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(SuperUserUI, self).tearDown()

    def test_login_stats_standard_csv_file(self):
        self.go_to_super_user_template()
        self.check_login_stats_datepicker()
        self.selenium.find_element_by_name("csv_export_button").click()

    def test_login_stats_predef_date_standard_csv_file(self):
        self.go_to_super_user_template()
        self.check_login_stats_predefdate()
        self.selenium.find_element_by_name("csv_export_button").click()

    def test_login_stats_european_csv_file(self):
        self.go_to_super_user_template()
        self.check_login_stats_datepicker()
        list = self.selenium.find_elements_by_name("csv_type")
        list[1].click()
        #self.selenium.find_element_by_xpath("//input[value='euro']").click()
        self.selenium.find_element_by_name("csv_export_button").click()

    def test_login_stats_empty_date_inputs(self):
        self.go_to_super_user_template()
        self.selenium.find_element_by_name("loginStats").click()
        self.selenium.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.selenium.find_element_by_name("csv_export_button").click()

    def test_login_stats_empty_champs(self):
        self.go_to_super_user_template()
        self.selenium.find_element_by_name("loginStats").click()
        self.selenium.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.selenium.find_element_by_name("csv_export_button").click()

    def test_resources_stats_date_standard_csv_file(self):
        self.go_to_super_user_template()
        self.check_resource_student_stats_datepicker()
        self.selenium.find_element_by_name("csv_export_button").click()

    def test_resources_stats_predef_date_standard_csv_file(self):
        self.go_to_super_user_template()
        self.check_resource_student_stats_predefdate()
        self.selenium.find_element_by_name("csv_export_button").click()

    def test_auth_stats_date_standard_csv_file(self):
        self.go_to_super_user_template()
        self.check_authentication_student_stats_datepicker()
        self.selenium.find_element_by_name("csv_export_button").click()

    def test_auth_stats_predef_date_standard_csv_file(self):
        self.go_to_super_user_template()
        self.check_authentication_student_stats_predefdate()
        self.selenium.find_element_by_name("csv_export_button").click()

    def test_exam_and_skill_stats_standard_csv_file(self):
        self.go_to_super_user_template()
        self.check_exam_student_stats()
        self.check_exam_skill_student_stats()
        self.selenium.find_element_by_name("csv_export_button").click()

    def testpredefined_dates(self):
        self.go_to_super_user_template()
        self.check_predefdate_valid()

####################################################################################################

    def check_login_stats_datepicker(self):
        self.selenium.find_element_by_name("loginStats").click()
        # check some user types
        self.selenium.find_element_by_name("professor").click()
        self.selenium.find_element_by_name("admin").click()

        self.selenium.execute_script("document.getElementById('startDateLS').valueAsDate = new Date('2017-11-01');")
        self.selenium.execute_script("document.getElementById('endDateLS').valueAsDate = new Date('2017-11-22');")

        time.sleep(2)

        # using the JavaScriptExecutor to scroll down to bottom of window
        self.selenium.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def check_resource_student_stats_datepicker(self):
        # using the JavaScriptExecutor to scroll down to center of window
        self.selenium.execute_script("window.scroll(0, (document.body.scrollHeight / 2) / 2);")

        self.selenium.find_element_by_name("resStudent").click()

        self.selenium.execute_script("document.getElementById('startDateRS').valueAsDate = new Date('2017-11-01');")
        self.selenium.execute_script("document.getElementById('endDateRS').valueAsDate = new Date('2017-11-22');")

        time.sleep(2)

        # using the JavaScriptExecutor to scroll down to bottom of window
        self.selenium.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def check_authentication_student_stats_datepicker(self):
        # using the JavaScriptExecutor to scroll down to center of window
        self.selenium.execute_script("window.scroll(0, (document.body.scrollHeight / 2) / 2);")

        self.selenium.find_element_by_name("authStudent").click()

        time.sleep(2)

        self.selenium.execute_script("document.getElementById('startDateAS').valueAsDate = new Date('2017-11-01');")
        self.selenium.execute_script("document.getElementById('endDateAS').valueAsDate = new Date('2017-11-22');")

        # using the JavaScriptExecutor to scroll down to bottom of window
        self.selenium.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def check_login_stats_predefdate(self):
        # login stats checkbox
        self.selenium.find_element_by_name("loginStats").click()
        # check some user types
        self.selenium.find_element_by_name("professor").click()
        self.selenium.find_element_by_name("admin").click()

        select = Select(self.selenium.find_element_by_name("preDefDateLS"))
        select.select_by_value('01/09/2016-31/12/2016')

        time.sleep(2)

        # using the JavaScriptExecutor to scroll down to bottom of window
        self.selenium.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def check_resource_student_stats_predefdate(self):
        # using the JavaScriptExecutor to scroll down to center of window
        self.selenium.execute_script("window.scroll(0, (document.body.scrollHeight / 2) / 2);")

        self.selenium.find_element_by_name("resStudent").click()

        select = Select(self.selenium.find_element_by_name("preDefDateRS"))
        select.select_by_value('01/09/2016-31/12/2016')

        time.sleep(2)

        # using the JavaScriptExecutor to scroll down to bottom of window
        self.selenium.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def check_authentication_student_stats_predefdate(self):
        # using the JavaScriptExecutor to scroll down to center of window
        self.selenium.execute_script("window.scroll(0, (document.body.scrollHeight / 2) / 2);")

        self.selenium.find_element_by_name("authStudent").click()

        time.sleep(2)

        select = Select(self.selenium.find_element_by_name("preDefDateAS"))
        select.select_by_value('01/09/2016-31/12/2016')

        time.sleep(2)

        # using the JavaScriptExecutor to scroll down to bottom of window
        self.selenium.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def check_exam_student_stats(self):
        # using the JavaScriptExecutor to scroll down to bottom of window
        self.selenium.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        self.selenium.find_element_by_name("examStudent").click()

        time.sleep(2)

    def check_exam_skill_student_stats(self):
        # using the JavaScriptExecutor to scroll down to bottom of window
        self.selenium.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        self.selenium.find_element_by_name("examStudentSkill").click()

        time.sleep(2)

    def check_predefdate_valid(self):
        # login stats checkbox
        self.selenium.find_element_by_name("loginStats").click()
        # check some user types
        self.selenium.find_element_by_name("professor").click()
        self.selenium.find_element_by_name("admin").click()

        select = Select(self.selenium.find_element_by_name("preDefDateLS"))
        for index in range(len(select.options)):
            select = Select(self.selenium.find_element_by_name('preDefDateLS'))
            select.select_by_index(index)
            dateString = select.first_selected_option.get_attribute("value")
            print(dateString)


        time.sleep(2)

        # using the JavaScriptExecutor to scroll down to bottom of window
        self.selenium.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def go_to_super_user_template(self):
        self.selenium.get("%s%s" % (self.live_server_url, "/accounts/usernamelogin/"))
        self.selenium.find_element_by_id("id_username").click()
        self.selenium.find_element_by_id("id_username").clear()
        self.selenium.find_element_by_id("id_username").send_keys("prof")
        self.selenium.find_element_by_css_selector("input.btn.btn-primary").click()
        self.selenium.find_element_by_id("id_password").click()
        self.selenium.find_element_by_id("id_password").clear()
        self.selenium.find_element_by_id("id_password").send_keys("prof")
        self.selenium.find_element_by_css_selector("input.btn.btn-primary").click()
        self.selenium.get(self.live_server_url + "/stats/superuser/")

if __name__ == "__main__":
    unittest.main()
