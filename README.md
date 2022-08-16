# CS50web Project4 - Network
This project is an assignment from the course: [CS50 Web Programming with Python and Javascript](https://cs50.harvard.edu/web/2020/).

## Assignment
Design a Twitter-like social network website for making posts and following users. Assignment details [here](https://cs50.harvard.edu/web/2020/projects/4/network/).

## Project Description
"Network" is a social media website written in Python and JavaScript and uses the framework “Django”. The website allows registered Users to create new posts, like/dislike existing posts and to follow other User-profiles. The User may edit existing posts. Further, the website filters the displayed posts based on the current subpage settings (all posts / the currently visited profile / only people the User follows). Unregistered visitors to the page may create a new Account. Without login in, the user will only have the possibility to read posts without interaction (like, follow).

## Technical Description
Django handles all server request and database entries in Python.
The database (models.py) consists of 3 types of models: User (default), Post and Profile (one-to-one related to User, with 2 asymmetrical Many-to-Many relations to self and to Post).
Updates in existing database entries (likes, follows) and client-side changes (static/buttonevents.js) are written in JavaScript using the “JS Fetch API” via PUT-request.
Django’s Pagination reduces the page’s length to only display 10 posts at a time.

## Project Demo
Click [here](https://youtu.be/clRNlMUcz9w) to watch a demonstration of this project on YouTube.

## Distribution Code 
[Distribution Code](https://cdn.cs50.net/web/2020/spring/projects/4/network.zip).
All further requirements and terminal commands to run this project are found on the [Project Assignment Page](https://cs50.harvard.edu/web/2020/projects/4/network/).
