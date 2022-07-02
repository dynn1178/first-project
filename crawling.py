from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime
from bs4 import BeautifulSoup
import openpyxl

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("window-size=1920x1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.141 Whale/3.15.136.29 Safari/537.36")

a = 0
d_today = datetime.date.today()
wb = openpyxl.load_workbook("E:\\업무폴더\\0. Tableau\\1. data\\price.xlsx")
sheet = wb['참좋은']
list = ['APP2091', 'JPP022']

for a in range(len(list)): # list 수 만큼 반복
    driver = webdriver.Chrome("E:\\업무폴더\\3.Python\\chromedriver.exe", options=options)
    driver.get("https://m.verygoodtour.com/Product/PackageMaster?MasterCode="+list[a]+"&dType=L&Calendar=Y")
    time.sleep(5)  # 5초 딜레이

    for i in range(4):  # 개월 수 
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        res = soup.find_all(class_="tours_info_wrap sky")
        year = soup.select_one("div.month").get_text().strip()[:4]

        for b in range(len(res)):  # 긁어오는 항목 
            date_n = str(year)+"-"+res[b].find("span", attrs={"class":"first_line"}).get_text().replace(".","-")[:-3] # 날짜
            title_n = res[b].find("div", attrs={"class":"tour_tit"}).get_text().strip() # 제목
            period_n = res[b].find("span", attrs={"class":"period"}).get_text().strip().replace(" ","") # 패턴
            price_n = res[b].find("div", attrs={"class":"price"}).get_text().strip().replace(",","")[:-2] # 가격
            air_n = res[b].find("p", attrs={"class":"airline"}).get_text().strip().replace("\n","").replace("  ","(").replace(" ","")+")" # 항공
            air_m = air_n[:2] # 항공2
            status_n = res[b].find("div", attrs={"class":"status"}).get_text().strip() #상태
            sheet.append([d_today, list[a], date_n, title_n, period_n, int(price_n), air_m, air_n, status_n]) # 엑셀로 넘기기 
            wb.save("E:\\업무폴더\\0. Tableau\\1. data\\price.xlsx") # 엑셀 저장

        driver.find_element(By.XPATH, "//*[@id='content']/div/div[2]/div[1]/div/button[2]").click() #다음 페이지로 넘김
        time.sleep(3)    # 3초 딜레이



