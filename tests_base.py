#################### tests_base.py ####################

from time import sleep
from vini import Vini
import unittest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
import os
from vcsv import CSVData

#
# open_page(self,section, key ) --> try to open url defined with "key" under [section] in *.ini file 
#
# find_locator(self, section, key )
# - looks for locator defined with "key" under [section] in *.ini file  
# find_locator_and_click(self, section, key )
# - looks for - and clicks if possible - locator defined with "key" under [section] in *.ini file
# find_locator_and_send_keys(self, section, key, send_keys )
# - looks for and - send charakters - if possible locator defined with "key" under [section] in *.ini file
#
# verify_existence_directly_defined(self, type, parameter1, parameter2="" )
# - verify if obiect defined with type exists
# - type is one of [locator, title, alert, locator.text]
# - i.e. verify_existence_directly_defined(	self, "locator", 'By.ID, "login2"')
#
# verify_existence_defined_in_ini_file(self, page, key_begin )
# - verify if obiect defined under [section] with key_begin + "_confirmation_type" exists
#

class BaseForTests(unittest.TestCase):

    def setUp(self):
        self.inifilevalue = Vini()
        self.log_on = self.inifilevalue.read_boolean_from_ini("settings","log")
        self.implicit_wait = self.inifilevalue.read_float_from_ini("settings","implicit_wait")
        self.driver = webdriver.Chrome()
        if self.implicit_wait > 0.0:
            self.driver.implicitly_wait(self.implicit_wait)
        self.explicit_wait = self.inifilevalue.read_float_from_ini("settings","explicit_wait")
        self.show_wait = self.inifilevalue.read_float_from_ini("settings","show_wait")
        self.driver.maximize_window()
        #self.driver.minimize_window()
        self.alert = Alert(self.driver)
        self.path = self.inifilevalue.get_full_path()
        self.log("BaseForTests.setUp()")
        self.log("using: " + self.path)
        self.CSVfile_login_page_data = CSVData(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'login_page_data.csv' ))
        self.CSVfile_new_user_page_data = CSVData(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'new_user_page_data.csv' ))
        pass

    def tearDown(self):
        self.driver.quit()
        self.log("BaseForTests.tearDown()")
        pass

