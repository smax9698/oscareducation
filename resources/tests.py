# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# -*- coding: utf-8 -*-
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestAdmin(LiveServerTestCase):

    STUDENT_USERNAME = "test27"
    STUDENT_PASSWORD = "test27"

    PROFESSOR_USERNAME = "prof"
    PROFESSOR_PASSWORD = "prof"

    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "admin"

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
        self.base_url = "http://127.0.0.1:8000"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_admin1(self):
        """ As an administrator, I want to change the ordering of the criteria used to order the skills.
        """
        driver = self.driver
        driver.get(self.base_url + "/admin/login/?next=/admin/")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys(self.ADMIN_PASSWORD)
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys(self.ADMIN_USERNAME)
        driver.find_element_by_id("djHideToolBarButton").click()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("(//a[contains(text(),'Modifier')])[10]").click()
        driver.find_element_by_link_text("Ajouter professor criteria").click()
        Select(driver.find_element_by_id("id_criteria")).select_by_visible_text("Group")
        driver.find_element_by_id("id_order").clear()
        driver.find_element_by_id("id_order").send_keys("1")
        Select(driver.find_element_by_id("id_professor")).select_by_visible_text("prof")
        driver.find_element_by_name("_save").click()
        driver.find_element_by_link_text("Ajouter professor criteria").click()
        Select(driver.find_element_by_id("id_professor")).select_by_visible_text("prof")
        Select(driver.find_element_by_id("id_criteria")).select_by_visible_text("Time")
        driver.find_element_by_id("id_order").clear()
        driver.find_element_by_id("id_order").send_keys("1")
        driver.find_element_by_id("id_order").clear()
        driver.find_element_by_id("id_order").send_keys("2")
        driver.find_element_by_name("_save").click()
        driver.find_element_by_link_text("Ajouter professor criteria").click()
        Select(driver.find_element_by_id("id_professor")).select_by_visible_text("prof")
        Select(driver.find_element_by_id("id_criteria")).select_by_visible_text("Level")
        driver.find_element_by_id("id_order").clear()
        driver.find_element_by_id("id_order").send_keys("1")
        driver.find_element_by_id("id_order").clear()
        driver.find_element_by_id("id_order").send_keys("2")
        driver.find_element_by_id("id_order").clear()
        driver.find_element_by_id("id_order").send_keys("3")
        driver.find_element_by_name("_save").click()
        driver.find_element_by_link_text(u"Déconnexion").click()

    def test_admin2(self):
        """As an administrator, I want to update the ordering of the criteria
        """
        driver = self.driver
        driver.get(self.base_url + "/admin/login/?next=/admin/")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys(self.ADMIN_PASSWORD)
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys(self.ADMIN_USERNAME)
        driver.find_element_by_id("djHideToolBarButton").click()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("(//a[contains(text(),'Modifier')])[10]").click()
        driver.find_element_by_css_selector("tr.row2 > td.action-checkbox > input[name=\"_selected_action\"]").click()
        driver.find_element_by_xpath("(//input[@name='_selected_action'])[3]").click()
        Select(driver.find_element_by_name("action")).select_by_visible_text(
            u"Supprimer les professor criterias sélectionnés")
        driver.find_element_by_name("index").click()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_link_text("Ajouter professor criteria").click()
        Select(driver.find_element_by_id("id_professor")).select_by_visible_text("prof")
        Select(driver.find_element_by_id("id_criteria")).select_by_visible_text("Time")
        driver.find_element_by_id("id_order").clear()
        driver.find_element_by_id("id_order").send_keys("1")
        driver.find_element_by_id("id_order").clear()
        driver.find_element_by_id("id_order").send_keys("2")
        driver.find_element_by_id("id_order").clear()
        driver.find_element_by_id("id_order").send_keys("3")
        driver.find_element_by_name("_save").click()
        driver.find_element_by_link_text("Ajouter professor criteria").click()
        Select(driver.find_element_by_id("id_professor")).select_by_visible_text("prof")
        Select(driver.find_element_by_id("id_criteria")).select_by_visible_text("Level")
        driver.find_element_by_id("id_order").clear()
        driver.find_element_by_id("id_order").send_keys("1")
        driver.find_element_by_id("id_order").clear()
        driver.find_element_by_id("id_order").send_keys("2")
        driver.find_element_by_name("_save").click()
        driver.find_element_by_link_text(u"Déconnexion").click()

    def test_admin3(self):
        """As an administrator, I want to delete my ordering of the criteria and then have the default ordering criteria
        """
        driver = self.driver
        driver.get(self.base_url + "/admin/login/?next=/admin/")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys(self.ADMIN_PASSWORD)
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys(self.ADMIN_USERNAME)
        driver.find_element_by_id("djHideToolBarButton").click()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_xpath("(//a[contains(text(),'Modifier')])[10]").click()
        driver.find_element_by_name("_selected_action").click()
        driver.find_element_by_css_selector("tr.row2 > td.action-checkbox > input[name=\"_selected_action\"]").click()
        driver.find_element_by_xpath("(//input[@name='_selected_action'])[3]").click()
        Select(driver.find_element_by_name("action")).select_by_visible_text(
            u"Supprimer les professor criterias sélectionnés")
        driver.find_element_by_name("index").click()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_link_text(u"Déconnexion").click()

    def test_prof1(self):
        ''' As a professor, I want to assign target skills to a student '''
        self.create_learning_track()
        self.exit()

    def test_prof2(self):
        ''' As a professor, I want to modify the learning track that has been generated '''
        self.create_learning_track()
        self.switch_skills()
        self.exit()

    def test_student1(self):
        '''As a student, I want to see my recommended skills'''
        driver = self.driver
        self.access_student_page()

    def test_student2(self):
        """As a student, I can see a detailed view of my learning track. """
        driver = self.driver
        self.access_student_page()
        driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
        time.sleep(5)
        driver.find_element_by_css_selector("button.close").click()
        driver.find_element_by_css_selector("a.icon.logout").click()

    def create_student_in_hankar(self):
        ''' Create a new student in the class named Hankar. The current page must be the Hanker class detail'''
        driver = self.driver
        name = "%s %s"%(self.STUDENT_USERNAME, self.STUDENT_PASSWORD)

        #Check if the test student is already present
        try:
            driver.find_element_by_link_text(name)
        except NoSuchElementException:
            pass
        else:
            return False

        #Fill the form to add a new student
        driver.get(self.base_url + "/professor/lesson/134/")
        driver.find_element_by_xpath("//div[@id='students']/div[2]/div[2]/a[2]/img").click()
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.find_element_by_xpath("(//button[@type='button'])[3]").click()
        driver.find_element_by_id("id_first_name").clear()
        driver.find_element_by_id("id_first_name").send_keys(self.STUDENT_USERNAME)
        driver.find_element_by_id("id_last_name").clear()
        driver.find_element_by_id("id_last_name").send_keys(self.STUDENT_PASSWORD)
        driver.find_element_by_css_selector("form[name=\"manual_add\"] > div.form-group > button.btn.btn-primary").click()
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        link = driver.find_element_by_link_text("%s %s"%(self.STUDENT_USERNAME, self.STUDENT_PASSWORD)).get_attribute('href')
        link = link.replace('student','students_password_page')

        #Generate and get the code of the new student
        driver.get(link)
        elem = driver.find_element_by_xpath(".//td[3]")
        code = elem.text[-4:]

        driver.get(self.base_url + "/professor/dashboard/")
        time.sleep(1)
        driver.find_element_by_css_selector("a.icon.logout").click()
        driver.find_element_by_css_selector("a.icon.logout").click()

        # Log in as the new student with the stored code
        driver.get(self.base_url + "/accounts/usernamelogin/")
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys("%s.%s"%(self.STUDENT_USERNAME,self.STUDENT_PASSWORD))
        time.sleep(1)
        driver.find_element_by_css_selector("input.btn.btn-primary").click()
        time.sleep(5)
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys(code)
        driver.find_element_by_css_selector("input.btn.btn-primary").click()
        time.sleep(1)
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys(self.STUDENT_PASSWORD)
        driver.find_element_by_name("confirmed_password").clear()
        driver.find_element_by_name("confirmed_password").send_keys(self.STUDENT_PASSWORD)
        driver.find_element_by_css_selector("input.btn.btn-primary").click()
        time.sleep(1)
        driver.find_element_by_css_selector("a.icon.logout").click()
        return True

    def go_to_hankar_class(self):
        ''' Open the browser and go to the Hankar class detail page'''
        driver = self.driver
        driver.get(self.base_url + "/accounts/usernamelogin/")
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys(self.PROFESSOR_USERNAME)
        driver.find_element_by_css_selector("input.btn.btn-primary").click()
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys(self.PROFESSOR_PASSWORD)
        driver.find_element_by_css_selector("input.btn.btn-primary").click()
        driver.find_element_by_class_name("list-group-item").click()

    def create_learning_track(self):
        '''Create a learning track for a student'''
        driver = self.driver

        self.go_to_hankar_class()
        time.sleep(1)

        '''Only create the student if it doesn't already exists'''
        if self.create_student_in_hankar():
            time.sleep(5)
            self.go_to_hankar_class()
            time.sleep(5)

        '''Go to the students targets skills interface'''
        driver.find_element_by_css_selector("a[href*='list_student_target']").click()

        name = "%s %s"%(self.STUDENT_USERNAME, self.STUDENT_PASSWORD)

        '''Assign targets as skill to the student'''
        element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, ".//a[text()='%s']/../input"%(name))))
        driver.execute_script("return arguments[0].scrollIntoView();", element)
        ActionChains(driver).move_to_element(element).perform()
        time.sleep(2)
        element.click()
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        Select(driver.find_element_by_xpath("//select")).select_by_visible_text(u"S13d - Utiliser la soustraction comme la réciproque de l'addition et la division comme la réciproque de la multiplication")
        driver.find_element_by_id("addSkillToTestButtonForStage9").click()
        Select(driver.find_element_by_xpath("//select")).select_by_visible_text(u"S13g - Choisir et utiliser avec pertinence le calcul mental, le calcul écrit ou la calculatrice en fonction de la situation.")
        driver.find_element_by_id("addSkillToTestButtonForStage9").click()
        driver.find_element_by_id("setTargetButton").click()

    def switch_skills(self):
        '''Drag and drop feature for a professor to modify a learning track'''
        driver = self.driver
        source_element = driver.find_element_by_xpath(".//*[@class = 'ui-sortable-handle' ][1]")
        dest_element = driver.find_element_by_xpath(".//*[@class = 'ui-sortable-handle' ][3]")
        ActionChains(driver).drag_and_drop(source_element, dest_element).perform()

    def access_studyesent_page(self):
        '''Log in as student'''
        driver = self.driver
        driver.get(self.base_url + "/accounts/usernamelogin/")
        name = "%s.%s" % (self.STUDENT_USERNAME, self.STUDENT_PASSWORD)
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys(name)
        driver.find_element_by_css_selector("input.btn.btn-primary").click()
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys(self.STUDENT_PASSWORD)
        driver.find_element_by_css_selector("input.btn.btn-primary").click()

    def exit(self):
        '''Exit the application once the learning track is created'''
        self.driver.find_element_by_id("finish").click()
        self.driver.find_element_by_css_selector("a.icon.logout").click()

    def is_element_present(self, how, what):
        '''Check if a specific element is present on the current page'''
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
