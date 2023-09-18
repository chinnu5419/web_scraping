import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def name(soup_new):
    property_name=soup_new.find("h1",attrs={'class':"ProjectInfo__imgBox1 title_bold"})
    if property_name:
        return ''.join(property_name.find_all(string=True, recursive=False)).strip()
    return "None"


def cost(soup_new):
    property_cost=soup_new.find("span",attrs={'class':"list_header_semiBold configurationCards__configurationCardsHeading"})
    if property_cost:
        property_cost=property_cost.get_text().encode().split()
    else:
        return "None"
    if property_cost[0]!=b'Price':
        property_cost=property_cost[1:]
    s=''
    for i in property_cost:
        s+=i.decode()    
    return s.strip()



def type1(soup_new):
    type1=soup_new.find("span",attrs={'class':"ellipsis list_header_semiBold configurationCards__configurationCardsSubHeading"})
    if type1:
        return type1.get_text().strip()
    return "None"
    


def locality(soup_new):
    loc=soup_new.find("h1",attrs={'class':"ProjectInfo__imgBox1 title_bold"}).find("span",attrs={'class':"ProjectInfo__hideTxt"})
    if loc:
        return loc.get_text().split(',')
    return "None,None"




def area(soup_new):
    are=soup_new.find("span",attrs={"class":"caption_subdued_medium configurationCards__cardAreaSubHeadingOne"})
    if are:
        return are.get_text().strip()
    return "None"


cities=["hyderabad","delhi","pune","mumbai","lucknow","agra","ahmedabad","kolkata","jaipur","chennai","bangalore"]

d={"Property Name":[],"Property Cost":[],"Property Type":[],"Property Area":[],"propertyLocality":[],"propertyCity":[],"Individual Property Link":[]}

driver=webdriver.Chrome()



headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

for i in cities:
    
    driver.get("https://www.99acres.com/")
    search=driver.find_element(By.ID, 'keyword2')
    
    search.send_keys(i)

    search.send_keys(Keys.RETURN)

    time.sleep(2)

    url=driver.current_url    

    print(url)

    res = requests.get(url,headers=headers)
    soup_data = BeautifulSoup(res.text, 'html.parser')

    anchors = soup_data.find_all("a",attrs={'class':"srpTuple__dFlex"})
    anchors1= soup_data.find_all("a",attrs={'class':"projectTuple__projectName projectTuple__pdWrap20 ellipsis"})




    linked_list=[]
    for i in anchors:
        linked_list.append("https://www.99acres.com/"+i.get('href'))    

    for i in anchors1:
        linked_list.append(i.get('href'))    


    for i in linked_list:
        res=requests.get(i,headers=headers)
        soup_new = BeautifulSoup(res.text, 'html.parser')
            
        d["Property Name"].append(name(soup_new))
            
        d["Property Cost"].append(cost(soup_new))
            
        d["Property Type"].append(type1(soup_new))
            
        a=locality(soup_new)
            
        d["propertyCity"].append(a[1].strip())
            
        d["propertyLocality"].append(a[0].strip())
            
        d["Property Area"].append(area(soup_new))
            
        d["Individual Property Link"].append(i)
        print(d)

driver.quit()

print(d)
