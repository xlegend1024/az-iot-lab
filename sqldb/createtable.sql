CREATE TABLE tbl1mavg (
idx int NOT NULL primary key IDENTITY(1,1),
deviceid varchar(100),
timecreated DATETIME2,
timeinserted DATETIME2 default GETDATE(),
machine_temp float,
machine_press float,
ambient_temp float,
ambient_humi float
);

CREATE TABLE tbl1havg (
idx int NOT NULL primary key IDENTITY(1,1),
deviceid varchar(100),
timecreated DATETIME2,
timeinserted DATETIME2 default GETDATE(),
machine_temp float,
machine_press float,
ambient_temp float,
ambient_humi float
);
