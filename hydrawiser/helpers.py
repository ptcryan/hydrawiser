"""
Helper functions to query and send
commands to the controller.
"""
import requests

REQUESTS_TIMEOUT = 10


def status_schedule(token):
    """
    Returns the json string from the Hydrawise server after calling
    statusschedule.php.

    :param token: The users API token.
    :type token: string
    :returns: The response from the controller. If there was an error returns
              None.
    :rtype: string or None
    """

    url = 'https://app.hydrawise.com/api/v1/statusschedule.php'

    payload = {
        'api_key': token}

    get_response = requests.get(url, params=payload, timeout=REQUESTS_TIMEOUT)

    if get_response.status_code == 200 and \
       'error_msg' not in get_response.json():
        return get_response.json()

    return None

def status_schedule(token, controller_id):
    """
    Returns the json string from the Hydrawise server after calling
    statusschedule.php.

    :param token: The users API token.
    :type token: string
    :param controller_id: The specific controller ID we are looking at.
    :type controller_id: string
    :returns: The response from the controller. If there was an error returns
              None.
    :rtype: string or None
    """

    url = 'https://app.hydrawise.com/api/v1/statusschedule.php'

    payload = {
        'api_key': token,
        'controller_id': controller_id}

    get_response = requests.get(url, params=payload, timeout=REQUESTS_TIMEOUT)

    if get_response.status_code == 200 and \
       'error_msg' not in get_response.json():
        return get_response.json()

    return None


def customer_details(token):
    """
    Returns the json string from the Hydrawise server after calling
    customerdetails.php.

    :param token: The users API token.
    :type token: string
    :returns: The response from the controller. If there was an error returns
              None.
    :rtype: string or None.
    """

    url = 'https://app.hydrawise.com/api/v1/customerdetails.php'

    payload = {
        'api_key': token,
        'type': 'controllers'}

    get_response = requests.get(url, params=payload, timeout=REQUESTS_TIMEOUT)

    if get_response.status_code == 200 and \
       'error_msg' not in get_response.json():
        return get_response.json()

    return None


def set_zones(token, action, relay=None, controller=None, time=None):
    """
    Controls the zone relays to turn sprinklers on and off.

    :param token: The users API token.
    :type token: string
    :param action: The action to perform. Available actions are: run, runall,
                   stop, stopall, suspend, and suspendall.
    :type action: string
    :param relay: The zone to take action on. If no zone is specified then the
                  action will be on all zones.
    :type relay: int or None
    :param controller: The controller that the zone is attached to. If no zone
                       is specified then the action will be on all zones of the
                       primary controller.
    :type controller: int or None
    :param time: The number of seconds to run or unix epoch time to suspend.
    :type time: int or None
    :returns: The response from the controller. If there was an error returns
              None.
    :rtype: string or None
    """
    # Actions must be one from this list.
    action_list = [
        'run',        # Run a zone for an amount of time.
        'runall',     # Run all zones for an amount of time.
        'stop',       # Stop a zone.
        'stopall',    # stop all zones.
        'suspend',    # Suspend a zone for an amount of time.
        'suspendall'  # Suspend all zones.
    ]

    # Was a valid action specified?
    if action not in action_list:
        return None

    # Set the relay id if we are operating on a single relay.
    if action in ['runall', 'stopall', 'suspendall']:
        if relay is not None:
            return None
        else:
            relay_cmd = ''
    else:
        relay_cmd = '&relay_id={}'.format(relay)

    # Add a time argument if the action requires it.
    if action in ['run', 'runall', 'suspend', 'suspendall']:
        if time is None:
            return None
        else:
            custom_cmd = '&custom={}'.format(time)
            period_cmd = '&period_id=999'
    else:
        custom_cmd = ''
        period_cmd = ''

    # If action is on a single relay then make sure a relay is specified.
    if action in ['stop', 'run', 'suspend'] and relay is None:
        return None
    if controller is None:
        get_response = requests.get('https://app.hydrawise.com/api/v1/'
                                    'setzone.php?'
                                    '&api_key={}'
                                    '&action={}{}{}{}'
                                    .format(token,
                                            action,
                                            relay_cmd,
                                            period_cmd,
                                            custom_cmd),
                                    timeout=REQUESTS_TIMEOUT)

        if get_response.status_code == 200 and \
            'error_msg' not in get_response.json():
            return get_response.json()

    else:
        get_response = requests.get('https://app.hydrawise.com/api/v1/'
                                    'setzone.php?'
                                    '&api_key={}'
                                    '&action={}{}{}{}'
                                    '&controller={}'
                                    .format(token,
                                            action,
                                            relay_cmd,
                                            period_cmd,
                                            custom_cmd,
                                            controller),
                                    timeout=REQUESTS_TIMEOUT)

        if get_response.status_code == 200 and \
            'error_msg' not in get_response.json():
            return get_response.json()

    return None
