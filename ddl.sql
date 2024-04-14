CREATE TABLE Rooms (
	room_ID SERIAL PRIMARY KEY,
    room_name VARCHAR(255) NOT NULL,
    capacity INT NOT NULL,
	status VARCHAR(10) NOT NULL
);

CREATE TABLE Equipment (
    equipment_ID SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    status VARCHAR(1) NOT NULL CHECK (status IN ('A', 'M')),
    last_maintenance_date DATE
);

CREATE TABLE Members (
    member_ID SERIAL PRIMARY KEY,
    phone VARCHAR(15) UNIQUE,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    dateOfBirth DATE NOT NULL,
    gender VARCHAR(1) NOT NULL,
    fitness_goals VARCHAR(255),
    health_metrics VARCHAR(255)
);

CREATE TABLE Trainers (
    trainer_ID SERIAL PRIMARY KEY,
    phone VARCHAR(15) UNIQUE,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    availability TIMESTAMP
);

CREATE TABLE Administrative (
    administrative_ID SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
	equipment_ID INT,
	room_ID INT,
	FOREIGN KEY (equipment_ID) REFERENCES Equipment(equipment_ID),
	FOREIGN KEY (room_ID) REFERENCES Rooms(room_ID)
);

CREATE TABLE GroupFitness (
    class_ID SERIAL PRIMARY KEY,
    class_name VARCHAR(255) NOT NULL,
    schedule VARCHAR(255),
    trainer_ID INT,
    room_ID INT,
	FOREIGN KEY (room_ID) REFERENCES Rooms(room_ID),
	FOREIGN KEY (trainer_ID) REFERENCES Trainers(trainer_ID)
);

CREATE TABLE GroupFitnessEnrollment (
    enrollment_ID SERIAL PRIMARY KEY,
    member_ID INT NOT NULL,
    class_ID INT NOT NULL,
    enrollment_status VARCHAR(10) NOT NULL,
    FOREIGN KEY (member_ID) REFERENCES Members(member_ID),
    FOREIGN KEY (class_ID) REFERENCES GroupFitness(class_ID)
);

CREATE TABLE PersonalTrainingSession (
    session_ID SERIAL PRIMARY KEY,
    trainer_ID INT,
    member_ID INT,
    dateTime TIMESTAMP NOT NULL,
    status VARCHAR(10) NOT NULL,
    FOREIGN KEY (trainer_ID) REFERENCES Trainers(trainer_ID),
    FOREIGN KEY (member_ID) REFERENCES Members(member_ID)
);

CREATE TABLE Billing (
    bill_ID SERIAL PRIMARY KEY,
    member_ID INT,
    amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(10) NOT NULL,
    due_date DATE NOT NULL,
    FOREIGN KEY (member_ID) REFERENCES Members(member_ID)
);
