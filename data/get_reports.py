from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
from time import sleep


data = pd.read_csv('ligue-1/ligue1-reports.csv',encoding='utf-8').to_numpy()

for i in range(275, len(data)):
    url = data[i][32]
    
    driver = webdriver.Chrome(executable_path=r"C:\Users\Danilo\Downloads\chromedriver_win32\chromedriver.exe")
    driver.implicitly_wait(0.5)
    driver.get(url)
    driver.maximize_window()

    if '365_euro' in url:
        position_info = driver.find_element_by_class_name('sr_preset').text
    else:
        continue

    if 'vs. Goalkeepers' == position_info:
        pos = 'GK'
    elif 'vs. Center Backs' == position_info:
        pos = 'CB'
    elif 'vs. Fullbacks' == position_info:
        pos = 'FB'
    elif 'vs. Midfielders' == position_info:
        pos = 'MF'
    elif 'vs. Att Mid / Wingers' == position_info:
        pos = 'AM'
    elif 'vs. Forwards' == position_info:
        pos = 'FW'
    else:
        continue

    share_button = driver.find_element_by_xpath('//*[@id="scout_full_' + pos + '_sh"]/div/ul/li[2]/span')

    a = ActionChains(driver)
    a.move_to_element(share_button).perform()
    sleep(2)

    csv_button = driver.find_element_by_xpath('//*[@id="scout_full_' + pos +'_sh"]/div/ul/li[2]/div/ul/li[4]/button')
    a.move_to_element(csv_button).click().perform()

    report = driver.find_element_by_tag_name('pre').text

    name_list = data[i][0].split(' ')
    file_name = name_list[0].lower() + '-' + name_list[-1].lower() + '-euro-365.csv'

    f = open(file_name, "w")
    f.write(report)
    f.close()

    driver.quit()
    sleep(10)