# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# -*- coding: utf-8 -*-
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re


class TestAdmin(LiveServerTestCase):

    STUDENT_USERNAME = "student.student"
    STUDENT_PASSWORD = "student"

    PROFESSOR_USERNAME = "prof"
    PROFESSOR_PASSWORD = "prof"

    ADMIN_USERNAME = "test"
    ADMIN_PASSWORD = "test"

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(300)
        self.base_url = "http://127.0.0.1:8000"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_admin1(self):
        """ As an administrator, I want to change the ordering of the criteria used to order the skills.\\
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

    def test_student(self):
        """As a student, I can see a detail view of my learning track. """
        driver = self.driver
        driver.get(self.base_url + "/accounts/usernamelogin/")
        driver.find_element_by_id("djHideToolBarButton").click()
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys(self.STUDENT_USERNAME)
        driver.find_element_by_css_selector("input.btn.btn-primary").click()
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys(self.STUDENT_PASSWORD)
        driver.find_element_by_css_selector("input.btn.btn-primary").click()
        driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
        time.sleep(5)
        driver.find_element_by_css_selector("button.close").click()
        driver.find_element_by_css_selector("a.icon.logout").click()

    def test_prof(self):
        driver = self.driver
        driver.get(self.base_url + "/accounts/usernamelogin/")
        driver.find_element_by_id("djHideToolBarButton").click()
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys(self.PROFESSOR_USERNAME)
        driver.find_element_by_css_selector("input.btn.btn-primary").click()
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys(self.PROFESSOR_PASSWORD)
        driver.find_element_by_css_selector("input.btn.btn-primary").click()
        driver.find_element_by_css_selector("a.icon.logout").click()

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
