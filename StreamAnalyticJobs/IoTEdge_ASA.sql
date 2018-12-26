SELECT
    *
INTO
    cosmosdb
FROM
    iothub

SELECT
    input.IoTHub.ConnectionDeviceId as deviceID, timeCreated, machine.temperature as machine_temp, machine.pressure as machine_press, ambient.temperature as ambient_temp, ambient.humidity as ambient_humi
INTO
    blob
FROM
    iothub as input

SELECT
    input.IoTHub.ConnectionDeviceId as deviceID, System.TimeStamp AS timeCreated, AVG(machine.temperature) as machine_temp, AVG(machine.pressure) as machine_press, avg(ambient.temperature) as ambient_temp, avg(ambient.humidity) as ambient_humi
INTO
    sql1mtbl
FROM
    iothub as input
GROUP BY
    input.IoTHub.ConnectionDeviceId, TumblingWindow(minute, 1)

SELECT
    input.IoTHub.ConnectionDeviceId as deviceID, System.TimeStamp AS timeCreated, AVG(machine.temperature) as machine_temp, AVG(machine.pressure) as machine_press, avg(ambient.temperature) as ambient_temp, avg(ambient.humidity) as ambient_humi
INTO
    sql1htbl
FROM
    iothub as input
GROUP BY
    input.IoTHub.ConnectionDeviceId, TumblingWindow(hour, 1)