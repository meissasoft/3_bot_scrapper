from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

max_delay = 30


def sleep_and_find(browser, selector, by, isAll=False, isVisbible=False):
    myElem = False
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


def get_browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-popup-blocking")
    options.add_argument("test-type")
    browser = webdriver.Chrome('chromedriver.exe', chrome_options=options)
    return browser


# Automatically Login

# Automatically Login
url = 'https://k2.mega683.com'
browser = get_browser()
browser.get(url)
username = sleep_and_find(browser, 'userName', By.ID)
password = sleep_and_find(browser, 'password', By.ID)
username.send_keys("Mega1649s1")
password.send_keys("Manstarwo22!")
login = sleep_and_find(browser, 'J_btnSubmit', By.ID)
if login:
    login.click()
    usermanagment = sleep_and_find(
        browser, '/html/body/div/aside/section/ul/li[3]/a', By.XPATH)
    if usermanagment:
        usermanagment.click()
        shoesize = WebDriverWait(browser, 40).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#d_tip_2 > div > div > button.btn.btn-default.btn-flat.dropdown-toggle')))
        shoesize.click()
        shoesize1 = WebDriverWait(browser, 40).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#d_tip_2 > div > div > ul > li:nth-child(1) > a')))
        shoesize1.click()
        ok_Button = sleep_and_find(browser, 'Button_OK', By.ID)
        if ok_Button:
            ok_Button.click()
            user = WebDriverWait(browser, 30).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="tblData"]')))
            user_list_data = []
            if user:
                user = user.text
                # print(user)
                userlist = user.split(" ")

                datalist = []
                for i in userlist:
                    data = i.split('\n')
                    datalist.append(data[0])
                user_list_data.append(datalist[0])
                datalist2 = []
                for i in userlist:
                    data = i.split('\n')
                    datalist2.append(data)
                datalist2
                for i in datalist2:
                    if len(i) == 2:
                        user_list_data.append(i[1])

            game_log = sleep_and_find(
                browser, '/html/body/div/aside/section/ul/li[6]/a', By.XPATH)
            if game_log:
                game_log.click()

                for user_name in user_list_data:
                    username_game_log = WebDriverWait(browser, 30).until(
                        EC.element_to_be_clickable((By.ID, "txt_UserName")))
                    print("Hello")
                    file1 = open("game.txt", "a+", encoding="utf-8")
                    file1.writelines("\n\nUser Name " + user_name+"\n")
                    file1.close()
                    username_game_log.clear()
                    username_game_log.send_keys(user_name)
                    ok_game_log_button = WebDriverWait(browser, 30).until(
                        EC.element_to_be_clickable((By.ID, "Button_OK")))
                    ok_game_log_button.click()
                    time.sleep(15)
                    browser.switch_to.frame(
                        browser.find_element(By.TAG_NAME, "iframe"))

                    try:
                        totalpages = browser.find_element(
                            By.CLASS_NAME, 'laypage_last').text
                        print(totalpages)
                        file1 = open("game.txt", "a+")
                        file1.writelines(
                            "\nTotal Pages are: " + totalpages + " \n")
                        file1.close()

                    except:
                        pass
                    final_data = []
                    match_data = []
                    # key=["RedEnvelope","JackPot","Setscore"]
                    n = 0
                    for n in range(int(totalpages)):

                        time.sleep(10)
                        rows = browser.find_elements(
                            "xpath", '//*[@id="tblData"]')
                        for row in rows:
                            row = row.text.replace("SAFARI Heat", "SAFARIHeat").replace("god of", "godof").replace(
                                "Sultan`s Gold", "Sultan`sGold").replace("Wong Choy", "WongChoy").replace('Lion Dance', 'LionDance').split("\n")
                            final_data.append(row)
                        try:
                            print("next page===============================")
                            next = WebDriverWait(browser, 30).until(
                                EC.element_to_be_clickable((By.CLASS_NAME, 'laypage_next')))
                            next.click()
                        except:
                            print("Hel")
                            break
                    browser.switch_to.default_content()

                    def unique(list1):
                        unique_list = []
                        for x in list1:
                            if x not in unique_list:
                                unique_list.append(x)
                        return unique_list
                    l = []
                    data_split = []
                    for i in final_data:
                        for j in i:
                            split_data = j.split(',')
                            data_split.append(split_data)
                    data_tableId = []
                    for i in data_split:
                        # for j in i:
                        data_space_splited = i[0].split(" ")
                        data_tableId.append(data_space_splited)
                    for ga in data_tableId:
                        l.append(ga[0])
                    game_list = unique(l)

                    file1 = open("game.txt", "a+", encoding="utf-8")
                    all_unique_game = ''
                    for game in game_list:
                        all_unique_game += " " + game + " "
                    file1.writelines("All Unique game " +
                                     all_unique_game + " \n")
                    file1.close()

                    banned_games = ["GreatBlue", "HighWay",
                                    "fish", "OceanKing", "Thunderbolt"]
                    final_results = []
                    for i in data_tableId:
                        # print(i[0])
                        if i[0] in banned_games:
                            # print(i[0])
                            final_results.append(i)
                        else:
                            pass
                            # print("No banned games found")
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
                        file1.writelines('No Banned games detected' + "\n")
                        file1.close()
                    else:
                        file1 = open("game.txt", "a+", encoding="utf-8")
                        for game in banned_game:
                            file1.writelines(
                                'Banned games played ' + game + "\n")
                        file1.close()
                    end_game_time = data_tableId[0][-2] + \
                        " " + data_tableId[0][-1]
                    start_game_time = data_tableId[-1][-2] + \
                        " " + data_tableId[-1][-1]
                    file1 = open("game.txt", "a+", encoding="utf-8")

                    file1.writelines('Start time game log ' +
                                     start_game_time + "\n")
                    file1.writelines('End time game log ' +
                                     end_game_time + "\n\n")
                    file1.close()

                    data_from_tableID = []
                    # data_tableId
                    for i in data_tableId:

                        if i[1] != "0" or len(i) < 2:
                            data_from_tableID.append(i)
                    for x in data_from_tableID:
                        file1 = open("game.txt", "a+", encoding="utf-8")
                        L = str(x).replace('[', '').replace(']', '')
                        file1.writelines(str(L)+"\n")
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

                    file1 = open("game.txt", "a+", encoding="utf-8")
                    file1.writelines("\nTotal Transfer in " +
                                     str(total_transfer_in)+"\n")
                    file1.writelines("\nTotal Transfer out " +
                                     str(total_transfer_out)+"\n")
                    file1.close()

                    # Total Bets

                    Bet = []
                    try:
                        for i in data_tableId:
                            if i[2] == "Free" or i[2] == "-" or len(i[2]) > 5:
                                be = '0.0'
                            else:
                                be = i[2]
                            Bet.append(be)
                    except Exception as e:
                        print(e)

                    bet_sum = float(0.0)
                    for i in Bet:
                        i = float(i)
                        bet_sum = bet_sum+i

                    file1 = open("game.txt", "a+", encoding="utf-8")
                    file1.writelines('\n\nTotal BETS ' + str(bet_sum) + "\n")
                    file1.close()

                    # Total Wins

                    Win = []
                    for i in data_tableId:
                        b = ''
                        if i[3] == "-":
                            print(type(i[3]))
                            be = '0.00'
                        elif i[3] == "game":
                            be = '0.00'
                        else:
                            be = i[3]
                        Win.append(be)

                    Win_sun = float(0.0)
                    for i in Win:
                        i = float(i)
                        Win_sun = Win_sun+i

                    file1 = open("game.txt", "a+", encoding="utf-8")
                    file1.writelines('Total WIN   ' + str(Win_sun) + "\n")
                    file1.close()
                    results = float(Win_sun)-float(bet_sum)
                    file1 = open("game.txt", "a+", encoding="utf-8")
                    file1.writelines(
                        "\nTotal NETTGAMING(Win/Loss) " + str(results)+"\n")
                    file1.close()
                    # Total Free Games

                    word = '0.0'
                    length = len(Bet)
                    print(length)
                    count = 0
                    for i in range(0, length):
                        if word == Bet[i]:
                            count += 1
                    if count == 0:
                        file1 = open("game.txt", "a+", encoding="utf-8")
                        file1.writelines("\n\nTotal FREE GAMES are 0""\n")
                        file1.close()
                    else:
                        file1 = open("game.txt", "a+", encoding="utf-8")
                        file1.writelines(
                            "\n\nTotal FREE GAMES "+str(count)+"\n")
                        file1.close()

                    free_game_list = []
                    sum = 0
                    for i in data_tableId:
                        # print(i[3])
                        if i[2] == "Free" and i[3] == 'game':
                            free_game_list.append(i)
                            sum = sum + float(i[4])
                    file1 = open("game.txt", "a+", encoding="utf-8")
                    file1.writelines(
                        "\n Free game winning is  " + str(sum) + "\n")
                    file1.close()
                    file1 = open("free_game.txt", "a+", encoding="utf-8")
                    file1.writelines(" user name " + user_name+"\n")
                    for x in free_game_list:
                        L = str(x).replace('[', '').replace(']', '')
                        file1.writelines(str(L)+"\n")
                    file1.close()

                    endtime = ''
                    starttime = ''

                    for game_name in game_list:
                        firsInstance = None
                        lastInstance = None

                        gameFound = False
                        for data in data_tableId:
                            if game_name in data:
                                gameFound = True
                                print("game_name", game_name)
                                print("game_data", data)
                                if (firsInstance is None):
                                    firsInstance = data
                                    print("firsInstance", firsInstance)
                                    endtime = ' '.join(str(e)
                                                       for e in firsInstance[-2:])
                                lastInstance = data
                                print("lastInstance", lastInstance)
                                starttime = ' '.join(str(e)
                                                     for e in lastInstance[-2:])
                            else:
                                if gameFound:
                                    break

                        print(firsInstance[0]+" end time", endtime)
                        print(lastInstance[0] + " start time", starttime)
                        file1 = open("game.txt", "a+", encoding="utf-8")
                        file1.writelines(
                            firsInstance[0] + "    end time     " + endtime+"\n")
                        file1.writelines(
                            lastInstance[0] + "    start time   " + starttime+"\n")
                        file1.close()
else:
    print('not login')
