-- Creates the database
DROP DATABASE IF EXISTS oois_assignment;
CREATE DATABASE oois_assignment;

-- Uses the database
USE oois_assignment;

-- Creates tables
CREATE TABLE IF NOT EXISTS blacklist_tokens (
    `id` INTEGER UNSIGNED NOT NULL auto_increment,
    `token` VARCHAR(500) UNIQUE NOT NULL,
    `blacklisted_on` DATETIME NOt NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
) AUTO_INCREMENT = 1;

CREATE TABLE IF NOT EXISTS user (
    `id` INTEGER UNSIGNED NOT NULL auto_increment,
    `email` VARCHAR(255) UNIQUE NOT NULL,
    `password_hash` VARCHAR(100),
    `name` VARCHAR(255) UNIQUE NOT NULL,
    `employee_number` VARCHAR(255) UNIQUE NOT NULL,
    `position` CHAR(1) NOT NULL DEFAULT 's',
    `admin` BIT NOT NULL DEFAULT 0,
    `registered_on` DATETIME NOt NULL DEFAULT CURRENT_TIMESTAMP,
    `public_id` VARCHAR(100) UNIQUE NOT NULL,
    PRIMARY KEY (id)
) AUTO_INCREMENT = 1;

CREATE TABLE IF NOT EXISTS patient (
    `id` INTEGER UNSIGNED NOT NULL auto_increment,
    `name` VARCHAR(255) UNIQUE NOT NULL,
    `address` VARCHAR(255) UNIQUE NOT NULL,
    `phone` VARCHAR(255) UNIQUE NOT NULL,
    `registered_on` DATETIME NOt NULL DEFAULT CURRENT_TIMESTAMP,
    `public_id` VARCHAR(100) UNIQUE NOT NULL,
    PRIMARY KEY (id)
) AUTO_INCREMENT = 1;

CREATE TABLE IF NOt EXISTS prescription (
    `id` INTEGER UNSIGNED NOT NULL auto_increment,
    `type` CHAR(1) NOT NULL DEFAULT 's',
    `patient_id` VARCHAR(255) NOT NULL,
    `doctor_id` VARCHAR(255) NOT NULL,
    `quantity` INT(4) NOT NULL DEFAULT 0,
    `dosage` VARCHAR(255) NOT NULL,
    `created_on` DATETIME NOt NULL DEFAULT CURRENT_TIMESTAMP,
    `public_id` VARCHAR(100) UNIQUE NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patient (public_id),
    FOREIGN KEY (doctor_id) REFERENCES user (public_id),
    PRIMARY KEY (id)
) AUTO_INCREMENT = 1;

CREATE TABLE IF NOT EXISTS appointment (
    `id` INT(10) UNSIGNED NOT NULL auto_increment,
    `type` CHAR(1) NOT NULL DEFAULT 's',
    `status` INT(1) NOT NULL DEFAULT 1,
    `healthcare_professional_id` VARCHAR(100) NOT NULL,
    `patient_id` VARCHAR(100) NOT NULL,
    `start_time` DATETIME NOT NULL,
    `end_time` DATETIME NOT NULL,
    `booked_on` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `public_id` VARCHAR(100) UNIQUE NOT NULL,
    FOREIGN KEY (healthcare_professional_id) REFERENCES user (public_id),
    FOREIGN KEY (patient_id) REFERENCES patient (public_id),
    PRIMARY KEY (id)
) AUTO_INCREMENT = 1;

-- Inserts data sets
INSERT INTO user (`email`, `password_hash`, `name`, `employee_number`, `position`, `admin`, `public_id`) VALUES (
    "kris.lai@gmail.com",
    "$2b$12$AU.l1xYhqvHgZnsng62fGu.qJtRyvZSvIxNO5mDIahVyf70bs6i3e",
    "Kris, Lai",
    "sf001",
    "r", -- receptionist
    1,
    "f487d4e8-cbbb-4833-89a0-9b9d28f5d06e"
);
INSERT INTO user (`email`, `password_hash`, `name`, `employee_number`, `position`, `admin`, `public_id`) VALUES (
    "kenny.law@gmail.com",
    "$2b$12$AU.l1xYhqvHgZnsng62fGu.qJtRyvZSvIxNO5mDIahVyf70bs6i3e",
    "Kenny, Law",
    "sf002",
    "d", -- doctor
    0,
    "00de28e7-73f9-4099-9edc-7d2f3902d7ba"
);
INSERT INTO user (`email`, `password_hash`, `name`, `employee_number`, `position`, `admin`, `public_id`) VALUES (
    "james.lam@gmail.com",
    "$2b$12$AU.l1xYhqvHgZnsng62fGu.qJtRyvZSvIxNO5mDIahVyf70bs6i3e",
    "James, Lam",
    "sf003",
    "n", -- nurse
    0,
    "67efe526-0bd0-43b9-8d0c-63ff104fcefa"
);

INSERT INTO patient (`name`, `address`, `phone`, `public_id`) VALUES (
    "Felix, Lee",
    "Unit A, ABC House",
    "852-98761234",
    "32cb0bb5-9fa7-49b0-9df2-e30698124af7"
);
INSERT INTO patient (`name`, `address`, `phone`, `public_id`) VALUES (
    "Peter, Chan",
    "Unit D, EFG House",
    "852-54326789",
    "dad6a212-51e2-4b67-9f95-9c9424500863"
);

INSERT INTO appointment (`healthcare_professional_id`, `patient_id`, `start_time`, `end_time`, `public_id`) VALUES (
    "00de28e7-73f9-4099-9edc-7d2f3902d7ba",
    "32cb0bb5-9fa7-49b0-9df2-e30698124af7",
    "2022-02-01 09:00:00",
    "2022-02-01 10:00:00",
    "b8f74dc8-1b06-40fc-a086-f85d220bf00b"
);

INSERT INTO appointment (`healthcare_professional_id`, `patient_id`, `start_time`, `end_time`, `public_id`) VALUES (
    "67efe526-0bd0-43b9-8d0c-63ff104fcefa",
    "32cb0bb5-9fa7-49b0-9df2-e30698124af7",
    "2022-02-01 11:00:00",
    "2022-02-01 12:00:00",
    "5a08be2e-269d-42cf-8867-bee3b20ced90"
);

INSERT INTO prescription (`type`, `patient_id`, `doctor_id`, `quantity`, `dosage`, `public_id`) VALUES (
    "s", -- standard
    "dad6a212-51e2-4b67-9f95-9c9424500863",
    "00de28e7-73f9-4099-9edc-7d2f3902d7ba",
    1,
    "Takes 1 per 4 hours",
    "fabe3b29-40c7-4a08-9254-a5dc707b3d81"
);
