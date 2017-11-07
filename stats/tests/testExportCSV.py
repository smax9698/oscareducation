from selenium.webdriver.support.select import Select

from TestingUI import GeneralUITest

class ButtonExportCSV(GeneralUITest):
    
    def test_csvfile_download_button_exists(self):
        self.go_to_stat_page()
        self.selenium.find_element_by_id("menu-toggle").click()
        self.assertTrue(self.selenium.find_element_by_name("csv_export_button").is_displayed())

   