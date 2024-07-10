-- insert role data
INSERT INTO roles (role_id, role_name) VALUES
(1, 'member'),
(2, 'trainer'),
(3, 'manager');

-- Add userdata
INSERT INTO users(id, username, password_hash, email, role_id, status) VALUES
(1, 'member1', 'pbkdf2:sha256:600000$QQsrQcOR$911ec057b561c91fab46b8d9ff56a68611c0a10ac8bd811464d83b4aadb20cfc', 'member1@gmail.com', 1, 1),
(2, 'member2', 'pbkdf2:sha256:600000$BWGIfDQi$39f02448fe2e99aaafbd90d0c2172674094db4010cec5ebc25ca374e33cf0d0c', 'member2@gmail.com', 1, 1),
(3, 'member3', 'pbkdf2:sha256:600000$mWyKucui$2384522e827a6c7d354074bcb65eabef9bc7e982293d29dfd16bd2bba3730204', 'member3@gmail.com', 1, 1),
(4, 'member4', 'pbkdf2:sha256:600000$Lk3wWe4m$0c4e1d736e0e66fd1c7dc760f6cc84d7f8371a4828fb4945c8867cceb3ac01f6', 'member4@gmail.com', 1, 1),
(5, 'member5', 'pbkdf2:sha256:600000$vfTPYZwd$755049ba91534ec120cd2dc1d10a824997e58f9f8372ba3aa685995d68a94156', 'member5@gmail.com', 1, 1),
(6, 'member6', 'pbkdf2:sha256:600000$WD5tvt3J$dab8b89aeedec9f5bbe8cdd35484062e2c099c00a9cb29a4f96f1ef7838cd685', 'member6@gmail.com', 1, 1),
(7, 'member7', 'pbkdf2:sha256:600000$Fhja8Kxv$52a264ed76f039a9e43f99b02c0161703df0e35011c498b0ab192eb8239675ba', 'member7@gmail.com', 1, 1),
(8, 'member8', 'pbkdf2:sha256:600000$W9uYQSG9$be5d6912deb6229d38f95a1de797cd1ac308cb4752c9c689c55cfd3f0326ec4a', 'member8@gmail.com', 1, 1),
(9, 'member9', 'pbkdf2:sha256:600000$IF0nbNOj$d7c9eb2b23bea8ab6228ec4c9041fd1950d301cb6631c0668bc083c4b9179fe8', 'member9@gmail.com', 1, 0),
(10, 'member10', 'pbkdf2:sha256:600000$VN2GILAA$844e37856760b56da546b6911955b28b4040578f3ec9c6fab7b0c0ed5578c4d6', 'member10@gmail.com', 1, 0),
(11, 'member11', 'pbkdf2:sha256:600000$QQsrQcOR$911ec057b561c91fab46b8d9ff56a68611c0a10ac8bd811464d83b4aadb20cfc', 'member11@gmail.com', 1, 1),
(12, 'member12', 'pbkdf2:sha256:600000$BWGIfDQi$39f02448fe2e99aaafbd90d0c2172674094db4010cec5ebc25ca374e33cf0d0c', 'member12@gmail.com', 1, 1),
(13, 'member13', 'pbkdf2:sha256:600000$mWyKucui$2384522e827a6c7d354074bcb65eabef9bc7e982293d29dfd16bd2bba3730204', 'member13@gmail.com', 1, 1),
(14, 'member14', 'pbkdf2:sha256:600000$Lk3wWe4m$0c4e1d736e0e66fd1c7dc760f6cc84d7f8371a4828fb4945c8867cceb3ac01f6', 'member14@gmail.com', 1, 1),
(15, 'member15', 'pbkdf2:sha256:600000$vfTPYZwd$755049ba91534ec120cd2dc1d10a824997e58f9f8372ba3aa685995d68a94156', 'member15@gmail.com', 1, 1),
(16, 'member16', 'pbkdf2:sha256:600000$WD5tvt3J$dab8b89aeedec9f5bbe8cdd35484062e2c099c00a9cb29a4f96f1ef7838cd685', 'member16@gmail.com', 1, 1),
(17, 'member17', 'pbkdf2:sha256:600000$Fhja8Kxv$52a264ed76f039a9e43f99b02c0161703df0e35011c498b0ab192eb8239675ba', 'member17@gmail.com', 1, 1),
(18, 'member18', 'pbkdf2:sha256:600000$W9uYQSG9$be5d6912deb6229d38f95a1de797cd1ac308cb4752c9c689c55cfd3f0326ec4a', 'member18@gmail.com', 1, 1),
(19, 'member19', 'pbkdf2:sha256:600000$IF0nbNOj$d7c9eb2b23bea8ab6228ec4c9041fd1950d301cb6631c0668bc083c4b9179fe8', 'member19@gmail.com', 1, 0),
(20, 'member20', 'pbkdf2:sha256:600000$VN2GILAA$844e37856760b56da546b6911955b28b4040578f3ec9c6fab7b0c0ed5578c4d6', 'member20@gmail.com', 1, 0),
(21, 'trainer1', 'pbkdf2:sha256:600000$6WKaBF0y$c839dc523a23c12343363da9ed7c2f23fb15ad4e85a4bfec2eb9fe55f0965bad', 'trainer1@gmail.com', 2, 1),
(22, 'trainer2', 'pbkdf2:sha256:600000$kuSzpxT5$b83ca273a1fe6fda2dbfb43bd58645904fe29759e824816a7bbb1f41af054b28', 'trainer2@gmail.com', 2, 1),
(23, 'trainer3', 'pbkdf2:sha256:600000$7eVceCnc$49526677a7dc8d162d100240814b17e314bec60b6608dfb05d2d489e2f00bb31', 'trainer3@gmail.com', 2, 1),
(24, 'trainer4', 'pbkdf2:sha256:600000$6WKaBF0y$c839dc523a23c12343363da9ed7c2f23fb15ad4e85a4bfec2eb9fe55f0965bad', 'trainer1@gmail.com', 2, 1),
(25, 'trainer5', 'pbkdf2:sha256:600000$kuSzpxT5$b83ca273a1fe6fda2dbfb43bd58645904fe29759e824816a7bbb1f41af054b28', 'trainer2@gmail.com', 2, 1),
(26, 'trainer6', 'pbkdf2:sha256:600000$7eVceCnc$49526677a7dc8d162d100240814b17e314bec60b6608dfb05d2d489e2f00bb31', 'trainer3@gmail.com', 2, 1),
(27, 'manager1', 'pbkdf2:sha256:600000$juQ0WUSZ$941c5a494829a6c11d8b91ccae1792690b7b7e75d5ef080cf4a7f0e90f206c50', 'manager@gmail.com', 3, 1),
(28, 'manager2', 'pbkdf2:sha256:600000$VN2GILAA$844e37856760b56da546b6911955b28b4040578f3ec9c6fab7b0c0ed5578c4d6', 'manager@gmail.com', 3, 1);


