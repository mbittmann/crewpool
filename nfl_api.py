from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup

URL_STR = "https://www.nfl.com/schedules/{}/{}{}"

def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    driver = webdriver.Chrome(options=options)
    return driver


def load_soup_for_page(url):
    driver = init_driver()
    driver.get(url)
    timeout = 15
    try:
        wait = WebDriverWait(driver, timeout, .1)
        ec = EC.presence_of_element_located((By.CLASS_NAME, 'nfl-o-matchup-group'))
        wait.until(ec)
        html_source = driver.page_source
    except TimeoutException as e:
        raise e
    finally:
        driver.quit()

    soup = BeautifulSoup(html_source, 'html.parser')
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
                away_score = None
                home_score = None

            game_time_span = strip.select("span.nfl-c-matchup-strip__date-time")
            
            if len(game_time_span):  # TODO: Figure out what game time is for live games
                game_time = game_time_span[0].get_text().strip()
            else:
                game_time = None

            quarter_span = strip.select("span.nfl-c-matchup-strip__quarter")
            if len(quarter_span):
                quarter = quarter_span[0].get_text().strip()
            else:
                quarter = None

            channel_span = strip.select("p.nfl-c-matchup-strip__networks")
            if len(channel_span):
                channel = channel_span[0].get_text().strip()
            else:
                channel = None

            game_dict = {}
            game_dict['date'] = datestr
            game_dict['time'] = game_time
            game_dict['away'] = away
            game_dict['away_score'] = away_score
            game_dict['home'] = home
            game_dict['home_score'] = home_score
            game_dict['quarter'] = quarter
            game_dict['channel'] = channel
            
            if away_score == None:
                game_dict['status'] = 'PREGAME'
            else:
                game_dict['status'] = 'ACTIVE_PLACEHOLDER'
            
            game_dict['clock'] = '99:99'              
            games.append(game_dict)
            
    return games


def get_game_data(year, phase, week):
    url = URL_STR.format(year, phase, week)
    soup = load_soup_for_page(url)
    return parse_page_to_dict(soup)