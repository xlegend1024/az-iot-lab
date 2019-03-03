# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import random
import time
import sys
import datetime

import iothub_client
# pylint: disable=E0611
from iothub_client import IoTHubModuleClient, IoTHubClientError, IoTHubTransportProvider
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError

# messageTimeout - the maximum time in milliseconds until a message times out.
# The timeout period starts at IoTHubModuleClient.send_event_async.
# By default, messages do not expire.
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

# global counters
RECEIVE_CALLBACKS = 0
SEND_CALLBACKS = 0

# Choose HTTP, AMQP or MQTT as transport protocol.  Currently only MQTT is supported.
PROTOCOL = IoTHubTransportProvider.MQTT

# Callback received when the message that we're forwarding is processed.
def send_confirmation_callback(message, result, user_context):
    global SEND_CALLBACKS
    print ( "Confirmation[%d] received for message with result = %s" % (user_context, result) )
    map_properties = message.properties()
    key_value_pair = map_properties.get_internals()
    print ( "    Properties: %s" % key_value_pair )
    SEND_CALLBACKS += 1
    print ( "    Total calls confirmed: %d" % SEND_CALLBACKS )


# receive_message_callback is invoked when an incoming message arrives on the specified 
# input queue (in the case of this sample, "input1").  Because this is a filter module, 
# we will forward this message onto the "output1" queue.
def receive_message_callback(message, hubManager):
    global RECEIVE_CALLBACKS
    message_buffer = message.get_bytearray()
    size = len(message_buffer)
    print ( "    Data: <<<%s>>> & Size=%d" % (message_buffer[:size].decode('utf-8'), size) )
    map_properties = message.properties()
    key_value_pair = map_properties.get_internals()
    print ( "    Properties: %s" % key_value_pair )
    RECEIVE_CALLBACKS += 1
    print ( "    Total calls received: %d" % RECEIVE_CALLBACKS )
    hubManager.forward_event_to_output("output1", message, 0)
    return IoTHubMessageDispositionResult.ACCEPTED

class HubManager(object):

    def __init__(
            self,
            protocol=IoTHubTransportProvider.MQTT):
        self.client_protocol = protocol
        self.client = IoTHubModuleClient()
        self.client.create_from_environment(protocol)

        # set the time until a message times out
        self.client.set_option("messageTimeout", MESSAGE_TIMEOUT)
        
        # sets the callback when a message arrives on "input1" queue.  Messages sent to 
        # other inputs or to the default will be silently discarded.
        self.client.set_message_callback("input1", receive_message_callback, self)

    # Forwards the message received onto the next stage in the process.
    def forward_event_to_output(self, outputQueueName, event, send_context):
        self.client.send_event_async(
            outputQueueName, event, send_confirmation_callback, send_context)

def main(protocol):
    try:
        print ( "\nPython %s\n" % sys.version )
        print ( "IoT Hub Client for Python" )

        hub_manager = HubManager(protocol)

        print ( "Starting the IoT Hub Python sample using protocol %s..." % hub_manager.client_protocol )
        print ( "The sample is now waiting for messages and will indefinitely.  Press Ctrl-C to exit. ")

        while True:
            # Build the message with simulated telemetry values.
            items = ITEMS + random.randrange(10)
            partnerid = PARTNERID[random.randrange(3)]
            storeid = STOREID[random.randrange(4)]
            bagid = random.randrange(10000,11000,2)
            employeeid = EMPLOYEEID[random.randrange(5)]

            # OPEN BAG
            msg_txt_formatted = MSG_TXT % (EVENT[0], bagid, partnerid, employeeid, storeid, "", datetime.datetime.utcnow())
            message = IoTHubMessage(msg_txt_formatted)

            # Send the message.
            hub_manager.forward_event_to_output("sensorOutput", message, 0)
            print( "[%s] Bag %s is scaned wait for pipeline events" % (EVENT[0], bagid))

            # wait untill the bag moves
            time.sleep(random.randrange(60,300,2))

            # Sorting in a prodcution line
            for i in range(items):
                msg_txt_formatted = MSG_TXT % (EVENT[1], bagid, partnerid, employeeid, storeid, PIPEID[random.randrange(4)], datetime.datetime.utcnow())
                message = IoTHubMessage(msg_txt_formatted)

                # Send the message.
                hub_manager.forward_event_to_output("sensorOutput", message, 0)
                print("[%d/%d] Sending message: %s" % (i, items,message.get_string()) )
                interval = INTERVAL + random.randrange(5,20,2)
                time.sleep(interval)

            # CLOSE BAG
            msg_txt_formatted = MSG_TXT % (EVENT[2], bagid, partnerid, employeeid, storeid, "", datetime.datetime.utcnow())
            message = IoTHubMessage(msg_txt_formatted)
            hub_manager.forward_event_to_output("sensorOutput", message, 0)
            print( "[%s] Bag %s is scaned wait for pipeline events" % (EVENT[2], bagid))

    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubModuleClient sample stopped" )

if __name__ == '__main__':
    main(PROTOCOL)