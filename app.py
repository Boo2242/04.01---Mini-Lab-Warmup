import os
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request

load_dotenv()

app = Flask(__name__)

CANVAS_API_TOKEN = os.getenv("CANVAS_API_TOKEN")
CANVAS_BASE_URL = os.getenv("CANVAS_BASE_URL", "https://boisestatecanvas.instructure.com")

def get_canvas_headers():
    return {
        "Authorization": f"Bearer {CANVAS_API_TOKEN}"
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    if not CANVAS_API_TOKEN:
        return "Error: CANVAS_API_TOKEN is missing from your .env file!", 500

    # Endpoint 1: Fetch ALL courses across pages using Link header pagination
    courses_url = f"{CANVAS_BASE_URL}/api/v1/courses"
    courses_params = {
        "enrollment_type": "student",
        "enrollment_state": "active",
        "include[]": "term",
        "per_page": 50  # Request up to 50 items per page to reduce round trips
    }

    all_courses = []
    current_url = courses_url

    try:
        # Loop through paginated responses
        while current_url:
            # Note: params are only passed on the initial call; next links in Canvas already include pagination parameters
            response = requests.get(
                current_url, 
                headers=get_canvas_headers(), 
                params=courses_params if current_url == courses_url else None
            )
            response.raise_for_status()
            
            page_data = response.json()
            all_courses.extend(page_data)

            # Canvas uses the HTTP Link header to point to the next page
            # Example header: <https://.../courses?page=2>; rel="next", <https://.../courses?page=1>; rel="first"
            link_header = response.headers.get('Link')
            current_url = None
            
            if link_header:
                links = link_header.split(',')
                for link in links:
                    if 'rel="next"' in link:
                        # Extract the URL inside the angle brackets <...>
                        current_url = link.split(';')[0].strip('<> ')
                        break

    except requests.exceptions.RequestException as e:
        return f"Error fetching courses: {e}", 500

    # Extract unique terms from ALL fetched courses across all pages
    terms = {}
    for course in all_courses:
        term_info = course.get('term')
        if term_info:
            terms[term_info['id']] = term_info['name']

    # Read selected term and course IDs from form submission
    selected_term_id = request.form.get('term_id') if request.method == 'POST' else None
    selected_course_id = request.form.get('course_id') if request.method == 'POST' else None

    # Filter courses list by term if selected
    if selected_term_id:
        displayed_courses = [c for c in all_courses if str(c.get('enrollment_term_id')) == str(selected_term_id)]
    else:
        displayed_courses = all_courses

    selected_course = None
    enrollment_details = None

    # Handle course lookup from the complete master list
    if selected_course_id:
        selected_course = next((c for c in all_courses if str(c['id']) == str(selected_course_id)), None)

        if selected_course:
            # Endpoint 2: Fetch specific enrollment/grade details for the selected course ID
            enrollment_url = f"{CANVAS_BASE_URL}/api/v1/courses/{selected_course_id}/enrollments"
            enrollment_params = {"user_id": "self"}

            try:
                enrollment_response = requests.get(enrollment_url, headers=get_canvas_headers(), params=enrollment_params)
                enrollment_response.raise_for_status()
                enrollments = enrollment_response.json()
                
                if enrollments:
                    enrollment_details = enrollments[0]
            except requests.exceptions.RequestException as e:
                return f"Error fetching enrollment details: {e}", 500

    return render_template(
        'index.html',
        courses=displayed_courses,
        selected_course=selected_course,
        enrollment_details=enrollment_details,
        terms=terms,
        selected_term_id=selected_term_id
    )

if __name__ == '__main__':
    app.run(debug=True)