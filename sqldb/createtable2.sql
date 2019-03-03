CREATE TABLE tbl10mperf (
idx int NOT NULL primary key IDENTITY(1,1),
startdatetime DATETIME2,
enddatetime DATETIME2,
employeeid varchar(10),
storeid varchar(100),
totalsort int,
totalbag int
);

CREATE TABLE tblbaghistory (
idx int NOT NULL primary key IDENTITY(1,1),
deviceid varchar(100),
captureddatetime DATETIME2,
timeinserted DATETIME2 default GETDATE(),
eventtype varchar(10),
bagid varchar(10),
partnerid varchar(100),
employeeid varchar(100),
storeid varchar(100),
eventcount int
);

CREATE TABLE tblprocduration(
idx int NOT NULL PRIMARY KEY IDENTITY(1,1),
employeeid varchar(100),
bagid varchar(10),
duration int
);

CREATE TABLE tblworklogs(
idx int NOT NULL PRIMARY KEY IDENTITY(1,1),
eventdatetime DATETIME2,
storeid varchar(100),
partnerid varchar(100),
bagid varchar(10),
employeeid varchar(100),
pipeid varchar(50)
);

CREATE TABLE tblbagevent(
idx int NOT NULL PRIMARY KEY IDENTITY(1,1),
eventdatetime DATETIME2,
storeid varchar(100),
partnerid varchar(100),
eventtype varchar(10),
bagid varchar(10),
employeeid varchar(100),
);

