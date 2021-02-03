-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 19, 2020 at 09:08 PM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.4.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `recipes`
--

-- --------------------------------------------------------

--
-- Table structure for table `celebration_calendar`
--

CREATE TABLE `celebration_calendar` (
  `Date` date NOT NULL,
  `Celebration` varchar(100) NOT NULL,
  `Message` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `celebration_calendar`
--

INSERT INTO `celebration_calendar` (`Date`, `Celebration`, `Message`) VALUES
('2020-02-24', 'pancake', 'Tomorrow it\'s Pancake Day!'),
('2020-02-25', 'pancake', 'It\'s Pancake Day!'),
('2020-03-01', 'st david', 'Happy St David\'s Day!'),
('2020-03-02', 'spring', 'It\'s the Spring!'),
('2020-03-03', 'spring', 'It\'s the Spring!'),
('2020-03-04', 'spring', 'It\'s the Spring!'),
('2020-03-05', 'spring', 'It\'s the Spring!'),
('2020-03-17', 'st patrick', 'Happy St. Patrick\'s Day!'),
('2020-04-08', 'passover', 'It\'s the first day of Passover!'),
('2020-04-09', 'easter', '3 day \'till Easter!'),
('2020-04-10', 'easter', '2 day \'till Easter!'),
('2020-04-11', 'easter', '1 day \'till Easter!'),
('2020-04-12', 'easter', 'Happy Easter!'),
('2020-04-13', 'baisakhi', 'Happy Baisant!'),
('2020-04-14', 'baisakhi', 'Happy Baisant!'),
('2020-04-15', 'passover', 'It\'s the 8th day of Passover!'),
('2020-04-16', 'passover', 'It\'s the last day of Passover, still time to celebrate'),
('2020-04-23', 'st george', 'Happy St Georges Day!'),
('2020-05-24', 'eid', 'Evening of Eid al-Fitr '),
('2020-05-25', 'eid', 'Eid al-Fitr Celebration!'),
('2020-06-01', 'summer', 'It\'s the First Day of Summer!'),
('2020-09-01', 'autumn', 'It\'s the First Day of Autumn!'),
('2020-10-31', 'halloween', 'Have a spooky Halloween!'),
('2020-11-05', 'bonfire', 'Remember, remember the 5th of November!'),
('2020-11-14', 'diwali', 'HAPPY DIWALI!'),
('2020-11-26', 'thanksgiving', 'Thanksgiving!'),
('2020-12-01', 'winter', 'It\'s  the first day of winter!'),
('2020-12-10', 'hanukkah', 'Happy 1st Day of Hanukkah!'),
('2020-12-11', 'hanukkah', 'Happy 2st Day of Hanukkah!'),
('2020-12-12', 'hanukkah', 'Happy 3st Day of Hanukkah!'),
('2020-12-13', 'hanukkah', 'Happy 4th Day of Hanukkah!'),
('2020-12-14', 'hanukkah', 'Happy 5th Day of Hanukkah!'),
('2020-12-15', 'hanukkah', 'Happy 4th Day of Hanukkah!'),
('2020-12-16', 'hanukkah', 'Happy 5th Day of Hanukkah!'),
('2020-12-17', 'hanukkah', 'Happy 4th Day of Hanukkah!'),
('2020-12-18', 'hanukkah', 'Happy 5th Day of Hanukkah!'),
('2020-12-19', 'christmas', '6 days \'till Christmas'),
('2020-12-20', 'christmas', '5 days \'till Christmas'),
('2020-12-21', 'christmas', '4 days \'till Christmas'),
('2020-12-22', 'christmas', '3 days \'till Christmas'),
('2020-12-23', 'christmas', '2 days \'till Christmas'),
('2020-12-24', 'christmas', 'It\'s Christmas Eve!'),
('2020-12-25', 'christmas', 'Ho Ho Ho! Merry Christmas'),
('2020-12-26', 'boxing', 'Happy Boxing Day'),
('2020-12-31', 'new year', 'Happy NYE!!!'),
('2021-01-25', 'burns', 'Have a wonderful Burn\'s Night!'),
('2021-02-14', 'valentines', 'All the Valentine\'s specials <3');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
