import uuid
import time
import random
import numpy
import Adafruit_BluefruitLE
import struct
import pickle

DEVICE_NAME = "BLE-Server"

SERVICE_UUID = uuid.UUID('00000180-0000-1000-8000-00805F9B34FB')
WRITE_UUID = uuid.UUID('0000DEAD-0000-1000-8000-00805F9B34FB')
READ_UUID_S1 = uuid.UUID('0000FEF4-0000-1000-8000-00805F9B34FB')
READ_UUID_N1 = uuid.UUID('0000FEF5-0000-1000-8000-00805F9B34FB')
READ_UUID_S2 = uuid.UUID('0000FEF6-0000-1000-8000-00805F9B34FB')
READ_UUID_N2 = uuid.UUID('0000FEF7-0000-1000-8000-00805F9B34FB')
READ_UUID_S3 = uuid.UUID('0000FEF8-0000-1000-8000-00805F9B34FB')
READ_UUID_N3 = uuid.UUID('0000FEF9-0000-1000-8000-00805F9B34FB')

#SERVICE_UUID = uuid.UUID('0180')
#WRITE_UUID = uuid.UUID('DEAD')
#READ_UUID = uuid.UUID('FEF4')

ble = Adafruit_BluefruitLE.get_provider()


def scan_for_peripheral(adapter):
    """Scan for BLE peripheral and return device if found"""
    print('  Searching for device...')
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
    print('   Sleeping for ' + str(duration_sec) + 'sec')
    time.sleep(duration_sec)


def main():
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
        print('Using adapter: {0}'.format(adapter.name))

        # This loop contains the main logic for testing the BLE peripheral.
        # We scan and connect to the peripheral, discover services,
        # read/write to characteristics, and keep track of errors.
        # This test repeats 10 times.
        # while test_iteration < 10:
        connected_to_peripheral = False

        while not connected_to_peripheral:
            # the try passes if it finds the server and connects
            try:
                peripheral = scan_for_peripheral(adapter)
                peripheral.connect(timeout_sec=10)
                connected_to_peripheral = True
                test_iteration += 1
                # print('Test #{} --'.format(test_iteration))

            except BaseException as e:
                print("Connection failed: " + str(e))
                time.sleep(1)
                print("Retrying...")

        # attempts to discover the UUIDs defined above
        try:
            #print('  Discovering services and characteristics...')
            peripheral.discover([SERVICE_UUID], [WRITE_UUID, READ_UUID_S1, READ_UUID_N1,
                                READ_UUID_S2, READ_UUID_N2, READ_UUID_S3, READ_UUID_N3])

            # Find the service and its characteristics
            service = peripheral.find_service(SERVICE_UUID)
            tx = service.find_characteristic(WRITE_UUID)
            rx_s1 = service.find_characteristic(READ_UUID_S1)
            rx_s1_numElements = service.find_characteristic(READ_UUID_N1)
            rx_s2 = service.find_characteristic(READ_UUID_S2)
            rx_s2_numElements = service.find_characteristic(READ_UUID_N2)
            rx_s3 = service.find_characteristic(READ_UUID_S3)
            rx_s3_numElements = service.find_characteristic(READ_UUID_N3)

            # Randomize the intervals between different operations
            # to simulate user-triggered BLE actions.
            #sleep_random(1, 1000)

            # Write random value to characteristic.
            #write_val = bytearray([random.randint(1, 255)])
            #print('  Writing ' + str(write_val) + ' to the write char')
            # tx.write_value(write_val)

            #sleep_random(1, 1000)

            while True:
                s1 = 0
                s2 = int.from_bytes(
                    rx_s2_numElements.read_value(), "little", signed=False)
                s3 = int.from_bytes(
                    rx_s3_numElements.read_value(), "little", signed=False)
                i = 0
                while s2 == 0 or s3 == 0:
                    print(f"waiting for data{'.'*i}", end="\r")
                    s1 = 0
                    s2 = int.from_bytes(
                        rx_s2_numElements.read_value(), "little", signed=False)
                    s3 = int.from_bytes(
                        rx_s3_numElements.read_value(), "little", signed=False)
                    i += 1
                # s1 = s1 * 6
                # s2 = s2 * 6
                # s3 = s3 * 6
                print(f"printing {s1} amount of values from sensor 1")
                #start = time.time()
                data_1 = []
                s1_diff = 0
                for i in range(s1_diff, s1 // 2):
                    rx_s1_read = rx_s1.read_value()

                    list_of_data_1 = struct.unpack(
                        '<' + 'h' * (len(rx_s1_read) // 2), rx_s1_read)
                    data_1.append(list_of_data_1)

                data_1 = [item for sublist in data_1 for item in sublist]

                #end = time.time()
                #print(end - start)

                print(f"printing {s2} amount of values from sensor 2")
                #start = time.time()
                data_2 = []
                s2_diff = s2 - 106
                for i in range(s2_diff, s2 // 2):
                    rx_s2_read = rx_s2.read_value()

                    list_of_data_2 = struct.unpack(
                        '<' + 'h' * (len(rx_s2_read) // 2), rx_s2_read)

                    data_2.append(list_of_data_2)

                data_2 = [item for sublist in data_2 for item in sublist]

                print(f"printing {s3} amount of values from sensor 3")
                data_3 = []
                s3_diff = s3 - 106
                for i in range(s3_diff, s3 // 2):
                    rx_s3_read = rx_s3.read_value()

                    list_of_data_3 = struct.unpack(
                        '<' + 'h' * (len(rx_s3_read) // 2), rx_s3_read)

                    data_3.append(list_of_data_3)

                data_3 = [item for sublist in data_3 for item in sublist]

                # print(f'Data from sensor 1: {data_1}, length: {len(data_1)}')
                # print(f'Data from sensor 2: {data_2}, length: {len(data_2)}')
                # print(f'Data from sensor 3: {data_3}, length: {len(data_3)}')

                data = [data_1, data_2, data_3]

                data = [item for sublist in data for item in sublist]
                print(data)

                with open('data.txt', 'wb') as f:
                    pickle.dump(data, f)

                tx.write_value(bytearray([72]))

            # peripheral.disconnect()
            #sleep_random(1, 1000)
        # except BaseException as e:
        #    misc_error_count = misc_error_count + 1
            #print('Unexpected error: ' + str(e))
            #print('Current error count: ' + str(misc_error_count))
        #    time.sleep(1)
            # print('Retrying...')

        except BaseException as e:
            print(f"Unexpected Error: {e}")
            time.sleep(1)

    except BaseException as e:
        print(f"Unexpected Error: {e}")
        time.sleep(1)
    # finally:
        # Disconnect device on exit.
    #    peripheral.disconnect
        #print('\nConnection count: ' + str(test_iteration))
        #print('Echo mismatch count: ' + str(echo_mismatch_count))
        #print('Misc error count: ' + str(misc_error_count))


# this must be called before any other BLE calls
ble.initialize()


# FROM ADAFRUIT DEF OF run_mainloop_with: Start the mainloop to process BLE events, and run the provided function in
# a background thread.  When the provided main function stops running, returns
# an integer status code, or throws an error the program will exit.

# on webserver going to try to run in own background thread
ble.run_mainloop_with(main)
