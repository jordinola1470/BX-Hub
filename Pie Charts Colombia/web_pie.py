# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 01:25:25 2022

@author: usuario
"""

import os, shutil
import re
import ssl
import sys
import time
import numpy as np
import pandas as pd
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import traceback

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
  })

start_date = '2020-05-20' # YYYY-MM-DD 2020-01-01

end_date = '2022-02-04' # PATTERN YYYY-MM-DD - YYYY-MM-DD

constrasena = 'Libertad5%'
usuario = 'julio.daly@gmail.com'
path_destino = r'D:\Trabajo\Barómetro\BX\Web Scraping\Pie Charts Ecuador' + '\\'
path_descargas = r'C:\Users\usuario\Downloads' + '\\'
boton_descargas = '/html/body/div[1]/div/div/div/div/div/div[1]/section/div[2]/section/div[1]/div[4]/article/header/span[1]/ul/li[3]/a/span[2]'
URL = 'https://app.brandwatch.com/login'
dashboard = 'https://app.brandwatch.com/project/1998317449/dashboards/1182073' # Dashboard Ecuador
apply_btn = '/html/body/div[1]/div/div/div/div/div/div[1]/section/div[2]/section/div[1]/div[4]/article/aside/form/div[2]/div[1]/p/ax-button'
date_input = '/html/body/div[1]/div/div/div/div/div/div[1]/section/div[2]/section/div[1]/div[4]/article/aside/form/div[2]/div[1]/fieldset[2]/div/input'
filter_button = '/html/body/div[1]/div/div/div/div/div/div[1]/section/div[2]/section/div[1]/div[4]/article/header/span[1]/ul/li[4]/a/span[2]'
excel_download = '/html/body/div[24]/div/ul/li[1]'
# Hay que probar que pasa cuando metemos mas cosas al dashboard

def barra_carga(tiempo):
    sys.stdout.write("%s: [" % ('Esperando '+str(tiempo)+' segundos'))
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

def next_week(fecha:str) -> str:
    nueva_fecha = datetime.datetime.strptime(fecha,'%Y-%m-%d').date()
    nueva_fecha = nueva_fecha + datetime.timedelta(days=7)
    return str(nueva_fecha)

def daterange(start_date, end_date):
    start_date = datetime.datetime.strptime(start_date,'%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(end_date,'%Y-%m-%d').date()
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)
        
folder_descargas = os.path.dirname(path_descargas)
folder_bases = os.path.dirname(path_destino)


def query_pie_chart(start_date: str, end_date: str) -> list:
    centinela = True
    retorno = list()
    two_weeks = next_week(next_week(start_date)) 
    n = 0
    while centinela == True:
        if n == 0:
            envio_range_fechas = start_date + " - " + two_weeks
            retorno.append(envio_range_fechas)
        else:
            start_date = two_weeks
            two_weeks = next_week(next_week(start_date))
            two_weeks_verif = datetime.datetime.strptime(two_weeks,'%Y-%m-%d').date()
            end_date_verif = datetime.datetime.strptime(end_date,'%Y-%m-%d').date()
            if int((end_date_verif - two_weeks_verif).days) < 0:
                centinela = False
            else:
                envio_range_fechas = start_date + " - " + two_weeks
                retorno.append(envio_range_fechas)
        n+=1
    return retorno

fechas = query_pie_chart(start_date, end_date)



# Etapa de login

driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
driver.get(URL)
user = driver.find_element_by_xpath("/html/body/div/div[1]/div/div/div/div/form/div[1]/label/div/input")
user.send_keys(usuario)
pas = driver.find_element_by_xpath("/html/body/div/div[1]/div/div/div/div/form/div[2]/label/div/input")
pas.send_keys(constrasena)
login = driver.find_element_by_xpath("/html/body/div/div[1]/div/div/div/div/form/div[3]/ax-submit-button")
login.click()
driver.get(dashboard)
barra_carga(15)

# Etapa de recuperación de base
# Test
"""
filter_btn = driver.find_element_by_xpath(filter_button)
filter_btn.click()
date_input_fechas = driver.find_element_by_xpath(date_input)
date_input_fechas.clear()
date_input_fechas.send_keys(fechas[0])
applybtn = driver.find_element_by_xpath(apply_btn)
applybtn.click()
barra_carga(10)
export_btn = driver.find_element_by_xpath(boton_descargas)
export_btn.click()
excel_btn = driver.find_element_by_xpath(excel_download)
excel_btn.click()
"""

z = 0 #Cambiar a 0
for i in range(len(fechas)):
    print("Voy en la base número: " + str(z))
    if z == 0: #Cambiar a 0
        filter_btn = driver.find_element_by_xpath(filter_button)
        filter_btn.click()
    date_input_fechas = driver.find_element_by_xpath(date_input)
    date_input_fechas.clear()
    date_input_fechas.send_keys(fechas[i])
    applybtn = driver.find_element_by_xpath(apply_btn)
    applybtn.click()
    barra_carga(10)
    export_btn = driver.find_element_by_xpath(boton_descargas)
    export_btn.click()
    excel_btn = driver.find_element_by_xpath(excel_download)
    excel_btn.click()
    barra_carga(5)
    shutil.move(path_descargas + "chart_data-volume-all-categories.xlsx", path_destino + "chart_data-volume-all-categories.xlsx")
    old_name = path_destino + "chart_data-volume-all-categories.xlsx"
    new_name = path_destino + "archivo_" + str(z) + ".xlsx"
    os.rename(old_name, new_name)
    z+=1
    
#with open(path_destino + "Semanas_descargadas.txt") as f:
#    for element in fechas:
#        f.write(element + "\n")


"""
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
driver.get(URL)

user = driver.find_element_by_xpath("/html/body/div/div[1]/div/div/div/div/form/div[1]/label/div/input")
user.send_keys(usuario)
pas = driver.find_element_by_xpath("/html/body/div/div[1]/div/div/div/div/form/div[2]/label/div/input")
pas.send_keys(constrasena)
login = driver.find_element_by_xpath("/html/body/div/div[1]/div/div/div/div/form/div[3]/ax-submit-button")
login.click()

for single_date in daterange(start_date, end_date):
    print("Estoy en esta fecha: " + single_date.strftime("%Y-%m-%d"))
    actual = single_date.strftime("%Y-%m-%d")
    print('Refrescando...')
    barra_carga(1)
    driver.implicitly_wait(3)
    #driver.refresh()
    descarga = driver.find_element_by_xpath(boton_descargas)
    descarga.click()
    barra_carga(3)
    shutil.move(path_descargas + "geoMap.csv", path_destino + "geoMap.csv")
    old_name = path_destino + "\geomap.csv"
    new_name = path_destino + "\dia " + actual + ".csv"
    os.rename(old_name, new_name)
    barra_carga(2)
"""