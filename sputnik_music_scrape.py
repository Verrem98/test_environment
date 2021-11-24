from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq


def return_page(url):
    """Use unreal soup to return the html of a webpage"""

    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()
    return soup(page_html, "html.parser")


def get_artist_album_info(artist):

    artist = str(artist).replace(" ", "+").replace("_", "+")
    url = f'https://www.sputnikmusic.com/search_results.php?genreid=0&search_in=Bands&search_text={artist}&x=0&y=0'
    page = return_page(url)


    data_blocks = str(page.find("table")).split("""color="#111111">""")[1:]

    dic = {}
    for block in data_blocks:


        rating = block.split("<b>")[1].split("</b>")[0]


        if len(rating) > 3:
            rating = "not available"
            rating_count = "not available"
        else:
            rating_count = block.split("""size="1">""")[2].split(" ")[0]

        dic[block.split("</")[0]] = {"rating": rating, "rating_count": rating_count,
                                     "release_year": block.split("""size="1">""")[1].split(" ")[0]}

    return dic


print(get_artist_album_info("Fleetwood Mac")['Rumors'])
