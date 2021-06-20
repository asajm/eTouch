import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException 
from selenium.webdriver.common.keys import Keys
import time
import datetime
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
import re
import math

class eTouch():
    def __init__(self, browser, wait):
        self.browser = browser
        self.wait = wait

    def _open_frame(self, name):
        try:
            self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, name)))
            return self.browser.execute_script('return self.name')
        except Exception as e:
            print(e)
            return None

    def _open_frame__gobtn(self):
        result = None
        self.browser.switch_to.default_content()
        for frame in ['gobtn']:
            result = self._open_frame(frame)
        return result

    def _open_frame__menubar(self):
        result = None
        self.browser.switch_to.default_content()
        for frame in ['product','tab_1003','menubar']:
            result = self._open_frame(frame)
        return result
    
    def _open_frame__cai_main(self):
        result = None
        self.browser.switch_to.default_content()
        for frame in ['product','tab_1003','role_main','cai_main']:
            result = self._open_frame(frame)
        return result
    
    def waiting_sand_clock(self):
        self.browser.switch_to.default_content()
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, 'gobtn')))
        self.wait.until(EC.invisibility_of_element_located((By.ID, 'busygifLayer')))

    def click_button(self, id, name):
        self.wait.until(EC.visibility_of_element_located((By.ID, id)))
        self.wait.until(EC.element_to_be_clickable((By.ID, id)))
        _btn = self.browser.find_element_by_id(id)
        if(_btn.text == name):
            _btn.click()
        else:
            raise NameError('incorrect ID or NAME of the button!')

    def fillout_field(self, id, text=None, press_tab=False):
        self.wait.until(EC.visibility_of_element_located((By.ID, id)))
        _field = self.browser.find_element_by_id(id) 
        _field.clear()
        _field.send_keys(text) if type(text) == str else None
        _field.send_keys(Keys.TAB) if press_tab else None

    def close_all_windows(self):
        for window in self.browser.window_handles[1:]:
            self.browser.switch_to.window(window)
            self.browser.close()
        self.browser.switch_to.window(self.browser.window_handles[0])

    def is_alert_present(self):
        try:
            WebDriverWait(self.browser, 3).until(EC.alert_is_present())
            return True
        except:
            return False

    # options are : "Document by ID", "Incident", "Issue", "Knowledge", "Problem", "Request", "User by ID", "User by Name", "User by Phone"
    def _select_ticket_type_gobtn(self, option):
        self._open_frame__gobtn()
        el = self.browser.find_element_by_id('ticket_type')
        for op in el.find_elements_by_tag_name('option'):
            if op.text == option:
                op.click()
                break

    def _fillout_search_field_gobtn(self, ticket_num):
        self._open_frame__gobtn()
        self.browser.find_element_by_name('searchKey').clear()
        self.browser.find_element_by_name('searchKey').send_keys(ticket_num)
        
    def _click_go_gobtn(self):
        self._open_frame__gobtn()
        self.browser.find_element_by_id('imgBtn0').click()
