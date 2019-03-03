# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

import random
import time
import sys
import datetime

# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
# The sample connects to a device-specific MQTT endpoint on your IoT Hub.
import iothub_client
# pylint: disable=E0611
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue

# The device connection string to authenticate the device with your IoT hub.
# Using the Azure CLI:
# az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
CONNECTION_STRING = ""

# Using the MQTT protocol.
PROTOCOL = IoTHubTransportProvider.MQTT
MESSAGE_TIMEOUT = 10000

# Define the JSON message to send to IoT Hub.
ITEMS = 10
EVENT = ["openbag","sort","closebag"]
PARTNERID = ["thearc","fra","safenest","bigbrothersbigsisters"]
STOREID = ["seattle", "bellevue", "kirkland","redmond"]
PIPEID = ["men","woman","kid","accessories"]
EMPLOYEEID = ["HYUN", "ARTHUR","ROJY","JACK","MATT"]
MSG_TXT = "{\"eventtype\": \"%s\", \"bagid\": \"%s\", \"partnerid\": \"%s\", \"employeeid\": \"%s\",  \"storeid\": \"%s\", \"pipeevent\": {\"pipeid\": \"%s\", \"captureddatetime\": \"%s\" }}"
INTERVAL = 30

def send_confirmation_callback(message, result, user_context):
    #print ( "IoT Hub responded to message with status: %s" % (result) )

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
    return client

# Handle direct method calls from IoT Hub
def device_method_callback(method_name, payload, user_context):
    global INTERVAL
    print ( "\nMethod callback called with:\nmethodName = %s\npayload = %s" % (method_name, payload) )
    device_method_return_value = DeviceMethodReturnValue()
    if method_name == "SetTelemetryInterval":
        try:
            INTERVAL = int(payload)
            # Build and send the acknowledgment.
            device_method_return_value.response = "{ \"Response\": \"Executed direct method %s\" }" % method_name
            device_method_return_value.status = 200
        except ValueError:
            # Build and send an error response.
            device_method_return_value.response = "{ \"Response\": \"Invalid parameter\" }"
            device_method_return_value.status = 400
    else:
        # Build and send an error response.
        device_method_return_value.response = "{ \"Response\": \"Direct method not defined: %s\" }" % method_name
        device_method_return_value.status = 404
    return device_method_return_value

def bag_event(client, eventtype, bagid, partnerid, employeeid, storeid):
    try:
        msg_txt_formatted = MSG_TXT % (eventtype, bagid, partnerid, employeeid, storeid, "", datetime.datetime.utcnow())
        message = IoTHubMessage(msg_txt_formatted)

        # Send the message.
        print( "[%s] Bag %s is scaned wait for pipeline events" % (eventtype, bagid))
        print( "%s" % message.get_string())
        client.send_event_async(message, send_confirmation_callback, None)
        interval = random.randrange(1,5,2)
        time.sleep(interval)
    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return

def iothub_client_telemetry_sample_run():
    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )

        # Set up the callback method for direct method calls from the hub.
        client.set_device_method_callback(
            device_method_callback, None)

        while True:
            # Build the message with simulated telemetry values.
            items = ITEMS + random.randrange(10)
            partnerid = PARTNERID[random.randrange(3)]
            storeid = STOREID[random.randrange(4)]
            bagid = random.randrange(10000,11000,2)
            employeeid = EMPLOYEEID[random.randrange(5)]

            # OPEN BAG
            bag_event(client, EVENT[0], bagid, partnerid, employeeid, storeid)

            # Sorting in a prodcution line
            for i in range(items):
                msg_txt_formatted = MSG_TXT % (EVENT[1], bagid, partnerid, employeeid, storeid, PIPEID[random.randrange(4)], datetime.datetime.utcnow())
                message = IoTHubMessage(msg_txt_formatted)
                client.send_event_async(message, send_confirmation_callback, None)
                # Send the message.
                print("[%d/%d] Sending message: %s" % (i, items,message.get_string()) )
                interval = INTERVAL + random.randrange(10,20,2)
                time.sleep(interval)

            # CLOSE BAG
            bag_event(client, EVENT[2], bagid, partnerid, employeeid, storeid)
    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    print ( "IoT Hub Quickstart #2 - Simulated device" )
    #print ( "Press Ctrl-C to exit" )
    iothub_client_telemetry_sample_run()