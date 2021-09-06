CREATE DATABASE mttDatabase
USE mttDatabase
CREATE TABLE Student (
  SID int PRIMARY KEY,
  Name varchar(50),
  Surname varchar(50),
  Email NVARCHAR(350),
  Password NVARCHAR(500)
);

CREATE TABLE Notes (
  NoteId int PRIMARY KEY IDENTITY(1,1),
  CourseId varchar(255),
  Date datetime,
  Content NVARCHAR(MAX),
  SID int,
  Course_Id int
);

CREATE TABLE Courses (
  ID int PRIMARY KEY IDENTITY(1,1),
  Course_Id NVARCHAR(50),
  name NVARCHAR(50),
  Course_Time_Day varchar(25),
  Course_Time_StartHour time,
  Course_Time_EndHour time,
  CourseLink varchar(MAX),
  Resource_Link varchar(MAX),
  Professor_Email NVARCHAR(350),
  Ta_Email NVARCHAR(350),
  SID int
);

CREATE TABLE Event (
  EventId int PRIMARY KEY IDENTITY(1,1),
  start_date datetime,
  end_date datetime,
  Name NVARCHAR(150),
  Description varchar(450),
  SID int,
);

ALTER TABLE Notes ADD FOREIGN KEY (SID) REFERENCES Student (SID);

ALTER TABLE Notes ADD FOREIGN KEY (Course_Id) REFERENCES Courses (ID);

ALTER TABLE Courses ADD FOREIGN KEY (SID) REFERENCES Student (SID);

ALTER TABLE Event ADD FOREIGN KEY (SID) REFERENCES Student (SID);

ALTER TABLE Event ADD FOREIGN KEY (Course_Id) REFERENCES Courses (ID);