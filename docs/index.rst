.. Hydrawiser documentation master file, created by
   sphinx-quickstart on Wed Mar  7 19:15:05 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Hydrawiser's documentation!
======================================
This is a Python 2 and 3 library for controlling the Hunter (https://www.hunterindustries.com) Pro-HC sprinkler controller.

.. warning::
  Note that this project has no official relationship to Hunter Industries. It was developed using the Hydrawise API (https://support.hydrawise.com/hc/en-us/article_attachments/205632298/Hydrawise_API.pdf). Use at your own risk.

.. note::
  | Hydrawise Youtube video: https://youtu.be/raOEK8JjSUA
  | Hydrawise official site: https://hydrawise.com
  | Project documentation: https://hydrawiser.readthedocs.io
  | Source code: https://github.com/ptcryan/hydrawiser

Usage
=====

The following are examples for using the Hydrawiser library.

.. code-block:: python

  from hydrawiser.core import Hydrawiser

  # Register with a hydrawise account to obtain an API key.
  hw = Hydrawiser('0000-1111-2222-3333')

  # List all the controller information.
  hw.controller_info
  {'boc_topology_desired': {'boc_gateways': []}, . . . .

  # Get the controller status.
  hw.status
  'All good!'

  # Get the name of the controller.
  hw.name
  'Home Controller'

  # Get information about the relays on this controller.
  hw.relays
  [{'relay_id': 987654, 'relay': 1, 'name': 'yard', . . . .

  # Get the number of relays on this controller.
  hw.num_relays
  6

  # You can index a specific relay information.
  hw.relays[2]  # Return information for the 3rd relay. Relays is zero indexed.

  # Get the name of the 1st relay.
  hw.relay_info[0, 'name')
  'Back yard'

  # Suspend all relays for 60 days.
  hw.suspend_zone(60)

  # Suspend relay 3 for 2 days.
  hw.suspend_zone(2, 3)

  # Stop all relays.
  hw.run_zone(0)

  # Run all relays for 15 minutes.
  hw.run_zone(15)

  # Run relay 5 for 10 minutes.
  hw.run_zone(10, 5)

  # Refresh the controller attributes.
  hw.update_controller_info()

  # Test to see if a zone is running.
  hw.is_zone_running(3)
  True

  hw.time_remaining(3)
  247

Limitations
===========

* Only one controller is supported

.. toctree::
  :maxdepth: 4
  :caption: Contents:

Developing
==========

hydrawiser package
==================

Submodules
----------

hydrawiser.core module
----------------------

.. automodule:: hydrawiser.core
    :members:
    :undoc-members:
    :show-inheritance:

hydrawiser.helpers module
-------------------------

.. automodule:: hydrawiser.helpers
    :members:
    :undoc-members:
    :show-inheritance:


Module contents
---------------

.. automodule:: hydrawiser
    :members:
    :undoc-members:
    :show-inheritance:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
