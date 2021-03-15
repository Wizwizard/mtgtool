import requests
from bs4 import BeautifulSoup


MTGAZONE_BASEURL = "https://mtgazone.com/decks"
STANDARD = "standard"
HISTORIC = "historic"

USER_AGENT_CHROME = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36"
HEARDERS = {
    "user-agent": USER_AGENT_CHROME,
    "referer": "https://mtgazone.com/decks/standard/"
}


def get_html_by_url(url):
    response = requests.get(url, HEARDERS, timeout=10)
    html = response.text
    return html


def get_decks_by_format(meta=STANDARD):
    url = MTGAZONE_BASEURL + "/" + meta
    html = get_html_by_url(url)
    soup = BeautifulSoup(html, features="lxml")
    # <h4 class="pt-cv-title">
    # <a href="https://mtgazone.com/deck/naya-ramp-by-noxus-blackmountain-394-mythic-november-2020-season/"
    # class="_self cvplbd" target="_self" >
    # Naya Ramp by Noxus Blackmountain &#8211; #394 Mythic – November 2020 Season</a></h4>
    deck_tags = soup.find_all("h4", class_="pt-cv-title")
    # (name, details_url)
    decks = []
    for deck_tag in deck_tags:
        child = deck_tag.contents[0]
        deck_details_url = child["href"]
        deck_name = child.string
        decks.append((deck_name, deck_details_url))
    return decks


def get_deck_code_by_details_url(url):
    html = get_html_by_url(url)
    soup = BeautifulSoup(html, features="lxml")
    mtga_export_button = soup.find("div", class_="icon mtga-icon")
    #<div role="button" class="icon mtga-icon "
    # onclick="copy('Companion\r\n1 Jegantha, the Wellspring\r\n\r\nDeck\r\n3 Bala Ged Recovery\r\n4 Cultivate\r\n2 Evolving Wilds\r\n4 Fabled Passage\r\n4 Felidar Retreat\r\n11 Forest\r\n4 Llanowar Visionary\r\n4 Lotus Cobra\r\n2 Mountain\r\n4 Phylath, World Sculptor\r\n2 Plains\r\n4 Solemn Simulacrum\r\n4 Tangled Florahedron\r\n4 Ugin, the Spirit Dragon\r\n4 Wolfwillow Haven\r\n\r\nSideboard\r\n3 Chainweb Aracnir\r\n4 Elder Gargaroth\r\n1 Jegantha, the Wellspring\r\n2 Klothys, God of Destiny\r\n4 Mazemind Tome\r\n1 Shredded Sails\r\n')"></div>
    deck_code = mtga_export_button["onclick"][6:-2].replace("\\r\\n", "\n")
    # print(deck_code)
    return deck_code