-- Add member data
INSERT INTO members (id, user_id, first_name, last_name, `position`, phone_number, address, birth_date,health_info, profile_image) VALUES
(1, 1, 'John', 'Doe', 'Software Engineer', '0234567890', '123 Main St, City, Country', '1990-05-15','Some examples of health information include:
notes of your symptoms or diagnosis.
information about a health service you''ve had or will receive.
specialist reports and test results.
prescriptions and other pharmaceutical purchases.
dental records.
your genetic information.
your wishes about future health services.', 'profile1.jpg'),
(2, 2, 'Alice', 'Smith', 'Data Analyst', '0987654321', '456 Elm St, City, Country', '1988-09-20','Headache', 'profile2.jpg'),
(3, 3, 'Michael', 'Johnson', 'Project Manager', '0122334455', '789 Oak St, City, Country', '1985-11-10','Back injury', 'profile3.jpg'),
(4, 4, 'Emily', 'Brown', 'Marketing Specialist', '0555666777', '321 Pine St, City, Country', '1992-03-25', 'Joint strain','profile4.jpg'),
(5, 5, 'David', 'Jones', 'HR Manager', '0443322111', '654 Cedar St, City, Country', '1983-07-12', 'I can''t move my knee hard','profile5.jpg'),
(6, 6, 'Emma', 'Wilson', 'Financial Analyst', '0777333444', '987 Maple St, City, Country', '1995-01-30','', 'profile6.jpg'),
(7, 7, 'Daniel', 'Martinez', 'Sales Representative', '0888999900', '159 Birch St, City, Country', '1991-08-05','', 'profile7.jpg'),
(8, 8, 'Olivia', 'Garcia', 'Graphic Designer', '0666777888', '852 Walnut St, City, Country', '1987-12-08', '','profile8.jpg'),
(9, 9, 'James', 'Lopez', 'Customer Service Manager', '0223344556', '753 Ash St, City, Country', '1993-06-18', '','profile9.jpg'),
(10, 10, 'Sophia', 'Hernandez', 'Product Manager', '0999888777', '369 Cherry St, City, Country', '1989-04-22', '','profile10.jpg'),
(11, 11, 'Benjamin', 'Clark', 'IT Specialist', '0111222333', '234 Willow St, City, Country', '1990-05-16', '', 'profile11.jpg'),
(12, 12, 'Charlotte', 'Morales', 'Quality Assurance', '0222444666', '123 Beech St, City, Country', '1986-08-24', 'Migraine', 'profile12.jpg'),
(13, 13, 'Ethan', 'Harris', 'Business Analyst', '0333555777', '456 Birch St, City, Country', '1982-12-30', 'Ankle sprain', 'profile13.jpg'),
(14, 14, 'Amelia', 'Davis', 'Software Engineer', '0444666888', '789 Willow St, City, Country', '1994-01-15', 'Elbow pain', 'profile14.jpg'),
(15, 15, 'Matthew', 'Martinez', 'Logistics Coordinator', '0555777999', '321 Cedar St, City, Country', '1981-09-19', 'Wrist strain', 'profile15.jpg'),
(16, 16, 'Ava', 'Taylor', 'Human Resources', '0666888111', '654 Maple St, City, Country', '1992-04-08', '', 'profile16.jpg'),
(17, 17, 'Lucas', 'Thomas', 'Operations Manager', '0777999222', '987 Oak St, City, Country', '1988-07-07', '', 'profile17.jpg'),
(18, 18, 'Mia', 'Wilson', 'Customer Support', '0888111333', '159 Pine St, City, Country', '1995-11-23', '', 'profile18.jpg'),
(19, 19, 'William', 'Anderson', 'Marketing Director', '0999222444', '321 Ash St, City, Country', '1983-03-12', 'Knee injury', 'profile19.jpg'),
(20, 20, 'Sophie', 'Moore', 'Product Developer', '0111333444', '753 Cherry St, City, Country', '1991-06-25', '', 'profile20.jpg');


-- Add trainer data
INSERT INTO trainers (id, user_id, first_name, last_name, `title`, phone_number, profile_image, description) VALUES
(1, 21, 'John', 'Doe', 'Certified Personal Trainer', '01325551234', 'john_profile.jpg', 'Experienced personal trainer specializing in weight loss and strength training.'),
(2, 22, 'Emily', 'Smith', 'Fitness Coach', '01255555678', 'emily_profile.jpg', 'Passionate about helping clients achieve their fitness goals through personalized workout plans.'),
(3, 23, 'Michael', 'Johnson', 'Yoga Instructor', '01245559876', 'michael_profile.jpg', 'Certified yoga instructor with a focus on mindfulness and flexibility training.'),
(4, 24, 'Sarah', 'Williams', 'Pilates Instructor', '01445557788', 'sarah_profile.jpg', 'Dedicated Pilates instructor with expertise in core strengthening and posture improvement.'),
(5, 25, 'David', 'Brown', 'Athletic Coach', '01565554433', 'david_profile.jpg', 'Experienced in coaching athletes for competitive sports and performance enhancement.'),
(6, 26, 'Rachel', 'Wilson', 'Nutritionist', '01675553322', 'rachel_profile.jpg', 'Registered nutritionist specializing in dietary planning for fitness and health optimization.');



-- Add manager data
INSERT INTO managers (id, user_id, first_name, last_name, `title`, phone_number) VALUES
(1, 27, 'Alice', 'Johnson', 'Fitness Center Manager', '02655552468'),
(2, 28, 'Daisy', 'Johnson', 'Fitness Center Manager', '02655552466');

-- Add course type data
INSERT INTO course_types (id, name, description) VALUES
(1, 'class', 'A membership group class that does not require an additional fee.'),
(2, 'session', 'One-on-one courses with a trainer that require an additional fee.');

-- Add location data with fictional addresses
INSERT INTO location (id, name, description) VALUES
(1, 'Central Park', '123 Park Ave, City, Country'),
(2, 'Riverside Walkway', '456 Riverside Dr, City, Country'),
(3, 'Mountain View Trail', '789 Mountain Rd, City, Country'),
(4, 'Community Sports Field', '321 Community Ln, City, Country'),
(5, 'Beachfront Area', '654 Ocean Blvd, City, Country');


-- Add class data
INSERT INTO fitness_classes (id, name, description, course_type_id, trainer_id, schedule_time, location_id, price, capacity) VALUES
-- Active class
(1, 'Morning Yoga', 'Start your day with energy and peace.', 1, 1, '2024-05-01 09:00:00', 1, 0.00, 15),
(2, 'HIIT', 'High intensity cardio class for maximum calorie burn.', 1, 2, '2024-05-01 10:00:00', 2, 0.00,15),
(3, 'Strength Training', 'Build your strength and endurance.', 1, 3, '2024-05-01 11:00:00', 3, 0.00, 15),
(4, 'Outdoor Running', 'Improve your running technique and stamina.', 1, 4, '2024-05-01 13:00:00', 4, 0.00, 15),
(5, 'Outdoor Cycling', 'Energetic cycling session for all levels.', 1, 5, '2024-05-01 14:00:00', 5, 0.00, 15),
--
(6, 'Boot Camp', 'Intense boot camp workout to push your limits.', 1, 1, '2024-05-03 10:00:00', 2, 0.00,15),
(7, 'Zumba Dance', 'Fun and energetic dance workout for all.', 1, 2, '2024-05-03 11:00:00', 3, 0.00, 15),
(8, 'Power Yoga', 'High-Intensity Interval Training for fast results.', 1, 3, '2024-05-03 13:00:00', 4, 0.00, 15),
(9, 'Pilates', 'A challenging yoga class to improve strength and flexibility.', 1, 4, '2024-05-03 14:00:00', 5, 0.00, 15),
(10,'Boxing Fitness', 'Calm your mind with our guided meditation.', 1, 5, '2024-05-03 15:00:00', 1, 0.00, 15),
-- 
(11, 'Morning Yoga', 'Start your day with energy and peace.', 1, 1, '2024-04-24 09:00:00', 1, 0.00, 15),
(12, 'HIIT', 'High intensity cardio class for maximum calorie burn.', 1, 2, '2024-04-24 10:00:00', 2, 0.00,15),
(13, 'Strength Training', 'Build your strength and endurance.', 1, 3, '2024-04-24 11:00:00', 3, 0.00, 15),
(14, 'Outdoor Running', 'Improve your running technique and stamina.', 1, 4, '2024-04-24 13:00:00', 4, 0.00, 15),
(15, 'Outdoor Cycling', 'Energetic cycling session for all levels.', 1, 5, '2024-04-24 14:00:00', 5, 0.00, 15),
--
(16, 'Boot Camp', 'Intense boot camp workout to push your limits.', 1, 1, '2024-04-25 10:00:00', 2, 0.00,15),
(17, 'Zumba Dance', 'Fun and energetic dance workout for all.', 1, 2, '2024-04-25 11:00:00', 3, 0.00, 15),
(18, 'Power Yoga', 'High-Intensity Interval Training for fast results.', 1, 3, '2024-04-25 13:00:00', 4, 0.00, 15),
(19, 'Pilates', 'A challenging yoga class to improve strength and flexibility.', 1, 4, '2024-04-25 14:00:00', 5, 0.00, 15),
(20,'Boxing Fitness', 'Calm your mind with our guided meditation.', 1, 5, '2024-04-25 15:00:00', 1, 0.00, 15),
-- 
(21, 'Morning Yoga', 'Start your day with energy and peace.', 1, 1, '2024-04-26 09:00:00', 1, 0.00, 15),
(22, 'HIIT', 'High intensity cardio class for maximum calorie burn.', 1, 2, '2024-04-26 10:00:00', 2, 0.00,15),
(23, 'Strength Training', 'Build your strength and endurance.', 1, 3, '2024-04-26 11:00:00', 3, 0.00, 15),
(24, 'Outdoor Running', 'Improve your running technique and stamina.', 1, 4, '2024-04-26 13:00:00', 4, 0.00, 15),
(25, 'Outdoor Cycling', 'Energetic cycling session for all levels.', 1, 5, '2024-04-26 14:00:00', 5, 0.00, 15),
--
(26, 'Boot Camp', 'Intense boot camp workout to push your limits.', 1, 1, '2024-04-29 10:00:00', 2, 0.00,15),
(27, 'Zumba Dance', 'Fun and energetic dance workout for all.', 1, 2, '2024-04-29 11:00:00', 3, 0.00, 15),
(28, 'Power Yoga', 'High-Intensity Interval Training for fast results.', 1, 3, '2024-04-29 13:00:00', 4, 0.00, 15),
(29, 'Pilates', 'A challenging yoga class to improve strength and flexibility.', 1, 4, '2024-04-29 14:00:00', 5, 0.00, 15),
(30,'Boxing Fitness', 'Calm your mind with our guided meditation.', 1, 5, '2024-04-29 15:00:00', 1, 0.00, 15),
-- 
(31, 'Morning Yoga', 'Start your day with energy and peace.', 1, 1, '2024-04-30 09:00:00', 1, 0.00, 15),
(32, 'HIIT', 'High intensity cardio class for maximum calorie burn.', 1, 2, '2024-04-30 10:00:00', 2, 0.00,15),
(33, 'Strength Training', 'Build your strength and endurance.', 1, 3, '2024-04-30 11:00:00', 3, 0.00, 15),
(34, 'Outdoor Running', 'Improve your running technique and stamina.', 1, 4, '2024-04-30 13:00:00', 4, 0.00, 15),
(35, 'Outdoor Cycling', 'Energetic cycling session for all levels.', 1, 5, '2024-04-30 14:00:00', 5, 0.00, 15),
--
(36, 'Boot Camp', 'Intense boot camp workout to push your limits.', 1, 1, '2024-05-01 10:00:00', 2, 0.00,15),
(37, 'Zumba Dance', 'Fun and energetic dance workout for all.', 1, 2, '2024-05-01 11:00:00', 3, 0.00, 15),
(38, 'Power Yoga', 'High-Intensity Interval Training for fast results.', 1, 3, '2024-05-01 13:00:00', 4, 0.00, 15),
(39, 'Pilates', 'A challenging yoga class to improve strength and flexibility.', 1, 4, '2024-05-01 14:00:00', 5, 0.00, 15),
(40,'Boxing Fitness', 'Calm your mind with our guided meditation.', 1, 5, '2024-05-01 15:00:00', 1, 0.00, 15),
-- 
(41, 'Morning Yoga', 'Start your day with energy and peace.', 1, 1, '2024-05-02 09:00:00', 1, 0.00, 15),
(42, 'HIIT', 'High intensity cardio class for maximum calorie burn.', 1, 2, '2024-05-02 10:00:00', 2, 0.00,15),
(43, 'Strength Training', 'Build your strength and endurance.', 1, 3, '2024-05-02 11:00:00', 3, 0.00, 15),
(44, 'Outdoor Running', 'Improve your running technique and stamina.', 1, 4, '2024-05-02 13:00:00', 4, 0.00, 15),
(45, 'Outdoor Cycling', 'Energetic cycling session for all levels.', 1, 5, '2024-05-02 14:00:00', 5, 0.00, 15),
-- expired class;
(55, 'Morning Yoga', 'Start your day with energy and peace.', 1, 1, '2024-04-02 09:00:00', 1, 0.00, 15),
(46, 'HIIT', 'High intensity cardio class for maximum calorie burn.', 1, 2, '2024-04-02 10:00:00', 2, 0.00,15),
(47, 'Strength Training', 'Build your strength and endurance.', 1, 3, '2024-04-02 11:00:00', 3, 0.00, 15),
(48, 'Outdoor Running', 'Improve your running technique and stamina.', 1, 4, '2024-04-02 12:00:00', 4, 0.00, 15),
(49, 'Outdoor Cycling', 'Energetic cycling session for all levels.', 1, 5, '2024-04-02 13:00:00', 5, 0.00, 15),
(50, 'Boot Camp', 'Intense boot camp workout to push your limits.', 1, 1, '2024-04-02 15:00:00', 2, 0.00,15),
(51, 'Zumba Dance', 'Fun and energetic dance workout for all.', 1, 2, '2024-04-03 09:00:00', 3, 0.00, 15),
(52, 'Power Yoga', 'High-Intensity Interval Training for fast results.', 1, 3, '2024-04-03 10:00:00', 4, 0.00, 15),
(53, 'Pilates', 'A challenging yoga class to improve strength and flexibility.', 1, 4, '2024-04-03 11:00:00', 5, 0.00, 15),
(54, 'Boxing Fitness', 'Calm your mind with our guided meditation.', 1, 5, '2024-04-03 09:00:00', 1, 0.00, 15);

-- Add session data
INSERT INTO fitness_classes (id, name, description, course_type_id, trainer_id, schedule_time, location_id, price, capacity) VALUES
-- Active session
(56, 'Personal Training', 'Tailored fitness program to meet your personal goals.', 2, 1, '2024-05-02 11:00:00', 1, 50.00, 1),
(57, 'Cardio Coaching', 'Personalized yoga session to deepen your practice.', 2, 2, '2024-05-01 12:00:00', 2, 50.00, 1),
(58, 'Strength Training', 'Customized cardio training for maximum effectiveness.', 2, 3, '2024-05-01 13:00:00', 3, 50.00, 1),
(59, 'Strength Training', 'One-on-one consultation and training session for strength.', 2, 4, '2024-04-24 14:00:00', 4, 50.00, 1),
(60, 'Cardio Coaching', 'A private Pilates class focusing on your needs.', 2, 5, '2024-04-24 15:00:00', 5, 50.00, 1),
(61, 'Personal Training', 'Develop a personalized fitness plan with a professional.', 2, 1, '2024-04-24 16:00:00', 1, 50.00, 1),
(62, 'Personal Training', 'Comprehensive one-on-one coaching on fitness and nutrition.', 2, 2, '2024-04-25 09:00:00', 2, 50.00,1),
(63, 'Cardio Coaching', 'Explore advanced yoga poses and techniques in a private setting.', 2, 3, '2024-04-25 10:00:00', 3, 50.00,1),
(64, 'Strength Training', 'Improve your running technique with personal coaching.', 2, 4, '2024-04-25 11:00:00', 4, 50.00,1),
(65, 'Cardio Coaching', 'One-on-one session to learn and practice meditation.', 2, 5, '2024-04-26 12:00:00', 5, 50.00, 1 ),
(66, 'Strength Training', 'Tailored fitness program to meet your personal goals.', 2, 2, '2024-04-26 11:00:00', 1, 50.00, 1),
(67, 'One-on-One Yoga', 'Personalized yoga session to deepen your practice.', 2, 3, '2024-04-26 12:00:00', 2, 50.00, 1),
(68, 'Personal Training', 'Customized cardio training for maximum effectiveness.', 2, 1, '2024-04-27 13:00:00', 3, 50.00, 1),
(69, 'Strength Training Consultation', 'One-on-one consultation and training session for strength.', 2, 4, '2024-04-27 14:00:00', 4, 50.00, 1),
(70, 'Strength Training', 'A private Pilates class focusing on your needs.', 2, 5, '2024-04-27 15:00:00', 5, 50.00, 1),
(71, 'CPersonal Training', 'Develop a personalized fitness plan with a professional.', 2, 1, '2024-04-28 16:00:00', 1, 50.00, 1),
(72, 'Strength Training', 'Comprehensive one-on-one coaching on fitness and nutrition.', 2, 2, '2024-04-28 09:00:00', 2, 50.00,1),
(73, 'Personal Training', 'Explore advanced yoga poses and techniques in a private setting.', 2, 3, '2024-04-28 10:00:00', 3, 50.00,1),
(74, 'Strength Training', 'Improve your running technique with personal coaching.', 2, 4, '2024-05-01 11:00:00', 4, 50.00,1),
-- expired session
(75, 'One-on-One Yoga', 'One-on-one session to learn and practice meditation.', 2, 3, '2024-03-02 12:00:00', 5, 50.00, 1 ),
(76, 'One-on-One Yoga', 'Tailored fitness program to meet your personal goals.', 2,1, '2024-04-02 11:00:00', 1, 50.00, 1),
(77, 'Personal Training', 'Personalized yoga session to deepen your practice.', 2, 2, '2024-02-02 12:00:00', 2, 45.00, 1),
(78, 'One-on-One Yoga', 'Customized cardio training for maximum effectiveness.', 2, 4, '2024-02-03 13:00:00', 3, 40.00, 1),
(79, 'One-on-One Yoga', 'One-on-one consultation and training session for strength.', 2, 5, '2024-01-03 14:00:00', 4, 55.00, 1),
(80, 'Personal Training', 'A private Pilates class focusing on your needs.', 2, 2, '2024-01-03 15:00:00', 5, 50.00, 1),
(81, 'One-on-One Yoga', 'Develop a personalized fitness plan with a professional.', 2, 2, '2024-04-03 16:00:00', 1, 60.00, 1),
(82, 'Personal Training', 'Comprehensive one-on-one coaching on fitness and nutrition.', 2, 4, '2023-12-04 09:00:00', 2, 65.00,1),
(83, 'Cardio Coaching', 'Explore advanced yoga poses and techniques in a private setting.', 2, 1, '2023-12-04 10:00:00', 3, 70.00,1),
(84, 'Cardio Coaching', 'Improve your running technique with personal coaching.', 2, 2, '2023-11-04 11:00:00', 4, 45.00,1),
(85, 'Cardio Coaching', 'One-on-one session to learn and practice meditation.', 2, 5, '2023-11-05 12:00:00', 5, 50.00, 1 );



-- Add subscription plan data
INSERT INTO subscription_plans (id, type, price) VALUES
(1, '1 mounths', 50.00),
(2, '3 mounths', 75.00),
(3, '6 mounths', 100.00),
(4, '12 mounths', 125.00);

-- Active subscriptions
INSERT INTO specific_subscriptions (user_id, subscription_plan_id, start_date, end_date) VALUES
(1, 1, '2024-04-02', '2024-05-02'),
(2, 2, '2024-04-16', '2024-07-16'),
(3, 3, '2024-04-15', '2024-10-15'),
(4, 4, '2024-04-15', '2025-04-15');

-- Expired subscriptions

INSERT INTO specific_subscriptions (user_id, subscription_plan_id, start_date, end_date) VALUES
(1, 1, '2023-01-10', '2023-02-10'),
(2, 2, '2023-01-15', '2023-04-15'),
(3, 3, '2023-01-20', '2023-07-20'),
(4, 4, '2023-01-25', '2024-01-25'),
(5, 1, '2023-02-10', '2023-03-10'),
(6, 2, '2023-02-15', '2023-05-15'),
(7, 3, '2023-02-20', '2023-08-20'),
(8, 4, '2023-02-25', '2024-02-25'),
(1, 3, '2023-03-25', '2023-09-25'),
(2, 4, '2023-04-05', '2024-04-05'),
(3, 1, '2023-04-15', '2023-05-15'),
(4, 2, '2023-04-25', '2023-07-25'),
(5, 3, '2023-05-05', '2023-11-05'),
(7, 1, '2023-06-05', '2023-07-05'),
(8, 2, '2023-06-15', '2023-09-15'),
(1, 1, '2023-07-15', '2023-08-15'),
(2, 2, '2023-07-25', '2023-10-25'),
(3, 3, '2023-08-05', '2024-02-05'),
(5, 1, '2023-09-05', '2023-10-05'),
(6, 2, '2023-09-15', '2023-12-15'),
(7, 3, '2023-09-25', '2024-03-25'),
(3, 1, '2023-12-05', '2024-01-05'),
(4, 2, '2023-12-15', '2024-03-15'),
(7, 1, '2024-02-05', '2024-03-05'),
(8, 2, '2024-01-30', '2024-04-30'),
(11, 1, '2023-01-10', '2023-02-10'),
(12, 2, '2023-01-15', '2023-04-15'),
(13, 3, '2023-01-20', '2023-07-20'),
(14, 4, '2023-01-25', '2024-01-25'),
(15, 1, '2023-02-10', '2023-03-10'),
(16, 2, '2023-02-15', '2023-05-15'),
(17, 3, '2023-02-20', '2023-08-20'),
(18, 4, '2023-02-25', '2024-02-25'),
(11, 3, '2023-03-25', '2023-09-25'),
(12, 4, '2023-04-05', '2024-04-05'),
(13, 1, '2023-04-15', '2023-05-15'),
(14, 2, '2023-04-25', '2023-07-25'),
(15, 3, '2023-05-05', '2023-11-05'),
(16, 1, '2023-06-05', '2023-07-05'),
(18, 2, '2023-06-15', '2023-09-15'),
(11, 1, '2023-07-15', '2023-08-15'),
(12, 2, '2023-07-25', '2023-10-25'),
(13, 3, '2023-08-05', '2024-02-05'),
(15, 1, '2023-09-05', '2023-10-05'),
(16, 2, '2023-09-15', '2023-12-15'),
(17, 3, '2023-09-25', '2024-03-25'),
(13, 1, '2023-10-05', '2024-11-05'),
(14, 2, '2023-11-15', '2024-04-15'),
(17, 1, '2024-02-05', '2024-03-05'),
(18, 2, '2024-01-30', '2024-04-30');

-- Note: Users 9 and 10 do not have subscriptions based on your instructions, so no entries for them.

-- BOOKING
INSERT INTO bookings (member_id, fitness_class_id, booking_date, status, is_attend, is_paid) VALUES
(1, 46, '2024-04-01 10:00:00', 1, 1, 1),
(1, 47, '2024-04-01 10:00:00', 1, 1, 1),
(1, 48, '2024-04-01 11:00:00', 1, 1, 1),
(1, 49, '2024-04-01 12:00:00', 1, 1, 1),
(1, 50, '2024-04-01 14:00:00', 1, 0, 1),
(1, 51, '2024-04-02 08:00:00', 1, 1, 1),
(1, 52, '2024-04-02 09:00:00', 1, 1, 1),
(1, 53, '2024-04-02 10:00:00', 1, 1, 1),
(1, 54, '2024-04-02 08:00:00', 1, 0, 1),
(1, 55, '2024-04-01 08:00:00', 1, 1, 1),
(2, 46, '2024-04-01 09:00:00', 1, 1, 1),
(2, 47, '2024-04-01 09:00:00', 1, 1, 1),
(2, 48, '2024-04-01 10:00:00', 1, 1, 1),
(2, 49, '2024-04-01 11:00:00', 1, 1, 1),
(2, 50, '2024-04-01 12:00:00', 1, 1, 1),
(2, 51, '2024-04-01 13:00:00', 1, 1, 1),
(2, 52, '2024-04-02 08:00:00', 1, 1, 1),
(2, 53, '2024-04-02 09:00:00', 1, 1, 1),
(2, 54, '2024-04-02 10:00:00', 1, 1, 1),
(2, 55, '2024-04-01 08:00:00', 1, 1, 1),
(3, 46, '2024-04-01 09:00:00', 1, 1, 1),
(3, 47, '2024-04-01 09:00:00', 1, 1, 1),
(3, 48, '2024-04-01 10:00:00', 1, 0, 1),
(3, 49, '2024-04-01 11:00:00', 1, 0, 1),
(3, 50, '2024-04-01 12:00:00', 1, 0, 1),
(3, 51, '2024-04-01 13:00:00', 1, 1, 1),
(3, 52, '2024-04-02 08:00:00', 1, 0, 1),
(3, 53, '2024-04-02 09:00:00', 1, 1, 1),
(3, 54, '2024-04-02 10:00:00', 1, 0, 1),
(3, 55, '2024-04-01 08:00:00', 1, 1, 1),
(4, 46, '2024-04-01 09:00:00', 1, 1, 1),
(4, 47, '2024-04-01 09:00:00', 1, 1, 1),
(4, 48, '2024-04-01 10:00:00', 1, 0, 1),
(4, 49, '2024-04-01 11:00:00', 1, 0, 1),
(4, 50, '2024-04-01 12:00:00', 1, 0, 1),
(4, 51, '2024-04-01 13:00:00', 1, 0, 1),
(4, 52, '2024-04-02 08:00:00', 1, 0, 1),
(4, 53, '2024-04-02 09:00:00', 1, 0, 1),
(4, 54, '2024-04-02 10:00:00', 1, 0, 1),
(4, 55, '2024-04-01 08:00:00', 1, 1, 1),
(5, 46, '2024-04-01 10:00:00', 1, 1, 1),
(5, 47, '2024-04-01 10:00:00', 1, 1, 1),
(5, 48, '2024-04-01 11:00:00', 1, 1, 1),
(5, 49, '2024-04-01 12:00:00', 1, 1, 1),
(5, 50, '2024-04-01 14:00:00', 1, 0, 1),
(5, 51, '2024-04-02 08:00:00', 1, 1, 1),
(5, 52, '2024-04-02 09:00:00', 1, 1, 1),
(5, 53, '2024-04-02 10:00:00', 1, 1, 1),
(5, 54, '2024-04-02 08:00:00', 1, 0, 1),
(5, 55, '2024-04-01 08:00:00', 1, 1, 1),
(6, 46, '2024-04-01 09:00:00', 1, 1, 1),
(6, 47, '2024-04-01 09:00:00', 1, 1, 1),
(6, 48, '2024-04-01 10:00:00', 1, 1, 1),
(6, 49, '2024-04-01 11:00:00', 1, 1, 1),
(6, 50, '2024-04-01 12:00:00', 1, 1, 1),
(6, 51, '2024-04-01 13:00:00', 1, 1, 1),
(6, 52, '2024-04-02 08:00:00', 1, 1, 1),
(6, 53, '2024-04-02 09:00:00', 1, 1, 1),
(6, 54, '2024-04-02 10:00:00', 1, 1, 1),
(6, 55, '2024-04-01 08:00:00', 1, 1, 1),
(7, 46, '2024-04-01 09:00:00', 1, 1, 1),
(7, 47, '2024-04-01 09:00:00', 1, 1, 1),
(7, 48, '2024-04-01 10:00:00', 1, 0, 1),
(7, 49, '2024-04-01 11:00:00', 1, 0, 1),
(7, 50, '2024-04-01 12:00:00', 1, 0, 1),
(7, 51, '2024-04-01 13:00:00', 1, 1, 1),
(7, 52, '2024-04-02 08:00:00', 1, 0, 1),
(7, 53, '2024-04-02 09:00:00', 1, 1, 1),
(7, 54, '2024-04-02 10:00:00', 1, 0, 1),
(7, 55, '2024-04-01 08:00:00', 1, 1, 1),
(8, 46, '2024-04-01 09:00:00', 1, 1, 1),
(8, 47, '2024-04-01 09:00:00', 1, 1, 1),
(8, 48, '2024-04-01 10:00:00', 1, 0, 1),
(8, 49, '2024-04-01 11:00:00', 1, 0, 1),
(8, 50, '2024-04-01 12:00:00', 1, 0, 1),
(8, 51, '2024-04-01 13:00:00', 1, 0, 1),
(8, 52, '2024-04-02 08:00:00', 1, 0, 1),
(8, 53, '2024-04-02 09:00:00', 1, 0, 1),
(8, 54, '2024-04-02 10:00:00', 1, 0, 1),
(8, 55, '2024-04-01 08:00:00', 1, 1, 1),
(1, 75, '2024-04-01 10:00:00', 1, 1, 1),
(1, 76, '2024-04-01 10:00:00', 1, 0, 0),
(1, 77, '2024-02-01 11:00:00', 1, 1, 1),
(1, 78, '2024-02-01 12:00:00', 1, 0, 0),
(1, 79, '2024-01-01 14:00:00', 1, 0, 1),
(1, 80, '2024-01-02 08:00:00', 1, 0, 1),
(2, 81, '2024-04-02 09:00:00', 1, 1, 1),
(2, 82, '2023-12-02 10:00:00', 1, 1, 1),
(3, 83, '2023-12-02 08:00:00', 1, 1, 1),
(3, 84, '2023-11-01 08:00:00', 1, 1, 1),
(3, 85, '2023-11-01 09:00:00', 1, 1, 1);

--
INSERT INTO bookings (member_id, fitness_class_id, booking_date, status, is_attend, is_paid) VALUES
(1, 1, '2024-04-01 10:00:00', 1, 0, 1),
(1, 6, '2024-04-01 10:00:00', 1, 0, 1),
(1, 11, '2024-04-01 11:00:00', 1, 0, 1),
(1, 16, '2024-04-01 12:00:00', 1, 0, 1),
(1, 21, '2024-04-01 14:00:00', 1, 0, 1),
(1, 26, '2024-04-02 08:00:00', 1, 0, 1),
(1, 31, '2024-04-02 09:00:00', 1, 0, 1),
(1, 36, '2024-04-02 10:00:00', 1, 0, 1),
(1, 41, '2024-04-02 08:00:00', 1, 0, 1),
(2, 1, '2024-04-01 10:00:00', 1, 0, 1),
(2, 7, '2024-04-01 10:00:00', 1, 0, 1),
(2, 17, '2024-04-01 11:00:00', 1, 0, 1),
(3, 3, '2024-04-01 12:00:00', 1, 0, 1),
(3, 17, '2024-04-01 14:00:00', 1, 0, 1),
(4, 18, '2024-04-02 08:00:00', 1, 0, 1),
(4, 20, '2024-04-02 09:00:00', 1, 0, 1),
(4, 21, '2024-04-02 10:00:00', 1, 0, 1),
(4, 30, '2024-04-02 08:00:00', 1, 0, 1),
(1, 56, '2024-04-01 10:00:00', 1, 0, 0),
(1, 57, '2024-04-01 10:00:00', 1, 0, 1),
(2, 71, '2024-04-01 11:00:00', 1, 0, 0),
(2, 59, '2024-04-01 12:00:00', 1, 0, 1),
(1, 26, '2024-04-02 08:00:00', 1, 0, 1),
(1, 58, '2024-04-02 09:00:00', 1, 0, 1),
(1, 60, '2024-04-02 10:00:00', 1, 0, 1);


-- News
INSERT INTO news (id, title, content, published_at, modified_at, manager_id) VALUES
(1, 'Top 5 Exercises for Building Muscle', 'Lorem ipsum dolor sit amet, consectetur adipisci elit, sed eiusmod tempor incidunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur. Quis aute iure reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint obcaecat cupiditat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.Lorem ipsum dolor sit amet, consectetur adipisci elit, sed eiusmod tempor incidunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur. Quis aute iure reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint obcaecat cupiditat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', '2024-04-15 09:00:00', CURRENT_TIMESTAMP, 3),
(2, 'New Study Shows Benefits of High-Intensity Interval Training', 'A recent study published in a leading health journal reveals the incredible benefits of HIIT workouts for both weight loss and cardiovascular health.', '2024-04-14 10:30:00', CURRENT_TIMESTAMP, 3),
(3, 'How to Stay Motivated During Your Fitness Journey', 'Struggling to stay motivated? Discover tips and tricks to keep you on track and reaching your fitness goals.', '2024-04-13 11:45:00', CURRENT_TIMESTAMP, 3),
(4, '5 Healthy Habits to Boost Your Workout Results', 'Incorporate these 5 healthy habits into your daily routine to maximize the results of your workouts and improve overall well-being.', '2024-04-12 14:20:00', CURRENT_TIMESTAMP, 3),
(5, 'The Importance of Proper Nutrition for Muscle Growth', 'Learn why nutrition is just as important as exercise when it comes to building lean muscle mass and achieving your fitness goals.', '2024-04-11 15:55:00', CURRENT_TIMESTAMP, 3),
(6, 'The Benefits of Yoga for Mind and Body', 'Discover the numerous physical and mental benefits of practicing yoga, from increased flexibility to reduced stress levels.', '2024-04-10 17:10:00', CURRENT_TIMESTAMP, 3),
(7, 'How to Prevent Common Workout Injuries', 'Avoid setbacks in your fitness journey by learning how to prevent common workout injuries with these helpful tips.', '2024-04-09 18:25:00', CURRENT_TIMESTAMP, 3),
(8, '5 Must-Try Protein-Packed Recipes for Fitness Enthusiasts', 'Revamp your meal prep routine with these delicious and nutritious protein-packed recipes designed to fuel your workouts and support muscle recovery.', '2024-04-08 20:00:00', CURRENT_TIMESTAMP, 3),
(9, 'The Role of Sleep in Exercise Recovery', 'Discover why getting enough quality sleep is essential for proper exercise recovery and optimizing athletic performance.', '2024-04-07 21:15:00', CURRENT_TIMESTAMP, 3),
(10, '10 Tips for Getting Started with Weightlifting', 'Interested in weightlifting but not sure where to begin? Follow these 10 expert tips to kickstart your weightlifting journey safely and effectively.', '2024-04-06 22:30:00', CURRENT_TIMESTAMP, 3);
