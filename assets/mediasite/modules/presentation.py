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
        increment = 50
        presentations_list = []

        next_page = f'$skip={str(current)}&$top={str(increment)}'
        while next_page:
            result = self.mediasite.api_client.request("get", "Presentations", next_page)
            if self.mediasite.experienced_request_errors(result):
                return result
            elif "odata.error" in result:
                logging.error(result["odata.error"]["code"] + ": " + result["odata.error"]["message"]["value"])
                return result.json()

            result = result.json()
            presentations_list.extend(result["value"])
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

    def get_presentation_by_id(self, presentation_id, content=None):
        """
        Gets mediasite presentation given presentation guid

        params:
            presentation_id: guid of a mediasite presentation
            content: specific content resource of the presentation

        returns:
            resulting response from the mediasite web api request
        """

        debug_message = 'Getting the presentation.'
        if content:
            debug_message += f'Content: {content}.'
        debug_message += f'ID: {presentation_id}'
        logging.debug(debug_message)

        route = f'Presentations(\'{presentation_id}\')/'
        result = self.mediasite.api_client.request('get', route)

        if not self.mediasite.experienced_request_errors(result):
            data = result.json()
            if "odata.error" in data:
                logging.error(result["odata.error"]["code"] + ": " + result["odata.error"]["message"]["value"])
            else:
                return data
        logging.error('Presentation ID: ' + presentation_id)
        return None

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

    def get_all_presentations_content(self, resource_content):
        """
        Gathers a listing of the specified content of all presentations.

        params:
            content: content requested
        returns:
            list of resulting responses from the mediasite web api request
        """

        logging.info('Getting all presentations content : ' + resource_content)

        presentations_list = self.get_all_presentations()
        content_list = []
        current = 0
        for presentation in presentations_list:
            # Printing progression
            print('Requesting content : ', current, '/', len(presentations_list), end='\r', flush=True)

            content = self.get_presentation_by_id(presentation['Id'], resource_content)
            content_list.append(content)
            current += 1
        return content_list

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
        logging.error('Content Server ID: ' + content_server_id)
        return None

    def get_presentation_content(self, presentation_id, resource_content):
        """
        Gets the presentation's specified content using its ID

        params:
            content: content requested; all contents (video and slides) if not specified.
                (example: OnDemandContent, SlideDetailsContent, ...)
        returns:
            list of resulting responses from the mediasite web api request
        """

        logging.debug(f'Getting presentation content. Content: {resource_content}. Presentation ID: {presentation_id}')

        route = f'Presentations(\'{presentation_id}\')/{resource_content}'
        result = self.mediasite.api_client.request('get', route)

        # allow 404 if slide request so as to catch it later
        allowed_status = None
        if resource_content == "SlideDetailsContent":
            allowed_status = 404

        if not self.mediasite.experienced_request_errors(result, allowed_status):
            data = result.json()
            if 'odata.error' in result:
                # catch error 404 when there is no slide content so as to prevent flooding logs
                if data['odata.error']['code'] == 'NavigationPropertyNull' and resource_content == 'SlideDetailsContent':
                    logging.debug('No slide for this presentation: ' + presentation_id)
                else:
                    # re-check for others 404 errors
                    self.mediasite.experienced_request_errors(result)
            elif not self.mediasite.experienced_request_errors(result):
                return data

        logging.warning('Presentation ID: ' + presentation_id)
        return None

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