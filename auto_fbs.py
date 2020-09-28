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

users = [
    {"USERNAME": "A19DC154", "PASSWORD": "Ryuya1045_"},
    {"USERNAME": "A19DC558", "PASSWORD": "93041419"},
    {"USERNAME": "A19DC132", "PASSWORD": "ameneko0422"},
]

myself = "cOSdNL5uBPUeNOClZCXQHKQwaTOXXjn6AsZl8uctdQ5"  # dhw
bot = LINENotifyBot(access_token=myself)

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
# driver = webdriver.Chrome()
url = 'https://portal.dhw.ac.jp/uprx/up/pk/pky001/Pky00101.xhtml'
driver.implicitly_wait(3)  # 3-5
wait = WebDriverWait(driver, 3)

MESSAGE = ''


def java_click_byclassname2(id1, id2):
    # wait.until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, id1)))
    element = driver.find_element_by_class_name(id1).find_element_by_class_name(id2)
    driver.execute_script("arguments[0].click();", element)
    sleep(0.5)


def fbsubmit():
    global MESSAGE
    fb_title = driver.find_element_by_class_name('enqHeaderTitle').text  # fb授業名 [NON CHANGED]
    driver.find_element_by_class_name('btnAltColor').click()  # 回答ボタン [NON CHANGED]
    java_click_byclassname2('dlgCaution', 'ui-button-text-icon-left')  # ok1 [NON CHANGED]
    java_click_byclassname2('dlgWarning', 'ui-button-text-icon-left')  # ok2 [NON CHANGED]
    wait.until(expected_conditions.visibility_of_element_located(
        (By.ID, 'functionHeaderForm:breadCrumb')))  # アンケート回答一覧バー [NON CHANGED]
    print("Submit")
    MESSAGE += "\n・{} を提出しました\n".format(fb_title)


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
    MESSAGE += login_user[:login_user.find('ん') + 1] + '\n'


def back_home():
    wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="headerForm"]/header/a')))
    main = driver.find_element_by_xpath('//*[@id="headerForm"]/header/a')
    driver.execute_script("arguments[0].click();", main)
    sleep(0.5)


