from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import random
import re
from Notify import LINENotifyBot

# USERNAME = "A19DC154"
# PASSWORD = "Ryuya1045_"
# USERNAME = "A19DC558"
# PASSWORD = "93041419"

users = [
    {"USERNAME": "A19DC154", "PASSWORD": "Ryuya1045_"},
    {"USERNAME": "A19DC558", "PASSWORD": "93041419"},
]

myself = "amHdHYRhdd9aqJImvTI2jhSlI0lciHHoEqbZnIoYSO0"  # dhw
bot = LINENotifyBot(access_token=myself)

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
url = 'https://portal.dhw.ac.jp/uprx/up/pk/pky001/Pky00101.xhtml'
driver.implicitly_wait(3)  # 3-5
wait = WebDriverWait(driver, 3)

MESSAGE = ''


def login(username, password):
    global MESSAGE
    driver.get(url)
    # driver.maximize_window()

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
    MESSAGE += login_user[:login_user.find('ん') + 1]


def back_home():
    wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="headerForm"]/header/a')))
    main = driver.find_element_by_xpath('//*[@id="headerForm"]/header/a')
    driver.execute_script("arguments[0].click();", main)
    sleep(0.5)


def answer_fb():
    global MESSAGE

    wait.until(expected_conditions.visibility_of_element_located((By.ID, 'headerForm:j_idt67')))  # ID:top img
    webElement = driver.find_element_by_xpath(
        '//*[@id="menuForm:mainMenu"]/ul/li[5]/ul/table/tbody/tr/td[3]/ul/li[2]/a')  # お知らせ―>アンケート回答ボタン
    driver.execute_script("arguments[0].click();", webElement)
    sleep(1)

    wait.until(expected_conditions.visibility_of_element_located((By.ID, 'funcForm:j_idt570')))  # 回答対象アンケートからの全体範囲
    sleep(0.5)
    if driver.find_element_by_id('funcForm:j_idt575:j_idt578:0:j_idt579_header'):  # フィードバックシートの黒いバー
        get_remaining_fb = len(driver.find_elements_by_class_name('ui-panelgrid-even'))  # check later when its mulitple
        if len(driver.find_elements_by_class_name('ctgrHeaderGrid')) == 2:
            get_remaining_fb -= 1

        print("\nDetected {} Feedback-Sheet\n".format(get_remaining_fb))
        # MESSAGE += "\nDetected {} Feedback-Sheet\n".format(get_remaining_fb)

        fbs_list_num = 0
        subjects = [
            "フィードバックシート（捜査と裁判）",
        ]
        for i in range(get_remaining_fb):

            fbs = driver.find_element_by_id(
                'funcForm:j_idt575:j_idt578:{}:j_idt580'.format(fbs_list_num))  # 一番上にあるフィードバックシート

            get_fin_or_yet = driver.find_element_by_xpath(
                '//*[@id="funcForm:j_idt575:j_idt578:0:j_idt580"]/tbody/tr/td[3]'.format(
                    fbs_list_num)).text  # 一番上にあるフィードバックシートの回答済みか
            if get_fin_or_yet == '回答済':
                print("All answered")
                MESSAGE += "\nFb全回答済\n"
                break

            driver.execute_script("arguments[0].click();", fbs)
            wait.until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'enqHeaderTitle')))

            try:
                driver.find_element_by_xpath('//*[@id="funcForm:enqQuestList:0:j_idt675"]/tbody/tr[1]/td[1]/div')  # ボタン
                driver.find_element_by_xpath('//*[@id="funcForm:enqQuestList:2:j_idt675"]/tbody/tr[2]/td[1]/div')
                driver.find_element_by_xpath('//*[@id="funcForm:enqQuestList:3:j_idt675"]/tbody/tr[1]/td[1]/div')
            except:
                fb_title = driver.find_element_by_xpath(
                    '//*[@id="funcForm:j_idt645"]/div/div[1]/table[1]/tbody/tr/td/span').text  # fbシートのタイトル
                if fb_title in subjects:
                    driver.find_element_by_name('funcForm:j_idt706').click()  # submit_btn
                    wait.until(
                        expected_conditions.visibility_of_element_located((By.NAME, 'funcForm:j_idt711:j_idt712')))
                    ok1_btn = driver.find_element_by_name('funcForm:j_idt711:j_idt712')  # ok1
                    driver.execute_script("arguments[0].click();", ok1_btn)
                    wait.until(
                        expected_conditions.visibility_of_element_located((By.NAME, 'funcForm:j_idt716:j_idt717')))
                    ok2_btn = driver.find_element_by_name('funcForm:j_idt716:j_idt717')  # ok2
                    driver.execute_script("arguments[0].click();", ok2_btn)

                    wait.until(expected_conditions.visibility_of_element_located(
                        (By.ID, 'funcForm:j_idt570')))  # 全体範囲
                    continue
                else:
                    print("{}\n上記授業は通常フォーマットに該当しません スキップします\n".format(fb_title))
                    fbs_list_num += 1
                    driver.find_element_by_xpath(
                        '//*[@id="functionHeaderForm:breadCrumb"]/ul/li[1]/a').click()  # 左上アンケート回答一覧リンク
                    continue

            driver.find_element_by_xpath(
                '//*[@id="funcForm:enqQuestList:0:j_idt675"]/tbody/tr[1]/td[1]/div').click()  # 理解できた
            driver.find_element_by_xpath(
                '//*[@id="funcForm:enqQuestList:2:j_idt675"]/tbody/tr[2]/td[1]/div').click()  # 適切だった

            random_select_num = random.randrange(1, 6, 2)
            driver.find_element_by_xpath(
                '//*[@id="funcForm:enqQuestList:3:j_idt675"]/tbody/tr[{}]/td[1]/div'.format(random_select_num)).click()
            # print("今回は{}番目の選択を選びました。".format(random_select_num))

            driver.find_element_by_name('funcForm:j_idt706').click()  # submit_btn
            wait.until(expected_conditions.visibility_of_element_located((By.NAME, 'funcForm:j_idt711:j_idt712')))
            ok1_btn = driver.find_element_by_name('funcForm:j_idt711:j_idt712')  # ok1
            driver.execute_script("arguments[0].click();", ok1_btn)
            wait.until(expected_conditions.visibility_of_element_located((By.NAME, 'funcForm:j_idt716:j_idt717')))
            ok2_btn = driver.find_element_by_name('funcForm:j_idt716:j_idt717')  # ok2
            driver.execute_script("arguments[0].click();", ok2_btn)

            wait.until(
                expected_conditions.visibility_of_element_located((By.ID, 'funcForm:j_idt570')))  # 全体範囲

            print("Submit")
            MESSAGE += "Submit\n"
    else:
        print("\n---- FB not existing ----\n")
        MESSAGE += "\n---- FB not existing ----\n"

    back_home()


