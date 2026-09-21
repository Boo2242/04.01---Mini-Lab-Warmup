Title: Canvas Grade Checker

Description: This tool takes the courses the given user has and allows you to sort by term to choose a class to check your grade.

Instructions for use:

1. clone the github repository: "git clone https://github.com/Boo2242/04.01---Mini-Lab-Warmup.git"
2. install and run python venv "python -m venv venv" then "venv\Scripts\activate" for windows or "python3 -m venv venv" then "source venv/bin/activate" for Mac/Linux
3. install Flask: "pip install flask requests python-dotenv"
4. set up your .env file: using .env.example as a reference fill in and create a .env file
5. run the web dashboard: python app.py
6. to close the app use ctrl + C

APIs: This program uses the /api/v1/courses/:id/enrollments api to retrieve the grades from courses and the /api/v1/courses api to gather the courses and their term

Over all this project was rather challenging. I was able to successfully complete it but I had a rather hard time finding out how to actually use python and flask together. I had originally wanted to make a full page that showed each grade and had a calendar showing every assignment from classes. This would then allow users to click a link directly to the assignment to then access it. I was unable to do this as I had a few issues getting the classes to even show up by term.

I learned that moving forward I need to look ahead at these assignments. I also learned how to call a session token (at least for canvas) and how to effectively utilize them to interface with a secondary site. From there I was able to understand how to gather the necessary information with the help of the canvas knowledge base and AI helping to parse out when I needed the term keyword rather than the enrollment_term_id. Over all I believe I'm slowly but surely getting the hang of this, however I do feel as if I'm behind the curve in understanding still.