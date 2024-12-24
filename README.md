# Clinic management system
A website which supports to manage Clinics.

# Table of contents
<ul>
  <li>Project participants</li>
  <li>General Information</li>
  <li>Technology used</li>
  <li>Features</li>
  <li>Setup</li>
  <li>Project status</li>
</ul>

# Project participants
<ul>
  <li>Châu Bình Nguyên</li>
  <li>Phạm Thế Nguyên</li>
  <li>Vương Minh Trí</li>
</ul>

# General Information
Nowadays, information technology is developing strongly, supporting management more conveniently and scientifically. 
Skills in analyzing, designing information systems and software processing play an important role in building effective 
software products, meeting the management needs of enterprises.

# Technology used
<ul>
  <li>Python: programming language. Version: 3.12.1.</li>
  <li>Python Flask: a web framework which helps to build and develop a web application.</li>
  <li>MySQL: a database management system which is used to manage data.</li>
</ul>

# Features
<h2>1. Make an appointment</h2>
<li>This function helps patients register for an appointment, the appointment will be sent 
  to the Nurse and the Nurse will filter and create an examination list of up to 40 
  people/examination list.</li>

<h2>2. Make a medical examination form</h2>
<li>This function allows the Doctor to create an examination form for the patient being examined.</li>

<h2>3. Make payment invoice</h2>
<li>This function allows the Cashier to bill the Patient.</li>

<h2>4. Statistical report</h2>
<li>The function allows the Administrator to report revenue and drug usage by month.</li>

# Setup

<h2>To run this project:</h2>
<ul>
    <li>Make sure the equipments has downloaded python.</li>
    <li>Use IDE like Pycharm or Visual Studio Code to run the project.</li>
    <li>Create virtual environment.</li>
    <li>Install everything according to file requirements.txt .</li>
    <li>Create a database in MySQL and declare the database's name and password of MySQL in file __init__.py . Fill in: "mysql+pymysql://root:%s@localhost/database's name?charset=utf8mb4" % quote ("password")</li>
    <li>Run file models.py to download data into database in MySQL</li>
    <li>Run file index.py to run the project.</li>
</ul>

# Project status

Project is under construction.
