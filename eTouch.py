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
        df = pd.read_html(self.browser.page_source)[12]
        df = df[~df['Change #'].isna()]
        df['Change #'] = df['Change #'].astype(int)

        return df['Change #'].tolist()
        
    def get_free_workflow_list(self):
        self._open_frame__cai_main()
        df = pd.read_html(self.browser.page_source)[12]
        df = df[~df['Change #'].isna()]
        df['Change #'] = df['Change #'].astype(int)
        
        return df[df['Assignee'].isna()]['Change #'].tolist()

    def open_workflow(self, CO):
        self._open_frame__cai_main()
        self.wait.until(EC.visibility_of_element_located( (By.XPATH, "//td[@title='{}']".format(CO)) ))
        
        self.browser.find_element_by_xpath( "//td[@title='{}']".format(CO)).find_element_by_tag_name('a').click()
        
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

class eTouch_CO(eTouch):
    def __init__(self, browser, wait):
        super().__init__(browser, wait)
        self.title_search = 'eTouCH - Change Order Search'
        self.title_list = 'eTouCH - Change Order List'
        self.title_detail = '{} Change Order Detail - eTouCH'
        self.title_update = '{} Update Change Order - eTouCH'

        
    def open_co_search(self):
        self._open_frame__menubar()
        self.browser.execute_script('javascript:window.parent.role_main.cai_main.setActKeyMenuState(2)')

        self.browser.switch_to.parent_frame()
        self.browser.switch_to.parent_frame()
        self.browser.find_element_by_id('amSearch_4').click()

    def fillout_status_field(self, status=None):
        self._open_frame__cai_main()
        self.fillout_field('sf_2_0', status, press_tab=True)      

    def fillout_category_field(self, category):
        self._open_frame__cai_main()
        self.fillout_field('sf_2_1', category, press_tab=True)
        
    def select_active_field(self, option='<empty>'):
        self._open_frame__cai_main()
        el = self.browser.find_element_by_id('sf_1_4')
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

    def click_search_filter(self):
        self._open_frame__cai_main()
        self.click_button('imgBtn5', 'Search')

    def click_more_links(self):
        self._open_frame__cai_main()
        self.browser.find_element_by_id('sf_3_1').click()
        self.browser.find_element_by_id('sf_8_3').click()
        self.browser.find_element_by_id('sf_15_4').click()

    def fillout_earlies_open_date_field(self, days=180):
        self._open_frame__cai_main()
        start_date = datetime.datetime.now() - datetime.timedelta(days) 
        date = start_date.strftime('%m/%d/%Y 12:00 am')
        self.fillout_field('sf_11_2', date, press_tab=True)     

    def fillout_latest_open_date_field(self, now=False):
        self._open_frame__cai_main()       
        date = datetime.datetime.now().strftime('%m/%d/%Y {}'.format( '%I:%m %p' if now else '12:00 am' ))
        self.fillout_field('sf_11_3', date, press_tab=True)

    def get_num_tickets(self):
        self._open_frame__cai_main()
        text = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'ui-paging-info'))).text
        if(text == 'No change orders found'): 
            return 0
        elif(text == '1 change order found'):
            return 1
        else:
            return int(text.split(' of ')[1])

    def get_CO_list(self):
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
            _df = _df[~_df['Change Order #'].isna()]
            _df['Change Order #'] = _df['Change Order #'].astype(str)
            _df['Violated'] = _df['Change Order #'].str.contains('\*\*')==True
            _df['Change Order #'] = _df['Change Order #'].str.extract('(\d+)')
            df = df.append(_df)

            if(pages > 1):
                elm = self.browser.find_element_by_id('dataGrid_toppager_center').find_element_by_id('next_t_dataGrid_toppager')
                if('ui-state-disabled' not in elm.get_attribute('class').split()):
                    elm.click()
                else:
                    break

        return df

    def search_CO(self, ticket_num):
        self._select_ticket_type_gobtn("Change Order")
        self._fillout_search_field_gobtn(ticket_num)
        self._click_go_gobtn()