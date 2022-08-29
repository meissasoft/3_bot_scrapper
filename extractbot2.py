import json
from typing import List, Dict

from selenium import webdriver
import time
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common import keys

USER_DETAILS_FILE = 'userdetails.json'
GAME_TXT_FILE = "game.txt"

USER_ID = "ID :"
START_DATE_TIME = "Start Date Time :"
END_DATE_TIME = "End Date Time :"

max_delay = 60


def sleep_and_find(browser, selector, by, is_all=False, is_visible=False):
    my_elem = False
    for i in range(1, max_delay):
        try:
            if is_visible:
                my_elem = WebDriverWait(browser, i).until(EC.invisibility_of_element((by, selector)))

                break
            if is_all:
                my_elem = WebDriverWait(browser, i).until(EC.presence_of_all_elements_located((by, selector)))

            else:
                my_elem = WebDriverWait(browser, i).until(EC.presence_of_element_located((by, selector)))

            break
        except Exception as ex:
            print("selector ", selector, " not found in ", i, " seconds")
    return my_elem


def get_browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-popup-blocking")
    options.add_argument("test-type")
    return webdriver.Chrome('chromedriver.exe', chrome_options=options)


# Automatically Login
login_credentials = open('loginCredientials.json')
data = json.load(login_credentials)
login_username_enter = data["username"]
URL_enter = data["url"]
password_enter = data["password"]


def find_games_chronology(games_data_dict: Dict):
    game_txt_file = open(GAME_TXT_FILE, "a+", encoding="utf-8")
    game_txt_file.writelines("\nGame Chronology\n")
    for game_dict in games_data_dict:
        game_name = game_dict.split('_')
        game_txt_file.writelines(game_name[0] + " " + games_data_dict[game_dict]["game_started_at"] + "\n")
        game_txt_file.writelines(game_name[0] + " " + games_data_dict[game_dict]["game_ended_at"] + "\n")
    game_txt_file.close()


def find_free_games(games_data_dict: Dict):
    game_txt_file = open(GAME_TXT_FILE, "a+", encoding="utf-8")
    game_txt_file.writelines("\nFree Games\n")
    free_game_started_at = None
    total_free_games_wins: float = 0.0
    win_amount_sum: float = 0.0
    for game_dict in games_data_dict:
        game_name = game_dict.split('_')
        for game_item in games_data_dict[game_dict][game_name[0]]:
            is_free_game = False
            if game_item[2] == "Free":
                is_free_game = True
                win_amount_sum = win_amount_sum + float(game_item[4])
                free_game_started_at = f"{game_item[-2]} {game_item[-1]}"

            if is_free_game:
                total_free_games_wins = win_amount_sum + win_amount_sum
                game_txt_file.writelines(f"{game_name[0]} free game win is + {round(win_amount_sum, 2)} {free_game_started_at}\n")
            print(game_item)
    # Todo where from get date for total from game wins
    game_txt_file.writelines(f"Total free game win is + {round(total_free_games_wins, 2)} {free_game_started_at}\n")
    game_txt_file.close()


def find_unique(list1):
    unique_list = []
    prev_value = None
    for x in list1:
        # x containing alphabet or chinese
        if (x.isalpha() or re.search(u'[\u4e00-\u9fff]', x)) and (x not in unique_list or x != prev_value):
            unique_list.append(x)
        prev_value = x
    return unique_list


