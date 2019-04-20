import requests, json, os, datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

# 將 20190420-myserviceaccount.json 檔案的內容放置在此，設定為一個 dict
service_account_keyfile_dict = {
  "type": "service_account",
  "project_id": "symmetric-blade-238115",
  "private_key_id": "7aa6052dda19ea67769e758b0ff0c91813878087",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDC30GQ8qDy1O3i\npN7wkeebTUe9rOGuj6yjZnW5a2R88i26Ozd9mEiPqhRbY458GACO9FMlcxxizSxB\n3ccJpWfZDCUQGLBDSifAjFNBT5oUxUNohQQ+fgRth6O3WBT7v7mwnamZnJrBRNI8\nhzyNTXiiYM0iBVnxoHlv8FPFQ1LeNGsfmyHG9aQyVfAUUsA4oF5FsLGT/SrxLMZH\nvkl3KcmGPWE30Z2bQBuwpx5bRgubfUbSCSk9WOMBirheFmd1rz/dUmlTSZzJrvAo\nEuHlBED7ODyY1AOuOT69BiKvMonGRTeuecjGwZaaX5vBKxThLbay0qYaF4vI3Psk\noRqt5pfXAgMBAAECggEAVBAY6Z0wvvAJmn6CyYY3QfBJZVIhnLrPv0EgwZbJJ3kV\nLsQCwQQjMQ4ub+n3eiKkgwZ0o7APa7OURumTxd57eM7bYiE0UCK6GT6vX3omPpWF\n6Z2P4iFcaZ9ciWfOzXa8dKrekaxTudGlW4T/Ivlrc6iMdQOX9DrEh/xFNtA+/Ckg\nUN9v/VzA6EQobUdzDLBAMqSKtvc11mqrDGiK05n5ZUB/JaBUbsLfC/qD33dns/c2\nedEbUfKOjbeKuFrtA1TUJIw+/gPK+bks4pIwwb3PLOMaV1dqdRClL9NobAowCejf\naoxSfSGiBwUJhkQ0nabhHWOnyl1/u0z449EpXEjV+QKBgQD91zaqxqD25lLtIQTW\nHtD8rX2UE+r2bfauI+9CLZVfYBi0+ptBe2sMuGKmoSeB37HraJ2IxI9ArUEmJ9SC\nA7k4JjHcbiocr85fShlzoC/iYLTAfgkbYMHhswoWhnpr2L2GNqKNkSLdo0nM+IiY\nod8SfGCcbm2RXhiIhq/K6jxxlQKBgQDEh6CTGffpse140XUDC/PwK3wwBcyZdqWr\nH5oLVXPzpC8L5bUdPn2PRkXmVi70HrSLAXhnCwxwXoA005Fci8wJbGHC2kkw0Wgu\nKuN+/EPXCmpawBIS/lvljRlENPAvo5OwPeq6EaR9P8n3I9wBUKJngQtePK4+CL9S\nHFNnthkguwKBgGXS28H7dXw0/hTTBu6hY/HH4jTxHHKHv8kw7vvb7yxYDvEiCf9l\nc5ahrCjtQjzNr8Afsfm350LpfNXCanNQ7Q6B+8RRiKEDQMRmo/kGy86CPl9s71hF\nIuDXgfdxMFBsm/HnnqMtEhBYPPV0yM55OFNhAxwdC+ShGzRA2umJtn9VAoGAMj3B\n7RksaY/U95gEY90AZZuYSeaRoYHVZGPVy6Py2oxUgqQcovdAvgnnALVzl3DqEscz\ncpQ+f9OIzvhvJsuOQ7JzY47OOy6thW/tbJ8s8KJ3AfAsLrLb51kk5mzqIiOdM+cA\nRMUR2fsetJF0QtnMSs2QjGzS1oUB9AnNwKuqzNUCgYEAnVXVJKpgeNX7WDuEvCwC\nevARa78ot3dYLBtJjXld+a3khvabL5Yuw6lOG8HDaLtIRadHgwq4ck3APrrfGrky\n1YroXqRijdoz3m879Y/aUhDky7xS+2oL1H1pRAaj74GwicR2pxEPj8nGDJBPIVSb\nIrTiUdmaOjS5VtqEcp+Ep2E=\n-----END PRIVATE KEY-----\n",
  "client_email": "myserviceaccount@symmetric-blade-238115.iam.gserviceaccount.com",
  "client_id": "111777969878742573169",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/myserviceaccount%40symmetric-blade-238115.iam.gserviceaccount.com"
}
credentials = ServiceAccountCredentials.from_json_keyfile_dict(service_account_keyfile_dict, scope)

gc = gspread.authorize(credentials)
url = 'https://docs.google.com/spreadsheets/d/1Lp42K9Q2fFlfn6wtVYDlmD37Kn9znzzIfZHozfkphl0/edit?usp=sharing'
doc = gc.open_by_url(url)
wks = doc.worksheet('sheet1')
wks.update_acell('A1', '測站')
wks.update_acell('B1', 'PM25')
wks.update_acell('C1', '資料源更新時間')
wks.update_acell('D1', '上傳時間')


# 若來源資料為 https 則加上 verify=False 參數
response = requests.get('https://opendata.epa.gov.tw/ws/Data/ATM00625/?$format=json', verify=False)
sites = response.json()
for site in sites:
    if site['Site'] == '林園':
        wks.insert_row([site['Site'],  site['PM25'], site['DataCreationDate'], str(datetime.datetime.now())], 2)
        print(site)
