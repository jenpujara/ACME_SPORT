import json
import datetime

class Utils:

    def read_data(self,url):
        if url.status_code != 200:
            raise Exception('The GET request has status code {}'.format(url.status_code))

        return json.loads(url.text)

    def convert_date_format(self, date_obj):
        return date_obj.strftime('%d-%m-%Y')

    def fetch_date_format(self,date_obj):
        return datetime.datetime.strptime(date_obj, '%Y-%m-%d')


    def build_response(self,scoreboard, team_ranks):

        output = []

        for date in scoreboard['results'].keys():

            # Only consider data for non-empty date property
            if len(scoreboard['results'][date]) != 0:

                # convert date from 'YYYY-MM-DD' to 'DD-MM-YYYYY' format
                date_obj = self.convert_date_format(self.fetch_date_format(date))

                for id in scoreboard['results'][date]['data'].keys():

                    # build combined response from Scoreboard and Team_Rankings API endpoint as list of dictionaries(expected format)
                    dict = {}
                    dict['event_id'] = scoreboard['results'][date]['data'][id]['event_id']
                    dict['event_date'] = date_obj

                    # The event_time is fetched from event_date property in format HM:MM
                    dict['event_time'] = scoreboard['results'][date]['data'][id]['event_date'].split(" ")[1]
                    dict['away_team_id'] = scoreboard['results'][date]['data'][id]['away_team_id']
                    dict['away_nick_name'] = scoreboard['results'][date]['data'][id]['away_nick_name']
                    dict['away_city'] = scoreboard['results'][date]['data'][id]['away_city']

                    '''
                     Assumption: Considering data from Team_Rankings for team_id & team having corresponding equal values to away_team_id & away_display_name
                      of Scoreboard otherwise create properties with empty values
                    '''
                    for team in team_ranks['results']['data']:
                        if scoreboard['results'][date]['data'][id]['away_team_id'] == team['team_id'] and scoreboard['results'][date]['data'][id]['away_display_name'] == team['team']:
                            dict['away_rank'] = team['rank']

                            # adjusted_points is first converted to float, rounded off to 2 decimal places and then converted back to string value
                            dict['away_rank_points'] = str(round(float(team['adjusted_points']), 2))
                            break
                        else:
                            dict['away_rank'] = ""
                            dict['away_rank_points'] = ""

                    dict['home_team_id'] = scoreboard['results'][date]['data'][id]['home_team_id']
                    dict['home_nick_name'] = scoreboard['results'][date]['data'][id]['home_nick_name']
                    dict['home_city'] = scoreboard['results'][date]['data'][id]['home_city']

                    '''
                    Assumption: Considering data from Team_Rankings for team_id & team having corresponding equal values to home_team_id & home_display_name
                    of Scoreboard otherwise create properties with empty values
                    '''
                    for team in team_ranks['results']['data']:
                        if scoreboard['results'][date]['data'][id]['home_team_id'] == team['team_id'] and scoreboard['results'][date]['data'][id]['home_display_name'] == team['team']:
                            dict['home_rank'] = team['rank']

                            # adjusted_points is first converted to float, rounded off to 2 decimal places and then converted back to string value
                            dict['home_rank_points'] = str(round(float(team['adjusted_points']), 2))
                            break
                        else:
                            dict['home_rank'] = ""
                            dict['home_rank_points'] = ""

                    output.append(dict)

        final_output = json.dumps(output)

        return final_output
