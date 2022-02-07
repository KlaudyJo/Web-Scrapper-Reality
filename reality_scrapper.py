import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}
articles_texts = []
articles_links = []
lokalita = []
typOfarticles = []
datePfPublish = []
for i in range(1, 20):
    response = requests.get("https://www.annonce.cz/byty-na-prodej$18.html?perPage=all&page={}".format(i),
                            headers=header)
    annonce = response.text

    soup_1 = BeautifulSoup(annonce, "html.parser")
    articles = soup_1.find_all(name="a", class_="clickable")
    for tag in articles:
        text = tag.getText()
        articles_texts.append(text)
        link = tag.get("href")
        time.sleep(1)
        ch_link="https://www.annonce.cz" + link
        articles_links.append(ch_link)

    for td in soup_1.select("td[class='right']"):
        a = td.text.strip("'\n")
        lokalita.append(a)
    for article in soup_1.find_all(name="div", class_="request-type"):
        word = article.getText()
        word = word.strip()
        typOfarticles.append(word)
    for date in soup_1.find_all(name="div", class_="ad-date"):
        word = date.getText()
        word = word.strip()
        datePfPublish.append(word)
    time.sleep(1)
telNumber = []
time.sleep(20)
for i in articles_links:
    response = requests.get(i)
    annonce_det = response.text
    soup_1 = BeautifulSoup(annonce_det, "html.parser")
    word = ""
    try:
        i = soup_1.find(name="a", class_="phone-link")
        word = i.get("href")
        telNumber.append(word)
    except:
        word = "Není uvedeno"
        telNumber.append(word)
    time.sleep(5)

scrapped_d = {
    "Názov": articles_texts,
    "Nabídka": typOfarticles,
    "Odkaz": articles_links,
    "Lokalita": lokalita,
    "Zverejneno": datePfPublish,
    "Telefon": telNumber,
}

df = pd.DataFrame.from_dict(scrapped_d, orient="index")
df =df.transpose()
writer = pd.ExcelWriter("annonce_byty.xlsx")
df.to_excel(writer, "Byty")
writer.save()
print('DataFrame is written successfully to Excel Sheet.')