def get_table_rows_data(total_table_pages):
    table_rows_data = []
    games_data_dict = {}
    game_name = None

    for n in range(int(total_table_pages)):

        time.sleep(time_by_user)
        page = browser.find_elements("xpath", '//*[@id="tblData"]')
        for rows in page:
            rows = rows.text \
                .replace("SAFARI Heat", "SAFARIHeat") \
                .replace("god of", "godof") \
                .replace("Neptune Treasure", "NeptuneTreasure") \
                .replace("Sultan`s Gold", "Sultan`sGold") \
                .replace("Wong Choy", "WongChoy") \
                .replace('Lion Dance', 'LionDance') \
                .replace('Great Rhino', 'GreatRhino') \
                .replace('Dragon Gold', 'DragonGold') \
                .replace('Football Fans', 'FootballFans') \
                .replace('Tally Ho', 'TallyHo') \
                .replace('Hologram Wilds', 'HologramWilds').split("\n")

            table_rows_data.append(rows)

            # adding every game into dictionary
            for row in rows:
                new_row = row.split(' ')
                if new_row[0].isalpha() or re.search(u'[\u4e00-\u9fff]', new_row[0]):
                    if game_name and game_name != new_row[0]:
                        make_dict_index = f"{new_row[0]}_game_{len(games_data_dict) + 1}"
                        games_data_dict[make_dict_index] = {
                            f"{new_row[0]}": [],
                            "game_started_at": f"{new_row[-2]} {new_row[-1]}",
                            "game_ended_at": f"{new_row[-2]} {new_row[-1]}"
                        }

                    game_name = new_row[0]
                    if not games_data_dict:
                        games_data_dict[f"{game_name}_game_{len(games_data_dict) + 1}"] = {
                            f"{game_name}": [new_row],
                            "game_started_at": f"{new_row[-2]} {new_row[-1]}",
                            "game_ended_at": f"{new_row[-2]} {new_row[-1]}"
                        }

                    else:
                        dict_index = f"{game_name}_game_{len(games_data_dict)}"
                        games_data_dict[dict_index][f"{game_name}"] = games_data_dict[dict_index][f"{game_name}"] + [new_row]
                        games_data_dict[dict_index]["game_started_at"] = f"{new_row[-2]} {new_row[-1]}"

        try:
            print(f"Page Number========={n + 1}======================")
            next_page = WebDriverWait(browser, 2).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'laypage_next')))
            next_page.click()
        except Exception as ex:
            print(f"Exception: {str(ex)}")
            break
    return table_rows_data, games_data_dict


