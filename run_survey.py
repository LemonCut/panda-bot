import sys
import time
from playwright.sync_api import sync_playwright, TimeoutError

SLEEP_TIME = 0.5

def complete_panda_survey(survey_code, email):
    survey_code = survey_code.replace('-', '')
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
            # time.sleep(0.5)
                        
            # Page 1
            page.locator(".Opt5").click()
            page.locator("#NextButton").click()
            # time.sleep(0.5)
            
            question_text = page.locator("#textR000005").inner_text()
            if question_text == "Please select your visit type:":
                # Mode 1
                # Page 2
                page.get_by_text("Online order pick-up").click()
                page.locator("#NextButton").click()
                # time.sleep(1)
                
                # Page 3
                page.get_by_text("Panda mobile app").click()
                page.locator("#NextButton").click()
                
                # Page 4
                all_highly_satisfied = page.locator("td.Opt5")
                for option in all_highly_satisfied.all():
                    option.click()
                page.locator("#NextButton").click()

                # Page 5
                all_highly_satisfied = page.locator("td.Opt5")
                for option in all_highly_satisfied.all():
                    option.click()
                page.locator("#NextButton").click()
                
                # Page 6
                page.get_by_text("Prior positive experience").click()
                page.locator("#NextButton").click()
                
                # Page 7
                page.locator("td.Opt2").click()
                page.locator("#NextButton").click()
                
                # Page 8
                all_highly_satisfied = page.locator("td.Opt5")
                for option in all_highly_satisfied.all():
                    option.click()
                page.locator("#NextButton").click()
                
                # Page 9
                page.locator("#S000077").fill("Service was exceptional. Food was delicious as always. Portion sizes were adequate, but could have been better.")
                page.locator("#NextButton").click()
                
                # Page 10
                page.locator("td.Opt2").click()
                page.locator("#NextButton").click()
                
                # Page 11
                page.get_by_text("Four or more times").click()
                page.locator("#NextButton").click()
                
                # Page 12
                page.locator("#S000057").fill(email)
                page.locator("#S000064").fill(email)
                input()
                page.locator("#NextButton").click()
            else:
                # Mode 2
                pass
            

            # --- THIS IS WHERE THE MAIN LOGIC WILL GO ---
            # 3. Answer Survey Questions
            # This part will require you to find the specific selectors
            # for the "Highly Satisfied" options and "Next" buttons.

            # 4. Enter Email
            # Find the email input and submit button selectors.

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