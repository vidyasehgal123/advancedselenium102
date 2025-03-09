import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define capabilities for parallel execution on LambdaTest
LT_CAPABILITIES = [
    {
        "browserName": "Chrome",
        "browserVersion": "128.0",
        "platformName": "Windows 10",
        "LT:Options": {
            "build": "LambdaTest Selenium Test",
            "name": "Test Scenario 1 - Chrome",
            "network": True,
            "video": True,
            "console": True,
            "visual": True,
        },
    },
    {
        "browserName": "MicrosoftEdge",
        "browserVersion": "127.0",
        "platformName": "macOS Ventura",
        "LT:Options": {
            "build": "LambdaTest Selenium Test",
            "name": "Test Scenario 2 - Edge",
            "network": True,
            "video": True,
            "console": True,
            "visual": True,
        },
    },
]
@pytest.mark.parametrize("capabilities", LT_CAPABILITIES)
def test_lambdatest_integration(capabilities):
    USERNAME = "vidya_sehgal"
    ACCESS_KEY = "iLSg7GQ9o7VmQY2klGpwM5FTrB8LGfyId3c3pZpZE67922SbBC"
    grid_url = f"https://{USERNAME}:{ACCESS_KEY}@hub.lambdatest.com/wd/hub"

    driver = webdriver.Remote(command_executor=grid_url, options=webdriver.ChromeOptions() if capabilities["browserName"] == "Chrome" else webdriver.EdgeOptions())
    driver.capabilities.update(capabilities)

    try:
        # 1. Navigate to the LambdaTest website
        driver.get("https://www.lambdatest.com")
        driver.maximize_window()

        # 2. Explicit wait till all elements are loaded
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # 3. Scroll to "Explore all Integrations" button
        explore_integrations = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'Explore all Integrations')]")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", explore_integrations)
        time.sleep(1)

        # 4. Click the link (should open in a new tab)
        explore_integrations.click()

        # 5. Save window handles
        window_handles = driver.window_handles
        print("Window Handles:", window_handles)
        assert len(window_handles) == 2, "New tab did not open!"

        # Switch to new tab
        driver.switch_to.window(window_handles[1])

        # 6. Verify URL
        expected_url = "https://www.lambdatest.com/integrations"
        WebDriverWait(driver, 10).until(EC.url_to_be(expected_url))
        assert driver.current_url == expected_url, f"URL Mismatch: Expected {expected_url}, Got {driver.current_url}"

        # 7. Scroll to "Codeless Automation"
        codeless_automation = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(),'Codeless Automation')]")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", codeless_automation)

        # 8. Click "INTEGRATE TESTING WHIZ WITH LAMBDATEST"
        testing_whiz = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'INTEGRATE TESTING WHIZ WITH LAMBDATEST')]")))
        testing_whiz.click()

        # 9. Verify page title
        expected_title = "TestingWhiz Integration With LambdaTest"
        WebDriverWait(driver, 10).until(EC.title_is(expected_title))
        assert driver.title == expected_title, f"Title Mismatch: Expected {expected_title}, Got {driver.title}"

        # 10. Close the current window
        driver.close()

        # Switch back to the first tab
        driver.switch_to.window(window_handles[0])

        # 11. Print current window count
        print("Current window count:", len(driver.window_handles))

        # 12. Navigate to blog page
        driver.get("https://www.lambdatest.com/blog")

        # 13. Click on "Community" link & verify URL
        community_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Community")))
        community_link.click()
        WebDriverWait(driver, 10).until(EC.url_to_be("https://community.lambdatest.com/"))
        assert driver.current_url == "https://community.lambdatest.com/", "Community URL Mismatch"

        # 14. Close the browser
        driver.quit()

    except Exception as e:
        print(f"Test failed: {str(e)}")
        driver.quit()
        raise
