import logging


class content():

    def __init__(self, mediasite):
        self.mediasite = mediasite

    def get_authorization_ticket(self, presentation_id, lifespan=500000):
        logging.debug(f'Getting authorization ticket for presentation: {presentation_id}')
        data = dict()
        post_vars = {
            'ResourceId': presentation_id,
            'Username': self.mediasite.api_client.username,
            'MinutesToLive': str(lifespan)
        }
        result = self.mediasite.api_client.request('post', "AuthorizationTickets", post_vars=post_vars)

        if self.mediasite.experienced_request_errors(result):
            logging.error(f'Authorization ticket not delivered for presentation: {presentation_id}')
        else:
            result = result.json()
            if 'odata.error' in result:
                logging.error(result["odata.error"]["code"] + ": " + result["odata.error"]["message"]["value"])
            else:
                data = result
        return data

    def get_content(self, presentation_id, resource_content):
        """
        Gets the presentation's specified content using its ID

        params:
            content: content requested; all contents (video and slides) if not specified.
                (example: OnDemandContent, SlideDetailsContent, ...)
        returns:
            list of resulting responses from the mediasite web api request
        """

        logging.debug(f'Getting presentation content. Content: {resource_content}. Presentation ID: {presentation_id}')

        data = dict()
        route = f'Presentations(\'{presentation_id}\')/{resource_content}'
        result = self.mediasite.api_client.request('get', route)

        if not self.mediasite.experienced_request_errors(result):
            result = result.json()
            data = result if resource_content == 'SlideDetailsContent' else result.get('value')

        return data

    def get_content_server(self, content_server_id, slide=False):
        """
        Gets mediasite content server given server guid

        params:
            content_server__id: guid of a mediasite content server

        returns:
            resulting response from the mediasite web api request
        """

        logging.debug(f'Getting the content server : {content_server_id}')

        options = 'StorageEndpoint' if slide else ''
        route = f'ContentServers(\'{content_server_id}\')/{options}'
        result = self.mediasite.api_client.request('get', route)

        if not self.mediasite.experienced_request_errors(result):
            data = result.json()
            if "odata.error" in data:
                logging.warning(result["odata.error"]["code"] + ": " + result["odata.error"]["message"]["value"])
            else:
                return data
        logging.error('Not getting Content Server with ID: ' + content_server_id)
        return None

    def get_content_encoding_settings(self, settings_id):
        """
        Gets the content encoding settings of a video content, given the settings id.

        params:
            settings: the ContentEncodingSettingsId of the video content
        returns:
            resulting response from the mediasite api
        """

        logging.debug(f'Getting content encoding settings. Settings ID: {settings_id}')

        route = f'ContentEncodingSettings(\'{settings_id}\')'
        result = self.mediasite.api_client.request('get', route)
        if not self.mediasite.experienced_request_errors(result, allowed_status=400):
            data = result.json()
            if "odata.error" in data:
                if data['odata.error']['code'] == 'InvalidKey':
                    logging.debug('No encoding settings ID for this media.')
                    logging.debug(data["odata.error"]["code"] + ": " + data["odata.error"]["message"]["value"])
                else:
                    logging.error(data["odata.error"]["code"] + ": " + data["odata.error"]["message"]["value"])
            else:
                return data
        logging.debug(f'Content encoded settings ID: {settings_id}')
        return None
