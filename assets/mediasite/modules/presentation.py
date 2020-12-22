"""
Mediasite client class for presentation-sepcific actions

Last modified: May 2018
By: Dave Bunten

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

        # # test
        # i = 0
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
            # # test
            # i += 1
            # if i > 1:
            #     break

        return presentations_list

    def get_all_presentations_content(self, resource_content=None):
        """
        Gathers a listing of the specified content of all presentations.

        params:
            content: content requested; all contents (video and slides) if not specified.
                (example: OnDemandContent, SlideDetailsContent, ...)
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

        route = f'Presentations(\'{presentation_id}\')/{content}'
        result = self.mediasite.api_client.request("get", route)
        if not self.mediasite.experienced_request_errors(result):
            result = result.json()
            if "odata.error" in result:
                if result['odata.error']['code'] == 'NavigationPropertyNull':
                    logging.warning('Wrong navigation property or content doesn\'t exist for this presentation: ' + content + '. ID: ' + presentation_id)
                    return None
                else:
                    logging.error(result["odata.error"]["code"] + ": " + result["odata.error"]["message"]["value"] + ' -> ' + presentation_id)
        return result

    def get_number_of_presentations(self):
        next_page = '$skip=0&$top=1'
        result = self.mediasite.api_client.request("get", "Presentations", next_page)
        if not self.mediasite.experienced_request_errors(result):
            result = result.json()
            if "odata.error" in result:
                logging.error(result["odata.error"]["code"] + ": " + result["odata.error"]["message"]["value"])
        return int(result['odata.count'])

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