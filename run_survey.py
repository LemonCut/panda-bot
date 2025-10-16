import sys
import time
from playwright.sync_api import sync_playwright, TimeoutError

def complete_panda_survey(survey_code, email):
    if len(survey_code) != 24:
        raise ValueError("Survey code must be exactly 24 characters long.")
    with sync_playwright() as p:
        # 1. Launch Browser
        browser = p.chromium.launch(headless=False) # Use headless=False for local testing
        page = browser.new_page()

        try:
            # 2. Navigate and Enter Code
            print("Navigating to survey website...")
            page.goto("https://www.pandaguestexperience.com/")
            
            print(f"Entering survey code: {survey_code}")
            
            # Split survey_code into 6 chunks of 4 digits each
            chunks = [survey_code[i:i+4] for i in range(0, 24, 4)]
            for idx, chunk in enumerate(chunks, start=1):
                page.locator(f"#CN{idx}").fill(chunk)

            page.locator("#NextButton").click()

            # --- THIS IS WHERE THE MAIN LOGIC WILL GO ---
            # 3. Answer Survey Questions
            # This part will require you to find the specific selectors
            # for the "Highly Satisfied" options and "Next" buttons.

            # 4. Enter Email
            # Find the email input and submit button selectors.

            input("Press [Enter] to continue.")

            # 5. Confirm and Finish
            print("Survey submitted successfully!")
            browser.close()
            return "SUCCESS"

        except TimeoutError:
            print("Error: A page element took too long to load.")
            browser.close()
            return "ERROR: Page timeout"
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            browser.close()
            return f"ERROR: {e}"

if __name__ == "__main__":
    # This allows you to test the script directly from the command line
    if len(sys.argv) != 3:
        print("Usage: python3 run_survey.py <survey_code> <email>")
    else:
        code = sys.argv[1]
        user_email = sys.argv[2]
        result = complete_panda_survey(code, user_email)
        print(f"Script finished with status: {result}")