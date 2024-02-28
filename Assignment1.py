import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

driver.get("https://testpages.herokuapp.com/styled/tag/dynamic-table.html")
driver.find_element(By.XPATH, "//summary[normalize-space()='Table Data']").click()

# Wait for the textarea to be present
textarea = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//textarea[@id='jsondata']"))
)

# Clear existing content
textarea.clear()

# Accessing Local JSON file

Jsonfile = open('test.json', 'r')
data = json.load(Jsonfile)


# Convert list of dictionaries to JSON string
json_data = json.dumps(data, indent=2)

# Send JSON data to the textarea
textarea.send_keys(json_data)
driver.find_element(By.XPATH, "//button[@id='refreshtable']").click()

# Extract data from the table
table_rows = driver.find_elements(By.XPATH, '//*[@id="dynamictable"]/tr')

# Verifying No. of rows
print(len(table_rows))

# Initialize a list to store extracted data
extracted_data = []
# Loop through each row and extract data
for row in table_rows[1:]:
    columns = row.find_elements(By.XPATH, './td')  # Updated XPath to select cells within each row

    # Check if the row has the expected number of cells (in this case, 3)
    if len(columns) == 3:
        name = columns[0].text
        age = int(columns[1].text)
        gender = columns[2].text
        extracted_data.append({"name": name, "age": age, "gender": gender})
    else:
        print(f"Skipping row: {row.text} as it doesn't have the expected number of cells.")

print(extracted_data)
''''

for row in table_rows:
    columns = row.find_elements(By.XPATH, './td')
    name = columns[0].text
    age = int(columns[1].text)
    gender = columns[2].text
    extracted_data.append({"name": name, "age": age, "gender": gender})
    print(extracted_data)

'''
# Referencing the json file to find assertion
reference_file_path = "test.json"

# Handling errors
try:
    # Read the data from the reference JSON file
    with open(reference_file_path, 'r') as reference_json_file:
        reference_data = json.load(reference_json_file)

    # Compare the extracted data with the reference data
    assert extracted_data == reference_data, "Data mismatch between extracted data and reference JSON file."

    print("Assertion passed: Data matches with the reference JSON file.")

except FileNotFoundError:
    print(f"Reference JSON file '{reference_file_path}' not found.")
except AssertionError as e:
    print(f"Assertion failed: {e}")


time.sleep(5)

# Close the browser
driver.quit()



