-- phpMyAdmin SQL Dump
-- version 4.7.9
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Apr 29, 2019 at 01:02 AM
-- Server version: 5.7.21
-- PHP Version: 5.6.35

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `multiuser`
--

-- --------------------------------------------------------

--
-- Table structure for table `administrator`
--

DROP TABLE IF EXISTS `administrator`;
CREATE TABLE IF NOT EXISTS `administrator` (
  `SID` int(5) NOT NULL AUTO_INCREMENT,
  `Username` varchar(30) NOT NULL,
  `Password` varchar(30) NOT NULL,
  `Usertype` text NOT NULL,
  PRIMARY KEY (`SID`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `administrator`
--

INSERT INTO `administrator` (`SID`, `Username`, `Password`, `Usertype`) VALUES
(1, 'admin', 'password', 'Administrator');

-- --------------------------------------------------------

--
-- Table structure for table `attendance`
--

DROP TABLE IF EXISTS `attendance`;
CREATE TABLE IF NOT EXISTS `attendance` (
  `Username` varchar(30) NOT NULL,
  `Section` varchar(30) NOT NULL,
  `Course` varchar(30) NOT NULL,
  `Attendance` varchar(30) NOT NULL,
  `StartPeriodTime` varchar(30) NOT NULL,
  `EndPeriodTime` varchar(30) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `attendance`
--

INSERT INTO `attendance` (`Username`, `Section`, `Course`, `Attendance`, `StartPeriodTime`, `EndPeriodTime`) VALUES
('B15CS004', '4CSE-1', 'MT', 'Present', '2019-04-10 01:51 PM', '01:52 PM'),
('B15CS019', '4CSE-1', 'MT', 'Present', '2019-04-10 01:51 PM', '01:52 PM'),
('B15CS036', '4CSE-1', 'MT', 'Present', '2019-04-10 01:51 PM', '01:52 PM'),
('B15CS025', '4CSE-1', 'MT', 'Present', '2019-04-10 01:51 PM', '01:52 PM'),
('B15CS004', '4CSE-1', 'MT', 'Present', '2019-04-10 02:01 PM', '02:01 PM'),
('B15CS019', '4CSE-1', 'MT', 'Present', '2019-04-10 02:01 PM', '02:01 PM'),
('B15CS036', '4CSE-1', 'MT', 'Present', '2019-04-10 02:01 PM', '02:01 PM'),
('B15CS025', '4CSE-1', 'MT', 'Present', '2019-04-10 02:01 PM', '02:01 PM'),
('B15CS004', '4CSE-1', 'MT', 'Present', '2019-04-10 02:02 PM', '02:03 PM'),
('B15CS019', '4CSE-1', 'MT', 'Present', '2019-04-10 02:02 PM', '02:03 PM'),
('B15CS036', '4CSE-1', 'MT', 'Present', '2019-04-10 02:02 PM', '02:03 PM'),
('B15CS025', '4CSE-1', 'MT', 'Present', '2019-04-10 02:02 PM', '02:03 PM'),
('B15CS004', '4CSE-1', 'MT', 'Present', '2019-04-10 02:04 PM', '02:05 PM'),
('B15CS019', '4CSE-1', 'MT', 'Present', '2019-04-10 02:04 PM', '02:05 PM'),
('B15CS025', '4CSE-1', 'MT', 'Present', '2019-04-10 02:04 PM', '02:05 PM'),
('B15CS036', '4CSE-1', 'MT', 'Absent', '2019-04-10 02:04 PM', '02:05 PM'),
('B15CS004', '4CSE-1', 'MT', 'Present', '2019-04-10 02:09 PM', '02:10 PM'),
('B15CS025', '4CSE-1', 'MT', 'Present', '2019-04-10 02:09 PM', '02:10 PM'),
('B15CS019', '4CSE-1', 'MT', 'Absent', '2019-04-10 02:09 PM', '02:10 PM'),
('B15CS036', '4CSE-1', 'MT', 'Absent', '2019-04-10 02:09 PM', '02:10 PM'),
('B15CS019', '4CSE-1', 'MT', 'Present', '2019-04-10 02:11 PM', '02:13 PM'),
('B15CS036', '4CSE-1', 'MT', 'Present', '2019-04-10 02:11 PM', '02:13 PM'),
('B15CS025', '4CSE-1', 'MT', 'Present', '2019-04-10 02:11 PM', '02:13 PM'),
('B15CS004', '4CSE-1', 'MT', 'Absent', '2019-04-10 02:11 PM', '02:13 PM'),
('B15CS004', '4CSE-1', 'MT', 'Absent', '2019-04-10 02:14 PM', '02:15 PM'),
('B15CS019', '4CSE-1', 'MT', 'Absent', '2019-04-10 02:14 PM', '02:15 PM'),
('B15CS036', '4CSE-1', 'MT', 'Absent', '2019-04-10 02:14 PM', '02:15 PM'),
('B15CS025', '4CSE-1', 'MT', 'Absent', '2019-04-10 02:14 PM', '02:15 PM'),
('B15CS019', '4CSE-1', 'DBMS', 'Present', '2019-04-10 02:17 PM', '02:18 PM'),
('B15CS036', '4CSE-1', 'DBMS', 'Present', '2019-04-10 02:17 PM', '02:18 PM'),
('B15CS004', '4CSE-1', 'DBMS', 'Absent', '2019-04-10 02:17 PM', '02:18 PM'),
('B15CS025', '4CSE-1', 'DBMS', 'Absent', '2019-04-10 02:17 PM', '02:18 PM'),
('B15CS019', '4CSE-1', 'OS', 'Present', '2019-04-10 02:50 PM', '02:51 PM'),
('B15CS025', '4CSE-1', 'OS', 'Present', '2019-04-10 02:50 PM', '02:51 PM'),
('B15CS004', '4CSE-1', 'OS', 'Absent', '2019-04-10 02:50 PM', '02:51 PM'),
('B15CS036', '4CSE-1', 'OS', 'Absent', '2019-04-10 02:50 PM', '02:51 PM'),
('B15CS036', '4CSE-1', 'E-Commerce', 'Present', '2019-04-16 09:29 AM', '09:30 AM'),
('B15CS004', '4CSE-1', 'E-Commerce', 'Absent', '2019-04-16 09:29 AM', '09:30 AM'),
('B15CS019', '4CSE-1', 'E-Commerce', 'Absent', '2019-04-16 09:29 AM', '09:30 AM'),
('B15CS025', '4CSE-1', 'E-Commerce', 'Absent', '2019-04-16 09:29 AM', '09:30 AM'),
('B15CS036', '4CSE-1', 'STQA', 'Present', '2019-04-16 09:33 AM', '09:34 AM'),
('B15CS004', '4CSE-1', 'STQA', 'Absent', '2019-04-16 09:33 AM', '09:34 AM'),
('B15CS019', '4CSE-1', 'STQA', 'Absent', '2019-04-16 09:33 AM', '09:34 AM'),
('B15CS025', '4CSE-1', 'STQA', 'Absent', '2019-04-16 09:33 AM', '09:34 AM'),
('B15CS036', '4CSE-1', 'STQA', 'Present', '2019-04-28 03:49 PM', '03:50 PM'),
('B15CS004', '4CSE-1', 'STQA', 'Absent', '2019-04-28 03:49 PM', '03:50 PM'),
('B15CS019', '4CSE-1', 'STQA', 'Absent', '2019-04-28 03:49 PM', '03:50 PM'),
('B15CS025', '4CSE-1', 'STQA', 'Absent', '2019-04-28 03:49 PM', '03:50 PM'),
('B15CS036', '4CSE-1', 'STQA', 'Present', '2019-04-28 03:51 PM', '03:52 PM'),
('B15CS004', '4CSE-1', 'STQA', 'Absent', '2019-04-28 03:51 PM', '03:52 PM'),
('B15CS019', '4CSE-1', 'STQA', 'Absent', '2019-04-28 03:51 PM', '03:52 PM'),
('B15CS025', '4CSE-1', 'STQA', 'Absent', '2019-04-28 03:51 PM', '03:52 PM');

-- --------------------------------------------------------

--
-- Table structure for table `lecturer`
--

DROP TABLE IF EXISTS `lecturer`;
CREATE TABLE IF NOT EXISTS `lecturer` (
  `SID` int(5) NOT NULL AUTO_INCREMENT,
  `Usertype` varchar(30) NOT NULL,
  `Username` varchar(30) NOT NULL,
  `Fullname` varchar(30) NOT NULL,
  `Emailid` varchar(30) NOT NULL,
  `Mobilenumber` varchar(30) NOT NULL,
  `Password` varchar(30) NOT NULL,
  `AllottedCourse` varchar(30) NOT NULL,
  `AllottedSection` varchar(30) NOT NULL,
  PRIMARY KEY (`SID`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `lecturer`
--

INSERT INTO `lecturer` (`SID`, `Usertype`, `Username`, `Fullname`, `Emailid`, `Mobilenumber`, `Password`, `AllottedCourse`, `AllottedSection`) VALUES
(1, 'Lecturer', 'vijaykumar', 'P.Vijay Kumar', 'pvk@cse.kitsw.ac.in', '8897971827', 'vijaykumar123', 'E-Commerce', '4CSE-1'),
(2, 'Lecturer', 'vinaykumar', 'K.Vinay Kumar', 'kvk@cse.kits.ac.in', '9030070130', 'vinaykumar123', 'DBMS', '4CSE-1'),
(3, 'Lecturer', 'santhoshkumar', 'N.C.Santosh Kumar', 'ncs@cse.kitsw.ac.in', '9948838482', 'santhoshkumar123', 'STQA', '4CSE-1'),
(4, 'Lecturer', 'shankar', 'V. Shankar', 'vs@cse.kitsw.ac.in', '8008088344', 'shankar123', 'OS', '4CSE-1'),
(5, 'Lecturer', 'moeed', 'Syed Abdul Moeed', 'abdulmoeed.cse@kitsw.org', '9652428472', 'moeed123', 'BDM', '4CSE-1'),
(6, 'Lecturer', 'phridviraj', 'M.S.B.Phridviraj', 'msbp@cse.kitsw.ac.in', '9866576521', 'phridviraj123', 'MT', '4CSE-1'),
(7, 'Lecturer', 'chandrashekhar', 'V.Chandra Shekhar Rao', 'csr@cse.kitsw.ac.in', '9052452294', 'chandrashekhar123', 'DAA', '4CSE-1');

-- --------------------------------------------------------

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
CREATE TABLE IF NOT EXISTS `student` (
  `Usertype` varchar(30) NOT NULL,
  `Username` varchar(30) NOT NULL,
  `Section` varchar(30) NOT NULL,
  `Fullname` varchar(30) NOT NULL,
  `Emailid` varchar(30) NOT NULL,
  `ParentsEmailid` varchar(30) NOT NULL,
  `Mobilenumber` varchar(30) NOT NULL,
  `Password` varchar(30) NOT NULL,
  `Course` varchar(30) NOT NULL,
  `Attendance` varchar(10) NOT NULL,
  `DateandTime` varchar(30) NOT NULL,
  `AttPercentage` varchar(10) NOT NULL,
  PRIMARY KEY (`Username`),
  UNIQUE KEY `Username` (`Username`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `student`
--

INSERT INTO `student` (`Usertype`, `Username`, `Section`, `Fullname`, `Emailid`, `ParentsEmailid`, `Mobilenumber`, `Password`, `Course`, `Attendance`, `DateandTime`, `AttPercentage`) VALUES
('Student', 'B15CS004', '4CSE-1', 'Ajay Rao Polsani', 'ajaypolsani85@gmail.com', 'ajaypolsani85@gmail.com', '7731830383', 'ajay123', 'STQA', 'Absent', '2019-04-28 03:51 PM', '38.5%'),
('Student', 'B15CS019', '4CSE-1', 'Sri Lakshmi Hanuma Akula', 'anumailboxe@gmail.com', 'anumailboxe@gmail.com', '8639800265', 'anusree123', 'STQA', 'Absent', '2019-04-28 03:51 PM', '53.8%'),
('Student', 'B15CS036', '4CSE-1', 'Vishal Reddy Pachika', 'pachikavishalreddy@gmail.com', 'pachikavishalreddy@gmail.com', '7386559954', 'vishal123', 'STQA', 'Present', '2019-04-28 03:51 PM', '69.2%'),
('Student', 'B15CS025', '4CSE-1', 'Sai Charan Vudugula', 'charan.vudugula1996@gmail.com', 'charan.vudugula1996@gmail.com', '8886668555', 'charan123', 'STQA', 'Absent', '2019-04-28 03:51 PM', '53.8%');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
