# QTI Quiz File Generator Using text2qti

This project allows instructors to generate QTI quiz files from text files using the text2qti tool. It includes a Python virtual environment for seamless setup and execution across macOS, Linux, and Windows platforms. Additionally, the project automates quiz creation and association with item banks in Canvas.

## Requirements

- Python 3.x installed on your system.
- Git installed to clone the repository.
- API token from Canvas (required to create quizzes programmatically).
- Canvas course number where the quiz will be created.

## Setup Instructions

### Step 1: Create a Local Directory and Clone the Repository
1. Create a directory on your local machine where you’ll store the project files:
```bash
mkdir quiz_generator
cd quiz_generator
```

2. Clone the GitHub repository into the directory:
```bash
git clone https://github.com/learn-co-curriculum/contentQTIQuizCreation.git
cd contentQTIQuizCreation
```
### Step 2: Prepare a Quiz Template
Before running the script, you need to create a quiz template in a text file. This file should follow the format provided in the `New Quiz Template(1).txt` file in the repository.

You can use GPT or any text editor to generate the template, ensuring it aligns with the examples. Save this file in the repository directory (e.g., `my_quiz.txt`).

### Step 3: Run the Python Script
1. Get your API token from Canvas:
    * Go to your Canvas profile settings and scroll to the "Approved Integrations" section.
    * Click "+ New Access Token" and give it a name.
    * Copy the API token that is generated (you’ll need it later).
2. Get the Canvas Course Number:
    * Navigate to your course in Canvas and note the course number (visible in the course URL).
3. Run the script to generate the QTI file and create the quiz in Canvas:
```bash
python3 activatevenv.py
```
You’ll be prompted to:

- Enter the name of the quiz text file you created (e.g., `my_quiz.txt`).
- Enter your Canvas course ID.
- Enter your Canvas API token.

The script will:

- Create a QTI zip file based on your quiz template.
- Programmatically create the quiz in your specified Canvas course.

### Step 4: Import the QTI File to Canvas Item Banks
1. Go to the Canvas course where you want to add the quiz.
2. Navigate to **Item Banks** and click **+ Bank**.
3. Give the item bank a name and share it with the course.
4. Click **Create Bank**.
5. After creating the item bank, click the three dots at the top of the page and select **Import Content**.
6. Navigate to the `contentQTIQuizCreation` folder (the folder you created earlier) and attach the correct zip file. This will import all the questions into the item bank.
7. Each question's title will represent the **Learning Objective (LO)**. To attach the LO as metadata:
   * Open each question.
   * Copy the question title (which is the LO).
   * Scroll to the bottom of the question editing screen and find the **Tags and Metadata** section.
   * Paste the LO into the **Tags and Metadata** section and click Done to save the changes.

### Step 5: Associate the Quiz with the Item Bank
1. After the quiz is created by the script, go to the quiz in Canvas and click **Build**.
2. Click Item Banks and select the item bank you just created.
3. Press the + All/Random button to add all questions to the quiz.
4. Edit the item bank quiz questions to choose 15 random questions for the quiz.

## Troubleshooting

### Permission Denied 
If you encounter a `Permission Denied` error when running the script, ensure that you have the necessary execution permissions for the script files:
```bash
chmod +x activatevenv.py
```

### Missing Dependencies
If the virtual environment is not set up properly, make sure that the dependencies are installed:
```bash
pip install -r requirements.txt
```

## Contributing

Feel free to contribute to this project by forking the repository and submitting a pull request. Make sure to include detailed information about any new features or fixes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.
