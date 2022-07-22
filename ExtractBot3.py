from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import warnings
warnings.filterwarnings('ignore')
max_delay = 40
def sleep_and_find(browser, selector, by, isAll=False, isVisbible=False):
    myElem = False
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

def get_browser():
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument("start-maximized")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("test-type")
    browser = webdriver.Chrome('chromedriver.exe', chrome_options=options)
    return browser

#Automatically Login


url = 'http://pr2.pussy888.com/'
browser = get_browser()
# # time.sleep(10)
browser.get(url)
username = sleep_and_find(browser , 'userName', By.ID)
password = sleep_and_find(browser , 'passWd', By.ID)
print(username , password)
username.send_keys("pussysubrp")
password.send_keys("Danger4562")
login = sleep_and_find(browser, 'loginButton',By.ID)
if login:
    login.click()
    usermanagment = sleep_and_find(browser , '/html/body/div[2]/aside/section/ul/li[2]/a',By.XPATH)
    if usermanagment:
        usermanagment.click()
        agent_Data = sleep_and_find(browser , '//*[@id="t_agentList"]/tr[9]/td[2]/a',By.XPATH)
        if agent_Data:
            agent_Data.click()
            shoesize = WebDriverWait(browser, 40).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="d_tip_2"]/a[1]')))
            time.sleep(10)
            shoesize.click()
            ok_Button =sleep_and_find(browser,'Button_OK',By.ID)
            if ok_Button:
                ok_Button.click()         
                user = WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tblData"]')))
                user_list_data = []
                if user:
                    user =user.text
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
                for user_name in user_list_data:
                    search_log = sleep_and_find(browser , '/html/body/div[2]/aside/section/ul/li[3]/a',By.XPATH)
                    if search_log:
                        search_log.click()
                           
                        search_field = sleep_and_find(browser , 'txt_UserName',By.ID)
                        file1 = open("game.txt","a+",encoding="utf-8")
                        file1.writelines("\n\nUser Name " +user_name+"\n")
                        file1.close()
                        search_field.clear()
                        search_field.send_keys(user_name)
                        ok_Button =sleep_and_find(browser,'Button_OK',By.ID)
                        if ok_Button:
                            ok_Button.click()
                            username_game_log = WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tblData_1"]/tr/td[13]/button[3]')))
                            if username_game_log:
                                username_game_log.click()
                                ok_Button =sleep_and_find(browser,'Button_OK',By.ID)
                                if ok_Button:
                                    ok_Button.click()
                                    time.sleep(10)
                                    try:
                                        totalpages=browser.find_element(By.CLASS_NAME,"laypage_last").text
                                        file1 = open("game.txt","a+",encoding="utf-8")
                                        file1.writelines("\nTotal Pages are "+ totalpages + " \n")
                                        file1.close()
                                        print(totalpages)
                                    except:
                                        pass
                                    final_data=[]
                                    match_data=[]
                                    n = 1
                                    for n in range(int(totalpages)):
                                        rows=browser.find_elements("xpath",'//tr[@class="tr_h"]')
                                        for row in rows:
                                            row=str(row.text).replace("SAFARI Heat","SAFARIHeat").replace("god of","godof").replace("Sultan`s Gold","Sultan`sGold").replace("Wong Choy","WongChoy").replace('Great Rhino','GreatRhino').replace('Dragon Gold','DragonGold').replace('Football Fans' , 'FootballFans').replace('Tally Ho', 'TallyHo').replace()
                                            row=row.split(" ")
                                            final_data.append(row)
                                            # print("row",row)
                                            
                                        try:
                                            print("next page===============================")
                                            next=browser.find_element("xpath","//a[@class='laypage_next']")
                                            next.click()
                                            time.sleep(10)
                                        except:
                                            print("Hel")
                                            continue
                                    end_game_time = final_data[0][-2] +" " + final_data[0][-1]
                                    start_game_time = final_data[-1][-2] + " " + final_data[-1][-1]
                                    if end_game_time and start_game_time:
                                        file1 = open("game.txt","a+" ,encoding="utf-8")
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
                                    file1 = open("game.txt","a+" ,encoding="utf-8")
                                    file1.writelines('\n\nTotal BETS ' + str(bet_sum))
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
                                        file1 = open("game.txt","a+",encoding="utf-8")
                                        file1.writelines("\n\nTotal FREE GAMES are 0""\n")
                                        file1.close()
                                    else:
                                        file1 = open("game.txt","a+",encoding="utf-8")
                                        file1.writelines("\n\nTotal FREE GAMES "+str(count)+"\n")
                                        file1.close()

                                        
                                    
                                    free_game_list = []
                                    sum = 0
                                    for i in final_data:
                                        # print(i[3])
                                        if i[2] == "Free" and i[3] == 'game':
                                            free_game_list.append(i)
                                            sum = sum + float(i[4])
                                    file1 = open("game.txt","a+",encoding="utf-8")
                                    file1.writelines("\nFree game winning is  "+ str(sum) +"\n")
                                    file1.close()
                                    file1 = open("free_game.txt","a+",encoding="utf-8")
                                    file1.writelines(" user name " + user_name+"\n")
                                    for x in free_game_list:
                                        L = str(x).replace('[','').replace(']','')
                                        file1.writelines(str(L)+"\n")
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
                                        elif i[3]=="Free":
                                            be='0.00'
                                        else:
                                            be=i[3]
                                        Win.append(be)
                                    Win_sun = float(0.0)
                                    for i in Win:
                                        i=float(i)
                                        Win_sun = Win_sun+i
                                    file1 = open("game.txt","a+",encoding="utf-8")
                                    file1.writelines('Total WIN   ' + str(Win_sun)+ "\n")
                                    file1.close()
                                    results=float(Win_sun)-float(bet_sum)
                                    file1 = open("game.txt","a+",encoding="utf-8")
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
                                    file1 = open("game.txt","a+",encoding="utf-8")
                                    file1.writelines("Games Played " + gamelists +"\n")
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
                                        file1 = open("game.txt","a+",encoding="utf-8")
                                        file1.writelines('No Banned games detected' + "\n")
                                        file1.close()
                                    else:
                                        file1 = open("game.txt","a+",encoding="utf-8")
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
                                        file1.writelines(str(L)+"\n")
                                        file1.close()
                                    transfer_in_sum = 0
                                    transfer_out_sum = 0
                                    for i in data_from_tableID:
                                        if i[1] == "Set" and i[2][:5] == "score":
                                            if float( i[2][6:]) > 0.0:
                                                transfer_in_sum = transfer_in_sum + float( i[2][6:])
                                            elif float( i[2][6:]) < 0.0:
                                                transfer_out_sum = transfer_out_sum + float( i[2][6:])

                                    file1 = open("game.txt","a+",encoding="utf-8")
                                    file1.writelines("\nTotal Transfer in "+ str(transfer_in_sum) +"\n")
                                    file1.writelines("\nTotal Transfer out "+ str(transfer_out_sum) +"\n\n")
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
                                        file1 = open("game.txt","a+",encoding="utf-8")
                                        file1.writelines(firsInstance[0]+ "    end time     " +endtime+"\n")
                                        file1.writelines(lastInstance[0] +"    start time   "+ starttime+"\n")
                                        file1.close()

else:
    print("Not login")            
    