"""
This is the main library file. It contains the Hydrawiser
object, and its methods. To use this library import it,
and create an object using the api key for your controller.

See the README.md file for more details on the methods and
attributes available.
"""

import time
from hydrawiser.helpers import customer_details, status_schedule, set_zones
from requests.exceptions import ConnectTimeout, HTTPError


class Hydrawiser():
    """
    :param user_token: User account API key
    :type user_token: string
    :returns: Hydrawiser object.
    :rtype: object
    """

    def __init__(self, user_token):

        self._user_token = user_token

        # Attributes that we will be tracking from the controller.
        self.controller_info = []
        self.controller_status = []
        self.current_controller = []
        self.status = None
        self.controller_id = None
        self.customer_id = None
        self.num_relays = None
        self.relays = []
        self.status = None
        self.name = None
        self.sensors = []
        self.running = None

        self.update_controller_info()

    def update_controller_info(self):
        """
        Pulls controller information.

        :returns: True if successfull, otherwise False.
        :rtype: boolean
        """

        # Read the controller information.
        try:
            self.controller_info = customer_details(self._user_token)
            self.controller_status = status_schedule(self._user_token)
        except HTTPError as err:
            # Handling the newly introduced rate limit
            if err.response.status_code == 429:
                raise HTTPError(err.response.text)

        if self.controller_info is None or self.controller_status is None:
            return False

        # Only supports one controller right now.
        # Use the first one from the array.
        self.current_controller = self.controller_info['controllers'][0]
        self.status = self.current_controller['status']
        self.controller_id = self.current_controller['controller_id']
        self.customer_id = self.controller_info['customer_id']
        self.num_relays = len(self.controller_status['relays'])
        self.relays = self.controller_status['relays']
        self.name = self.controller_info['controllers'][0]['name']
        self.sensors = self.controller_status['sensors']
        try:
            self.running = self.controller_status['running']
        except KeyError:
            self.running = None

        return True

    def controller(self):
        """
        Check if multiple controllers are connected.

        :returns: Return the controller_id of the active controller.
        :rtype: string
        """

        if hasattr(self, 'controller_id'):
            if len(self.controller_info['controllers']) > 1:
                raise TypeError(
                    'Only one controller per account is supported.'
                )
            return self.controller_id
        raise AttributeError('No controllers assigned to this account.')

    def __repr__(self):
        """
        Object representation.
        :returns: Object name
        :rtype: string
        """

        return "<{0}: {1}>".format(self.__class__.__name__,
                                   self.controller_id)

    def relay_info(self, relay, attribute=None):
        """
        Return information about a relay.

        :param relay: The relay being queried.
        :type relay: int
        :param attribute: The attribute being queried, or all attributes for
                          that relay if None is specified.
        :type attribute: string or None
        :returns: The attribute being queried or None if not found.
        :rtype: string or int
        """

        # Check if the relay number is valid.
        if (relay < 0) or (relay > (self.num_relays - 1)):
            # Invalid relay index specified.
            return None
        else:
            if attribute is None:
                # Return all the relay attributes.
                return self.relays[relay]
            else:
                try:
                    return self.relays[relay][attribute]
                except KeyError:
                    # Invalid key specified.
                    return None

    def suspend_zone(self, days, zone=None):
        """
        Suspend or unsuspend a zone or all zones for an amount of time.

        :param days: Number of days to suspend the zone(s)
        :type days: int
        :param zone: The zone to suspend. If no zone is specified then suspend
                     all zones
        :type zone: int or None
        :returns: The response from set_zones() or None if there was an error.
        :rtype: None or string
        """
        if zone is None:
            zone_cmd = 'suspendall'
            relay_id = None
        else:
            if zone < 0 or zone > (len(self.relays) - 1):
                return None
            else:
                zone_cmd = 'suspend'
                relay_id = self.relays[zone]['relay_id']

        # If days is 0 then remove suspension
        if days <= 0:
            time_cmd = 0
        else:
            # 1 day = 60 * 60 * 24 seconds = 86400
            time_cmd = time.mktime(time.localtime()) + (days * 86400)

        return set_zones(self._user_token, zone_cmd, relay_id, time_cmd)

    def run_zone(self, minutes, zone=None):
        """
        Run or stop a zone or all zones for an amount of time.

        :param minutes: The number of minutes to run.
        :type minutes: int
        :param zone: The zone number to run. If no zone is specified then run
                     all zones.
        :type zone: int or None
        :returns: The response from set_zones() or None if there was an error.
        :rtype: None or string
        """
        if zone is None:
            zone_cmd = 'runall'
            relay_id = None
        else:
            if zone < 0 or zone > (len(self.relays) - 1):
                return None
            else:
                zone_cmd = 'run'
                relay_id = self.relays[zone]['relay_id']

        if minutes <= 0:
            time_cmd = 0
            if zone is None:
                zone_cmd = 'stopall'
            else:
                zone_cmd = 'stop'
        else:
            time_cmd = minutes * 60

        return set_zones(self._user_token, zone_cmd, relay_id, time_cmd)

    def list_running_zones(self):
        """
        Returns the currently active relay.

        :returns: Returns the running relay number or None if no relays are
                  active.
        :rtype: string
        """

        self.update_controller_info()

        if self.running is None or not self.running:
            return None
        return int(self.running[0]['relay'])

    def is_zone_running(self, zone):
        """
        Returns the state of the specified zone.

        :param zone: The zone to check.
        :type zone: int
        :returns: Returns True if the zone is currently running, otherwise
                  returns False if the zone is not running.
        :rtype: boolean
        """

        self.update_controller_info()

        if self.running is None or not self.running:
            return False

        if int(self.running[0]['relay']) == zone:
            return True

        return False

    def time_remaining(self, zone):
        """
        Returns the amount of watering time left in seconds.

        :param zone: The zone to check.
        :type zone: int
        :returns: If the zone is not running returns 0. If the zone doesn't
                  exist returns None. Otherwise returns number of seconds left
                  in the watering cycle.
        :rtype: None or seconds left in the waterting cycle.
        """

        self.update_controller_info()

        if zone < 0 or zone > (self.num_relays-1):
            return None

        if self.is_zone_running(zone):
            return int(self.running[0]['time_left'])

        return 0
