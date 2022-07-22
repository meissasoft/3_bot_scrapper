#Automatically Login
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
import warnings
warnings.filterwarnings('ignore')
from selenium.webdriver.common.by import By

import pickle


driver = webdriver.Chrome('chromedriver.exe')
max_delay = 30
def sleep_and_find(browser, selector, by, isAll=False, isVisbible=False):
    myElem = None
    for i in range(1, max_delay):
        try:
            if isVisbible:
                myElem = WebDriverWait(browser, 1).until(EC.invisibility_of_element((by, selector)))
                break
            if isAll:
                myElem = WebDriverWait(browser, 1).until(EC.presence_of_all_elements_located(((by, selector))))
                break
            else:
                myElem = WebDriverWait(browser, 1).until(EC.presence_of_element_located((by, selector)))
                break
        except Exception as ex:
            print("selector ", selector, " not found in ", str(i), " seconds")
    return myElem



url = 'https://k111.918kiss.com'
driver.get(url)
pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
time.sleep(5)
error =sleep_and_find(driver,'//div[@class="sa-confirm-button-container"]//button',By.XPATH)
error.click()
username = sleep_and_find(driver,"userName",By.ID)
password = sleep_and_find(driver,"passWd", By.ID)
username.send_keys("kissme07sub2")
password.send_keys("GGG678")
loginButton = sleep_and_find( driver, "loginButton", By.ID)
loginButton.click()
pin = sleep_and_find( driver, "txt_Password", By.ID)
pin.send_keys("999000")
sleep_and_find( driver, "Button_OK", By.ID).click()

isLoogedIn = sleep_and_find(driver,"body > div.wrapper > aside > section > ul > li:nth-child(3) > a", By.CSS_SELECTOR)

