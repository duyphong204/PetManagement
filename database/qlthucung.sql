-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 11, 2025 at 01:41 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `qlthucung`
--

-- --------------------------------------------------------

--
-- Table structure for table `bac_si`
--

CREATE TABLE `bac_si` (
  `id` int(11) NOT NULL,
  `ho_ten` varchar(100) NOT NULL,
  `chuyen_mon` varchar(100) DEFAULT NULL,
  `so_dien_thoai` varchar(15) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `id_nguoi_dung` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `chu_so_huu`
--

CREATE TABLE `chu_so_huu` (
  `id` int(11) NOT NULL,
  `ho_ten` varchar(100) NOT NULL,
  `so_dien_thoai` varchar(15) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `dia_chi` text NOT NULL,
  `id_nguoi_dung` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `chu_so_huu`
--

INSERT INTO `chu_so_huu` (`id`, `ho_ten`, `so_dien_thoai`, `email`, `dia_chi`, `id_nguoi_dung`) VALUES
(4, 'Nguyễn Văn A', '0987654321', 'nguyenvana@example.com', 'Hà Nội', 3),
(5, 'Trần Thị B', '0978123456', 'tranthib@example.com', 'TP. Hồ Chí Minh', 4);

-- --------------------------------------------------------

--
-- Table structure for table `dieu_tri`
--

CREATE TABLE `dieu_tri` (
  `id` int(11) NOT NULL,
  `id_thu_cung` int(11) NOT NULL,
  `id_bac_si` int(11) NOT NULL,
  `ngay_dieu_tri` date NOT NULL,
  `chan_doan` text NOT NULL,
  `don_thuoc` text NOT NULL,
  `chi_phi` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `hoa_don`
--

CREATE TABLE `hoa_don` (
  `id` int(11) NOT NULL,
  `id_chu_so_huu` int(11) NOT NULL,
  `ngay_tao` date NOT NULL DEFAULT curdate(),
  `tong_tien` decimal(10,2) NOT NULL,
  `trang_thai` enum('Chưa thanh toán','Đã thanh toán') DEFAULT 'Chưa thanh toán'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `lich_hen`
--

CREATE TABLE `lich_hen` (
  `id` int(11) NOT NULL,
  `ngay_hen` date NOT NULL,
  `gio_hen` time NOT NULL,
  `id_thu_cung` int(11) NOT NULL,
  `id_bac_si` int(11) NOT NULL,
  `trang_thai` enum('Chờ xác nhận','Đã xác nhận','Đã hoàn thành','Đã hủy') DEFAULT 'Chờ xác nhận'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `nguoi_dung`
--

CREATE TABLE `nguoi_dung` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  `role` enum('admin','bac_si','khach_hang') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `nguoi_dung`
--

INSERT INTO `nguoi_dung` (`id`, `username`, `password`, `email`, `role`) VALUES
(1, 'admin123', '12345', 'admin@example.com', 'admin'),
(2, 'bacsi01', '12345', 'bacsi@example.com', 'bac_si'),
(3, 'user01', '12345', 'user01@example.com', ''),
(4, 'user02', '12345', 'user02@example.com', '');

-- --------------------------------------------------------

--
-- Table structure for table `thu_cung`
--

CREATE TABLE `thu_cung` (
  `id` int(11) NOT NULL,
  `ten` varchar(50) NOT NULL,
  `loai` varchar(50) NOT NULL,
  `tuoi` int(11) DEFAULT NULL CHECK (`tuoi` >= 0),
  `gioi_tinh` enum('Đực','Cái') NOT NULL,
  `id_chu_so_huu` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `thu_cung`
--

INSERT INTO `thu_cung` (`id`, `ten`, `loai`, `tuoi`, `gioi_tinh`, `id_chu_so_huu`) VALUES
(4, 'Lucky', 'Chó Poodle', 2, 'Đực', 4),
(5, 'Mimi', 'Mèo Ba Tư', 3, 'Cái', 5),
(6, 'Rocky', 'Chó Corgi', 1, 'Đực', 4),
(12, 'puleeet', 'chó ấn độ', 12, 'Đực', 4);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bac_si`
--
ALTER TABLE `bac_si`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `so_dien_thoai` (`so_dien_thoai`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `id_nguoi_dung` (`id_nguoi_dung`);

--
-- Indexes for table `chu_so_huu`
--
ALTER TABLE `chu_so_huu`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `so_dien_thoai` (`so_dien_thoai`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `id_nguoi_dung` (`id_nguoi_dung`);

--
-- Indexes for table `dieu_tri`
--
ALTER TABLE `dieu_tri`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_thu_cung` (`id_thu_cung`),
  ADD KEY `id_bac_si` (`id_bac_si`);

--
-- Indexes for table `hoa_don`
--
ALTER TABLE `hoa_don`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_chu_so_huu` (`id_chu_so_huu`);

--
-- Indexes for table `lich_hen`
--
ALTER TABLE `lich_hen`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_thu_cung` (`id_thu_cung`),
  ADD KEY `id_bac_si` (`id_bac_si`);

--
-- Indexes for table `nguoi_dung`
--
ALTER TABLE `nguoi_dung`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `thu_cung`
--
ALTER TABLE `thu_cung`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_chu_so_huu` (`id_chu_so_huu`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `bac_si`
--
ALTER TABLE `bac_si`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `chu_so_huu`
--
ALTER TABLE `chu_so_huu`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `dieu_tri`
--
ALTER TABLE `dieu_tri`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `hoa_don`
--
ALTER TABLE `hoa_don`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `lich_hen`
--
ALTER TABLE `lich_hen`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `nguoi_dung`
--
ALTER TABLE `nguoi_dung`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `thu_cung`
--
ALTER TABLE `thu_cung`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `bac_si`
--
ALTER TABLE `bac_si`
  ADD CONSTRAINT `bac_si_ibfk_1` FOREIGN KEY (`id_nguoi_dung`) REFERENCES `nguoi_dung` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `chu_so_huu`
--
ALTER TABLE `chu_so_huu`
  ADD CONSTRAINT `chu_so_huu_ibfk_1` FOREIGN KEY (`id_nguoi_dung`) REFERENCES `nguoi_dung` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `dieu_tri`
--
ALTER TABLE `dieu_tri`
  ADD CONSTRAINT `dieu_tri_ibfk_1` FOREIGN KEY (`id_thu_cung`) REFERENCES `thu_cung` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `dieu_tri_ibfk_2` FOREIGN KEY (`id_bac_si`) REFERENCES `bac_si` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `hoa_don`
--
ALTER TABLE `hoa_don`
  ADD CONSTRAINT `hoa_don_ibfk_1` FOREIGN KEY (`id_chu_so_huu`) REFERENCES `chu_so_huu` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `lich_hen`
--
ALTER TABLE `lich_hen`
  ADD CONSTRAINT `lich_hen_ibfk_1` FOREIGN KEY (`id_thu_cung`) REFERENCES `thu_cung` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `lich_hen_ibfk_2` FOREIGN KEY (`id_bac_si`) REFERENCES `bac_si` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `thu_cung`
--
ALTER TABLE `thu_cung`
  ADD CONSTRAINT `thu_cung_ibfk_1` FOREIGN KEY (`id_chu_so_huu`) REFERENCES `chu_so_huu` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
