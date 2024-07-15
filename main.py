#Import required modules
from bs4 import BeautifulSoup
import requests
import csv


def save_to_csv():
    """
    Asks whether to save the output as csv file.
    """
    while True:
        user = input("Do you want to save the output as csv file? (yes/no) ")
        if user == "yes".lower():
            return True
        elif user == "no".lower():
            return False
        else:
            print("Please enter a valid option: ")


def write_to_csv(news_dict):
    """
    Saves the output as fcc_scrapper.csv file.
    """
    with open("fcc_scrape.csv", "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Title", "Link", "Author"])

        for title, details in news_dict.items():
            csv_writer.writerow([title, details[0], details[1]])


def get_source_html_text(url):
    """
    Fetch the HTML content of the given URL.
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def scrape_fcc_news_and_return_newsDict():
    """
    Scrape the FreeCodeCamp news page and return a dictionary of news articles.
    """
    url = "https://www.freecodecamp.org/news/"
    source = get_source_html_text(url)
    soup = BeautifulSoup(source, "lxml")

    news_dict = {}

    for article in soup.find_all("article", class_="post-card"):

        news = article.find("h2", class_="post-card-title")
        news_title = news.a.text.strip()

        try:
            news_link = ("https://www.freecodecamp.org" + news.a["href"]).strip()
        except Exception as e:
            news_link = None

        news_author = article.find("span", class_="meta-content").a.text.strip()

        news_dict[news_title] = [news_link, news_author]

    return news_dict

    
def pretty_print_fcc_newsDict(news_dict):
    """
    Print the news articles in a formatted manner.
    """
    for counter, (title, details) in enumerate(news_dict.items(), start=1):
        print(f"{counter}. {title} \nLink: {details[0]} \nAuthor: {details[1]}")
        print()


def main():
    """
    Main function to execute the script.
    """
    news_dict = scrape_fcc_news_and_return_newsDict()

    if save_to_csv():
        write_to_csv(news_dict)
    else:
        pretty_print_fcc_newsDict(news_dict)




if __name__ == "__main__":
    main()