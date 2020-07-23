import requests
import time
import random
from threading import Semaphore
from selenium import webdriver



def get_driver_moni_ip():

    get_ip_url="http://zhulong.v4.dailiyun.com/query.txt?key=NPACB534AB&word=&count=100&rand=false&detail=false"
    sema = Semaphore()
    sema.acquire()
    i = 3
    try:
        url = get_ip_url
        r = requests.get(url, timeout=40)
        time.sleep(0.5)
        ip = random.choice(r.text.strip().split('\r\n'))
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument("--proxy-server=http://%s" % (ip))
        driver = webdriver.Chrome(chrome_options=chromeOptions)

    except:
        ip = {}
    finally:
        sema.release()

    return driver