# az-iot-hol

Scenario

Architecutre

## Setup Hands-on Lab Environment

1. Create Resources

2. Download Sample Code (Node.js)

Download the sample Node.js project from https://github.com/Azure-Samples/azure-iot-samples-node/archive/master.zip and extract the ZIP archive.

## Create Azure IoT Hub

## Register a Device

## Device-to-Cloud (D2C)

https://docs.microsoft.com/en-us/azure/iot-hub/quickstart-send-telemetry-node


## Send Telemetry to Cloud

## Cloud-to-Device (C2D)

https://docs.microsoft.com/en-us/azure/iot-hub/quickstart-control-device-node

## Routing Messages

## Device Twin

## Configure Your Devices

https://docs.microsoft.com/en-us/azure/iot-hub/tutorial-device-twins

## Schedule and Broadcast Jobs

https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-node-node-schedule-jobs#schedule-jobs-for-calling-a-direct-method-and-updating-a-device-twins-properties

## IoT Edge

https://docs.microsoft.com/en-us/azure/iot-edge/quickstart-linux

az vm create --resource-group IoTEdgeResources --name EdgeVM --image Canonical:UbuntuServer:16.04-LTS:latest --admin-username azureuser --generate-ssh-keys --size Standard_B1ms