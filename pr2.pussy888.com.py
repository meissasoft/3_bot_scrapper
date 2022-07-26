import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
from selenium.webdriver.common import keys
import warnings
warnings.filterwarnings('ignore')
max_delay = 60


def sleep_and_find(browser, selector, by, is_all=False, is_visible=False):
    my_elem = False
    for i in range(1, max_delay):
        try:
            if is_visible:
                my_elem = WebDriverWait(browser, 6).until(
                    EC.invisibility_of_element((by, selector)))
                break
            if is_all:
                my_elem = WebDriverWait(browser, 6).until(
                    EC.presence_of_all_elements_located((by, selector)))
                break
            else:
                my_elem = WebDriverWait(browser, 6).until(
                    EC.presence_of_element_located((by, selector)))
                break
        except Exception as ex:
            print("selector ", selector, " not found in ", str(i), " seconds")
    return my_elem


def get_browser():
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument("start-maximized")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("test-type")
    browser = webdriver.Chrome('chromedriver.exe', chrome_options=options)
    return browser

# Automatically Login


login_credentials = open('loginCredientials.json')
data = json.load(login_credentials)
login_username_enter = data["username"]
URL_enter = data["url"]
password_enter = data["password"]
if URL_enter != "" and login_username_enter != '' and password_enter != "":
    browser = get_browser()
    browser.get(URL_enter)
    username = sleep_and_find(browser, 'userName', By.ID)
    password = sleep_and_find(browser, 'passWd', By.ID)
    username.send_keys(login_username_enter)
    password.send_keys(password_enter)
    login = sleep_and_find(browser, 'loginButton', By.ID)
    if login:
        login.click()
        f = open('userdetails.json')
        data = json.load(f)
        username_enter = data["username"]
        start_date_enter = data["startdate"]
        start_time_enter = data["starttime"]
        end_time_enter = data["endtime"]
        games = data["banned_games"]
        time_by_user = data["time_sleep"]
        print("start_date_enter", start_date_enter)
        print("start_time_enter", start_time_enter)
        print('end_time_enter', end_time_enter)
        search_log = sleep_and_find(
            browser, '/html/body/div[2]/aside/section/ul/li[3]/a', By.XPATH)
        if search_log:
            search_log.click()

            search_field = sleep_and_find(
                browser, 'txt_UserName', By.ID)
            file1 = open("game.txt", "a+",
                         encoding="utf-8")
            file1.writelines(
                "\nUser Name " + username_enter + "\n")
            file1.close()
            search_field.clear()
            search_field.send_keys(username_enter)
            ok_Button = sleep_and_find(
                browser, 'Button_OK', By.ID)
            if ok_Button:
                ok_Button.click()
            username_game_log = WebDriverWait(browser, 60).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="tblData_1"]/tr/td[13]/button[3]')))
            if username_game_log:
                username_game_log.click()
                start_date_log = WebDriverWait(browser, 60).until(
                    EC.element_to_be_clickable((By.ID, "txt_StartDateTime")))
                start_time_game_log = WebDriverWait(browser, 60).until(
                    EC.element_to_be_clickable((By.ID, "txt_StartDateTime_HM")))
                end_time_game_log = WebDriverWait(browser, 60).until(
                    EC.element_to_be_clickable((By.ID, "txt_EndDateTime_HM")))

                start_date_log.clear()
                start_time_game_log.clear()
                end_time_game_log.clear()
                start_date_log.send_keys(
                    start_date_enter)
                start_time_game_log.send_keys(
                    keys.Keys.BACKSPACE * 10)
                start_time_game_log.send_keys(
                    start_time_enter)
                end_time_game_log.send_keys(
                    keys.Keys.BACKSPACE * 10)
                end_time_game_log.send_keys(
                    end_time_enter)
                ok_Button = sleep_and_find(
                    browser, 'Button_OK', By.ID)
                if ok_Button:
                    try:
                        browser.execute_script(
                            "arguments[0].click();", ok_Button)
                    except Exception as e:
                        print("Error duw tp", e)

                    time.sleep(5+time_by_user)
                    try:
                        total_pages = browser.find_element(
                            By.CLASS_NAME, "laypage_last").text
                        file1 = open(
                            "game.txt", "a+", encoding="utf-8")
                        file1.writelines(
                            "\nTotal Pages are " + total_pages + " \n")
                        file1.close()
                        print(total_pages)
                    except:
                        pass
                    final_data = []
                    match_data = []
                    n = 1
                    for n in range(int(total_pages)):
                        rows = browser.find_elements(
                            "xpath", '//tr[@class="tr_h"]')
                        for row in rows:
                            row = str(row.text)\
                                .replace("Neptune Treasure", "NeptuneTreasure")\
                                .replace("SAFARI Heat", "SAFARIHeat")\
                                .replace("god of", "godof")\
                                .replace("Sultan`s Gold", "Sultan`sGold")\
                                .replace("Wong Choy", "WongChoy")\
                                .replace('Lion Dance', 'LionDance')\
                                .replace('Great Rhino', 'GreatRhino')\
                                .replace('Dragon Gold', 'DragonGold')\
                                .replace('Football Fans', 'FootballFans')\
                                .replace('Tally Ho', 'TallyHo')\
                                .replace('Hologram Wilds', 'HologramWilds')
                            row = row.split(" ")
                            final_data.append(row)
                            # print("row",row)

                        try:
                            print(
                                "next page===============================")
                            next_page = browser.find_element(
                                "xpath", "//a[@class='laypage_next']")
                            next_page.click()
                            time.sleep(time_by_user)
                        except:
                            print("Hel")
                            continue
                    end_game_time = final_data[0][-2] + \
                        " " + final_data[0][-1]
                    start_game_time = final_data[-1][-2] + \
                        " " + final_data[-1][-1]
                    if end_game_time and start_game_time:
                        file1 = open(
                            "game.txt", "a+", encoding="utf-8")
                        file1.writelines(
                            " start game time " + start_game_time + "\n")
                        file1.writelines(
                            " end game time " + end_game_time + "\n")
                        file1.close()
                    # Total Bets
                    bet_list = []
                    try:
                        for i in final_data:
                            if i[2] == "Free" or i[2] == "-" or len(i[2]) > 5:
                                bet = '0.0'
                            else:
                                bet = i[2]
                            bet_list.append(bet)
                    except Exception as e:
                        print(e)

                    bet_bree_game = []
                    try:
                        for i in final_data:
                            if i[2] == "Free" or len(i[2]) > 4 or i[3] == 'Free':
                                bet = '0.0'
                            else:
                                bet = i[2]
                            bet_bree_game.append(bet)
                    except Exception as e:
                        print(e)
                    bet_sum = float(0.0)
                    for i in bet_list:
                        bet_sum = bet_sum + float(i)
                    file1 = open(
                        "game.txt", "a+", encoding="utf-8")
                    file1.writelines(
                        '\n\nTotal BETS ' + str(round(bet_sum, 2)) + "\n")
                    file1.close()

                    # Total Wins
                    Win = []
                    for i in final_data:
                        b = ''
                        if i[3] == "-":
                            print(type(i[3]))
                            bet = '0.00'
                        elif i[3] == "game":
                            bet = i[4]
                        elif i[3] == "Free":
                            bet = i[5]
                        else:
                            bet = i[3]
                        Win.append(bet)
                    win_sum = float(0.0)
                    for i in Win:
                        win_sum = win_sum + float(i)
                    file1 = open(
                        "game.txt", "a+", encoding="utf-8")
                    file1.writelines(
                        'Total WIN   ' + str(round(win_sum, 2)) + "\n")
                    file1.close()
                    results = float(
                        win_sum) - float(bet_sum)
                    file1 = open(
                        "game.txt", "a+", encoding="utf-8")
                    file1.writelines(
                        "\nTotal NETTGAMING(Win/Loss) " + str(round(results, 2))+"\n")
                    file1.close()

                    # Total Free Games

                    word = '0.0'
                    length = len(bet_bree_game)
                    print(length)
                    count = 0
                    for i in range(0, length):
                        if word == bet_bree_game[i]:
                            count += 1
                    if count == 0:
                        file1 = open(
                            "game.txt", "a+", encoding="utf-8")
                        file1.writelines(
                            "\n\nTotal FREE GAMES are 0""\n")
                        file1.close()
                    else:
                        file1 = open(
                            "game.txt", "a+", encoding="utf-8")
                        file1.writelines(
                            "\n\nTotal FREE GAMES "+str(round(count, 2))+"\n")
                        file1.close()

                    free_game_list = []
                    sum = 0
                    for i in final_data:
                        # print(i[3])
                        if i[2] == "Free" and i[3] == 'game':
                            free_game_list.append(i)
                            sum = sum + float(i[4])
                    file1 = open(
                        "game.txt", "a+", encoding="utf-8")
                    file1.writelines(
                        "\nFree game winning is  " + str(round(sum, 2)) + "\n")
                    file1.close()
                    file1 = open(
                        "free_game.txt", "a+", encoding="utf-8")
                    file1.writelines(
                        " user name " + username_enter + "\n")
                    for x in free_game_list:
                        L = str(x).replace(
                            '[', '').replace(']', '')
                        file1.writelines(str(L)+"\n")
                    file1.close()

                    def unique(list1):
                        unique_list = []
                        for x in list1:
                            if x not in unique_list:
                                unique_list.append(x)
                        return unique_list
                    l = []
                    for ga in final_data:
                        l.append(ga[0])
                    game_list = unique(l)
                    game_lists = ' '.join(
                        [str(elem) for elem in game_list])
                    file1 = open(
                        "game.txt", "a+", encoding="utf-8")
                    file1.writelines(
                        "\n\nGames Played are " + game_lists + "\n")
                    file1.close()

                    final_results = []
                    for i in final_data:
                        if i[0] in games:
                            final_results.append(i)
                        else:
                            pass
                    banned_game_list = []
                    for i in final_results:
                        banned_game_list.append(i[0])
                    banned_game = unique(
                        banned_game_list)
                    if len(final_results) > 0:
                        for x in final_results:
                            file1 = open(
                                "banned_game_list.txt", "a+", encoding="utf-8")
                            L = str(x).replace(
                                '[', '').replace(']', '')
                            file1.writelines(
                                "\n"+str(L)+"\n")
                            file1.close()
                    if len(banned_game) == 0:
                        file1 = open(
                            "game.txt", "a+", encoding="utf-8")
                        file1.writelines(
                            '\nNo Banned games detected' + "\n")
                        file1.close()
                    elif len(banned_game) > 0:
                        file1 = open(
                            "game.txt", "a+", encoding="utf-8")
                        for game in banned_game:
                            file1.writelines(
                                '\nBanned games played ' + game + "\n")
                        file1.close()
                    data_from_tableID = []
                    for x in final_data:
                        if x[1] != '0':
                            data_from_tableID.append(x)
                    file1 = open(
                        "game.txt", "a+", encoding="utf-8")
                    file1.writelines("\n\nImportant credit logs are \n")
                    for x in data_from_tableID:
                        file1 = open(
                            "game.txt", "a+", encoding="utf-8")
                        L = str(x).replace(
                            '[', '').replace(']', '')
                        file1.writelines(str(L)+"\n")
                        file1.close()
                    transfer_in_sum = 0
                    transfer_out_sum = 0
                    for i in data_from_tableID:
                        if i[1] == "Set" and i[2][:5] == "score":
                            if float(i[2][6:]) > 0.0:
                                transfer_in_sum = transfer_in_sum + \
                                    float(i[2][6:])
                            elif float(i[2][6:]) < 0.0:
                                transfer_out_sum = transfer_out_sum + \
                                    float(i[2][6:])

                    file1 = open(
                        "game.txt", "a+", encoding="utf-8")
                    file1.writelines(
                        "\n\nTotal Transfer in " + str(transfer_in_sum) + "\n")
                    file1.writelines(
                        "Total Transfer out " + str(transfer_out_sum) + "\n\n")
                    file1.close()

                    file1 = open(
                        "game.txt", "a+", encoding="utf-8")

                    file1.writelines("\nGames Cronology is\n\n")

                    n = 0
                    end_time = ''
                    start_time = ''
                    firsInstance = None
                    lastInstance = None
                    for game_name in game_list:
                        print('game list')
                        firsInstance = None
                        gameFound = False
                        for data in final_data:
                            if game_name in data:
                                gameFound = True
                                if firsInstance is None:
                                    firsInstance = data
                                    end_time = ' '.join(
                                        str(e) for e in firsInstance[-2:])
                                lastInstance = data
                                start_time = ' '.join(
                                    str(e) for e in lastInstance[-2:])
                            else:
                                if gameFound:
                                    break
                        print(
                            firsInstance[0]+" end time", end_time)
                        print(
                            lastInstance[0] + " start time", start_time)
                        file1 = open(
                            "game.txt", "a+", encoding="utf-8")

                        file1.writelines(
                            firsInstance[0] + "    end time     " + end_time + "\n")
                        file1.writelines(
                            lastInstance[0] + "    start time   " + start_time + "\n")
                    file1.close()
                    browser.quit()

    else:
        print("Not login")
        browser.quit()
