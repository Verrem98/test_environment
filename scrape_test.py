from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq


def get_book_info(q, limit):
    q = q.replace(" ", "+")
    url = f'https://www.goodreads.com/search?q={q}'

    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()

    page_soup = soup(page_html, "html.parser")

    book_titles = [str(title)[str(title).find('''role="heading">''') + 15:str(title).find("</span>")] for title in
                   page_soup.findAll("a", {"class": "bookTitle"})[:limit]]
    book_ratings = [str(ratings)[str(ratings).find("avg rating") - 5:str(ratings).find("avg rating") - 1] for ratings in
                    page_soup.findAll("span", {"class": "minirating"})[:limit]]
    amount_of_book_ratings = [str(ratings)[str(ratings).find("avg rating") + 13:str(ratings).find("ratings") - 1] for
                              ratings in
                              page_soup.findAll("span", {"class": "minirating"})[:limit]]

    return book_titles, book_ratings, amount_of_book_ratings


def print_book_info(q, limit):
    book_titles, book_ratings, amount_of_book_ratings = get_book_info(q, limit)

    for x in range(len(book_ratings)):
        print(book_titles[x], '|', f"{book_ratings[x]}/5", "|", f"{amount_of_book_ratings[x]} ratings")


print_book_info("Stephen King", 10)

