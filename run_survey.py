import sys
from playwright.sync_api import sync_playwright, TimeoutError

SLEEP_TIME = 0.5
TESTING = False

def debug_pause(message):
    if TESTING:
        input(message)

def complete_panda_survey(survey_code, email):
    survey_code_formatted = survey_code.replace('-', '')
    if len(survey_code_formatted) < 24:
        raise ValueError("Survey code must be at least 24 characters long.")

    if ('-' not in survey_code_formatted) and len(survey_code_formatted) == 25:
        # Add dashes after first 4, 9, 13, 17, and 21 characters (e.g., 1234-56789-0123-4567-8901-2345)
        survey_code_formatted = survey_code_formatted[:4] + '-' + survey_code_formatted[4:9] + '-' + survey_code_formatted[9:13] + '-' + survey_code_formatted[13:17] + '-' + survey_code_formatted[17:21] + '-' + survey_code_formatted[21:25]
    
    with sync_playwright() as p:
        # 1. Launch Browser
        browser = p.chromium.launch(headless=True) # Use headless=False for local testing
        
        page = browser.new_page()

        try:
            # 2. Navigate and Enter Code
            print("Navigating to survey website...")
            page.goto(f"https://www.pandaguestexperience.com/?cn={survey_code_formatted}&source=QR25")
            
            print(f"Entering survey code: {survey_code_formatted}")
            
            debug_pause("Code entered. Press Enter to continue...") # Debugging pause

            # # Split survey_code into 6 chunks of 4 digits each
            # chunks = [survey_code[i:i+4] for i in range(0, 24, 4)]
            # for idx, chunk in enumerate(chunks, start=1):
            #     page.locator(f"#CN{idx}").fill(chunk)
            page.locator("#NextButton").click()
            # time.sleep(0.5)
                        
            # Page 1
            print("Page 1...")
            page.locator(".Opt5").click()
            page.locator("#NextButton").click()
            # time.sleep(0.5)

            debug_pause("Page 1 complete. Press Enter to continue...") # Debugging pause
            
            if page.get_by_text("Thank you for your interest in taking our survey").is_visible():
                print("Code is expired.")
                browser.close()
                return "EXPIRED"

            if page.get_by_text("Please select your visit type:").is_visible():
                print("Online Order...")
                # Mode 1
                # Page 2
                print("Page 2...")
                page.get_by_text("Online order pick-up").click()
                page.locator("#NextButton").click()
                # time.sleep(1)
                
                # Page 3
                print("Page 3...")
                page.get_by_text("Panda mobile app").click()
                page.locator("#NextButton").click()
            
            debug_pause("Page 3 complete. Press Enter to continue...") # Debugging pause

            # Page 4
            print("Page 4...")
            all_highly_satisfied = page.locator("td.Opt5")
            for option in all_highly_satisfied.all():
                option.click()
            page.locator("#NextButton").click()

            debug_pause("Page 4 complete. Press Enter to continue...") # Debugging pause

            # Page 5
            print("Page 5...")
            all_highly_satisfied = page.locator("td.Opt5")
            for option in all_highly_satisfied.all():
                option.click()
            page.locator("#NextButton").click()

            debug_pause("Page 5 complete. Press Enter to continue...") # Debugging pause
            
            # Page 6
            print("Page 6...")
            page.get_by_text("Prior positive experience").click()
            page.locator("#NextButton").click()
            
            debug_pause("Page 6 complete. Press Enter to continue...") # Debugging pause

            # Page 7
            print("Page 7...")
            page.locator("td.Opt2").click()
            page.locator("#NextButton").click()

            debug_pause("Page 7 complete. Press Enter to continue...") # Debugging pause
            
            # Page 8
            print("Page 8...")
            all_highly_satisfied = page.locator("td.Opt5")
            for option in all_highly_satisfied.all():
                option.click()
            page.locator("#NextButton").click()

            debug_pause("Page 8 complete. Press Enter to continue...") # Debugging pause
            
            # Page 9
            print("Page 9...")
            page.locator("#S000077").fill("Service was exceptional. Food was delicious as always. Portion sizes were adequate, but could have been better.")
            page.locator("#NextButton").click()
            debug_pause("Page 9 complete. Press Enter to continue...") # Debugging pause
            
            # Page 10
            print("Page 10...")
            page.locator("td.Opt2").click()
            page.locator("#NextButton").click()
            debug_pause("Page 10 complete. Press Enter to continue...") # Debugging pause
            
            # Page 11
            print("Page 11...")
            page.get_by_text("Four or more times").click()
            page.locator("#NextButton").click()
            debug_pause("Page 11 complete. Press Enter to continue...") # Debugging pause
            
            # Page 12
            print("Page 12...")
            page.locator("#S000057").fill(email)
            page.locator("#S000064").fill(email)
            page.locator("#NextButton").click()
            debug_pause("Page 12 complete. Press Enter to continue...") # Debugging pause
                
            print("Survey submitted successfully!")
            debug_pause("Survey complete. Press Enter to continue...") # Debugging pause
            browser.close()
            return "SUCCESS"

        except TimeoutError:
            debug_pause("Timeout hit. Press Enter to continue...")
            print("Error: A page element took too long to load.")
            browser.close()
            return "ERROR: Page timeout"
        except Exception as e:
            debug_pause("Unexpected error. Press Enter to continue...")
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
