"""Define basic data for unittests."""
import unittest
import requests_mock

from tests.extras import load_fixture

from tests.const import (
                              STATUS_SCHEDULE,
                              CUSTOMER_DETAILS,
                              SET_ZONE,
                              GOOD_API_KEY)


class UnitTestBase(unittest.TestCase):
    """Top level test class"""

    @requests_mock.Mocker()
    def setUp(self, mock):
        """Initialize rdy object for unittests."""
        from hydrawiser.core import Hydrawiser

        mock.get(STATUS_SCHEDULE, text=load_fixture('statusschedule.json'))
        mock.get(CUSTOMER_DETAILS, text=load_fixture('customerdetails.json'))
        mock.get(SET_ZONE, text=load_fixture('setzone.json'))

        # initialize self.rdy object
        self.rdy = Hydrawiser(GOOD_API_KEY)

    def cleanUp(self):
        """Cleanup any data created from the tests."""
        self.rdy = None

    def tearDown(self):
        """Stop everything initialized."""
        self.cleanUp()
