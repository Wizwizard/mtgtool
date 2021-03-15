import requests

base_url = "http://www.iyingdi.com"
magic_deck = "/magic/deck"

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
headers = {
    ":authority": "www.iyingdi.com",
    "method": "POST",
    "user-agent": user_agent
}

token = "6bae41e0f9084b6caf6c4aa8a34bdb07"
cards = '''Deck
4 Alseid of Life\'s Bounty
4 Faceless Haven
4 Giant Killer
1 Legion Angel
4 Luminarch Aspirant
4 Maul of the Skyclaves
3 Reidane, God of the Worthy
4 Seasoned Hallowblade
4 Selfless Savior
4 Skyclave Apparition
20 Snow-Covered Plains
4 Archon of Emeria

Sideboard
3 Drannith Magistrate
4 Glass Casket
3 Legion Angel
3 Usher of the Fallen
2 Idol of Endurance
'''
type = 1
format = "史迹"

data = {
    "token": token,
    "cards": cards,
    "type": type,
    "format": format
}

url = base_url + magic_deck
response = requests.post(url, data)
print(response.status_code)
print(response.text)