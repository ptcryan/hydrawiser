"""
A GraphQL (API v2) implementation
"""

from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
import requests


class HydrawiserV2():
    """
    :param email: E-mail used during Hydrawise account registration
    :type email: string
    :param password: Hydrawise account password
    :type password: string
    :param timeout: Requests timeout in seconds
    :type timeout: int
    :returns: Hydrawiser object.
    :rtype: object
    """
    CLIENT_ID = 'hydrawise_app'
    CLIENT_SECRET = 'zn3CrjglwNV1'
    TOKEN_ENDPOINT = 'https://app.hydrawise.com/api/v2/oauth/access-token'
    API_ENDPOINT = 'https://app.hydrawise.com/api/v2/graph'

    def __init__(self, email, password, timeout=10):
        self.timeout = timeout
        self._token = self.__fetch_token(email, password)
        self._client = self.__client(self._token)

    def __fetch_token(self, username, password):
        """
        Retrieves OAuth2 token and refresh token

        :param username: E-mail used during Hydrawise account registration
        :type username: string
        :param password: Hydrawise account password
        :type password: string

        :returns: JSON object containing access_token, refresh_token
        :rtype: JSON
        """

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
            data=payload,
            timeout=self.timeout
        )

        if resp.status_code != 200:
            print(resp.json())

        return resp.json()

    def __client(self, token):
        """
        Create gql client for communication with remote GraphQL API.

        :returns: GraphQL Client object
        :rtype: gql.Client
        """

        headers = {
            'Authorization': token['token_type'] + ' ' + token['access_token']
        }

        _transport = RequestsHTTPTransport(
            url=self.API_ENDPOINT,
            headers=headers,
            use_json=True,
            verify=True,
            timeout=self.timeout,
            retries=3,
        )

        return Client(
            transport=_transport,
            fetch_schema_from_transport=True,
        )

    def customer(self):
        """
        Fetches basic information about current user including all registered
        controllers.

        :returns: Information about current user
        :rtype: dict
        """

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
        """
        List all registered controllers, their IDs, version and status.

        :returns: Controllers information
        :rtype: array
        """

        query = gql("""{
          me {
            controllers {
              id
              name
              online
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

    def zones(self, controller_id=None):
        """
        List all zones and its controllers, their id and names.

        :returns: Available zones
        :rtype: array
        """

        query = gql("""{
          me {
            controllers {
              id
              name
              zones {
                id
                name
              }
            }
          }
        }
        """)
        result = self._client.execute(query)
        return result['me']['controllers']

    def sensors(self, controller_id=None):
        """
        List all sensors connected to a controller, their id and status
        information.

        :returns: Sensors list and state.
        :rtype: array
        """

        query = gql("""{
          me {
            controllers {
                id
                name
                sensors {
                    id
                    name
                    model {
                      id
                      name
                      modeType
                      active
                      offLevel
                      offTimer
                      delay
                      divisor
                      flowRate
                      customerId
                      sensorType
                      category {
                        name
                      }
                    }
                }
            }
          }
        }
        """)
        result = self._client.execute(query)
        return result['me']['controllers']
