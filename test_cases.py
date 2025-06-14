#################### test_cases.py ####################

from selenium.webdriver.common.by import By
from tests_base import BaseForTests
from tests_base import Vini
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
from vcsv import CSVData
from time import sleep

# _test00x(self, test_number, section)
# - checks if url defined in *.ini file under [section] can be opened
# - url can be defined directly or with connector (locator) from [MAIN_PAGE]
# - confirmation if url is opened is defined under [section] too 
# - conformation method is one of: [locator, title, alert, locator.text] with parameter1 and optional parameter2
#
# _test10x(self,csv_line_number)
# - tests login subpage defined under [LOGIN_PAGE_SECTION]
# - login options are defined in "login_page_data.csv" in line number "csv_line_number"
# - expected behavior for data entered is also defined in "login_page data.csv"
# - reaction is one of: [locator, title, alert, locator.text] with parameter1 and optional parameter2
#
# _test15x(self,csv_line_number)
# - tests new user registration defined under [NEW_USER_PAGE_SECTION]
# - options for new user are defined in "new_user_page_data.csv" in line number "csv_line_number"
# - expected behavior for data entered is also defined in "new_user_page_data.csv"
# - reaction is one of: [locator, title, alert, locator.text] with parameter1 and optional parameter2
#
# test000(self)..test003(self)
# - tests main page and subpages using _test00x()
# 
# test100(self):..test104(self)
# - tests various login combinations with _test10x()
# 
# test150(self):..test154(self)
# - tests various new user combinations with _test15x()
#
# allow_test(self, testnumber)
# - return True if test with testnumber should be skipped for faster debuggin
# 


MAIN_PAGE_SECTION = 'main_page'
LOGIN_PAGE_SECTION = 'login_page'
NEW_USER_PAGE_SECTION = 'new_user_page'
MAIN_PAGE_SECTION_OPEN_ERROR = "can't open main_page"
CART_PAGE_SECTION = 'cart_page'

class TestCases(BaseForTests):

    def allow_test(self, testnumber):
        decision = self.inifilevalue.read_boolean_from_ini("tests2run", "test" + f"{testnumber}")
        if not decision:
            self.log("canceling test #" + f"{testnumber}" )
            return False
        else:
            self.log("running test #" + f"{testnumber}")
            return True

    def _test00x(self, test_number, section):
        if not self.allow_test(test_number): return
        url = self.inifilevalue.read_string_from_ini(section, 'url')
        if url != "":
            self.open_page( section, 'url')
        else:
            self.open_page(MAIN_PAGE_SECTION, 'url')
            self.find_locator_and_click(section, MAIN_PAGE_SECTION + "_2_" + section +"_connector")
        sleep(self.show_wait)
        self.assertTrue(self.verify_existence_defined_in_ini_file(section, "page_opened"), "can't open page: " + section)
        pass

    def _test10x(self,csv_line_number):
        if not self.allow_test(csv_line_number+100): return
        self.assertTrue(self.open_page('main_page', 'url'),MAIN_PAGE_SECTION_OPEN_ERROR)
        self.find_locator_and_click( LOGIN_PAGE_SECTION,'main_page_2_login_page_connector')

        if self.inifilevalue.read_string_from_ini(LOGIN_PAGE_SECTION, "login_name_connector") is not None:
            if self.CSVfile_login_page_data.column_exists("login_name"):
                value = self.CSVfile_login_page_data.get("login_name",csv_line_number)
                self.find_locator_and_send_keys(LOGIN_PAGE_SECTION,"login_name_connector", value)

        if self.inifilevalue.read_string_from_ini(LOGIN_PAGE_SECTION, "login_name_connector") is not None:
            if self.CSVfile_login_page_data.column_exists("password"):
                value = self.CSVfile_login_page_data.get("password",csv_line_number)
                self.find_locator_and_send_keys(LOGIN_PAGE_SECTION,"password_connector", value)
        self.find_locator_and_click(LOGIN_PAGE_SECTION, 'login_accept_connector')

        if self.CSVfile_login_page_data.column_exists("final_confirmation_type"):
            final_confirmation_type = self.CSVfile_login_page_data.get("final_confirmation_type",csv_line_number)
        if self.CSVfile_login_page_data.column_exists("parameter1"):
            parameter1 = self.CSVfile_login_page_data.get("parameter1",csv_line_number)
        if self.CSVfile_login_page_data.column_exists("parameter2"):
            parameter2 = self.CSVfile_login_page_data.get("parameter2",csv_line_number)

        self.assertTrue(self.verify_existence_directly_defined(final_confirmation_type,parameter1,parameter2))
        pass

    def _test15x(self,csv_line_number):
        if not self.allow_test(csv_line_number+150): return
        self.assertTrue(self.open_page('main_page', 'url'),MAIN_PAGE_SECTION_OPEN_ERROR)
        self.find_locator_and_click( NEW_USER_PAGE_SECTION,'main_page_2_new_user_page_connector')

        if self.inifilevalue.read_string_from_ini(NEW_USER_PAGE_SECTION, "new_user_page_connector") is not None:
            if self.CSVfile_new_user_page_data.column_exists("login_name"):
                value = self.CSVfile_new_user_page_data.get("login_name",csv_line_number)
                self.find_locator_and_send_keys(NEW_USER_PAGE_SECTION,"login_name_connector", value)

        if self.inifilevalue.read_string_from_ini(NEW_USER_PAGE_SECTION, "new_user_page_connector") is not None:
            if self.CSVfile_new_user_page_data.column_exists("password"):
                value = self.CSVfile_new_user_page_data.get("password",csv_line_number)
                self.find_locator_and_send_keys(NEW_USER_PAGE_SECTION,"password_connector", value)
        self.find_locator_and_click(NEW_USER_PAGE_SECTION, 'login_accept_connector')

        if self.CSVfile_new_user_page_data.column_exists("final_confirmation_type"):
            final_confirmation_type = self.CSVfile_new_user_page_data.get("final_confirmation_type",csv_line_number)
        if self.CSVfile_new_user_page_data.column_exists("parameter1"):
            parameter1 = self.CSVfile_new_user_page_data.get("parameter1",csv_line_number)
        if self.CSVfile_new_user_page_data.column_exists("parameter2"):
            parameter2 = self.CSVfile_new_user_page_data.get("parameter2",csv_line_number)

        self.assertTrue(self.verify_existence_directly_defined(final_confirmation_type,parameter1,parameter2))
        pass

    def test000(self):
        self._test00x( 0, MAIN_PAGE_SECTION )

    def test001(self):
        self._test00x( 1, LOGIN_PAGE_SECTION )

    def test002(self):
        self._test00x( 2, NEW_USER_PAGE_SECTION )

    def test003(self):
        self._test00x( 3, CART_PAGE_SECTION )

    def test100(self):
        self._test10x(0)
        pass

    def test101(self):
        self._test10x(1)
        pass

    def test102(self):
        self._test10x(2)
        pass

    def test103(self):
        self._test10x(3)
        pass

    def test104(self):
        self._test10x(4)
        pass

    def test150(self):
        self._test15x(0) # test 150
        pass

    def test151(self):
        self._test15x(1)
        pass


    def test152(self):
        self._test15x(2)
        pass

    def test153(self):
        self._test15x(3)
        pass

    def test154(self):
        self._test15x(4)
        pass

if __name__ == "__main__":
    unittest.main(verbosity=0)
#    unittest.main()
