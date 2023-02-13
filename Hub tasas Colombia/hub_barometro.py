# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 10:15:49 2022

@author: JOSE
"""

import os
import re
import ssl
import sys
import time
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from webdriver_manager.chrome import ChromeDriverManager


constrasena = 'Libertad5%'
usuario = 'julio.daly@gmail.com'

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
  })

url = 'https://app.brandwatch.com/login'

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)

def barra_carga(tiempo, hits):
    sys.stdout.write("%s: [" % ('hitting '+str(hits)+' times'))
    sys.stdout.flush()
    sys.stdout.write("\b" * (tiempo+1))
    
    for i in range(tiempo):
        time.sleep(1) # do real work here
        # update the bar
        if (round(tiempo/(i+1))%5)==0:
            sys.stdout.write("-")
            sys.stdout.flush()
    sys.stdout.write("]\n")
    return

user = driver.find_element_by_xpath("/html/body/div/div[1]/div/div/div/div/form/div[1]/label/div/input")
user.send_keys(usuario)
pas = driver.find_element_by_xpath("/html/body/div/div[1]/div/div/div/div/form/div[2]/label/div/input")
pas.send_keys(constrasena)
login = driver.find_element_by_xpath("/html/body/div/div[1]/div/div/div/div/form/div[3]/ax-submit-button")
login.click()

url = "https://app.brandwatch.com/project/1998268711/dashboards/1165499"
driver.get(url)

barra_carga(tiempo = 60, hits = 5)

migracion = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div/div/div[1]/section/div[2]/section/div[1]/div[1]/article/div/div/consumer-research/div/div/div[1]/div/h5")


xenofobia = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div/div/div[1]/section/div[2]/section/div[1]/div[2]/article/div/div/consumer-research/div/div/div[1]/div/h5")

migracion = migracion.text.split()
xenofobia = xenofobia.text.split()

def limpiar(lista: list):
    retorno = []
    for item in lista:
        if item != "K":
            if item.find(".") != -1:
                num = float(item)
                num = num*1000
                num = int(num)
                retorno.append(num)
            else:
                retorno.append(item)
    if len(retorno) > 1:
        retorno = retorno[0] + retorno[1]
    else:
        retorno = int(retorno[0])
    return retorno

migracion = limpiar(migracion)
xenofobia = limpiar(xenofobia)

hub = pd.DataFrame()
hub["migración"] = int(migracion)
hub["xenofobia"] = int(xenofobia)
hub["tasa_xenofobia"] = int(xenofobia)/int(migracion)
print(hub.head(5))
