import requests_mock
from tests.const import GOOD_API_KEY, BAD_API_KEY

unauthorized_string = '{"error_msg": "unauthorized"}'
good_string = '{"controller_id":11111,"customer_id":22222}'


def test_status_schedule():
    from hydrawiser.helpers import status_schedule
    with requests_mock.Mocker() as m:

        # Test a valid api_key.
        m.get('https://app.hydrawise.com/api/v1/statusschedule.php?'
              'api_key={}'
              .format(GOOD_API_KEY),
              text=good_string)

        return_value = status_schedule(GOOD_API_KEY)
        assert return_value is not None

        # Test an invalid api_key.
        m.get('https://app.hydrawise.com/api/v1/statusschedule.php?'
              'api_key={}'
              .format(BAD_API_KEY),
              text=unauthorized_string)

        return_value = status_schedule(BAD_API_KEY)
        assert return_value is None


def test_customer_details():
    from hydrawiser.helpers import customer_details
    with requests_mock.Mocker() as m:

        # Test a valid api_key.
        m.get('https://app.hydrawise.com/api/v1/customerdetails.php?'
              'api_key={}'
              '&type={}'
              .format(GOOD_API_KEY, 'controllers'),
              text=good_string)

        return_value = customer_details(GOOD_API_KEY)
        assert return_value is not None

        # Test an invalid api_key.
        m.get('https://app.hydrawise.com/api/v1/customerdetails.php?'
              'api_key={}'
              '&type={}'
              .format(BAD_API_KEY, 'controllers'),
              text=unauthorized_string)

        return_value = customer_details(BAD_API_KEY)
        assert return_value is None


def test_set_zones():
    from hydrawiser.helpers import set_zones
    with requests_mock.Mocker() as m:

        # '{"message":"Invalid operation requested. Please contact \
        # Hydrawise.","message_type":"error"}'
        # '{"message":"Stopping all manually started zones on Home \
        # Controller 6 minutes","message_type":"info"}'
        # '{"error_msg":"unauthorised"}'

        info_string = '{"message": "ok", "message_type": "info"}'
        error_string = '{"message": "not ok", "message_type": "error"}'

        # Test positive use of the stop command.
        m.get('https://app.hydrawise.com/api/v1/setzone.php?'
              'api_key={}'
              '&action={}'
              '&relay_id={}'
              .format(GOOD_API_KEY, 'stop', 123456),
              text=info_string)

        return_value = set_zones(GOOD_API_KEY, 'stop', '123456')
        assert return_value is not None

        # Test negative use of the stop command.
        m.get('https://app.hydrawise.com/api/v1/setzone.php?'
              'api_key={}'
              '&action={}'
              .format(GOOD_API_KEY, 'stop'),
              text=error_string)

        return_value = set_zones(GOOD_API_KEY, 'stop')
        assert return_value is None

        # Test positive use of stopall.
        m.get('https://app.hydrawise.com/api/v1/setzone.php?'
              'api_key={}'
              '&action={}'
              .format(GOOD_API_KEY, 'stopall'),
              text=info_string)

        return_value = set_zones(GOOD_API_KEY, 'stopall')
        assert return_value is not None

        # Test positive use of run.
        m.get('https://app.hydrawise.com/api/v1/setzone.php?'
              'api_key={}'
              '&action={}'
              '&relay_id={}'
              '&period_id={}'
              '&custom={}'
              .format(GOOD_API_KEY, 'run', 123456, 999, 60),
              text=info_string)

        return_value = set_zones(GOOD_API_KEY, 'run', '123456', 60)
        assert return_value is not None

        # Test negative use of run.
        return_value = set_zones(GOOD_API_KEY, 'run')
        assert return_value is None

        return_value = set_zones(GOOD_API_KEY, 'run', '1234')
        assert return_value is None

        # Test positive use of runall.
        m.get('https://app.hydrawise.com/api/v1/setzone.php?'
              'api_key={}'
              '&action={}'
              '&period_id={}'
              '&custom={}'
              .format(GOOD_API_KEY, 'runall', 999, 60),
              text=info_string)

        return_value = set_zones(GOOD_API_KEY, 'runall', time=60)
        assert return_value is not None

        # Test negative use of runall.
        return_value = set_zones(GOOD_API_KEY, 'runall', '123456', 100)
        assert return_value is None

        # Test invalid command.
        return_value = set_zones(GOOD_API_KEY, 'something')
        assert return_value is None

        # Test bad api_key.
        m.get('https://app.hydrawise.com/api/v1/setzone.php?'
              'api_key={}'
              '&action={}'
              '&period_id={}'
              '&custom={}'
              .format(BAD_API_KEY, 'runall', 999, 60),
              text=unauthorized_string)

        return_value = set_zones(BAD_API_KEY, 'runall', time=60)
        assert return_value is None
