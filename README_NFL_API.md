This package queries the NFL site to pull basic live game data like score, clock time, and quarter. 


## Setup
- Requires selenium to pull dynamic content from nfl webpage
- Requires a headless web browser to run with selenium
- Requires beautiful soup to parse the html to pull game data


## Example Usage

Get the game data for 2019, week 1 of the regular season
`curl localhost:5000/games/2019/REG/1`