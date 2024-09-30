import subprocess
import requests
import re
import os

# Replace these variables with actual values
school="https://flatironlearn.instructure.com:443"

#  Runs the text2qti command to generate the zip file from the given text file.
def run_text2qti(txt_file_name, quiz_title):
    # Sanitize the quiz title to create a valid file name
    sanitized_title = re.sub(r'\W+', '_', quiz_title).lower()

    # Create the new file name by replacing the original txt file name
    new_txt_file_name = f"{sanitized_title}.txt"

    # Rename the original text file to the sanitized one
    os.rename(txt_file_name, new_txt_file_name)

    try:
        # Run the text2qti command and generate the zip file using the new file name
        result = subprocess.run(["text2qti", new_txt_file_name], check=True)
        print(f"QTI zip file generated for {new_txt_file_name}")
    except subprocess.CalledProcessError as e:
        print(f"Error running text2qti: {e}")
        return None

    # The zip file will have the same name as the new txt file but with .zip extension
    return new_txt_file_name.replace(".txt", ".zip")

# Extract the quiz title from the first line of the text file
def extract_quiz_title(txt_file_name):
    with open(txt_file_name, 'r', encoding='utf-8-sig') as file:
        # Read the first line from the file, automatically removing the BOM
        first_line = file.readline().strip()
        print(f"First line (after BOM removal): {first_line}")  # Debugging print
        
        # Extract title using a simpler approach without regex
        if first_line.lower().startswith("quiz title:"):
            # Strip off 'Quiz title:' and return only the actual title
            title = first_line[len("Quiz title:"):].strip()
            return title  # Return only the title without 'Quiz:'
        else:
            print("Error: Could not find quiz title in the text file.")
            return None
        
# Search for the assignment group ID by name in the course
def get_assignment_group_id(course_id, access_token):
    url = f"{school}/api/v1/courses/{course_id}/assignment_groups"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        groups = response.json()
        for group in groups:
            if group['name'] == "Module Quizzes":
                return group['id']
        print("Error: Could not find 'Module Quizzes' assignment group.")
    else:
        print(f"Failed to fetch assignment groups: {response.text}")
    
    return None       
# Updates quiz settings such as attempts, time limits, shuffling, and result view settings.
def create_new_quiz(course_id, title, assignment_group_id, access_token):
    url = f"{school}/api/quiz/v1/courses/{course_id}/quizzes"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Replace the [Module Title/Topic] placeholder with the quiz title
    instructions = f"""
        <div class="dp-callout dp-callout-placeholder card dp-callout-position-default w-100 dp-callout-type-info dp-callout-color-dp-secondary dp-margin-direction-tblr" style="margin-top: 14px; margin-bottom: 14px;">
        <h3 class="dp-callout-side-emphasis"><span class="dp-icon icon-clock icon-Solid"><img src="/files/4301594/download?download_frd=1" alt="untitled.svg" width="54" height="54" data-inst-icon-maker-icon="True" data-download-url="/files/4301594/download?download_frd=1&amp;icon_maker_icon=1" /></span></h3>
        <h2 class="dp-callout-side-emphasis"><span class="dp-icon icon-clock icon-Solid">{title}</span></h2>
        <div class="dp-callout-side-emphasis">
            <p>Welcome to the module quiz! This is your opportunity to demonstrate what you have learned about the key concepts and skills covered in the {title} module. You will have <strong>15, </strong>randomly chosen, multiple choice questions on this quiz and three attempts. You can review each attempt; the highest score will be recorded in the gradebook.</p>
            <h4><strong>Quiz Instructions:</strong></h4>
            <ul>
                <li>Please read each question carefully before selecting your answer.</li>
                <li>Choose the best answer from the options provided for each question.</li>
                <li>Navigate between questions using the "Next" and "Previous" buttons.</li>
                <li>You can pin (<sup><img src="/courses/8089/files/4337864/preview?verifier=vXoZMo1qWxySJkv358f01PIY1iQSv08ItokGlFLh" alt="2024-08-06_11-27-10-1.png" width="13" height="13" /></sup>) questions for review before your final submission.</li>
                <li>Use the "Submit Quiz" button to complete your attempt.</li>
            </ul>
        </div>
    </div>
    """
    data = {
        'quiz[title]': f"Quiz: {title}",
        'quiz[instructions]': instructions,
        'quiz[assignment_group_id]': assignment_group_id,
        'quiz[points_possible]': 15,
        'quiz[grading_type]': 'points',
        'quiz[published]': True,

        # Quiz settings
        'quiz[quiz_settings][allow_backtracking]': 'true',
        'quiz[quiz_settings][shuffle_answers]': 'true',
        'quiz[quiz_settings][shuffle_questions]': 'false',
        'quiz[quiz_settings][require_student_access_code]': 'false',
        'quiz[quiz_settings][has_time_limit]': 'false',

        # Multiple attempts settings
        'quiz[quiz_settings][multiple_attempts][max_attempts]': 3,
        'quiz[quiz_settings][multiple_attempts][attempt_limit]': 'true',
        'quiz[quiz_settings][multiple_attempts][score_to_keep]': 'highest',
        'quiz[quiz_settings][multiple_attempts][multiple_attempts_enabled]': 'true',

        # Result view settings
        'quiz[quiz_settings][result_view_settings][display_items]': 'true',
        'quiz[quiz_settings][result_view_settings][display_item_feedback]': 'true',
        'quiz[quiz_settings][result_view_settings][display_item_response]': 'true',
        'quiz[quiz_settings][result_view_settings][display_points_awarded]': 'true',
        'quiz[quiz_settings][result_view_settings][result_view_restricted]': 'true',
        'quiz[quiz_settings][result_view_settings][display_item_response_correctness]': 'true'
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        print("Quiz created successfully!")
    else:
        print(f"Failed to create quiz: {response.text}")

if __name__ == "__main__":
    # Step 1: Ask the user for the text file name
    txt_file_name = input("Please enter the name of the quiz text file (e.g., newQuiz.txt): ")

    # Step 2: Extract the quiz title from the text file
    quiz_title = extract_quiz_title(txt_file_name)
    if not quiz_title:
        exit(1)
        
    # Step 3: Run text2qti to generate the QTI zip file with the title as the zip name
    zip_file_name = run_text2qti(txt_file_name, quiz_title)

    # Step 4: Ask for the Canvas course ID, API token, and retrieve assignment group ID
    course_id = input("Please enter the Canvas course ID: ")
    access_token = input("Please enter your Canvas API access token: ")
    assignment_group_id = get_assignment_group_id(course_id, access_token)
    if not assignment_group_id:
        exit(1)

    # Step 5: Create the new quiz in Canvas with the extracted title and assignment group ID
    create_new_quiz(course_id, quiz_title, assignment_group_id, access_token)
