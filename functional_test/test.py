from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import unittest
import time
import os

MAX_WAIT = 10

class NewVisitorTest(StaticLiveServerTestCase):

    def wait_for_row_in_list_table(self,row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except(AssertionError, WebDriverException)as e:
                    if(time.time()-start_time > MAX_WAIT):
                        raise e
                    time.sleep(0.5)

    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://'+staging_server
        #time.sleep(2)


    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_a_retrieve_it_later(self):     
        #self.browser.get('http://localhost:8000')        
        self.browser.get(self.live_server_url)        
        self.assertIn('To-Do',self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do',header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),'Enter a to-do item'
        )
        inputbox.send_keys('Buy peacock feathers')

        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        #time.sleep(2)

        #table = self.browser.find_element_by_id('id_list_table')
        #rows = table.find_elements_by_tag_name('tr')
        #self.check_for_row_in_list_table('1: Buy peacock feathers')
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')

        inputbox.send_keys(Keys.ENTER)
        #time.sleep(2)
        #self.assertTrue(
        #    any(row.text == '1: Buy peacock feathers' for row in rows),
        #    f"New to-do item did not appear in table. Content were:\n{table.text}"
        #)

        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')

        #self.check_for_row_in_list_table('1: Buy peacock feathers')
        #self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
        #self.assertIn('1: Buy peacock feathers',[row.text for row in rows])
        #self.assertIn(
        #    '2: Use peacock feathers to make a fly',[row.text for row in rows]
        #)
        self.fail('Finish the test!')

    def check_for_row_in_list_table(self,row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text,[row.text for row in rows])

    def test_can_start_a_list_for_one_user(self):
    #edith has heard about a cool new online to-do app. she goes
        self.wait_for_row_in_list_table('1: Buy peacock feathers')        
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')

    def test_multiple_users_can_start_list_as_different_urls(self):
        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Buy peacock feathers')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        eidth_list_url = self.browser.current_url
        self.assertRegex(eidth_list_url,'/lists/.+')

        #now a new user, Francis come along to the site 

        #we use e new browser session
        self.browser.quit()
        self.browser = webdriver.Firefox()

        #francis visit home page a no sign of edith's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peackock feathers',page_text)
        self.assertNotIn('make a fly',page_text)

        #francis starts a new list by adding a new item
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Buy milk')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url,'/lists/.+')
        self.assertNotEqual(francis_list_url,eidth_list_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers',page_text)
        self.assertIn('Buy milk',page_text)

    def test_layout_and_styling(self):
    #giuditta va sulla home page
        self.browser.get(self.live_server_url)        
        self.browser.set_window_size(1024,768)

    #giuditta nota che la casella di input è centrata 
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('testing')
        input_box.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: testing')
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] /2, 512, delta=10
        )

#if __name__ == '__main__':
#    unittest.main(warnings='ignore')


