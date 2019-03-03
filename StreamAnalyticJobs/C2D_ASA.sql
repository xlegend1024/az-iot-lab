SELECT
    *
INTO
    cosmosdb
FROM
    iothub

SELECT
    input.IoTHub.ConnectionDeviceId as deviceID, timeCreated, temperature as machine_temp, pressure as machine_press, temperature as ambient_temp, humidity as ambient_humi
INTO
    blob
FROM
    iothub as input

SELECT
    input.IoTHub.ConnectionDeviceId as deviceID, System.TimeStamp AS timeCreated, AVG(temperature) as machine_temp, AVG(pressure) as machine_press, avg(temperature) as ambient_temp, avg(humidity) as ambient_humi
INTO
    sqldb
FROM
    iothub as input
GROUP BY
    input.IoTHub.ConnectionDeviceId, TumblingWindow(minute, 1)

SELECT
    input.IoTHub.ConnectionDeviceId as deviceID, System.TimeStamp AS timeCreated, AVG(temperature) as machine_temp, AVG(pressure) as machine_press, avg(temperature) as ambient_temp, avg(humidity) as ambient_humi
INTO
    sqldb2
FROM
    iothub as input
GROUP BY
    input.IoTHub.ConnectionDeviceId, TumblingWindow(hour, 1)