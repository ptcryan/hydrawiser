"""Define basic data for unittests."""
import unittest
import requests_mock

from tests.extras import load_fixture


class UnitTestBase(unittest.TestCase):
    """Top level test class"""

    @requests_mock.Mocker()
    def setUp(self, mock):
        """Initialize rdy object for unittests."""
        from hydrawiser.core_v2 import HydrawiserV2

        mock.post(
            HydrawiserV2.TOKEN_ENDPOINT,
            text=load_fixture('oauth2_resp.json')
        )

        # initialize self.rdy object
        self.rdy = HydrawiserV2('test@example.com', 's3cr3tP1ssw0rd')

    def cleanUp(self):
        """Cleanup any data created from the tests."""
        self.rdy = None

    def tearDown(self):
        """Stop everything initialized."""
        self.cleanUp()


class TestHydrawiserV2(UnitTestBase):

    def test_attributes(self):
        """ Test if attributes exist. """

        self.assertTrue(hasattr(self.rdy, 'customer'))
        self.assertTrue(hasattr(self.rdy, 'controllers'))
