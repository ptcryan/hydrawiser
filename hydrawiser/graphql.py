"""
A GraphQL (API v2) implementation
"""

from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
import requests


class HydrawiserV2():
    CLIENT_ID = 'hydrawise_app'
    CLIENT_SECRET = 'zn3CrjglwNV1'
    TOKEN_ENDPOINT = 'https://app.hydrawise.com/api/v2/oauth/access-token'
    API_ENDPOINT = 'https://app.hydrawise.com/api/v2/graph'
    """
    :param email: E-mail used during Hydrawise account registration
    :type email: string
    :param password: Hydrawise account password
    :type password: string
    :returns: Hydrawiser object.
    :rtype: object
    """

    def __init__(self, email, password):
        self._token = self.__fetch_token(email, password)
        self._client = self.__client(self._token)

    def __fetch_token(self, username, password):
        payload = {
            'grant_type': 'password',
            'client_id': self.CLIENT_ID,
            'client_secret': self.CLIENT_SECRET,
            'username': username,
            'password': password,
            'scope': 'all',
        }

        resp = requests.post(
            self.TOKEN_ENDPOINT,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=payload
        )

        if resp.status_code != 200:
            print(resp.json())

        return resp.json()

    def __client(self, token):
        headers = {
            'Authorization': token['token_type'] + ' ' + token['access_token']
        }

        _transport = RequestsHTTPTransport(
            url=self.API_ENDPOINT,
            headers=headers,
            use_json=True,
            verify=True,
            retries=3,
        )

        return Client(
            transport=_transport,
            fetch_schema_from_transport=True,
        )

    def customer(self):
        query = gql("""{
          me {
            id
            customerId
            name
            email
            customerId
            validated
            controllers {
                id
                name
                deviceId
            }
          }
        }
        """)
        result = self._client.execute(query)
        return result['me']

    def controllers(self):
        query = gql("""{
          me {
            controllers {
              id
              name
              deviceId
              wizardComplete
              hardware {
                serialNumber
                version
                status
                installationDate
              }
              softwareVersion
              boc
              lastAction {
                value
                timestamp
              }
            }
          }
        }
        """)
        result = self._client.execute(query)
        return result['me']['controllers']
