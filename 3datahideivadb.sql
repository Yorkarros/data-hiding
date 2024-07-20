-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Feb 22, 2024 at 02:24 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `2datahideivadb`
--

-- --------------------------------------------------------

--
-- Table structure for table `msgtb`
--

CREATE TABLE `msgtb` (
  `id` bigint(10) NOT NULL auto_increment,
  `SenderName` varchar(250) NOT NULL,
  `ReceiverName` varchar(250) NOT NULL,
  `Email` varchar(250) NOT NULL,
  `ImageName` varchar(250) NOT NULL,
  `Hidekey` varchar(250) NOT NULL,
  `Type` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=5 ;

--
-- Dumping data for table `msgtb`
--

INSERT INTO `msgtb` (`id`, `SenderName`, `ReceiverName`, `Email`, `ImageName`, `Hidekey`, `Type`) VALUES
(1, 'san', 'sangeeth', 'sangeeth5535@gmail.com', '1675.png', '1234', 'image'),
(2, 'san', 'sangeeth', 'sangeeth5535@gmail.com', '8723.png', '1234', 'image'),
(3, 'san', 'sangeeth', 'sangeeth5535@gmail.com', '8232.png', '1234', 'image'),
(4, 'san', 'sangeeth', 'sangeeth5535@gmail.com', '2515alert.wav', '1234', 'Audio');

-- --------------------------------------------------------

--
-- Table structure for table `recivertb`
--

CREATE TABLE `recivertb` (
  `id` bigint(10) NOT NULL auto_increment,
  `Name` varchar(250) NOT NULL,
  `Mobile` varchar(250) NOT NULL,
  `EmailId` varchar(250) NOT NULL,
  `Address` varchar(500) NOT NULL,
  `UserName` varchar(250) NOT NULL,
  `Password` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `recivertb`
--

INSERT INTO `recivertb` (`id`, `Name`, `Mobile`, `EmailId`, `Address`, `UserName`, `Password`) VALUES
(1, 'san', '9486365535', 'sangeeth5535@gmail.com', 'no 6 trichy', 'sangeeth', 'sangeeth');

-- --------------------------------------------------------

--
-- Table structure for table `sendertb`
--

CREATE TABLE `sendertb` (
  `id` bigint(10) NOT NULL auto_increment,
  `Name` varchar(250) NOT NULL,
  `Mobile` varchar(250) NOT NULL,
  `EmailId` varchar(250) NOT NULL,
  `Address` varchar(500) NOT NULL,
  `UserName` varchar(250) NOT NULL,
  `Password` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `sendertb`
--

INSERT INTO `sendertb` (`id`, `Name`, `Mobile`, `EmailId`, `Address`, `UserName`, `Password`) VALUES
(1, 'san', '9486365535', 'sangeeth5535@gmail.com', 'No 16, Samnath Plaza, Madurai Main Road, Melapudhur', 'san', 'san');
