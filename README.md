# README

# Members
- Mustafa Dursunoglu - 101226363
- Emrehan Sagin - 101223876
- Yavuz Selim Suzen - 101215831




# Project Report

# ER Diagram
![ERDiagram drawio (2)](https://github.com/yssuzen/3005final/assets/77358030/ac72343b-975c-4c41-9d44-039bc8f47a68)



# Database Schema
![databaseSchema drawio (2)](https://github.com/yssuzen/3005final/assets/77358030/550a1ce5-2b6f-4887-80f8-905ab034e152)



# DDL and DML
.SQL files are in the project repository.


# Design Decisions: Assumptions and Entity Definitions 
Assumptions
- **"Insert Into" Query Execution:**
- Assumption: All "Insert Into" queries will be executed after the corresponding tables have
been properly created and all necessary constraints and relationships are established.
- **User Sign-In After Registration:**
- Assumption: Users are required to log out and then log in to validate their credentials
and start using the system after registration.
- **User Input Syntax:**
- Assumption: Users will enter data in the correct format as required by input fields.
- **Linking Billing to Members:**
- Assumption: Each billing record is linked to a member's unique identifiers.
- **Shared Session Table for Trainers and Members:**
- Assumption: Trainers and members share a common table when they participate in a
session.
- **Administrative Interaction with Equipment and Rooms:**
- Assumption: Administrators manage equipment and room availability, including bookings
and maintenance.
- **Separate Booking Mechanisms for Members and Group Fitness:**
- Assumption: Members book for services like personal training sessions or group fitness
classes through different mechanisms or tables.


**Entity Definitions**
-Members: Individuals who register to access various fitness programs and services. They have
attributes such as name, email, phone number, and health metrics, which include fitness goals.
- Trainers: Certified professionals who provide personal training and lead group fitness classes.
Attributes include name, contact information, and availability.
- Administrative Staff: Manage and oversee the gym's operational aspects, such as room
bookings and equipment maintenance.
- Group Fitness Classes: Scheduled classes that are conducted in specific rooms and led by
trainers. Attributes might include class name, schedule, and associated room.
- Rooms: Physical locations within the gym where group fitness classes and potentially other
activities occur. Managed by the administrative staff.
- Equipment: Managed by the administrative staff, with details about maintenance and
availability for use in the gym.
- Billing: Stores the individual billings for the members.
- Personal Training Session: Stores the personal training session information, including the IDs
of both the trainers and the members taking part.

[Assumptions and Entity Definitions (1).pdf](https://github.com/yssuzen/3005final/files/14969104/Assumptions.and.Entity.Definitions.1.pdf)
