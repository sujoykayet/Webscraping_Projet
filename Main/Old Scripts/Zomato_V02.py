import selenium
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
# from lxml import html 

Driver = webdriver.Chrome()
Driver.get('https://www.zomato.com/')
Driver.maximize_window()
time.sleep(5)

def Navigation():
    # -- Checking Zomato website is opening or not --
    try:
        wait(Driver, 30).until(EC.presence_of_element_located((By.XPATH, '//h1[contains(text(), "Discover the best food & drinks in")]')))
        print("Zomato website is loaded successfully")
        time.sleep(2)
    except:
        print("!!! Unable to load Zomato webside")

    # -- Scroll upto Popular localities in and around Kolkata  section --
    try:
        InvoiceSectionElement = Driver.find_element(By.XPATH, '//p[contains(text(), "Popular localities in and around")]')
        Driver.execute_script("arguments[0].scrollIntoView();", InvoiceSectionElement)
        print("Scroll down successfully upto 1st invoice section")
        time.sleep(5)
    except:
        print("Unable to Scroll down successfully upto 1st invoice section")
        pass

    # -- Click on the see more button --
    try:
        wait(Driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "see more")]/..'))).click()
        print("See more button clicked")
        time.sleep(3)
    except:
        print("!!! Unable to click see more button")

def Scraped():
    # -- Scrped data of Popular localities in and around Kolkata one by one --
    AreaCount = 1
    AreaList = []
    while True:
        try:
            print("\n****************** Area Count is: " + str(AreaCount) + " ******************")
            AreaName = wait(Driver, 10).until(EC.presence_of_element_located((By.XPATH, '(//p[contains(text(), "Popular localities in and around")]/../..//div[contains(@class, "sc-bke1zw-0 fIuLDK")]//a)[' + str(AreaCount) + ']//h5'))).text
            print("Area Name        : " + AreaName)
            AreaList.append(AreaName)
            NumberOfPlaces = wait(Driver, 10).until(EC.presence_of_element_located((By.XPATH, '(//p[contains(text(), "Popular localities in and around")]/../..//div[contains(@class, "sc-bke1zw-0 fIuLDK")]//a)[' + str(AreaCount) + ']//p'))).text
            print("Number of places : " + NumberOfPlaces)
            time.sleep(1)
            AreaCount += 1
        except:
            try:
                LastAreaName = wait(Driver, 10).until(EC.presence_of_element_located((By.XPATH, '(//p[contains(text(), "Popular localities in and around")]/../..//div[contains(@class, "sc-bke1zw-0 fIuLDK")]//a)[' + str(AreaCount - 1) + ']//h5'))).text
                print("No more area left Last Area Name is: " + LastAreaName)
                print("\n================== All Data Stored Successfully ==================\n")
                break
            except:
                print("!!! Unable to Scrped Zomato webside data")

    print("All area list : ", AreaList)

    # -- Scrap all data of individul locations --
    for location in AreaList:
        try:
            print("\n+++++++++++++++++++ Area Name is: " + str(location) + " +++++++++++++++++++\n")
            wait(Driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//h5[contains(text(), "' + str(location) + '")]/../../..'))).click()
            print(location + " Location selected successfully")
            time.sleep(2)
        except:
            print("!!! Unable to Select location : " + location)
            
        # -- Check the page is loaded or not --
        try:
            wait(Driver, 30).until(EC.presence_of_element_located((By.XPATH, '//h1[contains(text(), "' + str(location) + '")]')))
            print("Correct location page is loaded successfully")
            time.sleep(2)
        except:
            print("!!! Unable to load Zomato webside")
        
        # -- Filter the top reated option --
        try:
            wait(Driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Filters")]'))).click()
            print("Filter option clicked")
            time.sleep(2)
            wait(Driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Rating: High to Low")]/../input/..'))).click()
            print("Select the Popularity option")
            wait(Driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Apply")]/../..'))).click()
            print("Apply button clicked")
            time.sleep(1)
        except:
            print("!!! Unable to Filter the top reated option")
        
        # -- Scroll upto Popular localities in and around Kolkata  section --
        try:
            InvoiceSectionElement = Driver.find_element(By.XPATH, '//h1[contains(text(), "' + str(location) + '")]')
            Driver.execute_script("arguments[0].scrollIntoView();", InvoiceSectionElement)
            print("Scroll down successfully upto 1st invoice section\n")
            time.sleep(3)
        except:
            print("Unable to Scroll down successfully upto 1st invoice section")
            pass

        # -- Scrap data --
        for PlaceCount in range(1,11):
            try:
                print("******* Place Count : " + str(PlaceCount) + " *******")
                PlaceName = wait(Driver, 10).until(EC.presence_of_element_located((By.XPATH, '(//div[contains(@class, "sc-1mo3ldo-0 sc")]/div[contains(@class, "sc-")]/div)[' + str(PlaceCount) + ']//a[2]/div[1]/h4'))).text
                print("\nPlace Name    : " + PlaceName)
                Price = wait(Driver, 10).until(EC.presence_of_element_located((By.XPATH, '(//div[contains(@class, "sc-1mo3ldo-0 sc")]/div[contains(@class, "sc-")]/div)[' + str(PlaceCount) + ']//a[2]/div[2]/p[2]'))).text
                print("Price Details : " + Price)
                Star = wait(Driver, 10).until(EC.presence_of_element_located((By.XPATH, '(//div[contains(@class, "sc-1mo3ldo-0 sc")]/div[contains(@class, "sc-")]/div)[' + str(PlaceCount) + ']//a[2]//div[@class="sc-1q7bklc-1 cILgox"]'))).text
                print("Rating      : " + Star + "*")
                MenuExample = wait(Driver, 10).until(EC.presence_of_element_located((By.XPATH, '(//div[contains(@class, "sc-1mo3ldo-0 sc")]/div[contains(@class, "sc-")]/div)[' + str(PlaceCount) + ']//a[2]/div[2]/p[1]'))).text
                print("Famous Items  : " + MenuExample)
                print("\n================================================================================================================\n")

                if PlaceCount == 10:
                    raise Exception
            except:
                try:
                    wait(Driver, 10).until(EC.presence_of_element_located((By.XPATH, '(//div[contains(@class, "sc-1mo3ldo-0 sc")]/div[contains(@class, "sc-")]/div)[' + str(PlaceCount - 1) + ']//a[2]/div[1]/h4'))).text # LastPlaceName
                    print("Here are the top 10 most reated suggestions of : " + location)
                    print("\n================== All Data Stored Successfully ==================\n")
                    break
                except:
                    print("!!! Issue whil scrap data of : " + location)

            # -- Generating CSV file for Scraped Data (Nothing to change here) --
            FileResult = open("Info.csv", 'a',encoding='utf-8')
            FileResult.write(str(location) + '|' + str(PlaceName) + '|' +  str(Price) + '|' + str(Star) + '|' + str(MenuExample) + '\n')
            FileResult.close()

        if location not in AreaList[-1]:
            Driver.get('https://www.zomato.com/')
            time.sleep(2)
            Navigation()
        else:
            print("=====================|||||| PROCESS END |||||=====================")

def Runbot():
    print("\n++++++++++++++++++++++++++++++++++++++++ Automation Process Start  ++++++++++++++++++++++++++++++++++++++++\n")
    FileResult = open("Info.csv", "w")
    FileResult.write('Area_Name|Place_Name|Price_Rate|Star_Rateing|Menu_Example\n')
    FileResult.close()
    Navigation()
    Scraped()

Runbot()
