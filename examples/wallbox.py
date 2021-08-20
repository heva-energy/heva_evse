"""
Wallbox example inspired by https://github.com/cliviu74/wallbox
"""

import httpx
from heva_evse import EVSEConnector


class Wallbox(EVSEConnector):
    def __init__(self, config, setup):
        self.username = config['username']
        self.password = config['password']
        self.charger_id = config['charger_id']
        self._request_timeout = None
        self.baseUrl = "https://api.wall-box.com/"

    @property
    def request_timeout(self):
        return self._request_timeout

    async def __aenter__(self):
        self.client = await self.authenticate()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    async def authenticate(self):
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"{self.baseUrl}auth/token/user",
                auth=(self.username, self.password),
                timeout=self._request_timeout
            )

            # Example response
            # {'jwt': 'XXXX', 'user_id': 123, 'ttl': 1629369282766370108, 'error': False, 'status': 200}

            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json;charset=UTF-8",
                "Authorization": f"Bearer {r.json()['jwt']}"
            }
            return httpx.AsyncClient(headers=headers, timeout=self._request_timeout)

    async def get_chargers_list(self):
        charger_ids = []
        response = await self.client.get(f"{self.baseUrl}v3/chargers/groups",
                                         )
        for group in response.json()["result"]["groups"]:
            for charger in group["chargers"]:
                charger_ids.append(charger["id"])

        return charger_ids

    async def get_charger_info(self):
        response = await self.client.get(f"{self.baseUrl}v2/charger/{self.charger_id}")
        # Example response
        # {'chargerData': {'id': 19414, 'serialNumber': '19414', 'name': 'Pulsar SN 19414', 'group': 129229,
        #                     'chargerType': 'Pulsar', 'softwareVersion': None, 'status': None,
        #                     'statusDescription': 'Offline', 'ocppConnectionStatus': 0, 'ocppReady': None,
        #                     'stateOfCharge': None, 'maxChgCurrent': 0, 'maxAvailableCurrent': 32,
        #                     'maxChargingCurrent': 1, 'locked': 0, 'lastConnection': None,
        #                     'lastSync': {'date': '2021-07-31 20:47:11.000000', 'timezone_type': 3, 'timezone': 'UTC'},
        #                     'midEnabled': 0, 'midMargin': None, 'midMarginUnit': None, 'midSerialNumber': None,
        #                     'midStatus': 0, 'wifiSignal': None, 'connectionType': None, 'chargerLoadName': 'Private',
        #                     'chargerLoadId': 0, 'chargingType': 'AC', 'connectorType': 'Type 2/Socket',
        #                     'protocolCommunication': None, 'accessType': 'guest', 'powerSharingStatus': None,
        #                     'resume': {'totalUsers': 1, 'totalSessions': 0, 'chargingTime': None, 'totalEnergy': 0,
        #                                'totalMidEnergy': 0, 'energyUnit': 'kWh'}}, 'users': [
        #     {'id': 127629, 'avatar': None, 'name': 'Ian', 'surname': 'Napier', 'email': '',
        #      'profile': 'super-admin', 'assigned': True, 'createdByUser': False}]}

        return response.json()['data']['chargerData']

    async def unlock(self):
        response = await self.client.put(f"{self.baseUrl}v2/charger/{self.charger_id}", json={"locked": 0})
        return response.json()

    async def lock(self):
        response = await self.client.put(f"{self.baseUrl}v2/charger/{self.charger_id}", json={"locked": 1})
        return response.json()

    async def get_lock_status(self):
        info = await self.get_charger_info()
        return info['locked'] == 1

    async def set_current_limit(self, max_current_value):
        response = await self.client.put(f"{self.baseUrl}v2/charger/{self.charger_id}",
                                         json={"maxChargingCurrent": max_current_value})

        return response.json()

    async def get_current_limit(self):
        info = await self.get_charger_info()
        return info['maxChargingCurrent']

    async def stop_charge(self):
        response = await self.client.post(
            f"{self.baseUrl}v3/chargers/{self.charger_id}/remote-action",
            json={"action": 2},
        )

        return response.json()

    async def start_charge(self):
        response = await self.client.post(
            f"{self.baseUrl}v3/chargers/{self.charger_id}/remote-action",
            json={"action": 1},
        )

        return response.json()

    async def get_charge_status(self):
        info = await self.get_charger_info()
        return info['status']

    def get_current(self) -> float:
        pass
