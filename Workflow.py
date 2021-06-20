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


class eTouch_Workflow(eTouch):
    def __init__(self, browser, wait):
        super().__init__(browser, wait)
        self.title_list = 'eTouCH - Change Workflow List'
        self.title_update = 'Update Change Workflow - eTouCH'
        self.title_detail = 'Change Workflow Detail - eTouCH'

    def _open_popup_win_frame__cai_main(self):
        self.browser.switch_to.default_content()
        result = self._open_frame('cai_main')
        return 

    def _open_frame__scoreboard(self):
        result = None
        self.browser.switch_to.default_content()
        for frame in ['product','tab_1003','role_main','scoreboard']:
            result = self._open_frame(frame)
        return result  
        
    def open_workflow_list(self):
        self._open_frame__scoreboard()
        try:
            self.browser.find_element_by_id('s3ds').click()
            self.waiting_sand_clock()
        except:
            self.browser.find_element_by_id('s1pm').click()
            self.browser.find_element_by_id('s3ds').click()
            self.waiting_sand_clock()

    def get_workflow_list(self):
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
            _df = _df[~_df['Change #'].isna()]
            _df['Change #'] = _df['Change #'].astype(str)
            _df['Violated'] = _df['Change #'].str.contains('\*\*')==True
            _df['Change #'] = _df['Change #'].str.extract('(\d+)')
            df = df.append(_df)

            if(pages > 1):
                elm = self.browser.find_element_by_id('dataGrid_toppager_center').find_element_by_id('next_t_dataGrid_toppager')
                if('ui-state-disabled' not in elm.get_attribute('class').split()):
                    elm.click()
                else:
                    break
        
        df = df[~df['Change #'].isna()]
        df['Change #'] = df['Change #'].astype(int)
        return df['Change #'].tolist()

        
    def get_free_workflow_list(self):
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
            _df = _df[~_df['Change #'].isna()]
            _df['Change #'] = _df['Change #'].astype(str)
            _df['Violated'] = _df['Change #'].str.contains('\*\*')==True
            _df['Change #'] = _df['Change #'].str.extract('(\d+)')
            df = df.append(_df)

            if(pages > 1):
                elm = self.browser.find_element_by_id('dataGrid_toppager_center').find_element_by_id('next_t_dataGrid_toppager')
                if('ui-state-disabled' not in elm.get_attribute('class').split()):
                    elm.click()
                else:
                    break
        
        df = df[~df['Change #'].isna()]
        df['Change #'] = df['Change #'].astype(int)
        return df[df['Assignee'].isna()]['Change #'].tolist()


    def open_workflow(self, CO):
        self._open_frame__cai_main()

        try:
            self.browser.find_element_by_id('top_view_all').click()
            self._open_frame__cai_main()
        except:
            pass

        _xpath = "//td[@title='{}']".format(CO)
        self.wait.until(EC.visibility_of_element_located( (By.XPATH, _xpath) ))
        
        self.browser.find_element_by_xpath(_xpath).find_element_by_tag_name('a').click()
        
        self.wait.until(EC.number_of_windows_to_be(2))
        self.browser.switch_to.window(self.browser.window_handles[len(self.browser.window_handles)-1])
        self.wait.until(EC.title_is(self.title_detail))
        self.waiting_sand_clock()
        
    def close_opend_workflow(self):
        self.browser.close()
        self.wait.until(EC.number_of_windows_to_be(1))
        self.browser.switch_to.window(self.browser.window_handles[0])

    def get_opend_workflow_category(self):
        self.wait.until(EC.title_is(self.title_detail))
        self._open_popup_win_frame__cai_main()
        self.wait.until(EC.visibility_of_element_located((By.ID, 'df_4_2')))
        el = self.browser.find_element_by_id('df_4_2')
        return el.text

    def click_edit(self):
        self.wait.until(EC.title_is(self.title_detail))
        self._open_popup_win_frame__cai_main()
        self.click_button('imgBtn0', 'Edit')
        self.waiting_sand_clock()
        self.wait.until(EC.title_is(self.title_update))

    def fillout_assignee_field(self, assignee):
        self._open_popup_win_frame__cai_main()
        self.fillout_field('df_1_0', assignee, press_tab=True) 

    def fillout_remarks_field(self, remarks):
        self._open_popup_win_frame__cai_main()
        self.fillout_field('df_6_0', remarks)

    def click_save(self):
        self.wait.until(EC.title_is(self.title_update))
        self._open_popup_win_frame__cai_main()
        self.click_button('imgBtn0', 'Save')
        self.waiting_sand_clock()
        self.wait.until(EC.title_is(self.title_detail))

    def click_cancel(self):
        self.wait.until(EC.title_is(self.title_update))
        self._open_popup_win_frame__cai_main()
        self.click_button('imgBtn1', 'Cancel')
        self.waiting_sand_clock()
        self.wait.until(EC.title_is(self.title_detail))
        
    def select_status_field(self, option):
        self.wait.until(EC.title_is(self.title_update))
        self._open_popup_win_frame__cai_main()

        el = self.browser.find_element_by_name('SET.status')
        for op in el.find_elements_by_tag_name('option'):
            if op.text == option:
                op.click()
                break

