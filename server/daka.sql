-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- 主机： localhost
-- 生成日期： 2020-06-12 15:52:47
-- 服务器版本： 5.5.62-log
-- PHP 版本： 7.3.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 数据库： `daka`
--

-- --------------------------------------------------------

--
-- 表的结构 `log`
--

CREATE TABLE `log` (
  `id` int(11) NOT NULL,
  `uid` int(11) NOT NULL,
  `temp` decimal(3,1) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `log`
--

INSERT INTO `log` (`id`, `uid`, `temp`, `time`) VALUES
(1, 3, '36.5', '2020-06-07 18:34:49'),
(2, 1, '36.5', '2020-06-08 02:24:43'),
(3, 1, '36.5', '2020-06-12 05:32:30'),
(4, 3, '36.5', '2020-06-12 05:33:10'),
(5, 2, '36.5', '2020-06-12 06:58:11'),
(6, 2, '37.2', '2020-06-12 07:16:06'),
(7, 2, '37.4', '2020-06-12 07:17:50'),
(8, 2, '36.1', '2020-06-12 07:23:07'),
(9, 2, '35.6', '2020-06-12 07:26:52'),
(10, 1, '36.9', '2020-06-12 07:29:05'),
(11, 2, '36.0', '2020-06-12 07:33:16'),
(12, 1, '35.2', '2020-06-12 07:42:57'),
(13, 1, '37.2', '2020-06-12 07:43:25');

-- --------------------------------------------------------

--
-- 表的结构 `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(16) NOT NULL,
  `url` varchar(255) NOT NULL,
  `status` enum('safety','warning') NOT NULL,
  `lasttime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `disabled` enum('true','false') NOT NULL DEFAULT 'false'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `user`
--

INSERT INTO `user` (`id`, `username`, `url`, `status`, `lasttime`, `disabled`) VALUES
(1, 'xiaoxie', 'http://domain.com/daka/faces/1.jpg', 'safety', '2020-06-12 07:43:25', 'false'),
(2, 'xiaomai', 'http://domain.com/daka/faces/2.jpg', 'safety', '2020-06-12 07:33:16', 'false'),
(3, 'xiaoliao', 'http://domain.com/daka/faces/3.jpg', 'safety', '2020-06-11 05:43:16', 'true');

--
-- 转储表的索引
--

--
-- 表的索引 `log`
--
ALTER TABLE `log`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `log`
--
ALTER TABLE `log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- 使用表AUTO_INCREMENT `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
