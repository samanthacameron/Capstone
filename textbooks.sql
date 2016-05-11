
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE IF NOT EXISTS `capstone` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `capstone`;


CREATE TABLE IF NOT EXISTS `school` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `grade` varchar(50),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=94 DEFAULT CHARSET=utf8;



CREATE TABLE IF NOT EXISTS `student` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) ,
  `first` varchar(50),
  `last` varchar(50),
  `student_id` varchar(50) ,
  `email` varchar(50) ,
  `school_id` int(11) DEFAULT NULL,
  `courses` varchar(1000) ,
  PRIMARY KEY (`id`),
  KEY `FK_school_id` (`school_id`),
  CONSTRAINT `FK_school_id` FOREIGN KEY (`school_id`) REFERENCES `school` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


  

CREATE TABLE IF NOT EXISTS `teacher` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) ,
  `first` varchar(50) ,
  `last` varchar(50) ,
  `email` varchar(50) ,
  `teacher_id` varchar(50) ,
  `school_id` int(11) DEFAULT NULL,
  `courses` varchar(1000) ,
  PRIMARY KEY (`id`),
  KEY `FK_school_id_teach` (`school_id`),
  CONSTRAINT `FK_school_id_teach` FOREIGN KEY (`school_id`) REFERENCES `school` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



CREATE TABLE IF NOT EXISTS `textbook` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `isbn` varchar(50) NOT NULL,
  `title` varchar(50) ,
  `author` varchar(50) ,
  `edition` varchar(50) ,
  `school_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_school_id_text` (`school_id`),
  CONSTRAINT `FK_school_id_text` FOREIGN KEY (`school_id`) REFERENCES `school` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `courses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `subject` varchar(50) ,
  `number` varchar(50) ,
  `name` varchar(50) ,
  `des` varchar(500) DEFAULT NULL,
  `school_id` int(11) DEFAULT NULL,
  `textbook_id` int(11) DEFAULT NULL,
  `teacher_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_text_id` (`textbook_id`),
  CONSTRAINT `FK_text_id` FOREIGN KEY (`textbook_id`) REFERENCES `textbook` (`id`),
  KEY `FK_teach_id` (`teacher_id`),
  CONSTRAINT `FK_teach_id` FOREIGN KEY (`teacher_id`) REFERENCES `teacher` (`id`),
  KEY `FK_school_id_course` (`school_id`),
  CONSTRAINT `FK_school_id_course` FOREIGN KEY (`school_id`) REFERENCES `school` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
  

