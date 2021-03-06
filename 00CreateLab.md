# Lab 00. Create hands on lab environment

Using Azure Cloud Shell and Azure Cli script you can create a lab environment fast and easy. In this lab, use Azure Cli script to set up Hands-on Lab environment.

## 1. Create Hands-on Lab envrironment using a script

1. Open browser and go to [Azure Portal](https://portal.azure.com)

1. __Click__ on _new Dashboard_

    ![new dashboard](./images/00.01.png)

1. __Type__ name of the dashboard as _Azure Workshop_

    ![new dashboard](./images/00.02.png)

1. Open cloud shell from the browser

    ![cloudshell](./images/00.03.png)

1. Download a script

    Run following commnad from the cloud shell prompt

    > Please copy below command and past it to cloud shell prompt

    ```
    wget -O azlab.azcli https://raw.githubusercontent.com/xlegend1024/az-iot-hol/master/azcli/00.azlab-iot_us.azcli
    ```

1. Run command to create a resource group and resource

    > Care with subscription name when you run the script

    ```bash
    sh ./azlab.azcli
    ```

    ![run script](./images/env01.01.png)

    Make sure you use correct __Azure Subscription__ for the Hands-on lab.

1. Make sure you have a resource group and resources:
    * Linux Virtual Machine
    * Windows Virtual Machine 
    * Blob 
    * CosmosDB
    * SQL Database

---
[Main](https://github.com/xlegend1024/az-iot-hol)