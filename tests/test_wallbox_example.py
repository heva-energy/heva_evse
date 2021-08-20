import unittest
import asyncio
from examples.wallbox import Wallbox


class TestWallbox(unittest.TestCase):
    loop = asyncio.get_event_loop()

    def test_basic(self):
        config = {
            'username': 'me@gmail.com',
            'password': 'my-password',
            'charger_id': 19414
        }

        async def main():
            async with Wallbox(config) as wb:
                print(await wb.get_charger())

        self.loop.run_until_complete(main())


if __name__ == '__main__':
    unittest.main()
