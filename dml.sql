INSERT INTO Rooms (room_name, capacity, status) VALUES
    ('Room 1', 20, 'free'),
    ('Room 2', 15, 'free'),
    ('Room 3', 30, 'free'),
    ('Room 4', 25, 'free'),
    ('Room 5', 10, 'free'),
    ('Room 6', 18, 'free'),
    ('Room 7', 22, 'free'),
    ('Room 8', 12, 'free'),
    ('Room 9', 28, 'free'),
    ('Room 10', 35, 'free'),
    ('Manager Room', 5, 'booked'),
    ('Assistant Manager Room', 5, 'booked');


INSERT INTO Equipment (name, status, last_maintenance_date) VALUES
    ('Treadmill', 'A', '2023-10-15'),
    ('Elliptical Machine', 'M', '2024-01-20'),
    ('Stationary Bike', 'A', '2024-03-05'),
    ('Rowing Machine', 'M', '2023-12-28'),
    ('Weight Bench', 'A', '2024-02-10'),
    ('Smith Machine', 'A', '2024-01-05'),
    ('Leg Press Machine', 'M', '2023-11-12'),
    ('Dumbbells', 'A', '2024-03-20'),
    ('Kettlebells', 'A', '2024-02-28'),
    ('Resistance Bands', 'M', '2023-12-10');


Insert Into Members (phone, name, email, password, dateOfBirth, gender, fitness_goals, health_metrics)
Values ('1234567890', 'John Doe', 'john@gmail.com', 'abc', '1990-01-01', 'M', 'Lose weight', 'Normal');


INSERT INTO Trainers (name, phone, email, password, availability)
VALUES
('Arda Guler', '555-0101', 'arda@gmail.com', 'ardaPass', '2024-04-03 14:00:00'),
('Leo Messi', '555-0102', 'leo@gmail.com', 'messiPass', '2024-04-03 16:00:00');


INSERT INTO Administrative (name, email, password, equipment_ID, room_ID) VALUES
    ('General Manager', 'gm@gmail.com', 'pwd1', Null, 1),
    ('Assistant Manager', 'am@gmail.com', 'pwd2', Null, 2),
    ('Front Desk', 'fd@gmail.com', 'pwd3', Null, 3);


INSERT INTO GroupFitness (class_name, schedule, trainer_ID, room_ID) VALUES
('Yoga', '2024-04-20 09:00:00', 1, 1),
('Cardio', '2024-04-20 11:00:00', 2, 2);


Insert Into GroupFitnessEnrollment (member_ID, class_ID, enrollment_status)
Values (1, 1, 'enrolled');


Insert Into PersonalTrainingSession (trainer_ID, member_ID, dateTime, status)
Values (1, 1, '2024-04-20 14:00:00', 'scheduled');


INSERT INTO Billing(member_ID, amount, status, due_date)
VALUES (4, 100, 'unpaid', '2024-04-15');



-- Note:
-- This DML file has provided for the section on the Grading Schema. 
-- To run the code 
-- First run DDL. 
-- Run;
-- Insert Into Rooms()
-- Insert Into Equipments()
-- Insert Into Trainers()
-- Insert Into Administrative()
-- The rest of the table will be filled by running the code that was provided in this project.
-- After you run the Insert Into() files that we provided, basic gym requirements will be done in the database. After that, each member needs to sign up manually. We do not ask to run other Insert Into queries. Provide other tables’ data by running python code. 
