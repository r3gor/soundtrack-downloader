from bs4 import BeautifulSoup
import requests
import wget
import sys
import os

if (len(sys.argv)<2):
    print("Usage: python main.py url output_folder")
    print("\n\t[*] url: the playlist url from downloads.khinsider.com")
    print("\t[*] output_folder: the folder where the mp3s are downloaded")
    print("\n\t[!] Put url and output_folder in quotes (example: 'http://downl...') ")
    exit(0)

url = sys.argv[1]
output_path = sys.argv[2]

try:
    os.mkdir(output_path)
except FileExistsError:
    print("Note: the folder already exists")

# main page
html = requests.get(url)
bs = BeautifulSoup(html.text, "html.parser")

table = bs.find("table", attrs={"id":"songlist"})
list_tr = table.find_all("tr")
list_tr = list_tr[1:-2]

for song in list_tr:
    td_link_song = song.find_all("td", attrs={"class":"clickable-row"})[0]
    element = td_link_song.find(href=True)
    
    name = element.text
    sub_url = element["href"]
    prefix_url = "https://downloads.khinsider.com/"
    sub_url = prefix_url + sub_url

    # sub page (donwload)
    html_sub = requests.get(sub_url)
    bs_sub = BeautifulSoup(html_sub.text, "html.parser")

    download_url = bs_sub.find_all("a", attrs={"style":"color: #21363f;"})[0]
    download_url = download_url["href"]
    
    # finally, download file
    print("song: \t" + name)
    wget.download(download_url, out=f"{output_path}/{name}.mp3")
    print()