import logging


class user():

    def __init__(self, mediasite):
        self.mediasite = mediasite

    def get_profile_by_username(self, username):
        """
        Gets mediasiuser profile given by username

        params:
            username: username of the searched profile

        returns:
            user profile resulting response from the mediasite web api request
        """

        logging.debug(f'Getting user profile by username: {username}')

        data = dict()
        route = 'UserProfiles'
        params = f'$filter=UserName eq \'{username}\''
        result = self.mediasite.api_client.request('get', route, params)

        if self.mediasite.experienced_request_errors(result):
            logging.error(f'Username: {username}')
        else:
            result = result.json()
            if 'odata.error' in result:
                logging.error(result["odata.error"]["code"] + ": " + result["odata.error"]["message"]["value"])
            else:
                data = result['value']
                if len(data) > 0:
                    data = data[0]

        return data
