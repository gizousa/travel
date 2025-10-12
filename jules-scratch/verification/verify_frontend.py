import time
from playwright.sync_api import Page, expect

def test_travel_assistant_page(page: Page):
    """
    This test verifies that the user can navigate to the AI Travel Assistant
    page and that the new layout is displayed correctly.
    """
    print("Navigating to the application...")
    page.goto("http://localhost:8501")
    page.wait_for_load_state()
    time.sleep(2)  # Add a delay
    print("Initial load complete.")
    page.screenshot(path="jules-scratch/verification/01_initial_load.png")
    print("Screenshot 1 taken.")

    print("Clicking on 'AI差旅助手'...")
    travel_assistant_radio = page.locator('text="AI差旅助手"')
    travel_assistant_radio.click()
    page.wait_for_load_state()
    time.sleep(2)  # Add a delay
    print("Clicked on 'AI差旅助手'.")
    page.screenshot(path="jules-scratch/verification/02_travel_assistant.png")
    print("Screenshot 2 taken.")

    print("Checking for 'AI差旅助手' heading...")
    expect(page.locator('text="AI差旅助手"').first).to_be_visible()
    print("Heading found.")

    print("Clicking on 'AI接待'...")
    receptionist_radio = page.locator('text="AI接待"')
    receptionist_radio.click()
    page.wait_for_load_state()
    time.sleep(2)  # Add a delay
    print("Clicked on 'AI接待'.")
    page.screenshot(path="jules-scratch/verification/03_receptionist.png")
    print("Screenshot 3 taken.")

    print("Checking for 'AI接待' heading...")
    expect(page.locator('text="AI接待"').first).to_be_visible()
    print("Heading found.")

    print("Clicking on '企业内部知识库'...")
    knowledge_base_radio = page.locator('text="企业内部知识库"')
    knowledge_base_radio.click()
    page.wait_for_load_state()
    time.sleep(2)  # Add a delay
    print("Clicked on '企业内部知识库'.")
    page.screenshot(path="jules-scratch/verification/04_knowledge_base.png")
    print("Screenshot 4 taken.")

    print("Checking for '企业内部知识库' heading...")
    expect(page.locator('text="企业内部知识库"').first).to_be_visible()
    print("Heading found.")
    print("Verification complete.")