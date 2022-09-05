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
    with open(GAME_TXT_FILE, "a+", encoding="utf-8") as game_txt_file:
        game_txt_file.writelines("\nGame Chronology\n")
        for game_dict in games_data_dict:
            game_name = game_dict.split('_')
            game_txt_file.writelines(f"{game_name[0]} " + games_data_dict[game_dict]["game_started_at"] + "\n")

            game_txt_file.writelines(f"{game_name[0]} " + games_data_dict[game_dict]["game_ended_at"] + "\n")


def find_free_games(games_data_dict: Dict):
    with open(GAME_TXT_FILE, "a+", encoding="utf-8") as game_txt_file:
        game_txt_file.writelines("\nFree Games\n")
        free_game_started_at = None
        total_free_games_wins: float = 0.0
        for game_dict in games_data_dict:
            is_free_game = False
            win_amount_sum: float = 0.0
            game_name = game_dict.split('_')
            for game_item in games_data_dict[game_dict][game_name[0]]:
                if game_item[2] == "Free":
                    is_free_game = True
                    win_amount_sum += float(game_item[4])
                    free_game_started_at = f"{game_item[-2]} {game_item[-1]}"
            if is_free_game:
                total_free_games_wins += win_amount_sum
                game_txt_file.writelines(
                    f"{game_name[0]} free game win is + {round(win_amount_sum, 2)} {free_game_started_at}\n")

        game_txt_file.writelines(f"Total free game win is + {round(total_free_games_wins, 2)}\n")


def other_wins_games(other_games: Dict):
    with open(GAME_TXT_FILE, "a+", encoding="utf-8") as game_txt_file:
        game_txt_file.writelines("\nOther Wins\n")
        for game_dict in other_games:
            if other_games[game_dict]['name'] != "Set score":
                score = "+ " + other_games[game_dict]['score']
                if other_games[game_dict]['score'][0] == '-':
                    score = other_games[game_dict]['score']
                game_txt_file.writelines(
                    f"{other_games[game_dict]['name']} {score} {other_games[game_dict]['other_game_date_time']}\n"
                )


def transfer_in_out(other_games: Dict):
    with open(GAME_TXT_FILE, "a+", encoding="utf-8") as game_txt_file:
        game_txt_file.writelines("\nTransfer in/out\n")
        total_transfer_in = 0.0
        total_transfer_out = 0.0

        for game_dict in other_games:
            if other_games[game_dict]["name"] != "Red Envelope":
                score = float(other_games[game_dict]['score']) * -1
                if score > 0:
                    total_transfer_out += score
                else:
                    total_transfer_in += score
                game_txt_file.writelines(
                    f"{other_games[game_dict]['name']} {score} {other_games[game_dict]['other_game_date_time']}\n"
                )

        game_txt_file.writelines(f"Total Transfer in {total_transfer_in}\n")
        game_txt_file.writelines(f"Total Transfer out {total_transfer_out}\n")


def get_table_rows_data(total_table_pages):
    table_rows_data = []
    games_data_dict = {}
    other_games = {}
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
                if new_row[0]:
                    if new_row[0][0].isalpha() or re.search(u'[\u4e00-\u9fff]', new_row[0]):
                        if new_row[0] == "Red":
                            game_score = new_row[1].split('：')
                            other_games_make_dict_index = f"{new_row[0]}_{game_score[0]}_game_{len(other_games) + 1}"
                            other_games[other_games_make_dict_index] = {
                                "name": "Red Envelope",
                                "score": game_score[1],
                                "other_game_date_time": f"{new_row[-2]} {new_row[-1]}"
                            }
                        else:
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
                                games_data_dict[dict_index][f"{game_name}"] = games_data_dict[dict_index][
                                                                                  f"{game_name}"] + [
                                                                                  new_row]
                                games_data_dict[dict_index]["game_started_at"] = f"{new_row[-2]} {new_row[-1]}"
                    else:
                        game_score = new_row[2].split('：')
                        if len(game_score) != 2:
                            game_score = new_row[1].split('：')
                        other_games_make_dict_index = f"{new_row[1]}_{game_score[0]}_game_{len(other_games) + 1}"
                        other_games[other_games_make_dict_index] = {
                            "name": f"{new_row[1]} {game_score[0]}",
                            "score": game_score[1],
                            "other_game_date_time": f"{new_row[-2]} {new_row[-1]}"
                        }
                else:
                    print("=========================")
                    print(new_row)
                    print("=========================")
        try:
            print(f"Page Number========={n + 1}======================")
            next_page = WebDriverWait(browser, 2).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'laypage_next')))
            next_page.click()
        except Exception as ex:
            print(f"Exception: {str(ex)}")
            break

    return table_rows_data, games_data_dict, other_games


if URL_enter != "" and login_username_enter != '' and password_enter != "":
    browser = get_browser()
    browser.get(URL_enter)
    username = sleep_and_find(browser, 'userName', By.ID)
    password = sleep_and_find(browser, 'password', By.ID)
    username.send_keys(login_username_enter)
    password.send_keys(password_enter)
    if login := sleep_and_find(browser, 'J_btnSubmit', By.ID):
        login.click()

        search_user = sleep_and_find(browser, '#txt_UserName', By.CSS_SELECTOR)
        user_details = open(USER_DETAILS_FILE)
        data = json.load(user_details)
        username_enter = data["username"]
        search_user.send_keys(username_enter)
        sleep_and_find(browser, '#Button_OK', By.CSS_SELECTOR).click()
        time.sleep(2)

        if game_log := sleep_and_find(browser, '/html/body/div/aside/section/ul/li[7]/a', By.XPATH):
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

            with open(GAME_TXT_FILE, "a+", encoding="utf-8") as file1:
                file1.writelines(USER_ID + username_enter + "\n")
                file1.writelines(START_DATE_TIME + start_date_enter + " " + start_time_enter + "\n")
                file1.writelines(END_DATE_TIME + end_time_enter + " " + end_time_enter + "\n")
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

            total_pages = None
            try:
                total_pages = browser.find_element(By.CLASS_NAME, 'laypage_last').text
            except:
                total_pages = browser.find_element(By.CLASS_NAME, 'laypage_last').text
                
            if total_pages is None:
                browser.quit()
                print("total pages not found")
                exit()

            final_data, final_games_data_dict, other_wins_games_data = get_table_rows_data(total_pages)

            browser.switch_to.default_content()

            find_games_chronology(final_games_data_dict)
            find_free_games(final_games_data_dict)
            other_wins_games(other_wins_games_data)
            transfer_in_out(other_wins_games_data)

            with open(GAME_TXT_FILE, "a+", encoding="utf-8") as game_txt_file:
                game_txt_file.writelines("\nThank you for your business. Please come again.\n\n")
            browser.quit()
        else:
            browser.close()

    else:
        browser.close()
        print('not login')
