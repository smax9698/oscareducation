# coding=utf-8
from TestingUI import GeneralUITest
import time


class TestReloadGraph(GeneralUITest):

    def test_graph_click(self):
        student = self.student_list[0].user
        self.go_to_stat_page()
        self.selenium.find_element_by_id(student.username).click()
        self.assertEquals(self.selenium.find_element_by_id("last_name").text, "Nom : "+student.last_name)
        self.assertEquals(self.selenium.find_element_by_id("first_name").text, u"Prénom : "+student.first_name)
        self.assertEquals(self.selenium.find_element_by_id("email").text, "Email : "+student.email)
        self.tearDown()

    def test_change_uaa(self):
        self.go_to_stat_page()  # go to professor page in class "Test"
        self.selenium.find_element_by_id(self.student_list[0].user.username).click()  # click on the graph of the first student
        self.selenium.find_element_by_xpath("//div[@id='page-content-wrapper']/div/div/div/div[2]/div/span").click() # UAA dropdrown
        self.tearDown()

    def test_change_student(self):
        student = self.student_list[1].user
        self.go_to_stat_page()
        self.selenium.find_element_by_id(self.student_list[0].user.username).click()
        self.selenium.find_element_by_id("student_choice").click()  # Student dropdown
        for i in range(0, len(self.student_list)):
            self.selenium.find_element_by_id(self.student_list[i].user.username).is_displayed()
        self.selenium.find_element_by_id(student.username).click()

        time.sleep(2)

        self.assertEquals(self.selenium.find_element_by_id("last_name").text, "Nom : "+student.last_name)
        self.assertEquals(self.selenium.find_element_by_id("first_name").text, u"Prénom : "+student.first_name)
        self.assertEquals(self.selenium.find_element_by_id("email").text, "Email : "+student.email)
        self.tearDown()

