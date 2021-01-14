from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options


class BotWhatsapp:
    def __init__(self):
        self.path_driver = "E:\chromedriver.exe" ## El path del ejecutador del chromedriver
        self.base_url = "https://web.whatsapp.com" ## La url del whatsapp o lo que quieras
        self.timeout = 15
        self.set_paths()

    def set_paths(self):
        self.base_input = '_1awRl'
        self.firs_contact = '//*[@id="pane-side"]/div[1]/div/div/div[1]'
        self.base_sent = '/html/body/div/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]'

    def start_browser(self):

        chrome_options = Options()
        chrome_options.add_argument(r'--user-data-dir=C:\Users\Sergi\AppData\Local\Google\Chrome\User Data\Wtsp')## para guardar la sesion y no tener que iniciar sesion cada vez que ejecutas
        chrome_options.binary_location = "E:\Sistema\Archivos de programa\Google\Chrome\Application\chrome.exe" ##La ruta del chrome.exe
        self.browser = webdriver.Chrome(options=chrome_options, executable_path=self.path_driver, )
        self.browser.maximize_window()
        self.browser.get(self.base_url)
       
        try:
            WebDriverWait(self.browser,self.timeout).until(
                EC.presence_of_all_elements_located(
                (By.CLASS_NAME, self.base_input)))
            print("Si he entrado")
            return True
        except Exception as e:
            print(e)
            self.browser.quit()
            return False

    def send_message_to_contact(self, contact, message):
        start = self.start_browser()
        if not start:
            return False
        user_search = self.search_user_or_group(contact)
        if not (user_search or contact or message):
            return False
        message = message.strip()
        try:
            send_msg = WebDriverWait(self.browser, self.timeout).until(
                EC.presence_of_element_located(
                    (By.XPATH, self.base_sent)))
        except Exception  as e:
            print(e)
            print("Nose encontro conctacto.")
            self.browser.quit()
            return
        messages = message.split("\n")
        for msg in messages:
            send_msg.send_keys(msg)
            send_msg.send_keys(Keys.SHIFT + Keys.ENTER)
            sleep(1)
            send_msg.send_keys(Keys.ENTER)
            print('Mensaje enviado')
            sleep(10)
            self.browser.quit()
            return True

    def search_user_or_group(self, contact):
        search = self.browser.find_element_by_class_name(self.base_input)
        search.clear()
        search.send_keys(contact)
        try:
            vali_ = WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, self.firs_contact)))
            if vali_.is_displayed():
                search.send_keys(Keys.ENTER)
                sleep(5)
                return True
        except Exception as e:
            print(e)
            print("Nose encontro conctacto.")
            return False
    def prueba(self):
        self.start_browser()

prueba = BotWhatsapp()
contact="python"
message="Es un mensaje automatizado para mostralo en likedIn"
prueba.send_message_to_contact(contact,message)

