from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup

URL_STR = "https://www.espn.com/nfl/scoreboard/"

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
        # ec = EC.presence_of_element_located((By.CLASS_NAME, 'sb-team-abbrev'))
        # wait.until(ec)
        html_source = driver.page_source
    except TimeoutException as e:
        raise e
    finally:
        driver.quit()

    soup = BeautifulSoup(html_source, 'html.parser')
    return soup


def parse_live_game(game):

    date_time = game.select("th.date-time")
    if len(date_time):
        time = date_time[0].get_text().strip()
        parts = time.split(" - ")
        
        if len(parts) > 1:
            clock = parts[0]
            quarter = parts[1]
        else:
            clock = None
            quarter = time
    else:
        clock = None
        quarter = None
        
    away = game.select("tr.away")
    if len(away):
        away_team = away[0].select("span.sb-team-abbrev")[0].get_text().strip()
        away_score = away[0].select("td.total")[0].get_text().strip()
    else:
        away_team = None
        away_score = None
        
    home = game.select("tr.home")
    if len(home):
        home_team = home[0].select("span.sb-team-abbrev")[0].get_text().strip()
        home_score = home[0].select("td.total")[0].get_text().strip()
    else:
        home_team = None
        home_score = None
        
    network_span = game.select("th.network")
    if len(network_span):
        network = network_span[0].get_text().strip()
    else:
        network = None

    game_dict = {}
    game_dict['day'] = None
    game_dict['time'] = None
    game_dict['away'] = away_team
    game_dict['away_score'] = away_score
    game_dict['home'] = home_team
    game_dict['home_score'] = home_score
    game_dict['quarter'] = quarter
    game_dict['network'] = network
    game_dict['clock'] = clock
    game_dict['status'] = "ACTIVE"   
    return game_dict


def parse_upcoming_game(game):
    day_span = game.select("span.month-day")
    if len(day_span):
        day = day_span[0].get_text().strip()
    else:
        day = None
    time_span = game.select("span.time")
    if len(time_span):
        time = time_span[0].get_text().strip()
    else:
        time = None

        
    away = game.select("tr.away")
    if len(away):
        away_team = away[0].select("span.sb-team-abbrev")[0].get_text().strip()
    else:
        away_team = None
        
    home = game.select("tr.home")
    if len(home):
        home_team = home[0].select("span.sb-team-abbrev")[0].get_text().strip()
    else:
        home_team = None
    
    network_span = game.select("th.network")
    if len(network_span):
        network = network_span[0].get_text().strip()
    else:
        network = None    
    
    game_dict = {}
    game_dict['day'] = day
    game_dict['time'] = time    
    game_dict['away'] = away_team
    game_dict['away_score'] = None
    game_dict['home'] = home_team
    game_dict['home_score'] = None
    game_dict['quarter'] = None
    game_dict['network'] = network
    game_dict['clock'] = None 
    game_dict['status'] = "PREGAME"   
    return game_dict
    
def get_game_data():
    soup = load_soup_for_page(URL_STR)

    games = []
    live_games = soup.select("section.sb-score.live")
    for live_game in live_games:
        game = parse_live_game(live_game)
        games.append(game)
    
    upcoming_games = soup.select("section.sb-score.pregame")

    for upcoming_game in upcoming_games:
        game = parse_upcoming_game(upcoming_game)
        games.append(game)
    return games
