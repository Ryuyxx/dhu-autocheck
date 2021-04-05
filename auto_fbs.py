from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from time import sleep
import random
import re, os
# from dotenv import load_dotenv
from Notify import LINENotifyBot

# load_dotenv()

users = [
    {"USERNAME": os.environ["User1"], "PASSWORD": os.environ["User1P"]},
    {"USERNAME": os.environ["User2"], "PASSWORD": os.environ["User2P"]},
]

myself = os.environ["lineAPI"]
bot = LINENotifyBot(access_token=myself)

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
url = os.environ["DHWURL"]
driver.implicitly_wait(3)
wait = WebDriverWait(driver, 3)

MESSAGE = ''


def java_click_by_2classname(id1, id2):
    element = driver.find_element_by_class_name(id1).find_element_by_class_name(id2)
    driver.execute_script("arguments[0].click();", element)
    sleep(0.5)


def login(username, password):
    global MESSAGE
    driver.get(url)

    webElement = 'loginForm:userId'
    wait.until(expected_conditions.visibility_of_element_located(
        (By.NAME, webElement)))
    user_input = driver.find_element_by_name(webElement)
    user_input.send_keys(username)

    pwd_input = driver.find_element_by_name('loginForm:password')
    pwd_input.send_keys(password)
    login_btn = driver.find_element_by_name('loginForm:loginButton')
    driver.execute_script("arguments[0].click();", login_btn)

    sleep(1)
    login_user = driver.find_element_by_class_name('loginInfo').text
    print(login_user[:login_user.find('ん') + 1] + " 自動処理実行します。")
    MESSAGE += login_user[:login_user.find('ん') + 1] + '\n'


def back_home():
    wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="headerForm"]/header/a')))
    main = driver.find_element_by_xpath('//*[@id="headerForm"]/header/a')
    driver.execute_script("arguments[0].click();", main)
    sleep(0.5)


def fbsubmit(title):
    global MESSAGE
    # 回答ボタン
    driver.find_element_by_class_name('btnAltColor').click()
    # アンケートで不要な回答は削除されます。
    java_click_by_2classname('dlgCaution', 'ui-button-text-icon-left')
    # 回答します。よろしいですか?
    java_click_by_2classname('dlgWarning', 'ui-button-text-icon-left')
    # アンケート回答一覧バーを待機
    wait.until(expected_conditions.visibility_of_element_located(
        (By.ID, 'functionHeaderForm:breadCrumb')))
    # 回答した情報を更新させるために再度アンケート回答クリック
    webElement = driver.find_element_by_xpath(
        '//*[@id="menuForm:mainMenu"]/ul/li[5]/ul/table/tbody/tr/td[4]/ul/li[2]/a')
    driver.execute_script("arguments[0].click();", webElement)
    sleep(1)
    print("\n・{} を提出しました\n".format(title))
    MESSAGE += "\n・{} を提出しました\n".format(title)


def answer_fb():
    global MESSAGE
    MESSAGE += '\n\n《フィードバックシート》\n'
    # 左上ロゴ
    wait.until(
        expected_conditions.visibility_of_element_located((By.ID, 'headerForm:j_idt67')))
    # アンケート回答
    webElement = driver.find_element_by_xpath(
        '//*[@id="menuForm:mainMenu"]/ul/li[5]/ul/table/tbody/tr/td[4]/ul/li[2]/a')
    driver.execute_script("arguments[0].click();", webElement)
    sleep(1)

    # アンケート回答一覧
    wait.until(expected_conditions.visibility_of_element_located(
        (By.ID, 'functionHeaderForm:breadCrumb')))
    sleep(0.5)

    try:
        # FBシートタブ
        fb_block = driver.find_elements_by_class_name('ui-datatable-data')[0]
        # tdのタグの数で対象の個数を確認 1の場合は無し
        td_tags = fb_block.find_elements_by_tag_name('td')
        remaining_fb = 0 if len(td_tags) == 1 else int(len(td_tags) / 4)
        if remaining_fb == 0:
            print("\nフィードバックシートはすべて回答されています😉\n")
            MESSAGE += "\nフィードバックシートはすべて回答されています😉\n"
        else:
            MESSAGE += "\n{}個フィードバックシートが残っています🙁\n".format(remaining_fb)

            for i in remaining_fb:
                tds = driver.find_elements_by_class_name('ui-datatable-data')[0].find_elements_by_tag_name(
                    'tr').find_elements_by_tag_name('td')

                deadline_texts = tds[3].text[3:]
                tds[0].click()

                title = driver.find_element_by_class_name('enqHeaderTitle').text
                title = title[:title.find("[") - 1]

                # 自動入力部
                try:
                    q1 = driver.find_elements_by_class_name('ui-selectoneradio')[0]
                    q3 = driver.find_elements_by_class_name('ui-selectoneradio')[1]
                    q4 = driver.find_elements_by_class_name('ui-selectoneradio')[2]
                except:
                    print("・{}\n上記授業は通常フォーマットに該当しません スキップします\n".format(title))
                    MESSAGE += "\n・{}はスキップされます\n".format(title)
                    # 一覧へ戻る
                    driver.find_element_by_xpath(
                        '//*[@id="functionHeaderForm:breadCrumb"]/ul/li[1]/a').click()
                    deadlineCount = int(re.compile('\d+').findall(re.findall("（.*）", deadline_texts)[0])[0])
                    if deadlineCount <= 1:
                        MESSAGE += "⚠️{}\n\n".format(deadline_texts.replace('2021/', ''))
                    else:
                        MESSAGE += "・{}\n\n".format(deadline_texts.replace('2021/', ''))
                    print("・{}\n\n".format(deadline_texts.replace('2021/', '')))
                    continue

                q1.find_elements_by_class_name('ui-radiobutton')[0].click()
                q3.find_elements_by_class_name('ui-radiobutton')[1].click()
                random_select_num = random.randrange(0, 5, 2)
                q4.find_elements_by_class_name('ui-radiobutton')[random_select_num].click()

                fbsubmit(title)

            if len(driver.find_elements_by_class_name('signStillAns')) > 0:
                print("\n未回答が残っています😱\n")
                MESSAGE += "\n未回答が残っています😱\n"
            else:
                print("\nすべて回答されました😎\n")
                MESSAGE += "\nすべて回答されました😎\n"
    except:
        print("\n- エラーが発生しました\n")
        MESSAGE += "\n・エラーが発生しました\n"

    back_home()