l = [('BO1 Sultai Ultimatum by Achux – #1199 Mythic – March 2021 Ranked Season', 'https://mtgazone.com/deck/bo1-sultai-ultimatum-by-achux-1199-mythic-march-2021-ranked-season/'), ('Jeskai Cycling by thekey – #48 Mythic – March 2021 Ranked Season', 'https://mtgazone.com/deck/jeskai-cycling-by-thekey-269-mythic-march-2021-ranked-season/'), ('Selesnya Toski by Dsanue – #836 Mythic – March 2021 Ranked Season', 'https://mtgazone.com/deck/selesnya-toski-by-dsanue-836-mythic-march-2021-ranked-season/'), ('Temur Transmogrify by HowlingMines – #848 Mythic – March 2021 Ranked Season', 'https://mtgazone.com/deck/temur-transmogrify-by-howlingmines-848-mythic-march-2021-ranked-season/'), ('Azorius Fable by Mythic Matt – #5 Mythic – March 2021 Season', 'https://mtgazone.com/deck/azorius-fable-by-mythic-matt-5-mythic-march-2021-season/'), ('Golgari Midrange by Symphoneers – #1284 Mythic – March 2021 Ranked Season', 'https://mtgazone.com/deck/golgari-midrange-by-symphoneers-1284-mythic-march-2021-ranked-season/'), ('Mono Green Aggro by Rint – #248 Mythic – March 2021 Ranked Season', 'https://mtgazone.com/deck/mono-green-aggro-by-rint-248-mythic-march-2021-ranked-season/'), ('Bant Adventures by TXSTChamp – #1241 Mythic – March 2021 Ranked Season', 'https://mtgazone.com/deck/bant-adventures-by-txstchamp-1241-mythic-march-2021-ranked-season/'), ('Dimir Rogues by Loydy – #540 Mythic – March 2021 Ranked Season', 'https://mtgazone.com/deck/dimir-rogues-by-loydy-540-mythic-march-2021-ranked-season/'), ('Mono Red Aggro by THE_AUSIL_RELOADED – #188 Mythic – March 2021 Ranked Season', 'https://mtgazone.com/deck/mono-red-aggro-by-the_ausil_reloaded-188-mythic-march-2021-ranked-season/'), ('Temur Turns by ganp – #218 Mythic – March 2021 Ranked Season', 'https://mtgazone.com/deck/temur-turns-by-ganp-218-mythic-march-2021-ranked-season/'), ('Temur Turns by SocalsFinest – $5K Strixhaven Championship Qualifier (12th)', 'https://mtgazone.com/deck/temur-turns-by-socalsfinest-5k-strixhaven-championship-qualifier-12th/'), ('Mono Red Aggro by laurent delade – $5K Strixhaven Championship Qualifier (11th)', 'https://mtgazone.com/deck/mono-red-aggro-by-laurent-delade-5k-strixhaven-championship-qualifier-11th/'), ('Naya Tokens by Brandon Downs – $5K Strixhaven Championship Qualifier (10th)', 'https://mtgazone.com/deck/naya-tokens-by-brandon-downs-5k-strixhaven-championship-qualifier-10th/'), ('Gruul Adventures by Achim Noffke – $5K Strixhaven Championship Qualifier (9th)', 'https://mtgazone.com/deck/gruul-adventures-by-achim-noffke-5k-strixhaven-championship-qualifier-9th/'), ('Sultai Ultimatum by Alexander Flynn – $5K Strixhaven Championship Qualifier (8th)', 'https://mtgazone.com/deck/sultai-ultimatum-by-alexander-flynn-5k-strixhaven-championship-qualifier-8th/'), ('Temur Turns by Nicholas DeMichele – $5K Strixhaven Championship Qualifier (7th)', 'https://mtgazone.com/deck/temur-turns-by-nicholas-demichele-5k-strixhaven-championship-qualifier-7th/'), ('Mono Red Aggro by Ruben da Silva – $5K Strixhaven Championship Qualifier (6th)', 'https://mtgazone.com/deck/mono-red-aggro-by-ruben-da-silva-5k-strixhaven-championship-qualifier-6th/'), ('Mono Red Aggro by Karl Sarap – $5K Strixhaven Championship Qualifier (5th)', 'https://mtgazone.com/deck/mono-red-aggro-by-karl-sarap-5k-strixhaven-championship-qualifier-5th/'), ('Naya Tokens by Omar B – $5K Strixhaven Championship Qualifier (4th)', 'https://mtgazone.com/deck/naya-tokens-by-omar-b-5k-strixhaven-championship-qualifier-4th/'), ('Jeskai Cycling by Tomohiro Nakagawa – $5K Strixhaven Championship Qualifier (3rd)', 'https://mtgazone.com/deck/jeskai-cycling-by-tomohiro-nakagawa-5k-strixhaven-championship-qualifier-3rd/'), ('Dimir Rogues by Toni Ramis Pascual – $5K Strixhaven Championship Qualifier (2nd)', 'https://mtgazone.com/deck/dimir-rogues-by-toni-ramis-pascual-5k-strixhaven-championship-qualifier-2nd/'), ('Jeskai Cycling by Claudinei Brasil Junior – $5K Strixhaven Championship Qualifier (1st)', 'https://mtgazone.com/deck/jeskai-cycling-by-claudinei-brasil-junior-5k-strixhaven-championship-qualifier-1st/'), ('BO1 Mono White Lifegain by FloCherry – #89 Mythic – March 2021 Ranked Season', 'https://mtgazone.com/deck/bo1-mono-white-lifegain-by-flocherry-89-mythic-march-2021-ranked-season/'), ('BO1 Sultai Ultimatum by TheChemist – #47 Mythic – March 2021 Ranked Season', 'https://mtgazone.com/deck/bo1-sultai-ultimatum-by-thechemist-47-mythic-march-2021-ranked-season/'), ('Jeskai Cycling by VCardarelli – #134 Mythic – March 2021 Ranked Season', 'https://mtgazone.com/deck/jeskai-cycling-by-vcardarelli-134-mythic-march-2021-ranked-season/'), ('Selesnya Plow by jsp – Mythic Rank – March 2021 Ranked Season', 'https://mtgazone.com/deck/selesnya-plow-by-jsp-mythic-rank-march-2021-ranked-season/'), ('Boros Equipment by Zazzy – #282 Mythic – March 2021 Ranked Season', 'https://mtgazone.com/deck/boros-equipment-by-zazzy-282-mythic-march-2021-ranked-season/'), ('Mono Green Stompy by previsioni_del_tempo – #90 Mythic – March 2021 Ranked Season', 'https://mtgazone.com/deck/mono-green-stompy-by-previsioni_del_tempo-90-mythic-march-2021-ranked-season/'), ('Mono White Aggro by Ozymandias – #84 Mythic – March 2021 Ranked Season', 'https://mtgazone.com/deck/mono-white-aggro-by-ozymandias-84-mythic-march-2021-ranked-season/'), ('Temur Turns by VisitorQ – #57 Mythic – March 2021 Ranked Season', 'https://mtgazone.com/deck/temur-turns-by-visitorq-57-mythic-march-2021-ranked-season/'), ('BO1 Mono White Lifegain by TheChemist – #41 Mythic – March 2021 Ranked Season', 'https://mtgazone.com/deck/bo1-mono-white-lifegain-by-thechemist-41-mythic-march-2021-ranked-season/'), ('Dimir Rogues by karmaprey – #28 Mythic – March 2021 Ranked Season', 'https://mtgazone.com/deck/dimir-rogues-by-karmaprey-28-mythic-march-2021-ranked-season/'), ('BO1 Mono Red Aggro by Piccirko – #28 Mythic – March 2021 Ranked Season', 'https://mtgazone.com/deck/bo1-mono-red-aggro-by-piccirko-28-mythic-march-2021-ranked-season/'), ('Temur Turns by Xixoxu – #30 Mythic – March 2021 Ranked Season', 'https://mtgazone.com/deck/temur-turns-by-xixoxu-30-mythic-march-2021-ranked-season/'), ('Jund Adventures by Delmo – #34 Mythic – March 2021 Season', 'https://mtgazone.com/deck/jund-adventures-by-delmo-34-mythic-march-2021-season/'), ('Naya Tokens by katoken – #24 Mythic – March 2021 Ranked Season', 'https://mtgazone.com/deck/naya-tokens-by-katoken-24-mythic-march-2021-ranked-season/'), ('Bant Mutate by uebelst4r – #26 Mythic – March 2021 Ranked Season', 'https://mtgazone.com/deck/bant-mutate-by-uebelst4r-26-mythic-march-2021-ranked-season/'), ('Naya Sky by Hagera – #2 Mythic – March 2021 Ranked Season', 'https://mtgazone.com/deck/naya-sky-by-hagera-2-mythic-march-2021-ranked-season/'), ('BO1 Mono White Lifegain by CovertGoBlue – #1 Mythic – March 2021 Ranked Season', 'https://mtgazone.com/deck/bo1-mono-white-lifegain-by-covertgoblue-1-mythic-march-2021-ranked-season/')]
print(len(l))