if URL_enter != "" and login_username_enter != '' and password_enter != "":
    browser = get_browser()
    browser.get(URL_enter)
    # start_click = sleep_and_find(
    #     browser, 'body > div > button', By.CSS_SELECTOR)
    # if start_click:
    #     start_click.click()
    # else:
    #     pass
    username = sleep_and_find(browser, 'userName', By.ID)
    password = sleep_and_find(browser, 'password', By.ID)
    username.send_keys(login_username_enter)
    password.send_keys(password_enter)
    login = sleep_and_find(browser, 'J_btnSubmit', By.ID)
    if login:
        login.click()

        search_user = sleep_and_find(browser, '#txt_UserName', By.CSS_SELECTOR)
        user_details = open(USER_DETAILS_FILE)
        data = json.load(user_details)
        username_enter = data["username"]
        search_user.send_keys(username_enter)
        sleep_and_find(browser, '#Button_OK', By.CSS_SELECTOR).click()
        time.sleep(2)

        game_log = sleep_and_find(browser, '/html/body/div/aside/section/ul/li[7]/a', By.XPATH)
        if game_log:
            game_log.click()

            user_details = open(USER_DETAILS_FILE)
            data = json.load(user_details)
            username_enter = data["username"]
            start_date_enter = data["startdate"]
            start_time_enter = data["starttime"]
            end_time_enter = data["endtime"]
            banned_games = data["banned_games"]
            time_by_user = data["time_sleep"]
            start_date_log = WebDriverWait(browser, 60).until(
                EC.element_to_be_clickable((By.ID, "txt_StartDateTime"))
            )
            start_time_game_log = WebDriverWait(browser, 60).until(
                EC.element_to_be_clickable((By.ID, "txt_StartDateTime_HM"))
            )
            end_time_game_log = WebDriverWait(browser, 60).until(
                EC.element_to_be_clickable((By.ID, "txt_EndDateTime_HM"))
            )

            file1 = open(GAME_TXT_FILE, "a+", encoding="utf-8")
            file1.writelines("\n" + USER_ID + username_enter + "\n")
            file1.writelines(START_DATE_TIME + start_date_enter + " " + start_time_enter + "\n")
            file1.writelines(END_DATE_TIME + end_time_enter + " " + end_time_enter + "\n")
            file1.close()

            start_date_log.clear()
            start_time_game_log.clear()
            end_time_game_log.clear()
            start_date_log.send_keys(start_date_enter)

            username_game_log = sleep_and_find(browser, '#txt_UserName', By.CSS_SELECTOR)
            username_game_log.click()
            username_game_log.send_keys(username_enter)

            start_time_game_log.send_keys(keys.Keys.BACKSPACE * 10)
            start_time_game_log.send_keys(start_time_enter)
            end_time_game_log.send_keys(keys.Keys.BACKSPACE * 10)
            end_time_game_log.send_keys(end_time_enter)
            ok_game_log_button = sleep_and_find(browser, 'Button_OK', By.ID)
            try:
                browser.execute_script("arguments[0].click();", ok_game_log_button)
            except Exception as e:
                print("Error duw tp", e)

            time.sleep(5 + time_by_user)
            browser.switch_to.frame(browser.find_element(By.TAG_NAME, "iframe"))

            try:
                total_pages = browser.find_element(By.CLASS_NAME, 'laypage_last').text
                # print("total_pages: ", total_pages)
                # file1 = open(GAME_TXT_FILE, "a+")
                # file1.writelines("\nTotal Pages are: " + total_pages + " \n")
                # file1.close()

            except:
                pass
                # total_pages = '1'
                # file1 = open(GAME_TXT_FILE, "a+")
                # file1.writelines("\nTotal Pages are: " + total_pages + " \n")
                # file1.close()
            final_data, final_games_data_dict = get_table_rows_data(total_pages)

            browser.switch_to.default_content()

            data_split = []
            for i in final_data:
                for j in i:
                    split_data = j.split(',')
                    data_split.append(split_data)
            data_tableId = []
            for i in data_split:
                # for j in i:
                data_space_split = i[0].split(" ")
                data_tableId.append(data_space_split)

            games_name_list = []
            for game in data_tableId:
                games_name_list.append(game[0])
            # Todo add multiple gamse with same name also
            game_list = find_unique(games_name_list)

            find_games_chronology(final_games_data_dict)
            find_free_games(final_games_data_dict)
            # # how is calculating?
            # end_game_time = data_tableId[0][-2] + " " + data_tableId[0][-1]
            # start_game_time = data_tableId[-1][-2] + " " + data_tableId[-1][-1]
            # file1 = open(GAME_TXT_FILE, "a+", encoding="utf-8")
            #
            # file1.writelines('Start time game log ' + start_game_time + "\n")
            # file1.writelines('End time game log ' + end_game_time + "\n\n")
            # file1.close()

            # Total Bets
            bet_list = []
            try:
                for i in data_tableId:
                    if i[2] == "Free" or i[2] == "-" or len(i[2]) > 5:
                        bet = '0.0'
                    else:
                        bet = i[2]
                    bet_list.append(bet)
            except Exception as e:
                print(e)

            bet_free_game = []
            try:
                for i in data_tableId:
                    if i[2] == "Free" or i[3] == 'Free':
                        bet = '0.0'
                    else:
                        bet = i[2]
                    bet_free_game.append(bet)
            except Exception as e:
                print(e)

            bet_sum = float(0.0)
            for i in bet_list:
                bet_sum = bet_sum + float(i)

            file1 = open(GAME_TXT_FILE, "a+", encoding="utf-8")
            file1.writelines('\n\nTotal BETS ' + str(round(bet_sum, 2)) + "\n")
            file1.close()

            # Total Wins
            total_wins = []
            win_sum = float(0.0)
            for i in data_tableId:
                if i[3] == "-":
                    print(type(i[3]))
                    bet = 0.0
                elif i[3] == "game":
                    bet = i[4]
                else:
                    bet = i[3]
                total_wins.append(bet)
                win_sum = win_sum + float(bet)

            file1 = open(GAME_TXT_FILE, "a+", encoding="utf-8")
            file1.writelines('Total WIN   ' + str(round(win_sum, 2)) + "\n")
            file1.close()
            results = float(win_sum) - float(bet_sum)
            file1 = open(GAME_TXT_FILE, "a+", encoding="utf-8")
            file1.writelines("Total NETT GAMING(Win/Loss) " + str(round(results, 2)) + "\n")
            file1.close()

            # Total Free Games
            word = '0.0'
            length = len(bet_free_game)
            print(bet_free_game)
            count = 0
            for i in range(0, length):
                if word == bet_free_game[i]:
                    count += 1
            if count == 0:
                file1 = open(GAME_TXT_FILE, "a+",
                             encoding="utf-8")
                file1.writelines("\n\nTotal FREE GAMES are 0\n")
                file1.close()
            else:
                file1 = open(GAME_TXT_FILE, "a+",
                             encoding="utf-8")
                file1.writelines(
                    "\n\nTotal FREE GAMES " + str(count) + "\n")
                file1.close()

            free_game_list = []
            free_game_wins_sum = 0
            for i in data_tableId:
                # print(i[3])
                if i[2] == "Free" and i[3] == 'game':
                    free_game_list.append(i)
                    free_game_wins_sum = free_game_wins_sum + float(i[4])
            file1 = open(GAME_TXT_FILE, "a+", encoding="utf-8")
            file1.writelines("Free game winning is  " + str(round(free_game_wins_sum, 2)) + "\n")
            file1.close()

            file1 = open("free_game.txt", "a+", encoding="utf-8")
            file1.writelines(" user name " + username_enter + "\n")
            for x in free_game_list:
                L = str(x).replace('[', '').replace(']', '')
                file1.writelines(str(L) + "\n")
            file1.close()

            file1 = open(GAME_TXT_FILE, "a+", encoding="utf-8")
            all_unique_game = ''
            for game in game_list:
                all_unique_game += " " + game + " "
            file1.writelines("\nGames Played are " + all_unique_game + " \n")
            file1.close()

            final_results = []
            for i in data_tableId:
                # print(i[0])
                if i[0] in banned_games:
                    # print(i[0])
                    final_results.append(i)
                else:
                    print("No banned games found")
            banned_game_list = []
            for i in final_results:
                banned_game_list.append(i[0])
            banned_game = find_unique(banned_game_list)
            if len(final_results) > 0:
                for x in final_results:
                    file1 = open("banned_game_list.txt", "a+", encoding="utf-8")
                    L = str(x).replace('[', '').replace(']', '')
                    file1.writelines("\n" + str(L) + "\n")
                    file1.close()
            if len(banned_game) == 0:
                file1 = open(GAME_TXT_FILE, "a+", encoding="utf-8")
                file1.writelines('No Banned games detected' + "\n")
                file1.close()
            elif len(banned_game) > 0:
                file1 = open(GAME_TXT_FILE, "a+", encoding="utf-8")
                for game in banned_game:
                    file1.writelines('\nBanned games played ' + game + "\n")
                file1.close()

            data_from_tableID = []

            # data_tableId
            for i in data_tableId:
                if i[1] != "0" or len(i) < 2:
                    data_from_tableID.append(i)
            file1 = open(GAME_TXT_FILE, "a+", encoding="utf-8")
            file1.writelines("\n\nImportant credit logs are \n")
            for x in data_from_tableID:
                file1 = open(GAME_TXT_FILE, "a+", encoding="utf-8")

                L = str(x).replace('[', '').replace(']', '')
                file1.writelines(str(L) + "\n")
                file1.close()
            total_transfer_in = 0
            total_transfer_out = 0

            for i in data_from_tableID:
                if i[1] == "Set" and i[2][:5] == "score":
                    if float(i[2][6:]) > 0.0:
                        total_transfer_in = total_transfer_in + \
                                            float(i[2][6:])
                    elif float(i[2][6:]) < 0.0:
                        total_transfer_out = total_transfer_out + \
                                             float(i[2][6:])

            file1 = open(GAME_TXT_FILE, "a+", encoding="utf-8")
            file1.writelines("\nTotal Transfer in " + str(total_transfer_in) + "\n")
            file1.writelines("Total Transfer out " + str(total_transfer_out) + "\n\n")
            file1.close()

            file1.close()
            browser.quit()
        else:
            browser.close()

    else:
        browser.close()
        print('not login')