def check_hw():
    any_notice = 0
    global MESSAGE
    MESSAGE += '\n\n《授業関連》\n'

    wait.until(expected_conditions.element_to_be_clickable(
        (By.ID, 'funcForm:j_idt361:j_idt2402:0:j_idt2481')))
    driver.find_element_by_id('funcForm:j_idt361:j_idt2402:0:j_idt2481').click()

    click_num = len(driver.find_elements_by_class_name('classList'))

    class_name_before = ''
    for nextClass_click in range(click_num):
        if nextClass_click != click_num - 1:
            wait.until(expected_conditions.element_to_be_clickable((By.ID, 'functionHeaderForm:j_idt154')))
        class_name = driver.find_element_by_xpath('//*[@id="functionHeaderForm:j_idt137"]/div[1]').text
        class_name = '\n' + re.sub('\d', '', class_name).replace('ui-button', '').replace('　', '').replace(' ', '')

        if class_name == class_name_before:
            class_name_before = class_name
            if nextClass_click != click_num - 1:
                driver.find_element_by_id('functionHeaderForm:j_idt154').click()
            continue

        flag = False
        for class_element in range(7):
            content = driver.find_element_by_id('funcForm:j_idt329:{}:j_idt331'.format(class_element))
            content_name = content.find_element_by_class_name('inlineBlock').text
            try:
                remain_hw = content.find_element_by_class_name('remainCount').text
                remain_hw_count = re.compile('\d+').findall(remain_hw)[0]
                if remain_hw_count != '0':
                    if flag == False:
                        print(class_name)
                        MESSAGE += class_name
                        any_notice += 1
                        flag = True
                    print("・{}が終了していません".format(content_name))
                    print("・{}".format(remain_hw))
                    MESSAGE += "・{}が終了していません\n".format(content_name)
                    MESSAGE += "・[{}]\n\n".format(remain_hw)
                    any_notice += 1
                    if content_name != '課題提出':
                        continue
                    content.click()
                    wait.until(expected_conditions.element_to_be_clickable(
                        (By.ID, 'functionHeaderForm:j_idt148')))
                    for hw_num in range(int(remain_hw_count)):
                        hw_name = driver.find_element_by_id(
                            'funcForm:gakKdiTstList:{}:j_idt370'.format(hw_num)).text.replace(' ', '') + ' '
                        hw_deadline = driver.find_element_by_xpath(
                            '//*[@id="funcForm:gakKdiTstList_data"]/tr[{}]/td[6]/span'.format(
                                hw_num + 1)).text
                        print('{}が{}までです'.format(hw_name, hw_deadline))
                        MESSAGE += '・{}が{}までです\n\n'.format(hw_name, hw_deadline)
                        any_notice += 1
                    driver.find_element_by_id('functionHeaderForm:j_idt148').click()

            except:
                try:
                    element = content.value_of_css_property('background-size')
                    if element != '80px':
                        if flag == False:
                            print(class_name)
                            MESSAGE += class_name
                            any_notice += 1
                            flag = True
                        print("・{}に新しい内容があります".format(content_name))
                        MESSAGE += "・{}に新しい内容があります\n".format(content_name)
                        any_notice += 1
                except:
                    pass

        class_name_before = class_name
        if nextClass_click != click_num - 1:
            driver.find_element_by_id('functionHeaderForm:j_idt154').click()

    back_home()
    if any_notice == 0:
        MESSAGE += '\n授業関連でのお知らせはありません\n'


def fin_action():
    sleep(0.5)
    print("\nProcess Finished\n")
    driver.quit()


def send_to_line():
    global MESSAGE
    bot.send(
        message=MESSAGE
    )
    MESSAGE = ''


if __name__ == '__main__':
    for user in users:
        login(user["USERNAME"], user["PASSWORD"])
        answer_fb()
        check_hw()
        send_to_line()
    fin_action()
