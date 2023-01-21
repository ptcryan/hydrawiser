"""
This is the main library file. It contains the Hydrawiser
object, and its methods. To use this library import it,
and create an object using the api key for your controller.

See the README.md file for more details on the methods and
attributes available.
"""

import time
from hydrawiser.helpers import customer_details, status_schedule, set_zones


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
        self.statuses = []
        self.controller_ids_info = []
        self.controller_ids = []
        self.customer_id = None
        self.num_relays = 0
        self.relays = []
        self.controllers_to_relays = []
        self.controllers_to_sensors = []
        self.status = None
        self.controller_names = []
        self.sensors = []
        self.running = None

        self.update_controller_info()

    def update_controller_info(self):
        """
        Pulls controller information.

        :returns: True if successfull, otherwise False.
        :rtype: boolean
        """

        # Read the customer information and gather all controller info.
        self.controller_info = customer_details(self._user_token)

        if self.controller_info is None:
            return False

        self.customer_id = self.controller_info['customer_id']

        self.controller_ids_info = self.controller_info['controllers']

        # Hydrawise supports a maximum of 5 controllers.

        for x in self.controller_ids_info:
            self.controller_status = status_schedule(self._user_token, self.controller_info['controllers'][x]['controller_id'])

            if self.controller_status is None:
                continue

            # Use the current one from the array.

            # These arrays are meant for keeping track of all controller information.
            self.current_controller = self.controller_info['controllers'][x]
            self.controller_names.append(self.controller_info['controllers'][x]['name'])
            self.statuses.append(self.current_controller['status'])
            self.controller_ids.append(self.current_controller['controller_id'])


            # These arrays are meant for keeping track of all relay/sensor information.

            self.num_relays += len(self.controller_status['relays'])
            self.relays.append(self.controller_status['relays'])

            # We keep an array in-sync with all relays and which controller ID they belong to.
            for y in len(self.controller_status['relays']):
                self.controllers_to_relays.append(self.current_controller['controller_id'])

            self.sensors.append(self.controller_status['sensors'])

            # We keep an array in-sync with all sensors and which controller ID they belong to.
            for z in len(self.controller_status['sensors']):
                self.controllers_to_sensors.append(self.current_controller['controller_id'])

            try:
                self.running = self.controller_status['running']
            except KeyError:
                self.running = None

        return True     

    def controllers(self):
        """
        Check if multiple controllers are connected.

        :returns: Return the controller_id of the active controller.
        :rtype: string
        """

        if hasattr(self, 'controller_ids'):
            return self.controller_ids
        raise AttributeError('No controllers assigned to this account.')

    def __repr__(self):
        """
        Object representation.
        :returns: Object name
        :rtype: string
        """

        return "<{0}: {1}>".format(self.__class__.__name__,
                                   self.controller_ids)

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
            controller_id = None
        else:
            if zone < 0 or zone > (len(self.relays) - 1):
                return None
            else:
                zone_cmd = 'suspend'
                relay_id = self.relays[zone]['relay_id']
                controller_id = self.controllers_to_relays[zone]

        # If days is 0 then remove suspension
        if days <= 0:
            time_cmd = 0
        else:
            # 1 day = 60 * 60 * 24 seconds = 86400
            time_cmd = time.mktime(time.localtime()) + (days * 86400)

        return set_zones(self._user_token, zone_cmd, relay_id, controller_id, time_cmd)

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
            controller_id = None
        else:
            if zone < 0 or zone > (len(self.relays) - 1):
                return None
            else:
                zone_cmd = 'run'
                relay_id = self.relays[zone]['relay_id']
                controller_id = self.controllers_to_relays[zone]

        if minutes <= 0:
            time_cmd = 0
            if zone is None:
                zone_cmd = 'stopall'
                controller_id = None
            else:
                zone_cmd = 'stop'
        else:
            time_cmd = minutes * 60

        return set_zones(self._user_token, zone_cmd, relay_id, controller_id, time_cmd)

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
