-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 19, 2025 at 04:40 PM
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
-- Database: `pos_system`
--

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `price` decimal(10,2) NOT NULL CHECK (`price` >= 0),
  `stock` int(11) NOT NULL CHECK (`stock` >= 0),
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `name`, `price`, `stock`, `created_at`, `updated_at`) VALUES
(1, 'Intel Core i9-14900K CPU', 32999.00, 10, '2025-12-17 22:23:56', '2025-12-19 06:22:23'),
(2, 'AMD Ryzen 9 7950X CPU', 30999.00, 4, '2025-12-17 22:23:56', '2025-12-18 11:24:44'),
(3, 'NVIDIA RTX 4090 GPU', 89999.00, 0, '2025-12-17 22:23:56', '2025-12-18 11:20:32'),
(4, 'AMD RX 7900 XTX GPU', 50999.00, 5, '2025-12-17 22:23:56', '2025-12-18 11:19:09'),
(5, 'Corsair Vengeance 32GB DDR5 RAM', 7299.00, 9, '2025-12-17 22:23:56', '2025-12-19 02:08:06'),
(6, 'G.Skill Trident Z5 64GB DDR5 RAM', 14099.00, 16, '2025-12-17 22:23:56', '2025-12-18 11:24:44'),
(7, 'ASUS ROG Strix Z790 Motherboard', 25399.00, 5, '2025-12-17 22:23:56', '2025-12-19 02:09:21'),
(8, 'MSI MAG B650 Motherboard', 11299.00, 10, '2025-12-17 22:23:56', '2025-12-19 02:07:44'),
(10, 'EVGA SuperNOVA 850W PSU', 7349.00, 11, '2025-12-17 22:23:56', '2025-12-19 06:25:02'),
(11, 'NZXT H7 Flow PC Case', 7349.00, 3, '2025-12-17 22:23:56', '2025-12-19 06:47:43'),
(12, 'Lian Li O11 Dynamic PC Case', 9049.00, 4, '2025-12-17 22:23:56', '2025-12-19 02:07:56'),
(13, 'MSi MAG A50', 1499.00, 22, '2025-12-17 22:23:56', '2025-12-19 06:47:43');

-- --------------------------------------------------------

--
-- Table structure for table `system_settings`
--

CREATE TABLE `system_settings` (
  `setting_key` varchar(50) NOT NULL,
  `setting_value` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `system_settings`
--

INSERT INTO `system_settings` (`setting_key`, `setting_value`) VALUES
('next_order_id', '6'),
('next_product_id', '14');

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE `transactions` (
  `id` int(11) NOT NULL,
  `order_id` varchar(20) NOT NULL,
  `staff_name` varchar(50) NOT NULL,
  `total_amount` decimal(10,2) NOT NULL CHECK (`total_amount` >= 0),
  `date` varchar(50) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `transactions`
--

INSERT INTO `transactions` (`id`, `order_id`, `staff_name`, `total_amount`, `date`, `created_at`) VALUES
(1, 'OR0001', 'admin', 14648.00, '2025-12-16 04:55:00', '2025-12-17 22:23:56'),
(2, 'OR0002', 'John', 31046.00, '2025-12-16 04:55:00', '2025-12-17 22:23:56'),
(3, 'OR0003', 'admin', 156995.00, '2025-12-17 17:56:00', '2025-12-17 22:23:56'),
(16, 'OR0004', 'admin', 32999.00, '12-19-2025 02:22 PM', '2025-12-19 06:22:23'),
(17, 'OR0005', 'John', 41594.00, '12-19-2025 02:25 PM', '2025-12-19 06:25:02'),
(18, 'OR0006', 'admin', 8868.00, '12-19-2025 02:47 PM', '2025-12-19 06:47:43');

-- --------------------------------------------------------

--
-- Table structure for table `transaction_items`
--

CREATE TABLE `transaction_items` (
  `id` int(11) NOT NULL,
  `transaction_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `product_name` varchar(255) NOT NULL,
  `quantity` int(11) NOT NULL CHECK (`quantity` > 0),
  `price` decimal(10,2) NOT NULL CHECK (`price` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `transaction_items`
--

INSERT INTO `transaction_items` (`id`, `transaction_id`, `product_id`, `product_name`, `quantity`, `price`) VALUES
(1, 1, 5, 'Corsair Vengeance 32GB DDR5 RAM', 1, 7299.00),
(2, 1, 10, 'EVGA SuperNOVA 850W PSU', 1, 7349.00),
(3, 2, 5, 'Corsair Vengeance 32GB DDR5 RAM', 1, 7299.00),
(4, 2, 12, 'Lian Li O11 Dynamic PC Case', 1, 9049.00),
(5, 2, 10, 'EVGA SuperNOVA 850W PSU', 2, 7349.00),
(6, 3, 1, 'Intel Core i9-14900K CPU', 1, 32999.00),
(7, 3, 2, 'AMD Ryzen 9 7950X CPU', 4, 30999.00),
(42, 16, 1, 'Intel Core i9-14900K CPU', 1, 32999.00),
(43, 17, 0, 'Mouse a4tech', 1, 500.00),
(44, 17, 9, 'Corsair RM1000e 1000W PSU', 1, 10199.00),
(45, 17, 11, 'NZXT H7 Flow PC Case', 1, 7349.00),
(46, 17, 10, 'EVGA SuperNOVA 850W PSU', 3, 7349.00),
(47, 17, 13, 'MSi MAG A50', 1, 1499.00),
(48, 18, 13, 'MSi MAG A50', 1, 1499.00),
(49, 18, 11, 'NZXT H7 Flow PC Case', 1, 7349.00),
(50, 18, 0, 'Tinapa', 1, 20.00);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('admin','staff') NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `role`, `created_at`) VALUES
(1, 'admin', 'admin123', 'admin', '2025-12-17 22:23:56'),
(2, 'Kervy', 'K3rv6747', 'admin', '2025-12-17 22:23:56'),
(4, 'Maria', 'Maria123', 'staff', '2025-12-17 22:23:56'),
(5, 'John ', 'John123 ', 'staff', '2025-12-18 11:22:26');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `system_settings`
--
ALTER TABLE `system_settings`
  ADD PRIMARY KEY (`setting_key`);

--
-- Indexes for table `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `order_id` (`order_id`),
  ADD KEY `idx_order_id` (`order_id`),
  ADD KEY `idx_staff_name` (`staff_name`);

--
-- Indexes for table `transaction_items`
--
ALTER TABLE `transaction_items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_transaction_id` (`transaction_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `transactions`
--
ALTER TABLE `transactions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `transaction_items`
--
ALTER TABLE `transaction_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `transaction_items`
--
ALTER TABLE `transaction_items`
  ADD CONSTRAINT `transaction_items_ibfk_1` FOREIGN KEY (`transaction_id`) REFERENCES `transactions` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
