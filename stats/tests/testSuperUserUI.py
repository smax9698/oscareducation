from TestingUI import GeneralUITest


class SuperUserUI(GeneralUITest):
    def test_get_standard_csv_file(self):
        self.check_login_stats()
        self.selenium.find_element_by_name("csv_export_button").click()

    def test_get_european_csv_file(self):
        self.check_login_stats()
        self.selenium.find_element_by_xpath("//input[value='euro']").click()
        self.selenium.find_element_by_name("csv_export_button").click()

    def check_login_stats(self):
        self.go_to_super_user_template()
        # login stats checkbox
        self.selenium.find_element_by_name("loginStats").click()
        # check some user types
        self.selenium.find_element_by_name("professor").click()
        self.selenium.find_element_by_name("admin").click()
        self.selenium.find_element_by_name('startDateLS').send_keys('01/11/2017')

    def go_to_super_user_template(self):
        #it's necessary to login as professor
        self.selenium.get("%s%s" % (self.live_server_url, "/accounts/usernamelogin/"))
        self.selenium.find_element_by_id("id_username").click()
        self.selenium.find_element_by_id("id_username").clear()
        self.selenium.find_element_by_id("id_username").send_keys("prof")
        self.selenium.find_element_by_css_selector("input.btn.btn-primary").click()
        self.selenium.find_element_by_id("id_password").click()
        self.selenium.find_element_by_id("id_password").clear()
        self.selenium.find_element_by_id("id_password").send_keys("prof")
        self.selenium.find_element_by_css_selector("input.btn.btn-primary").click()
        self.selenium.get("%s%s" % (self.live_server_url, "/stats/superuser/"))
