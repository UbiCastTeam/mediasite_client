import logging


class content():

    def __init__(self, mediasite):
        self.mediasite = mediasite

    def get_authorization_ticket(self, presentation_id):
        post_vars = {
            'ResourceId': presentation_id,
            'Username': self.mediasite.api_client.username,
            'MinutesToLive': '300'
        }
        result = self.mediasite.api_client.request('post', f"AuthorizationTickets('{presentation_id}')", post_vars=post_vars)

        if not self.mediasite.experienced_request_errors(result):
            data = result.json()
            if 'odata.error' in data:
                logging.error(data["odata.error"]["code"] + ": " + data["odata.error"]["message"]["value"])
            else:
                return data
        logging.error(f'Authorization Tickets not delivered for presentation: {presentation_id}')
        return None

    def get_content(self, content_id):
        return None
