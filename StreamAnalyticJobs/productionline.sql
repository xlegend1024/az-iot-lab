-- Save raw data to Blob as JSON form
SELECT
    *
INTO
    blob
FROM
    iothub 

-- Aggregate events every 10 minutes
SELECT 
    DATEADD(minute,-3,System.TimeStamp) as startdatetime,
    System.TimeStamp AS enddatetime,
    employeeid,
    storeid,
    count(DISTINCT pipeevent.pipeid) as totalsort,
    count(DISTINCT bagid) as totalbag
INTO tbl10mperf
FROM iothub  
GROUP BY employeeid, storeid, TumblingWindow(minute, 3)

-- query 3
SELECT 
    iothub.[IoTHub].[ConnectionDeviceId] as deviceid, 
    DATEADD(minute,-10,System.TimeStamp) as captureddatetime,
    eventtype,
    bagid,
    partnerid,
    employeeid,
    storeid,
    count(*) as eventcount
INTO tblbaghistory
FROM iothub 
GROUP BY iothub.[IoTHub].[ConnectionDeviceId], eventtype, employeeid, storeid, partnerid, bagid, TumblingWindow(minute, 10)

-- query 4
SELECT 
    pipeevent.captureddatetime as eventdatetime, 
    storeid, 
    partnerid, 
    bagid, 
    employeeid,
    pipeevent.pipeid as pipeid
INTO 
    tblworklogs
FROM iothub 
WHERE 
    eventtype = 'sort'

-- query 5
SELECT 
    pipeevent.captureddatetime as eventdatetime, 
    storeid, 
    partnerid, 
    eventype,
    bagid, 
    employeeid
INTO 
    tblbagevent
FROM iothub 
WHERE 
    eventtype = 'openbag' or eventtype ='closebag'

-- not working T.T
-- SELECT
--     [employeeid], 
--     bagid, 
--     DATEDIFF(second, LAST(pipeevent.captureddatetime) OVER (PARTITION BY [employeeid], bagid LIMIT DURATION(minute, 10) WHEN Event = 'openbag'), Time) as duration
-- INTO 
--     tblprocduration
-- FROM 
--     iothub  
-- WHERE 
--     Event = 'closebag'

