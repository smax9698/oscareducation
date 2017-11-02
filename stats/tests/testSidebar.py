from TestingUI import GeneralUITest

from selenium.webdriver.support.select import Select


class ButtonShowSidebar(GeneralUITest):

    def test_no_visible_on_start(self):
        self.go_to_stat_page()
        self.assertFalse(self.selenium.find_element_by_id('sidebar-wrapper').is_displayed())

    def test_visible_when_click(self):
        self.go_to_stat_page()
        self.selenium.find_element_by_id("menu-toggle").click()
        self.assertTrue(self.selenium.find_element_by_id('sidebar-wrapper').is_enabled())

    def test_no_visible_when_double_click(self):
        self.go_to_stat_page()
        button = self.selenium.find_element_by_id("menu-toggle")
        button.click()
        button.click()
        self.assertFalse(self.selenium.find_element_by_id('sidebar-wrapper').is_displayed())


class SelectTimespanChangeInput(GeneralUITest):

    def test_input_correct_after_selection(self):
        self.go_to_stat_page()
        self.selenium.find_element_by_id("menu-toggle").click()
        option = self.selenium.find_element_by_xpath("//select[@id='select_timespan']//option[2]")
        option.click()
        bound = option.get_attribute("value").split("-")
        start = bound[0]
        end = bound[1]
        self.assertEqual(self.selenium.find_element_by_id("startDate").get_attribute("value"), start)
        self.assertEqual(self.selenium.find_element_by_id("endDate").get_attribute("value"), end)

    def test_input_none_does_not_change(self):
        self.go_to_stat_page()
        self.selenium.find_element_by_id("menu-toggle").click()
        select = Select(self.selenium.find_element_by_id('select_timespan'))
        option = self.selenium.find_element_by_xpath("//select[@id='select_timespan']//option[2]")
        if not option.is_selected():
            option.click()
        else:
            option = self.selenium.find_element_by_xpath("//select[@id='select_timespan']//option[1]")
            option.click()
        bound = option.get_attribute("value").split("-")
        start = bound[0]
        end = bound[1]
        select.select_by_value("None")
        self.assertEqual(self.selenium.find_element_by_id("startDate").get_attribute("value"), start)
        self.assertEqual(self.selenium.find_element_by_id("endDate").get_attribute("value"), end)


