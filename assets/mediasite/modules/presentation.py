"""
Mediasite client class for presentation-specific actions

Last modified: December 2020
By: Nicolas Antunes

License: MIT - see license.txt
"""

import logging
from urllib.parse import quote
import json
import os


class presentation():
    def __init__(self, mediasite, *args, **kwargs):
        self.mediasite = mediasite

    def get_all_presentations(self):
        """
        Gathers a listing of all presentations.

        returns:
            resulting response from the mediasite web api request
        """
        logging.info("Getting a list of all presentations")

        #request mediasite folder information on the "Mediasite Users" folder
        current = 0
        # 1000 increment is usually the pre-configured maximum on Mediasite API
        increment = 1000
        presentations_list = []

        next_page = f'$select=full&$skip={str(current)}&$top={str(increment)}'
        while next_page:
            result = self.mediasite.api_client.request('get', 'Presentations', next_page)
            if not self.mediasite.experienced_request_errors(result):
                result = result.json()
                if "odata.error" in result:
                    logging.error(result["odata.error"]["code"] + ": " + result["odata.error"]["message"]["value"])
                else:
                    data = result['value']
                    presentations_list.extend(data)

                    next_link = result.get('odata.nextLink')
                    next_page = next_link.split('?')[-1] if next_link else None

        return presentations_list

    def get_number_of_presentations(self):
        next_page = '$skip=0&$top=1'
        result = self.mediasite.api_client.request("get", "Presentations", next_page)
        if not self.mediasite.experienced_request_errors(result):
            result = result.json()
            if "odata.error" in result:
                logging.error(result["odata.error"]["code"] + ": " + result["odata.error"]["message"]["value"])
        return int(result['odata.count'])

    def get_presentation_by_id(self, presentation_id):
        """
        Gets mediasite presentation given presentation guid

        params:
            presentation_id: guid of a mediasite presentation

        returns:
            resulting response from the mediasite web api request
        """

        logging.debug(f'Getting the presentation: {presentation_id} ')

        data = dict()
        route = f'Presentations(\'{presentation_id}\')/'
        result = self.mediasite.api_client.request('get', route)

        if self.mediasite.experienced_request_errors(result):
            logging.error('Presentation ID: ' + presentation_id)
        else:
            result = result.json()
            if "odata.error" in result:
                logging.error(result["odata.error"]["code"] + ": " + result["odata.error"]["message"]["value"])
            else:
                data = result['value']

        return data

    def get_presentations_by_name(self, name_search_query):
        """
        Gets presentations by name using provided name_search_querys

        params:
            template_name: name of the template to be found within mediasite

        returns:
            resulting response from the mediasite web api request
        """

        logging.info("Searching for presentations containing the text: "+name_search_query)

        #request mediasite folder information on the "Mediasite Users" folder
        result = self.mediasite.api_client.request("get", "Search", "search='"+name_search_query+"'&searchtype=Presentation","")

        if self.mediasite.experienced_request_errors(result):
            return result
        else:
            #if there is an error, log it
            if "odata.error" in result:
                logging.error(result["odata.error"]["code"] + ": " + result["odata.error"]["message"]["value"])

            return result

    def get_availability(self, presentation_id):
        """
        Gets presentation's availibility given by presentation guid

        params:
            presentation_id: guid of a mediasite presentation

        returns:
            resulting response from the mediasite web api request
        """

        logging.debug(f'Getting availability for presentation:{presentation_id}')

        data = str()
        route = f'MediasiteObjects(\'{presentation_id}\')'
        result = self.mediasite.api_client.request('get', route)

        if self.mediasite.experienced_request_errors(result):
            logging.error(f'Presentation: {presentation_id}')
        else:
            result = result.json()
            if 'odata.error' in result:
                logging.error(result["odata.error"]["code"] + ": " + result["odata.error"]["message"]["value"])
            else:
                data = result.get('Availability')

        return data

    def get_content(self, presentation_id, resource_content):
        return self.mediasite.content.get_content(presentation_id, resource_content)

    def get_presenters(self, presentation_id):
        """
        Gets listing of presentation's presenters given by presentation guid

        returns:
            resulting response value from the mediasite web api request: list of presenters
        """
        logging.debug(f'Getting presenters for presentation: {presentation_id}')

        data = list()
        route = f'Presentations(\'{presentation_id}\')/Presenters'
        result = self.mediasite.api_client.request('get', route)

        if self.mediasite.experienced_request_errors(result):
            logging.error(f'Presentation: {presentation_id}')
        else:
            result = result.json()
            if 'odata.error' in result:
                logging.error(result["odata.error"]["code"] + ": " + result["odata.error"]["message"]["value"])
            else:
                data = result.get('value')

        return data

    def delete_presentation(self, presentation_id):
        """
        Deletes mediasite presentation given presentation guid

        params:
            presentation_id: guid of a mediasite presentation

        returns:
            resulting response from the mediasite web api request
        """

        logging.info("Deleting Mediasite presentation: " + presentation_id)

        #request mediasite folder information on the "Mediasite Users" folder
        result = self.mediasite.api_client.request("delete", "Presentations('presentation_id')")

        if self.mediasite.experienced_request_errors(result):
            return result
        else:
            #if there is an error, log it
            if "odata.error" in result:
                logging.error(result["odata.error"]["code"] + ": " + result["odata.error"]["message"]["value"])

            return result

    def remove_publish_to_go(self, presentation_id):
        """
        Gathers mediasite root folder ID for use with other functions.
        
        params:
            template_name: name of the template to be found within mediasite

        returns:
            resulting response from the mediasite web api request
        """

        logging.info("Removing publish to go from presentation: "+presentation_id)

        #request mediasite folder information on the "Mediasite Users" folder
        result = self.mediasite.api_client.request("post", "Presentations('"+presentation_id+"')/RemovePublishToGo", "","")
        
        if self.mediasite.experienced_request_errors(result):
            return result
        else:
            #if there is an error, log it
            if "odata.error" in result:
                logging.error(result["odata.error"]["code"]+": "+result["odata.error"]["message"]["value"])

            return result

    def remove_podcast(self, presentation_id):
        """
        Gathers mediasite root folder ID for use with other functions.
        
        params:
            template_name: name of the template to be found within mediasite

        returns:
            resulting response from the mediasite web api request
        """

        logging.info("Finding Mediasite template information with name of: "+template_name)

        #request mediasite folder information on the "Mediasite Users" folder
        result = self.mediasite.api_client.request("post", "Presentations('"+presentation_id+"')/RemovePodcast", "","")
        
        if self.mediasite.experienced_request_errors(result):
            return result
        else:
            #if there is an error, log it
            if "odata.error" in result:
                logging.error(result["odata.error"]["code"]+": "+result["odata.error"]["message"]["value"])

            return result

    def remove_video_podcast(self, presentation_id):
        """
        Gathers mediasite root folder ID for use with other functions.
        
        params:
            template_name: name of the template to be found within mediasite

        returns:
            resulting response from the mediasite web api request
        """

        logging.info("Finding Mediasite template information with name of: "+template_name)

        #request mediasite folder information on the "Mediasite Users" folder
        result = self.mediasite.api_client.request("post", "Presentations('"+presentation_id+"')/RemoveVideoPodcast", "","")
        
        if self.mediasite.experienced_request_errors(result):
            return result
        else:
            #if there is an error, log it
            if "odata.error" in result:
                logging.error(result["odata.error"]["code"]+": "+result["odata.error"]["message"]["value"])

            return result