# Hydrawiser
[![Coverage Status](https://coveralls.io/repos/github/ptcryan/hydrawiser/badge.svg?branch=master)](https://coveralls.io/github/ptcryan/hydrawiser?branch=master)
[![Build Status](https://travis-ci.org/ptcryan/hydrawiser.svg?branch=master)](https://travis-ci.org/ptcryan/hydrawiser)
[![Documentation Status](https://readthedocs.org/projects/hydrawiser/badge/?version=latest)](http://hydrawiser.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/Hydrawiser.svg)](https://badge.fury.io/py/Hydrawiser)
![Format](https://img.shields.io/pypi/format/hydrawiser.svg)
![License](https://img.shields.io/pypi/l/hydrawiser.svg)

This is a Python 2 and 3 library for controlling the [Hunter](https://www.hunterindustries.com) Pro-HC sprinkler controller.

*Note that this project has no official relationship to Hunter Industries. It was developed using the Hydrawise API v1.4. Use at your own risk.*

Hydrawise Youtube video: https://youtu.be/raOEK8JjSUA<br/>
Hydrawise official site: https://hydrawise.com<br/>
Source code documentation: https://hydrawiser.readthedocs.io<br/>
Python Package Index: https://pypi.org/project/Hydrawiser/

## Usage API v1
```python
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
hw.relay_info(0, 'name')
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
```
### Limitations

  - Only one controller is supported
  - No sensor data


## Hydrawise GraphQL API (v2)

```python

from hydrawiser.graphql import HydrawiserV2

hw = HydrawiserV2('<you email>', '<your hydrawise password>')

# Information about your account
hw.customer()

# List all controllers
hw.controllers()

# List all controllers and their sensors
hw.sensors()

# List all controllers and their zones
hw.zones()
```

