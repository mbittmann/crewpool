from selenium import webdriver
from bs4 import BeautifulSoup

def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    driver = webdriver.Chrome(options=options)
    return driver


def load_soup_for_page(driver, url):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup

def parse_page_to_dict(soup):
    matchup_groups = soup.select("section.nfl-o-matchup-group")
    games = []
    for group in matchup_groups:
        datestr = group.find("h2", class_="d3-o-section-title").get_text()
        game_strips = group.select("div.nfl-c-matchup-strip")
        for strip in game_strips:
            
            team_abbv = strip.select("span.nfl-c-matchup-strip__team-abbreviation")
            away = team_abbv[0].get_text().strip()
            home = team_abbv[1].get_text().strip()
            
            scores = strip.select("div.nfl-c-matchup-strip__team-score")
            if len(scores):
                away_score = scores[0].get_text().strip()
                home_score = scores[1].get_text().strip()
            else:
                away_score = 0
                home_score = 0

            game_time_span = strip.select("span.nfl-c-matchup-strip__date-time")
            
            if len(game_time_span):  # TODO: Figure out what game time is for live games
                game_time = game_time_span[0].get_text().strip()
            else:
                game_time = None
            
            game_dict = {}
            game_dict['date'] = datestr
            game_dict['time'] = game_time
            game_dict['away'] = away
            game_dict['away_score'] = away_score
            game_dict['home'] = home
            game_dict['home_score'] = home_score
            games.append(game_dict)
            
    return games
            
def get_game_data(year, phase, week):
    driver = init_driver()        
    url = URL_STR.format(year, phase, week)
    soup = load_soup_for_page(driver, url)
    driver.close()
    return parse_page_to_dict(soup)