import uuid
import time
import random
import Adafruit_BluefruitLE

DEVICE_NAME = "BLE-Server"

SERVICE_UUID = uuid.UUID('00000180-0000-1000-8000-00805F9B34FB')
WRITE_UUID = uuid.UUID('0000DEAD-0000-1000-8000-00805F9B34FB')
READ_UUID = uuid.UUID('0000FEF4-0000-1000-8000-00805F9B34FB')
connected_to_peripheral = False
# SERVICE_UUID = uuid.UUID('0180')
# WRITE_UUID = uuid.UUID('DEAD')
# READ_UUID = uuid.UUID('FEF4')

ble = Adafruit_BluefruitLE.get_provider()


def scan_for_peripheral(adapter):
    """Scan for BLE peripheral and return device if found"""
    # print('  Searching for device...')
    try:
        adapter.start_scan()
        # Scan for the peripheral (will time out after 60 seconds
        # but you can specify an optional timeout_sec parameter to change it).
        device = ble.find_device(name=DEVICE_NAME)
        if device is None:
            raise RuntimeError('Failed to find device!')
        return device
    finally:
        # Make sure scanning is stopped before exiting.
        adapter.stop_scan()


def sleep_random(min_ms=1, max_ms=1000):
    """Add a random sleep interval between 1ms to 1000ms"""
    duration_sec = random.randrange(min_ms, max_ms)/1000
    # # print('   Sleeping for ' + str(duration_sec) + 'sec')
    time.sleep(duration_sec)


def search_ble():
    test_iteration = 0
    echo_mismatch_count = 0
    misc_error_count = 0

    # Clear any cached data because both BlueZ and CoreBluetooth have issues with
    # caching data and it going stale.
    ble.clear_cached_data()

    # Get the first available BLE network adapter and make sure it's powered on.
    adapter = ble.get_default_adapter()
    try:
        adapter.power_on()
        # print('Using adapter: {0}'.format(adapter.name))

        # This loop contains the main logic for testing the BLE peripheral.
        # We scan and connect to the peripheral, discover services,
        # read/write to characteristics, and keep track of errors.
        # This test repeats 10 times.
        while test_iteration < 10:
            connected_to_peripheral = False

            while not connected_to_peripheral:
                try:
                    peripheral = scan_for_peripheral(adapter)
                    peripheral.connect(timeout_sec=10)
                    connected_to_peripheral = True

                    with open('peripheral.txt', 'w') as f:
                        f.write(str(connected_to_peripheral))
                        f.write("connected")

                    test_iteration += 1
                    print('Test #{} --'.format(test_iteration))
                except BaseException as e:
                    print("Connection failed: " + str(e))
                    time.sleep(1)
                    print("Retrying...")
            print("Connected to peripheral: ", connected_to_peripheral) if connected_to_peripheral else print(
                "Not connected to peripheral: ", connected_to_peripheral)
            try:
                print('  Discovering services and characteristics...')
                peripheral.discover([SERVICE_UUID], [WRITE_UUID, READ_UUID])

                # Find the service and its characteristics
                service = peripheral.find_service(SERVICE_UUID)
                tx = service.find_characteristic(WRITE_UUID)
                rx = service.find_characteristic(READ_UUID)

                # Randomize the intervals between different operations
                # to simulate user-triggered BLE actions.
                sleep_random(1, 1000)

                # Write random value to characteristic.
                # write_val = bytearray([random.randint(1, 255)])
                # print('  Writing ' + str(write_val) + ' to the write char')
                # tx.write_value(write_val)

                sleep_random(1, 1000)

                # Read characteristic and make sure it matches the value written.
                read_val = rx.read_value()
                print('  Read ' + str(read_val) + ' from the read char')
                print('-------READ VALUE------- \n-> ', read_val)
                # if write_val != read_val:
                #     echo_mismatch_count = echo_mismatch_count + 1
                # print('  Read value does not match value written')

                peripheral.disconnect()
                test_iteration = 10
                sleep_random(1, 1000)
            except BaseException as e:
                misc_error_count = misc_error_count + 1
                print('Unexpected error: ' + str(e))
                print('Current error count: ' + str(misc_error_count))
                time.sleep(1)
                print('Retrying...')

    finally:
        # Disconnect device on exit.
        peripheral.disconnect
        # print('\nConnection count: ' + str(test_iteration))
        # print('Echo mismatch count: ' + str(echo_mismatch_count))
        # print('Misc error count: ' + str(misc_error_count))


def main():
    # Initialize the BLE system.  MUST be called before other BLE calls!
    ble.initialize()

    # Start the mainloop to process BLE events, and run the provided function in
    # a background thread.  When the provided main function stops running, returns
    # an integer status code, or throws an error the program will exit.
    ble.run_mainloop_with(search_ble)


if __name__ == '__main__':
    main()