#############

    def log(self,message):
        if self.log_on: print( datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f: ") + message)
        pass

    def log_success(self):
        self.log("...success")

    def log_failed(self):
        self.log("...failed")

#############

    def open_page(self,section, key ):
        value = self.inifilevalue.read_string_from_ini(section, key)
        self.log( "trying to open: " + value )
        try:
            self.driver.get(value)
            self.log_success()
            return True
        except:
            self.log_failed()
            return False
        pass

    def current_page_title(self):
        return self.driver.title
        pass

#############

    def _correct_parameter1(self, input_string):
        input_string = input_string.strip(" ")
        input_string = input_string.strip('"')
        input_string = input_string.strip("'")
        return input_string

    def _get_by_id(self, valueBy):
        match valueBy:
            case "By.ID":
                by_id = By.ID
            case "By.NAME":
                by_id = By.NAME
            case "By.LINK_TEXT":
                by_id = By.ID
            case "By.PARTIAL_LINK_TEXT":
                by_id = By.PARTIAL_LINK_TEXT
            case "By.CLASS_NAME":
                by_id = By.CLASS_NAME
            case "By.TAG_NAME":
                by_id = By.TAG_NAME
            case "By.CSS_SELECTOR":
                by_id = By.CSS_SELECTOR
            case "By.XPATH":
                by_id = By.XPATH
            case _:
                by_id = None
        return by_id

    def find_locator(self, section, key ):
        value = self.inifilevalue.read_string_from_ini(section, key)
        valueBy = value.split(",")[0]
        by_id = self._get_by_id(valueBy)
        if valueBy == None: return None;
        value = value.replace( valueBy + ",", '')
        value = self._correct_parameter1(value)
        if not value: return None;
        self.log( "trying to find: '%s' %s" % (value,valueBy ))
        try:
            self.waiter = WebDriverWait(self.driver, self.implicit_wait).until(EC.presence_of_element_located((by_id, value)))
            #self.waiter = self.driver.find_element(by_id, value)
            self.log_success()
        except:
            self.log_failed()
            return None
        return self.waiter

    def find_locator_and_click(self, section, key ):
        self.waiter = self.find_locator(section,key)
        self.log("trying to click")
        try:
            self.waiter.click()
            self.log_success()
        except:
            self.log_failed()
            return None
        return self.waiter

    def find_locator_and_send_keys(self, section, key, send_keys ):
        self.waiter = self.find_locator(section,key)
        self.log("trying to send keys: '%s'" %() send_keys )
        try:
            self.waiter.send_keys(send_keys)
            self.log_success()
        except:
            self.log_failed()
            return None
        return self.waiter

#############

    def verify_existence_defined_in_ini_file(self, page, key_begin ):
        type = self.inifilevalue.read_string_from_ini(page, key_begin + "_confirmation_type")
        parameter1 =self.inifilevalue.read_string_from_ini(page,key_begin + "_confirmation_parameter1")
        parameter2 =self.inifilevalue.read_string_from_ini(page,key_begin + "_confirmation_parameter2")
        return self.verify_existence_directly_defined(type,parameter1,parameter2)

#############

    def _verify_existence_directly_defined_locator_type(self,parameter1):
        valueBy = parameter1.split(",")[0]
        by_id = self._get_by_id(valueBy)
        if valueBy == None: return None;
        value = parameter1.replace( valueBy + ",", '')
        value = self._correct_parameter1(value)
        if not value: return None;
        self.log( "trying to find: '%s' %s" % (value,valueBy ))
        try:
            self.waiter = WebDriverWait(self.driver, self.implicit_wait).until(EC.presence_of_element_located((by_id, value)))
            #self.waiter = self.driver.find_element(by_id, value)
            self.log_success()
            return True
        except:
            self.log_failed()
            return False

    def _verify_existence_directly_defined_locator_type_text(self,parameter1,parameter2):
        valueBy = parameter1.split(",")[0]
        by_id = self._get_by_id(valueBy)
        if valueBy == None: return None;
        value = parameter1.replace( valueBy + ",", '')
        value = self._correct_parameter1(value)
        if not value: return None;
        self.log( "trying to find text: '%s' stored in '%s' %s" %(parameter2, value,valueBy))
        try:
            self.waiter = WebDriverWait(self.driver, self.implicit_wait).until(EC.text_to_be_present_in_element((by_id, value),parameter2))
            self.title = self.driver.find_element(by_id,value).text
            self.log_success()
            return True
        except:
            self.log_failed()
            return False

    def _verify_existence_directly_defined_title_type(self, title):
        self.log( "looking for title: '%s'" %(title) )
        self.check = title == self.current_page_title()
        if self.check:  self.log_success()
        else:           self.log_failed()
        return self.check

    def _verify_existence_directly_defined_alert_type(self, title):
        self.log( "looking for alert: '%s'" %(title) )
        try:
            self.waiter = WebDriverWait(self.driver, self.implicit_wait).until(EC.alert_is_present())
            self.check = self.alert.text == title
            self.alert.accept()
        except:
            self.check = False
        if self.check:
            self.log_success()
        else:
            self.log_failed()
        return self.check

    def verify_existence_directly_defined(self, type, parameter1, parameter2="" ):
        sleep(self.show_wait)
        match type:
            case "locator":
                self.check = self._verify_existence_directly_defined_locator_type(parameter1)
            case "locator.text":
                self.check = self._verify_existence_directly_defined_locator_type_text(parameter1,parameter2)
            case "title":
                self.check = self._verify_existence_directly_defined_title_type(parameter1)
            case "alert":
                self.check = self._verify_existence_directly_defined_alert_type(parameter1)
            case _:
                self.check = False
        return self.check

