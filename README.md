# HEVA EVSE Wrapper

The purpose of this module is to provide a standardised base class for OpenHEVA compatible EVSE wrappers.

Included below are instructions describing how to build a wrapper for any HTTP based EVSE control and metering API.

## Usage

First, install the module via pip install.

```shell script
pip install heva_evse
```

Next, import the EVSEConnector base class for use in your project.

```python
from heva_evse import EVSEConnector
```

Finally, use the base class as a guide to implement the required control and telemetry methods.

**Note 1:** The first argument of the constructor should be a dictionary of required config fields for a singular EVSE.

**Note 2:** The second argument to the constructor should also be a dictionary containing any fields required to integrate with the specific API (such as a generic API key).

```python
class MyEVSEWrapper(EVSEConnector):
    def __init__(self, config, setup):
        self.username = config['username']
        self.password = config['password']
        self.charger_id = config['charger_id']

        self.partner_api_key = setup['api_key']
    
    ...
```

An example wrapper is available in the examples folder of this repository, showing how the base class can be used to abstract control of the Wallbox API.

## Integration with OpenHEVA

In order to integrate your control and telemetry module into the OpenHEVA server, a simple yaml file must be included in the project root.

This file defines the import values and configuration fields required for successful operation, as well as brand and model information to assist in user onboarding.

For example:

```yaml
module_name: my_evse
import_name: MyEVSEWrapper
brand_name: "My EVSE"
model_names:
  - "The first and best v0"
  - "Supercharge v1.0"
config:
  - username
  - password
  - charger_id
setup:
  - api_key
```

With this file present, OpenHEVA is able to install the wrapper using only a git url (be it public or private).