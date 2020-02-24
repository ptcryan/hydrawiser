from tests.test_base import UnitTestBase
import requests_mock
from tests.const import SET_ZONE, STATUS_SCHEDULE, CUSTOMER_DETAILS
from tests.extras import load_fixture


class TestHydrawiserCore(UnitTestBase):

    def test_attributes(self):
        """ Test if attributes exist. """

        self.assertTrue(hasattr(self.rdy, 'controller_info'))
        self.assertTrue(hasattr(self.rdy, 'status'))
        self.assertTrue(hasattr(self.rdy, 'controller_id'))
        self.assertTrue(hasattr(self.rdy, 'customer_id'))
        self.assertTrue(hasattr(self.rdy, 'num_relays'))
        self.assertTrue(hasattr(self.rdy, 'sensors'))

    def test_controller(self):
        """ Test if the correct controller is present. """

        self.assertEqual(self.rdy.controller(), self.rdy.controller_id)

    def test_object_name(self):
        """ Tests if the object name is correct. """

        object_name = '<Hydrawiser: {}>'.format(self.rdy.controller_id)

        self.assertEqual(self.rdy.__repr__(), object_name)

    def test_relay_info(self):
        """ Tests if the relay method is giving proper information. """

        # Test if None is returned for an invalid relay number.
        self.assertEqual(self.rdy.relay_info(7), None)

        # Test if multiple attributes are returned if only relay is specified.
        self.assertEqual(len(self.rdy.relay_info(0)), 12)

        # Test is correct relay name is returned.
        self.assertEqual(self.rdy.relay_info(0, 'name'), 'Right yard')

        # Test if None is returned if the attribute doesn't exist.
        self.assertEqual(self.rdy.relay_info(0, 'blech'), None)

    @requests_mock.Mocker()
    def test_suspend_zone(self, mock):
        """ Tests the suspend operations. """

        mock.get(SET_ZONE, text=load_fixture('setzone.json'))

        self.assertIsNotNone(self.rdy.suspend_zone(1))
        self.assertIsNotNone(self.rdy.suspend_zone(-1))
        self.assertIsNotNone(self.rdy.suspend_zone(0))
        self.assertIsNone(self.rdy.suspend_zone(1, -1))
        self.assertIsNone(self.rdy.suspend_zone(1, 6))
        self.assertIsNotNone(self.rdy.suspend_zone(1, 1))

    @requests_mock.Mocker()
    def test_run_zone(self, mock):
        """ Test the run operations. """

        mock.get(SET_ZONE, text=load_fixture('setzone.json'))

        self.assertIsNone(self.rdy.run_zone(1, -1))
        self.assertIsNone(self.rdy.run_zone(1, len(self.rdy.relays)))
        self.assertIsNotNone(self.rdy.run_zone(1))
        self.assertIsNotNone(self.rdy.run_zone(0))
        self.assertIsNotNone(self.rdy.run_zone(0, 1))

    @requests_mock.Mocker()
    def test_list_running_zones(self, mock):
        """ Test to see if running zones are listed. """

        # Check that zone 3 is watterting using iswaterting.json.
        mock.get(STATUS_SCHEDULE, text=load_fixture('iswatering.json'))
        mock.get(CUSTOMER_DETAILS, text=load_fixture('customerdetails.json'))

        assert self.rdy.list_running_zones() == 3

        # Check that no zones are waterting using donewatering.json.
        # In this case running: [] is in the json results.
        mock.get(STATUS_SCHEDULE, text=load_fixture('donewatering.json'))

        assert self.rdy.list_running_zones() is None

        # Check that no zones are waterting using donewatering.json.
        # In this case running: [] is NOT in the json results.
        mock.get(STATUS_SCHEDULE, text=load_fixture('donewatering_2.json'))

        assert self.rdy.list_running_zones() is None

    @requests_mock.Mocker()
    def test_is_zone_running(self, mock):
        """ Test if proper zone is returned """

        # Check if zone 3 is watering.
        mock.get(STATUS_SCHEDULE, text=load_fixture('iswatering.json'))
        mock.get(CUSTOMER_DETAILS, text=load_fixture('customerdetails.json'))

        assert self.rdy.is_zone_running(3) is True
        assert self.rdy.is_zone_running(0) is False

        # Check that no zones are waterting using donewatering.json.
        # In this case running: [] is in the json results.
        mock.get(STATUS_SCHEDULE, text=load_fixture('donewatering.json'))

        assert self.rdy.is_zone_running(3) is False

        # Check that no zones are waterting using donewatering.json.
        # In this case running: [] is NOT in the json results.
        mock.get(STATUS_SCHEDULE, text=load_fixture('donewatering_2.json'))

        assert self.rdy.is_zone_running(3) is False

    @requests_mock.Mocker()
    def test_time_remaining(self, mock):
        """ Test is proper time is returned """

        mock.get(STATUS_SCHEDULE, text=load_fixture('iswatering.json'))
        mock.get(CUSTOMER_DETAILS, text=load_fixture('customerdetails.json'))

        # Test if checking zone #
        self.assertIsNone(self.rdy.time_remaining(-1))
        self.assertIsNone(self.rdy.time_remaining(self.rdy.num_relays))

        # Fixture has zone 3 running with 297 seconds remaining.
        self.assertEqual(self.rdy.time_remaining(3), 297)
        self.assertEqual(self.rdy.time_remaining(2), 0)
