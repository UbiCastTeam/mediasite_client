"""
Class for creating connections to Mediasite API

Last modified: May 2018
By: Dave Bunten

License: MIT - see license.txt
"""

import base64
import logging
import json
import ssl
import requests
requests.packages.urllib3.disable_warnings()

class client:
    def __init__(self, serviceroot, sfapikey, username, password):
        """
        params:
            serviceroot: root URL to send API requests to
            sfapikey: Mediasite API key for making requests
            username: Mediasite API username for making requests
            password: Mediasite API password for making requests
        """
        self.serviceroot = serviceroot
        self.sfapikey = sfapikey
        self.username = username
        self.password = password

        self.session = None

    #formatting for login credentials needed by Mediasite
    def get_basic_auth_header_value(self):
        """
        Creates authentication string necessary for making Mediasite API requests

        returns:
            String specifically created for making Mediasite API requests based on
            useraname and password provided to class.
        """
        return_string = "Basic " + \
            str(base64.b64encode(bytes(self.username + ":" + self.password, "utf-8")).decode("utf-8"))
        return return_string

    def close_sessions(self):
        if self.session:
            self.session.close()

    def request(self, request_type, resource, odata_attributes=None, post_vars=None):
        """
        Performs API request based on parameter data

        params:
            request_type: type of request to make, for ex. "get","post", etc.
            resource:  resource within the API to make requests on, for ex. "Presentations"
            odata_attributes: odata attributes to use when making the requests
            post_vars: variables to send when making post requests
        """
        if self.session is None:
            self.session = requests.Session()

        self.resource = resource
        self.odata_attributes = f'?{odata_attributes}' if (odata_attributes) else ''

        #What we're requesting
        url = self.serviceroot + self.resource + self.odata_attributes

        # Header values required for request
        auth_values = {
            "sfapikey": self.sfapikey,
            "Accept": "application/json",
            "Authorization": self.get_basic_auth_header_value()
        }

        req = self.session if self.session else requests
        try:
            if request_type == "get":
                rsp = req.get(url, headers=auth_values, verify=False)

            elif request_type == "post":
                rsp = req.post(url, headers=auth_values, json=post_vars, verify=False)

            elif request_type == "put":
                rsp = req.put(url, headers=auth_values, json=post_vars, verify=False)

            elif request_type == "delete":
                rsp = req.delete(url, headers=auth_values, verify=False)

            elif request_type == "patch":
                rsp = req.patch(url, headers=auth_values, json=post_vars, verify=False)

            elif request_type == "get stream":
                rsp = req.get(resource, headers=auth_values, verify=False, stream=True)

            elif request_type == "get job":
                rsp = req.get(resource, headers=auth_values, verify=False)

            return rsp

        #catch all exceptions and return them
        except requests.exceptions.RequestException as e:

            return "Error: " + str(e)
