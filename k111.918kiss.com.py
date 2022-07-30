# Automatically Login
import json
import pickle
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
import warnings
from selenium.webdriver.common import keys

warnings.filterwarnings('ignore')


driver = webdriver.Chrome('chromedriver.exe')
max_delay = 60


def sleep_and_find(browser, selector, by, isAll=False, isVisbible=False):
    myElem = None
    for i in range(1, max_delay):
        try:
            if isVisbible:
                myElem = WebDriverWait(browser, 1).until(
                    EC.invisibility_of_element((by, selector)))
                break
            if isAll:
                myElem = WebDriverWait(browser, 1).until(
                    EC.presence_of_all_elements_located(((by, selector))))
                break
            else:
                myElem = WebDriverWait(browser, 1).until(
                    EC.presence_of_element_located((by, selector)))
                break
        except Exception as ex:
            print("selector ", selector, " not found in ", str(i), " seconds")
    return myElem


f = open('loginCredientials.json')
data = json.load(f)
loginusernameenter = data["username"]
urlenter = data["url"]
passwordenter = data["password"]
pinenter = data["pin"]
if urlenter != "" and loginusernameenter != '' and passwordenter != "":
    driver.get(urlenter)
    driver.find_element(
        'xpath', '//div[@class="sa-confirm-button-container"]//button').click()
    username = sleep_and_find(driver, 'userName', By.ID)
    password = sleep_and_find(driver, 'passWd', By.ID)
    username.send_keys(loginusernameenter)
    password.send_keys(passwordenter)
    loginButton = sleep_and_find(driver, "loginButton", By.ID)
    loginButton.click()
    pin = sleep_and_find(driver, "txt_Password", By.ID)
    pin.send_keys(pinenter)
    sleep_and_find(driver, "Button_OK", By.ID).click()
    f = open('userdetails.json')
    data = json.load(f)
    usernameenter = data["username"]

    serch_user = sleep_and_find(
        driver, "#txt_UserName", By.CSS_SELECTOR)

    serch_user.send_keys(usernameenter)
    sleep_and_find(driver, "Button_OK", By.ID).click()

    # if isLoogedIn:
    #     isLoogedIn.click()
    #     time.sleep(30)
    #     togglebutton = WebDriverWait(driver, 60).until(EC.element_to_be_clickable(
    #         (By.CSS_SELECTOR, '#d_tip_2 > div > div > button.btn.btn-default.btn-flat.dropdown-toggle')))
    #     togglebutton.click()

    #     file1 = open("user_name_list.txt", "a+")
    #     file1.close()

    #     time.sleep(5)

    #     total_player_list = WebDriverWait(driver, 60).until(EC.element_to_be_clickable(
    #         (By.CSS_SELECTOR, "#d_tip_2 > div > div > ul > li:nth-child(1) > a")))
    #     total_player_list.click()
    #     time.sleep(15)

    #     driver.find_element('id', "Button_OK").click()
    #     time.sleep(15)

    #     user = WebDriverWait(driver, 60).until(
    #         EC.element_to_be_clickable((By.XPATH, '//*[@id="tblData"]')))
    #     user = user.text

    #     userlist = user.split(" ")
    #     user_list_data = []
    #     datalist = []
    #     for i in userlist:

    #         data = i.split('\n')
    #         datalist.append(data[0])

    #     user_list_data.append(datalist[0])
    #     user_list_data

    #     datalist2 = []
    #     for i in userlist:

    #         data = i.split('\n')
    #         datalist2.append(data)
    #     datalist2.pop(0)
    #     datalist2.pop()
    #     datalist2
    #     for i in datalist2:

    #         user_list_data.append(i[1])

    gamelog = WebDriverWait(driver, 60).until(EC.element_to_be_clickable(
        (By.XPATH, "//a[@href='com_Log_PlayerBetLog.aspx']")))
    if gamelog:
        gamelog.click()
        f = open('userdetails.json')
        data = json.load(f)
        usernameenter = data["username"]
        startdateenter = data["startdate"]
        starttimeenter = data["starttime"]
        endtimeenter = data["endtime"]
        games = data["banned_games"]
        time_by_user = data["time_sleep"]
        print("startdateenter", startdateenter)
        print("starttimeenter", starttimeenter)
        print('endtimeenter', endtimeenter)
        # for user_name in user_list_data:
        #     if user_name == usernameenter:
        username_game_log = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.ID, "txt_UserName")))
        start_date_log = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.ID, "txt_StartDateTime")))
        start_time_game_log = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.ID, "txt_StartDateTime_HM")))
        end_time_game_log = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.ID, "txt_EndDateTime_HM")))
        file1 = open("game.txt", "a+", encoding="utf-8")
        file1.writelines("\nUser Name " + usernameenter+"\n")
        file1.close()
        username_game_log.clear()
        start_date_log.clear()
        start_time_game_log.clear()
        end_time_game_log.clear()
        username_game_log.send_keys(usernameenter)
        start_date_log.send_keys(startdateenter)
        start_time_game_log.send_keys(
            keys.Keys.BACKSPACE * 10)
        start_time_game_log.send_keys(starttimeenter)
        end_time_game_log.send_keys(
            keys.Keys.BACKSPACE * 10)
        end_time_game_log.send_keys(endtimeenter)
        print("Hello")
        username_game_log.clear()
        username_game_log.send_keys(usernameenter)
        time.sleep(time_by_user+5)
        ok_game_log_button = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.ID, "Button_OK")))
        try:
            driver.execute_script(
                "arguments[0].click();", ok_game_log_button)
        except Exception as e:
            print("Error duw tp", e)

        time.sleep(time_by_user+5)
        try:
            totalpages = driver.find_element(
                'xpath', "//a[@class='laypage_last']").text
            file1 = open("game.txt", "a+", encoding="utf-8")
            file1.writelines("\nTotal Pages are " + totalpages + " \n")
            file1.close()
            print(totalpages)
        except:
            totalpages = '1'
            file1.writelines("\nTotal Pages are " + totalpages + " \n")
            file1.close()
            print(totalpages)
            pass

        final_data = []
        match_data = []
        n = 0
        for n in range(int(totalpages)):
            rows = driver.find_elements("xpath", '//tr[@class="tr_h"]')
            for row in rows:
                row = row.text.replace("SAFARI Heat", "SAFARIHeat").replace("god of", "godof").replace("Sultan`s Gold", "Sultan`sGold").replace("Wong Choy", "WongChoy").replace("Neptune Treasure", "NeptuneTreasure").replace(
                    'Great Rhino', 'GreatRhino').replace('Dragon Gold', 'DragonGold').replace('Football Fans', 'FootballFans').replace('Tally Ho', 'TallyHo').replace('Hologram Wilds', 'HologramWilds').split(" ")
                # print("row",row)
                if len(row) == 8:
                    final_data.append(row)
                if len(row) == 9:
                    final_data.append(row)
                if len(row) == 10:
                    match_data.append(row)
                if len(row) == 12:
                    match_data.append(row)
                if len(row) == 7:
                    match_data.append(row)
            try:
                print("next page===============================")
                next = driver.find_element(
                    "xpath", "//a[@class='laypage_next']")
                next.click()
                time.sleep(time_by_user)
            except:
                print("Hel")
                continue

        end_game_time = final_data[0][-2] + " " + final_data[0][-1]
        start_game_time = final_data[-1][-2] + " " + final_data[-1][-1]

        if end_game_time and start_game_time:
            file1 = open("game.txt", "a+", encoding="utf-8")
            file1.writelines(" start game time " +
                             start_game_time + "\n")
            file1.writelines(" end game time " + end_game_time + "\n")
            file1.close()

        # Total Bets
        Bet = []
        try:
            for i in final_data:
                if i[2] == "Free" or i[2] == "-" or len(i[2]) > 5:
                    be = '0.0'
                else:
                    be = i[2]
                Bet.append(be)
        except Exception as e:
            print(e)

        Bet_Free_game = []
        try:
            for i in final_data:
                if i[2] == "Free" or len(i[2]) > 4 or i[3] == 'Free':
                    be = '0.0'
                else:
                    be = i[2]
                Bet_Free_game.append(be)
        except Exception as e:
            print(e)
        bet_sum = float(0.0)
        for i in Bet:
            i = float(i)
            bet_sum = bet_sum+i
        file1 = open("game.txt", "a+", encoding="utf-8")
        file1.writelines('\n\nTotal BETS ' + str(round(bet_sum, 2))+"\n")
        file1.close()

        # Total Wins
        Win = []
        for i in final_data:
            b = ''
            if i[3] == "-":
                print(type(i[3]))
                be = '0.00'
            elif i[3] == "game":
                be = i[4]
            else:
                be = i[3]
            Win.append(be)
        Win_sun = float(0.0)
        for i in Win:
            i = float(i)
            Win_sun = Win_sun+i
        file1 = open("game.txt", "a+", encoding="utf-8")
        file1.writelines('Total WIN   ' + str(round(Win_sun, 2)) + "\n")
        file1.close()

        results = float(Win_sun)-float(bet_sum)
        file1 = open("game.txt", "a+", encoding="utf-8")
        file1.writelines(
            "Total NETTGAMING(Win/Loss) " + str(round(results, 2))+"\n")
        file1.close()

        # Total Free Games
        word = '0.0'
        length = len(Bet_Free_game)
        print(length)
        count = 0
        for i in range(0, length):
            if word == Bet_Free_game[i]:
                count += 1
        if count == 0:
            file1 = open("game.txt", "a+", encoding="utf-8")
            file1.writelines("\n\nTotal FREE GAMES are 0""\n")
            file1.close()
        else:
            file1 = open("game.txt", "a+", encoding="utf-8")
            file1.writelines("\n\nTotal FREE GAMES are " + str(count) + "\n")
            file1.close()

        free_game_list = []
        sum = 0
        for i in final_data:
            # print(i[3])
            if i[2] == "Free" and i[3] == 'game':
                free_game_list.append(i)
                sum = sum + float(i[4])
        file1 = open("game.txt", "a+", encoding="utf-8")
        file1.writelines("\n Total Free game winning is  " +
                         str(round(sum, 2)) + "\n")
        file1.close()

        file1 = open("free_game.txt", "a+", encoding="utf-8")
        file1.writelines(" user name " + usernameenter+"\n")
        for x in free_game_list:
            L = str(x).replace('[', '').replace(']', '')
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
        gamelists = ' '.join([str(elem) for elem in game_list])

        file1 = open("game.txt", "a+", encoding="utf-8")
        file1.writelines("\n\nGames played are " + gamelists + "\n")
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

        banned_game = unique(banned_game_list)
        if len(final_results) > 0:
            for x in final_results:
                file1 = open("banned_game_list.txt",
                             "a+", encoding="utf-8")
                L = str(x).replace('[', '').replace(']', '')
                file1.writelines("\n"+str(L)+"\n")
                file1.close()
        if len(banned_game) == 0:
            file1 = open("game.txt", "a+", encoding="utf-8")
            file1.writelines('\n\nNo Banned games detected' + "\n")
            file1.close()
        else:
            file1 = open("game.txt", "a+", encoding="utf-8")
            for game in banned_game:
                file1.writelines('\n\nBanned games played are' + game + "\n")
            file1.close()
        data_from_tableID = []
        for x in final_data:
            if x[1] != '0':
                data_from_tableID.append(x)
        file1 = open("game.txt", "a+", encoding="utf-8")
        file1.writelines("\n\nImportant credit logs are \n")
        for x in data_from_tableID:
            file1 = open("game.txt", "a+", encoding="utf-8")
            L = str(x).replace('[', '').replace(']', '')
            file1.writelines("\n"+str(L)+"\n")
            file1.close()

        transfer_in_sum = 0
        transfer_out_sum = 0

        for i in data_from_tableID:
            if i[1] == "Set" and i[2][:5] == "score":
                print(i[2][6:])
                if float(i[2][6:]) > 0.0:
                    transfer_in_sum = transfer_in_sum + float(i[2][6:])
                elif float(i[2][6:]) < 0.0:
                    transfer_out_sum = transfer_out_sum + \
                        float(i[2][6:])

        file1 = open("game.txt", "a+", encoding="utf-8")
        file1.writelines("\nTotal Transfer in " +
                         str(transfer_in_sum) + "\n")
        file1.writelines("\nTotal Transfer out " +
                         str(transfer_out_sum) + "\n")
        file1.close()

        file1 = open("game.txt", "a+", encoding="utf-8")
        file1.writelines("\nGames Cronology is\n\n")

        n = 0
        endtime = ''
        starttime = ''
        firsInstance = None
        lastInstance = None
        for game_name in game_list:
            print('game list')
            firsInstance = None
            gameFound = False
            for data in final_data:
                if game_name in data:
                    gameFound = True
                    if (firsInstance is None):
                        firsInstance = data
                        endtime = ' '.join(str(e)
                                           for e in firsInstance[-2:])
                    lastInstance = data
                    starttime = ' '.join(str(e)
                                         for e in lastInstance[-2:])
                else:
                    if gameFound:
                        break

            print(firsInstance[0]+" end time", endtime)
            print(lastInstance[0] + " start time", starttime)

            file1 = open("game.txt", "a+", encoding="utf-8")
            file1.writelines(firsInstance[0] +
                             "    end time     " + endtime+"\n")
            file1.writelines(lastInstance[0] +
                             "    start time   " + starttime+"\n")
            file1.close()

        file1.close()
        driver.quit()

    else:
        driver.close()
