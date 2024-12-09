import re
from playwright.sync_api import Page, sync_playwright, expect
from faker import Faker
import requests
from bs4 import BeautifulSoup

def generate_bangladeshi_phone_number(fake):
    prefixes = ["016", "017", "013", "019"]
    prefix = fake.random.choice(prefixes)
    number = fake.random_number(digits=8, fix_len=True)
    return f"{prefix}{number}"

def generate_nid_number(fake):
    length = fake.random.choice([10, 13])
    return str(fake.random_number(digits=length, fix_len=True))  # Ensure NID is a string

def extract_text_from_webpage(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    # Extract text from multiple tags
    tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'a', 'li']
    extracted_text = []
    for tag in tags:
        elements = soup.find_all(tag)
        for element in elements:
            extracted_text.append(element.get_text())
    return extracted_text

def test_example(page: Page) -> None:
    # Create a Faker instance
    fake = Faker()

    # Generate random data
    full_name = fake.name()
    dob = fake.date_of_birth(minimum_age=20, maximum_age=65).strftime("%Y-%m-%d")
    nationality = "Bangladeshi"  # Assuming nationality remains constant
    nid = generate_nid_number(fake)
    phone_number = generate_bangladeshi_phone_number(fake)
    email = fake.email()
    company = fake.company()
    position = fake.job()
    experience_years = str(fake.random_int(min=1, max=40))  # Ensure experience years is a string

    page.goto("https://dev-training.sla.gov.bd/")
    
    # Extract text from the webpage
    url = "https://dev-training.sla.gov.bd/"
    extracted_text = extract_text_from_webpage(url)
    for text in extracted_text:
        print(text)

    # Assert the page title to ensure the page has loaded correctly
    expect(page).to_have_title("SLA TMS")

    page.get_by_role("link", name="CXO Training").click()

    # Assert that the "Apply For Training" button is visible and clickable
    apply_button = page.get_by_role("button", name="Apply For Training")
    expect(apply_button).to_be_visible()
    apply_button.click()

    page.get_by_placeholder("Enter full name").click()
    page.get_by_placeholder("Enter full name").fill(full_name)
    page.get_by_label("Gender").select_option("Male")  # Assuming gender selection remains constant
    page.locator("#dobInput").fill(dob)
    page.get_by_placeholder("E.g., Bangladeshi").click()
    page.get_by_placeholder("E.g., Bangladeshi").fill(nationality)
    page.get_by_placeholder("10/13/17 digit NID number").fill(str(nid))  # Ensure NID is treated as string
    page.get_by_placeholder("01xxxxxxxx").click()
    page.get_by_placeholder("01xxxxxxxx").fill(str(phone_number))  # Ensure phone number is treated as string
    page.get_by_placeholder("example@mail.com").click()
    page.get_by_placeholder("example@mail.com").fill(email)
    page.get_by_label("Last Level of Education").select_option("Masters")
    page.get_by_placeholder("Enter your present company").click()
    page.get_by_placeholder("Enter your present company").fill(company)
    page.get_by_placeholder("Enter your current position").click()
    page.get_by_placeholder("Enter your current position").fill(position)
    page.get_by_placeholder("Enter your years of experience").click()
    page.get_by_placeholder("Enter your years of experience").fill(experience_years)

    submit_button = page.get_by_role("button", name="Submit")

    # Assert that the "Submit" button is visible and clickable
    expect(submit_button).to_be_visible()
    submit_button.click()

    # Assert that a success message or confirmation page appears
    success_message = page.locator("text=Your application has been submitted successfully")
    expect(success_message).to_be_visible()

    print("Form submission was successful with random data!")

# Run the test with Playwright
with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    test_example(page)
    browser.close()
    
#pytest test_script.py --html=report.html --self-contained-html
