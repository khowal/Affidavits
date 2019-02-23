import requests
from bs4 import BeautifulSoup
import os


# http://wbceo.in/affidavits_2006/6/DineshRoy/DineshRoy_SC1.htm
# http://wbceo.in/affidavits_2006/6/DineshRoy/DineshRoy_SC1.jpg

def CreateDir(url):
    path = os.getcwd()
    for dir in url.split('/')[4:-1]:
        path = path + '/' + dir
        try:
            os.mkdir(path)
        except:
            pass

    return path


def pdfDownload(url):
    content = requests.get(url)
    out_file = url.split('/')[-1]

    path = CreateDir(url)
    path = path +'/'+  out_file

    file = open(path, 'wb')
    file.write(content.content)
    file.close()

    return True

def imgDownload(url):
    content = requests.get(url)
    soup =  BeautifulSoup(content.text,"html.parser")
    image = soup.find('img')
    out_file = image['src'].strip()
    path = CreateDir(url)
    path = path +'/'+  out_file
    imgURL = url.replace(os.path.basename(url),"") + out_file

    response = requests.get(imgURL, stream=True)
    with open(out_file, 'wb') as out_file:
        out_file.write(response.content)
    del response

    return True

def giveLinks(baseUrl, url):
    links = []
    content = requests.get(url)
    soup = BeautifulSoup(content.text, "html.parser")
    anchors = soup.find_all('a')
    for anchor in anchors:
        link = baseUrl + anchor['href']
        links.append(link)

    return links


if __name__ == "__main__":
    url = "http://eci.nic.in/affidavits/AFF_AEFeb2005/Jharkhand/ACList.htm"
    bURL = "http://eci.nic.in/affidavits/AFF_AEFeb2005/Jharkhand/"
    acLinks = giveLinks( bURL , url)
    for acLink in acLinks:
        bURL = acLink.replace(os.path.basename(acLink),"")
        canLinks = giveLinks(bURL, acLink)
        for canLink in canLinks:
            print canLink
            bURL = canLink.replace(os.path.basename(canLink),"")
            canDocs = giveLinks(bURL, canLink)
            for canDoc in canDocs:
                print canDoc
                # imgDownload(canDoc)
