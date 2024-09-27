import os
import platform
import subprocess

def activate_venv():
    # Detect the operating system
    user_os = platform.system()
    
    if user_os == "Linux" or user_os == "Darwin":  # Darwin is macOS
        venv_activate = "./text2qti-env/bin/activate"
        activate_command = f"source {venv_activate}"
    elif user_os == "Windows":
        venv_activate = ".\\text2qti-env\\Scripts\\activate"
        activate_command = venv_activate
    else:
        raise Exception("Unsupported operating system.")

    # Activate the virtual environment and run the script
    print(f"Activating virtual environment for {user_os}...")
    subprocess.call(activate_command, shell=True)

    # Run your QTI script after activation
    try:
        subprocess.run(["python", "run_text2qti.py"], check=True)
        print("QTI file generated successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running the script: {e}")

if __name__ == "__main__":
    activate_venv()