def check_hw():
    global MESSAGE

    wait.until(expected_conditions.element_to_be_clickable(
        (By.ID, 'funcForm:j_idt361:j_idt2402:0:j_idt2481')))  # 一番上のクラスのクラスプロファイル
    driver.find_element_by_id('funcForm:j_idt361:j_idt2402:0:j_idt2481').click()

    click_num = len(driver.find_elements_by_class_name('classList'))

    class_name_before = ''
    for nextClass_click in range(click_num):
        if nextClass_click != click_num - 1:
            wait.until(expected_conditions.element_to_be_clickable((By.ID, 'functionHeaderForm:j_idt154')))  # 次の授業をクリック
        class_name = driver.find_element_by_xpath('//*[@id="functionHeaderForm:j_idt137"]/div[1]').text  # 左上のクラス名
        class_name = '\n' + re.sub('\d', '', class_name).replace('ui-button', '').replace('　', '').replace(' ', '')

        if class_name == class_name_before:
            class_name_before = class_name
            if nextClass_click != click_num - 1:
                driver.find_element_by_id('functionHeaderForm:j_idt154').click()  # 次の授業をクリック
            continue

        flag = False
        for class_element in range(7):
            content = driver.find_element_by_id('funcForm:j_idt329:{}:j_idt331'.format(class_element))  # 一つ一つの青丸
            content_name = content.find_element_by_class_name('inlineBlock').text
            try:
                remain_hw = content.find_element_by_class_name('remainCount').text
                remain_hw_count = re.compile('\d+').findall(remain_hw)[0]
                if remain_hw_count != '0':
                    if flag == False:
                        print(class_name)
                        MESSAGE += class_name
                        flag = True
                    print("・{}が終了していません".format(content_name))
                    print("・{}".format(remain_hw))
                    MESSAGE += "・{}が終了していません\n".format(content_name)
                    MESSAGE += "・[{}]\n".format(remain_hw)
                    if content_name != '課題提出':
                        continue
                    content.click()
                    wait.until(expected_conditions.element_to_be_clickable(
                        (By.ID, 'functionHeaderForm:j_idt148')))  # 左上のTOPボタン
                    for hw_num in range(int(remain_hw_count)):
                        hw_name = driver.find_element_by_id(
                            'funcForm:gakKdiTstList:{}:j_idt370'.format(hw_num)).text.replace(' ', '') + ' '  # 課題名
                        hw_deadline = driver.find_element_by_xpath(
                            '//*[@id="funcForm:gakKdiTstList_data"]/tr[{}]/td[6]/span'.format(
                                hw_num + 1)).text  # 課題提出終了日時
                        print('{}が{}までです'.format(hw_name, hw_deadline))
                        MESSAGE += '・{}が{}までです\n'.format(hw_name, hw_deadline)
                    driver.find_element_by_id('functionHeaderForm:j_idt148').click()  # 左上のTOPボタン

            except:
                try:
                    element = content.value_of_css_property('background-size')
                    if element != '80px':
                        if flag == False:
                            print(class_name)
                            MESSAGE += class_name
                            flag = True
                        print("・{}に新しい内容があります".format(content_name))
                        MESSAGE += "・{}に新しい内容があります\n".format(content_name)
                except:
                    pass

        class_name_before = class_name
        if nextClass_click != click_num - 1:
            driver.find_element_by_id('functionHeaderForm:j_idt154').click()  # 次の授業をクリック

    back_home()


def fin_action():
    global MESSAGE

    sleep(0.5)
    print("\nProcess Finished\n")
    # MESSAGE += "\nProcess Finished"
    driver.quit()


def test():
    print("hi")


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