if isLoogedIn:
    isLoogedIn.click()
    time.sleep(30)
    togglebutton = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#d_tip_2 > div > div > button.btn.btn-default.btn-flat.dropdown-toggle')))
    togglebutton.click()

    file1 = open("user_name_list.txt","a+")
    file1.close()

    time.sleep(5)

    total_player_list = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#d_tip_2 > div > div > ul > li:nth-child(1) > a")))
    total_player_list.click()
    time.sleep(15)

    driver.find_element('id',"Button_OK").click()
    time.sleep(15)

    user = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tblData"]')))
    user =user.text


    userlist = user.split(" ")
    user_list_data = []
    datalist = []
    for i in userlist:
        
        data = i.split('\n')
        datalist.append(data[0])

    user_list_data.append(datalist[0])
    user_list_data

    datalist2 = []
    for i in userlist:

        data = i.split('\n')
        datalist2.append(data)
    datalist2.pop(0)
    datalist2.pop()
    datalist2
    for i in datalist2:

        user_list_data.append(i[1])
    
    gamelog = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='com_Log_PlayerBetLog.aspx']")))
    gamelog.click()


    file1 = open('user_name_list.txt', 'r')
    uaerlist = file1.readlines()
    for user_name in user_list_data:
        print("for loop")
        for user in userlist:
            
            if user_name != user.strip(): 
                print("username",user_name)

                file1 = open("game.txt","a+")
                file1.writelines("User name " + user_name+"\n")
                file1.close()


                username_game_log = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "txt_UserName")))
                print("Hello")
                username_game_log.clear()
                username_game_log.send_keys(user_name)
                time.sleep(10)
                ok_game_log_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "Button_OK")))
                ok_game_log_button.click()
                time.sleep(20)
                try:
                    totalpages=driver.find_element('xpath',"//a[@class='laypage_last']").text
                    file1 = open("game.txt","a+")
                    file1.writelines("\nTotal Pages are "+ totalpages + " \n")
                    file1.close()
                    print(totalpages)
                except:
                    pass

                final_data=[] 
                match_data=[] 
                n = 1
                for n in range(int(totalpages)): 
                    rows=driver.find_elements("xpath",'//tr[@class="tr_h"]') 
                    for row in rows:
                        row=row.text.replace("SAFARI Heat","SAFARIHeat").replace("god of","godof").replace("Sultan`s Gold","Sultan`sGold").replace("Wong Choy","WongChoy").replace('Great Rhino','GreatRhino').replace('Dragon Gold','DragonGold').replace('Football Fans' , 'FootballFans').replace('Tally Ho', 'TallyHo').split(" ") 
                        # print("row",row)
                        if len(row)==8: 
                            final_data.append(row) 
                        if len(row)==9: 
                            final_data.append(row) 
                        if len(row)==10: 
                            match_data.append(row) 
                        if len(row)==12:  
                            match_data.append(row)
                        if len(row)==7: 
                            match_data.append(row) 
                    try:
                        print("next page===============================") 
                        next=driver.find_element("xpath","//a[@class='laypage_next']") 
                        next.click() 
                        time.sleep(10) 
                    except: 
                        print("Hel")
                        continue

                        
                end_game_time = final_data[0][-2] +" " + final_data[0][-1]
                start_game_time = final_data[-1][-2] + " " + final_data[-1][-1]

                if end_game_time and start_game_time:
                    file1 = open("game.txt","a+")
                    file1.writelines(" start game time " + start_game_time +"\n")
                    file1.writelines(" end game time " + end_game_time +"\n")
                    file1.close()

                # Total Bets
                Bet=[]
                try:
                    for i in final_data:
                        if i[2]=="Free" or i[2]=="-" or len(i[2]) >5:
                            be='0.0'
                        else:
                            be=i[2]
                        Bet.append(be)
                except Exception as e:
                    print(e)
                bet_sum = float(0.0)
                for i in Bet:
                    i=float(i)
                    bet_sum = bet_sum+i
                file1 = open("game.txt","a+")
                file1.writelines('\n\nTotal BETS ' + str(bet_sum)+"\n")
                file1.close()

                # Total Wins
                Win=[]
                for i in final_data:
                    b = ''
                    if i[3]=="-":
                        print(type(i[3]))
                        be='0.00'
                    elif i[3]=="game":
                        be='0.00'
                    else:
                        be=i[3]
                    Win.append(be)
                Win_sun = float(0.0)
                for i in Win:
                    i=float(i)
                    Win_sun = Win_sun+i
                file1 = open("game.txt","a+")
                file1.writelines('Total WIN   ' + str(Win_sun)+ "\n")
                file1.close()

                results=float(Win_sun)-float(bet_sum)
                file1 = open("game.txt","a+")
                file1.writelines("\nTotal NETTGAMING(Win/Loss) " + str(results)+"\n")
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

                file1 = open("game.txt","a+")
                file1.writelines(" Games played " + gamelists +"\n")
                file1.close()

                games = ["GreatBlue","HighWay","fish","OceanKing","Thunderbolt"]
                final_results=[]
                for i in final_data:
                    if i[0] in games:
                        final_results.append(i)
                    else:
                        pass

                banned_game_list = []
                for i in final_results:
                    banned_game_list.append(i[0])

                banned_game = unique(banned_game_list)
                if len(final_results)>0:
                    for x in final_results:
                        file1 = open("banned_game_list.txt","a+",encoding="utf-8")
                        L = str(x).replace('[','').replace(']','')
                        file1.writelines("\n"+str(L)+"\n")
                        file1.close()
                if len(banned_game)==0:
                    file1 = open("game.txt","a+")
                    file1.writelines('No Banned games detected' + "\n")
                    file1.close()
                else:
                    file1 = open("game.txt","a+")
                    for game in banned_game:
                        file1.writelines('Banned games played '+ game + "\n")
                    file1.close()
                data_from_tableID = []
                for x in final_data:
                    if x[1] !='0':
                        data_from_tableID.append(x)

                for x in data_from_tableID:
                    file1 = open("game.txt","a+",encoding="utf-8")
                    L = str(x).replace('[','').replace(']','')
                    file1.writelines("\n"+str(L)+"\n")
                    file1.close()

                transfer_in_sum = 0
                transfer_out_sum = 0

                for i in data_from_tableID:
                    if i[1] == "Set" and i[2][:5] == "score":
                        print(i[2][6:])
                        if float( i[2][6:]) > 0.0:
                            transfer_in_sum = transfer_in_sum + float( i[2][6:])
                        elif float( i[2][6:]) < 0.0:
                            transfer_out_sum = transfer_out_sum + float( i[2][6:]) 


                file1 = open("game.txt","a+")
                file1.writelines("\nTotal Transfer in "+ str(transfer_in_sum) +"\n")
                file1.writelines("\nTotal Transfer out "+ str(transfer_out_sum) +"\n")
                file1.close()

                # Total Free Games
                word='0.0'
                length=len(Bet)
                print(length)
                count=0
                for i in range(0,length):
                    if word == Bet[i]:
                        count+=1
                if count == 0:
                    file1 = open("game.txt","a+")
                    file1.writelines("\n\nTotal FREE GAMES are 0""\n")
                    file1.close()
                else:
                    file1 = open("game.txt","a+")
                    file1.writelines("\n\nTotal FREE GAMES "+str(count)+"\n")
                    file1.close()

                free_game_list = []
                sum = 0
                for i in final_data:
                    # print(i[3])
                    if i[2] == "Free" and i[3] == 'game':
                        free_game_list.append(i)
                        sum = sum + float(i[4])
                file1 = open("game.txt","a+")
                file1.writelines("\n Free game winning is  "+ str(sum) +"\n")
                file1.close()


                file1 = open("free_game.txt","a+",encoding="utf-8")
                file1.writelines(" user name " + user_name+"\n")
                for x in free_game_list:
                    L = str(x).replace('[','').replace(']','')
                    file1.writelines(str(L)+"\n")
                file1.close()

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
                                endtime = ' '.join(str(e) for e in firsInstance[-2:])
                            lastInstance = data
                            starttime = ' '.join(str(e) for e in lastInstance[-2:])
                        else:
                            if gameFound:
                                break

                    print(firsInstance[0]+" end time",endtime)
                    print(lastInstance[0] +" start time", starttime)

                    file1 = open("game.txt","a+")
                    file1.writelines(firsInstance[0]+ "    end time     " +endtime+"\n")
                    file1.writelines(lastInstance[0] +"    start time   "+ starttime+"\n")
                    file1.close()

                file1 = open("user_name_list.txt","a+")
                file1.writelines(user_name +"\n")
                file1.close()
            
            else:
                print('same user exist')
            break
                           
else:
    print("Unable to Login")







 