def answer_fb():
    global MESSAGE
    MESSAGE += '\n\n《フィードバックシート》\n'
    wait.until(
        expected_conditions.visibility_of_element_located((By.ID, 'headerForm:j_idt67')))  # ID:top img [NON CHANGED]
    webElement = driver.find_element_by_xpath(
        '//*[@id="menuForm:mainMenu"]/ul/li[5]/ul/table/tbody/tr/td[3]/ul/li[2]/a')  # お知らせ―>アンケート回答ボタン [NON CHANGED]
    driver.execute_script("arguments[0].click();", webElement)
    sleep(1)

    wait.until(expected_conditions.visibility_of_element_located(
        (By.ID, 'functionHeaderForm:breadCrumb')))  # アンケート回答一覧バー [NON CHANGED]
    sleep(0.5)
    if driver.find_element_by_class_name('ctgrHeaderGrid'):  # フィードバックシートの横バー [NON CHANGED]
        get_remaining_fb = len(
            driver.find_elements_by_class_name('ui-panelgrid-even'))  # check len of fbs [NON CHANGED]
        if len(driver.find_elements_by_class_name('ctgrHeaderGrid')) > 1:  # フィードバックシートの横バー [NON CHANGED]
            get_remaining_fb -= 1

        print("\nDetected {} Feedback-Sheet\n".format(get_remaining_fb))
        # MESSAGE += "\nDetected {} Feedback-Sheet\n".format(get_remaining_fb)

        fbs_list_num = 0
        subjects = [
            "フィードバックシート（捜査と裁判）",
        ]
        self_subjects = {
            "フィードバックシート（Webデザイン概論）",
        }
        for i in range(get_remaining_fb):

            fbss = driver.find_elements_by_class_name('enqName')  # フィードバックシートリスト取得 [NON CHANGED]

            fin_or_yets = driver.find_elements_by_class_name('sign')[fbs_list_num].text  # 一番上にあるフィードバックシートの回答済みか [NON CHANGED]
            if fin_or_yets == '回答済':
                text = "All answered"
                msg_text = "\nフィードバックシートはすべて回答されています😉\n"
                if fbs_list_num != 0:
                    text = "Remaining {} Feedback Sheet".format(fbs_list_num)
                    msg_text = "\n{}個フィードバックシートが残っています🙁\n".format(fbs_list_num)
                print(text)
                MESSAGE += msg_text
                break

            fbss[fbs_list_num].click()
            wait.until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'enqHeaderTitle')))  # fb授業名表示されるまで [NON CHANGED]
            fb_title = driver.find_element_by_class_name('enqHeaderTitle').text  # fb授業名 [NON CHANGED]

            try:
                q1 = driver.find_elements_by_class_name('ui-selectoneradio')[0]  # ボタン選択式エリアがあるか [NON CHANGED]
                q3 = driver.find_elements_by_class_name('ui-selectoneradio')[1]  # ボタン選択式エリアがあるか [NON CHANGED]
                q4 = driver.find_elements_by_class_name('ui-selectoneradio')[2]  # ボタン選択式エリアがあるか [NON CHANGED]
                if fb_title in self_subjects:
                    MESSAGE += "\n・{}には課題を入力する必要があります。後で追記してください\n".format(fb_title)
            except:
                if fb_title in subjects:
                    fbsubmit()
                    continue
                else:
                    print("{}\n上記授業は通常フォーマットに該当しません スキップします\n".format(fb_title))
                    MESSAGE += "\n・{}はスキップされます\n".format(fb_title)
                    driver.find_element_by_xpath(
                        '//*[@id="functionHeaderForm:breadCrumb"]/ul/li[1]/a').click()  # 左上アンケート回答一覧リンク [NON CHANGED]
                    deadline_texts =  driver.find_elements_by_class_name('kigen')[fbs_list_num].text
                    deadlineCount = int(re.compile('\d+').findall(re.findall("（.*）",deadline_texts)[0])[fbs_list_num])
                    if deadlineCount <= 1:
                        MESSAGE += "⚠️{}\n\n".format(deadline_texts.replace('2020/',''))
                    else:
                        MESSAGE += "・{}\n\n".format(deadline_texts.replace('2020/',''))
                    fbs_list_num += 1
                    continue
            q1.find_elements_by_class_name('ui-radiobutton')[0].click()  # q1理解できた
            q3.find_elements_by_class_name('ui-radiobutton')[1].click()  # q2理解できた
            random_select_num = random.randrange(0, 5, 2)
            q4.find_elements_by_class_name('ui-radiobutton')[random_select_num].click()  # q4 ランダム選択

            fbsubmit()
            if get_remaining_fb == 1:
                print("All answered")
                MESSAGE += "\nフィードバックシートはすべて回答されています😉\n"

    else:
        print("\n----  No Feedback Sheet  ----\n")
        MESSAGE += "\n----  No Feedback Sheet  ----\n"

    back_home()


def check_hw():
    any_notice = 0
    global MESSAGE
    MESSAGE += '\n\n《授業関連》\n'

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
                        (By.ID, 'functionHeaderForm:j_idt148')))  # 左上のTOPボタン
                    for hw_num in range(int(remain_hw_count)):
                        hw_name = driver.find_element_by_id(
                            'funcForm:gakKdiTstList:{}:j_idt370'.format(hw_num)).text.replace(' ', '') + ' '  # 課題名
                        hw_deadline = driver.find_element_by_xpath(
                            '//*[@id="funcForm:gakKdiTstList_data"]/tr[{}]/td[6]/span'.format(
                                hw_num + 1)).text  # 課題提出終了日時
                        print('{}が{}までです'.format(hw_name, hw_deadline))
                        MESSAGE += '・{}が{}までです\n\n'.format(hw_name, hw_deadline)
                        any_notice += 1
                    driver.find_element_by_id('functionHeaderForm:j_idt148').click()  # 左上のTOPボタン

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
            driver.find_element_by_id('functionHeaderForm:j_idt154').click()  # 次の授業をクリック

    back_home()
    if any_notice == 0:
        MESSAGE += '\n授業関連でのお知らせはありません\n'


def fin_action():
    sleep(0.5)
    print("\nProcess Finished\n")
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
