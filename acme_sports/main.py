import requests
from utils import Utils
import json

class ProcessData:

    # Get the api url to read NFL data from Scoreboard and Team_Rankings API endpoint
    api_url1 = requests.get('https://delivery.chalk247.com/scoreboard/NFL/2020-01-12/2020-01-19.json?api_key=74db8efa2a6db279393b433d97c2bc843f8e32b0')
    api_url2 = requests.get('https://delivery.chalk247.com/team_rankings/NFL.json?api_key=74db8efa2a6db279393b433d97c2bc843f8e32b0')

    def main(self):

        # Instantiate the Utils class to utilise its methods
        util = Utils()

        # read the API data in json format
        score_data = util.read_data(self.api_url1)
        rank_data = util.read_data(self.api_url2)

        response_data = util.build_response(score_data, rank_data)

        print("Combined Response for date range 2020-01-12 to 2020-01-19 - ")
        print(response_data)


process = ProcessData()
process.main()
