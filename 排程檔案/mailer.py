import time, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import requests
import pandas as pd
import smtplib
from email.mime.text import MIMEText




def mailer(subject, html, mailto='jiangzero@gmail.com', mailfrom='jiangsir@tea.nknush.kh.edu.tw', passwd='igajmuqzhnhuyzil'):
    mime=MIMEText(html, "html", "utf-8")
    mime["Subject"]=subject
    mime["From"]="教師研習自動通知"
    mime["To"]=""
    msg=mime.as_string()

    smtpssl=smtplib.SMTP_SSL("smtp.gmail.com", 465) 
    smtpssl.ehlo()
    smtpssl.login(mailfrom, passwd)

    to_addr=[mailto]
    status=smtpssl.sendmail(mailfrom, to_addr, msg)
    if status=={}:
        print("郵件傳送成功!")
    else:
        print("郵件傳送失敗!")
    smtpssl.quit()    

def query(driver, keyword):
    driver.get("https://www4.inservice.edu.tw/NAPP/OpenQuery.aspx")
    driver.find_element_by_id("ctl00_CPH_Content_RTB_CourseName").click()
    driver.find_element_by_id("ctl00_CPH_Content_RTB_CourseName").clear()
    driver.find_element_by_id("ctl00_CPH_Content_RTB_CourseName").send_keys(keyword)
    driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='顯示更多方式'])[1]/following::span[1]").click()
    element = driver.find_element_by_xpath('//*[@id="ctl00_CPH_Content_RG_SearchResult_ctl00"]')
    html = element.get_attribute('outerHTML')
    return pd.read_html(html)

driver = webdriver.Chrome(executable_path="C:\\Users\\jiangsir\\Anaconda3\\chromedriver.exe")
driver.implicitly_wait(30)
verificationErrors = []
accept_next_alert = True

keywords = ["人工智慧", "物聯網"]

df = pd.DataFrame()
for keyword in keywords:
    df1 = query(driver, keyword)
    if df.empty:
        df = df1[0]
    else:
        df = pd.concat([df, df1[0]])

#driver.close()
driver.quit()

mailer("教師研習網篩選通知("+str(keywords)+")", df.to_html())

