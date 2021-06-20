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
from .eTouch import eTouch

class eTouch_Incident(eTouch):
    def __init__(self, browser, wait):
        super().__init__(browser, wait)
        self.title_search = 'eTouCH - Incident Search'
        self.title_list = 'eTouCH - Incident List'
        self.title_detail = '{} Incident Detail - eTouCH'
        self.title_update = '{} Update Incident - eTouCH'
        
    def open_incident_search(self):   
        self._open_frame__menubar()
        self.browser.execute_script('javascript:window.parent.role_main.cai_main.setActKeyMenuState(2)')

        self.browser.switch_to.parent_frame()
        self.browser.switch_to.parent_frame()
        self.browser.find_element_by_id('amSearch_1').click()
   
    def fillout_status_field(self, status=None):
        self._open_frame__cai_main()
        self.fillout_field('sf_0_4', status, press_tab=True)
          
    def fillout_group_field(self, group):
        self._open_frame__cai_main()
        self.fillout_field('sf_0_3', group, press_tab=True)

    def select_active_field(self, option='<empty>'):
        self._open_frame__cai_main()
        el = self.browser.find_element_by_id('sf_1_1')
        for op in el.find_elements_by_tag_name('option'):
            if op.text == option:
                op.click()
                break
                          
    def click_search(self):
        self._open_frame__cai_main()
        self.click_button('imgBtn0', 'Search')

    def click_search_filter(self):
        self._open_frame__cai_main()
        self.click_button('imgBtn1', 'Search')

    def click_export(self):
        self._open_frame__cai_main()
        self.click_button('imgBtn4', 'Export')

    def click_more_links(self):
        self._open_frame__cai_main()
        self.browser.find_element_by_id('sf_5_1').click()
        self.browser.find_element_by_id('sf_12_4').click()
        self.browser.find_element_by_id('sf_13_4').click()

    def fillout_earlies_open_date_field(self, days=180):
        self._open_frame__cai_main()
        start_date = datetime.datetime.now() - datetime.timedelta(days) 
        date = start_date.strftime('%m/%d/%Y 12:00 am')
        self.fillout_field('sf_7_2', date, press_tab=True)
         
    def fillout_latest_open_date_field(self, now=False):
        self._open_frame__cai_main()       
        date = datetime.datetime.now().strftime('%m/%d/%Y {}'.format( '%I:%m %p' if now else '12:00 am' ))
        self.fillout_field('sf_7_3', date, press_tab=True)

    def get_num_tickets(self):
        self._open_frame__cai_main()
        text = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'ui-paging-info'))).text
        if(text == 'No change orders found'): 
            return 0
        elif(text == '1 change order found'):
            return 1
        else:
            return int(text.split(' of ')[1])
        
    def get_incident_list(self):
        self._open_frame__cai_main()
        try:
            elm_td = self.browser.find_element_by_id('dataGrid_toppager_center')
            pages = int(elm_td.find_element_by_id('sp_1_dataGrid_toppager').text)
        except:
            pages = 1

        df = pd.DataFrame()
        for i in range(pages):
            self.wait.until(EC.visibility_of_element_located((By.ID, 'dataGrid')))
            table = self.browser.find_element_by_id('dataGrid')
            _df = pd.read_html(table.get_attribute("outerHTML"))[0]
            _df.drop(_df.columns[0], axis=1, inplace=True)
            _df = _df[~_df['Incident #'].isna()]
            _df['Incident #'] = _df['Incident #'].astype(str)
            _df['Violated'] = _df['Incident #'].str.contains('\*\*')==True
            _df['Incident #'] = _df['Incident #'].str.extract('(\d+)')
            df = df.append(_df)

            if(pages > 1):
                elm = self.browser.find_element_by_id('dataGrid_toppager_center').find_element_by_id('next_t_dataGrid_toppager')
                if('ui-state-disabled' not in elm.get_attribute('class').split()):
                    elm.click()
                else:
                    break

        return df

    def search_incident(self, ticket_num):
        self._select_ticket_type_gobtn("Incident")
        self._fillout_search_field_gobtn(ticket_num)
        self._click_go_gobtn()
