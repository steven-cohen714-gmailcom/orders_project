"""
Requisition System Integration Test Suite
----------------------------------------
A comprehensive test suite that validates the full requisition pipeline
from login through submission to database storage and frontend display.
"""

import os
import sys
import json
import time
import requests
import unittest
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime, timedelta
import uuid
import re

# Install required packages with:
# pip install selenium requests webdriver-manager

class TestResult:
    """Stores the result of a single test case with before/after state"""
    def __init__(self, name):
        self.name = name
        self.start_time = datetime.now()
        self.end_time = None
        self.passed = False
        self.before_state = {}
        self.after_state = {}
        self.assertions = []
        self.error = None
        self.stacktrace = None
    
    def add_assertion(self, assertion_name, passed, expected=None, actual=None):
        """Add a single assertion result"""
        self.assertions.append({
            "name": assertion_name,
            "passed": passed,
            "expected": expected,
            "actual": actual
        })
    
    def set_before_state(self, state):
        """Set the before state snapshot"""
        self.before_state = state
    
    def set_after_state(self, state):
        """Set the after state snapshot"""
        self.after_state = state
    
    def set_error(self, error, stacktrace):
        """Record an error with stacktrace"""
        self.error = str(error)
        self.stacktrace = stacktrace
    
    def finalize(self, passed):
        """Mark the test as complete with final result"""
        self.passed = passed
        self.end_time = datetime.now()
    
    def to_dict(self):
        """Convert to dictionary for serialization"""
        return {
            "name": self.name,
            "duration": (self.end_time - self.start_time).total_seconds() if self.end_time else None,
            "passed": self.passed,
            "before_state": self.before_state,
            "after_state": self.after_state,
            "assertions": self.assertions,
            "error": self.error,
            "stacktrace": self.stacktrace
        }
    
    def __str__(self):
        """Format the test result for display"""
        result = f"Test: {self.name}\n"
        result += f"Status: {'PASSED' if self.passed else 'FAILED'}\n"
        result += f"Duration: {(self.end_time - self.start_time).total_seconds():.2f}s\n\n"
        
        # Print before state
        result += "Before State:\n"
        result += json.dumps(self.before_state, indent=2) + "\n\n"
        
        # Print after state
        result += "After State:\n"
        result += json.dumps(self.after_state, indent=2) + "\n\n"
        
        # Print assertions
        result += "Assertions:\n"
        for assertion in self.assertions:
            status = "✓" if assertion["passed"] else "✗"
            result += f"{status} {assertion['name']}\n"
            if not assertion["passed"]:
                result += f"  Expected: {assertion['expected']}\n"
                result += f"  Actual:   {assertion['actual']}\n"
        
        # Print error
        if self.error:
            result += "\nError:\n"
            result += self.error + "\n\n"
            result += "Stacktrace:\n"
            result += self.stacktrace + "\n"
        
        return result

class ValidationSuite:
    """Collects and summarizes multiple test results"""
    def __init__(self):
        self.results = []
    
    def add_result(self, result):
        """Add a test result to the suite"""
        self.results.append(result)
    
    def print_summary(self):
        """Print a summary of all test results"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed
        
        print("\n===== VALIDATION SUMMARY =====")
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Success Rate: {(passed/total)*100:.2f}%")
        print("=============================\n")
        
        for result in self.results:
            print(result)
            print("-----------------------------\n")
    
    def has_failures(self):
        """Check if any tests failed"""
        return any(not r.passed for r in self.results)

class DatabaseHelper:
    """Helper for database operations via API"""
    def __init__(self, base_url):
        self.base_url = base_url
    
    def get_requisition_count(self):
        """Get the total number of requisitions"""
        response = requests.get(f"{self.base_url}/api/requisitions")
        if response.status_code == 200:
            return len(response.json())
        return 0
    
    def get_transaction_count(self):
        """Get the total number of transactions"""
        response = requests.get(f"{self.base_url}/api/transactions")
        if response.status_code == 200:
            return len(response.json())
        return 0
    
    def get_requisition_by_order_number(self, order_number):
        """Get a requisition by its order number"""
        response = requests.get(f"{self.base_url}/api/requisitions")
        if response.status_code == 200:
            requisitions = response.json()
            return [r for r in requisitions if r.get("order_number") == order_number]
        return []
    
    def get_requisition_items(self, requisition_id):
        """Get all items for a requisition"""
        response = requests.get(f"{self.base_url}/api/requisition_items/{requisition_id}")
        if response.status_code == 200:
            return response.json()
        return []
    
    def get_transaction_by_order_number(self, order_number):
        """Get a transaction by its order number"""
        response = requests.get(f"{self.base_url}/api/transactions")
        if response.status_code == 200:
            transactions = response.json()
            return [t for t in transactions if t.get("order_number") == order_number]
        return []
    
    def get_next_order_number(self):
        """Get the next order number from settings"""
        response = requests.get(f"{self.base_url}/api/settings/order_number_start")
        if response.status_code == 200:
            data = response.json()
            return data.get("order_number_start", 1000)
        return 1000

class RequisitionSystemTests:
    """Main test suite for the requisition system"""
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.validation = ValidationSuite()
        
        # Setup WebDriver for browser automation
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service
        
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.implicitly_wait(10)
        
        # Setup database helper
        self.db = DatabaseHelper(self.base_url)
    
    def teardown(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()
    
    def login(self, username="Steven"):
        """Log in to the application"""
        self.driver.get(self.base_url)
        
        try:
            # Check if already logged in
            if "currentUser" in self.driver.page_source:
                current_user = self.driver.find_element(By.ID, "currentUser").text
                if username in current_user:
                    return True
            
            # Enter username
            username_input = self.driver.find_element(By.ID, "username")
            username_input.clear()
            username_input.send_keys(username)
            
            # Submit form
            login_form = self.driver.find_element(By.ID, "loginForm")
            login_form.submit()
            
            # Wait for login to complete
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "mainApp"))
            )
            
            return True
        except Exception as e:
            print(f"Login failed: {e}")
            return False
    
    def fill_requisition_form(self, data):
        """Fill out the requisition form with test data"""
        # Navigate to form tab
        self.driver.get(self.base_url)
        
        # Wait for page to fully load
        time.sleep(5)
        print("Page loaded, checking for new requisition tab...")
        
        # Set a longer wait time
        wait = WebDriverWait(self.driver, 30)
        
        # Ensure we're on the new requisition tab
        try:
            # Try explicit wait first
            print("Waiting for new requisition tab button...")
            new_req_tab = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.tab-button[onclick=\"showTab('new-requisition')\"]"))
            )
            print("Found tab button, clicking...")
            new_req_tab.click()
            print("Tab button clicked")
        except Exception as e:
            print(f"Error clicking tab button: {e}")
            # If direct click fails, try JavaScript click as fallback
            try:
                print("Attempting fallback method to find tab...")
                new_req_tab = self.driver.find_element(By.CSS_SELECTOR, "button.tab-button[onclick=\"showTab('new-requisition')\"]")
                print("Found tab via fallback, executing JavaScript click...")
                self.driver.execute_script("arguments[0].click();", new_req_tab)
                print("JavaScript click executed")
            except Exception as e2:
                print(f"Fallback method failed: {e2}")
                # Direct JavaScript call to the function as last resort
                print("Last resort: directly calling showTab function...")
                self.driver.execute_script("showTab('new-requisition');")
                print("showTab function called directly")
        
        # Wait for the form to be visible
        print("Waiting for requisition form to become visible...")
        wait.until(
            EC.visibility_of_element_located((By.ID, "requisitionForm"))
        )
        print("Form is now visible")
        
        # Fill form fields
        if "requestDate" in data:
            print("Setting request date...")
            date_input = wait.until(
                EC.element_to_be_clickable((By.ID, "requestDate"))
            )
            date_input.clear()
            date_input.send_keys(data["requestDate"])
            print("Request date set")
        
        if "requester" in data:
            print("Setting requester...")
            self.driver.find_element(By.ID, "requester").send_keys(data["requester"])
            print("Requester set")
        
        if "supplier" in data:
            print("Setting supplier...")
            self.driver.find_element(By.ID, "supplier").send_keys(data["supplier"])
            print("Supplier set")
        
        if "note" in data:
            print("Setting note...")
            self.driver.find_element(By.ID, "note").send_keys(data["note"])
            print("Note set")
        
        # Fill stock items
        print(f"About to fill {len(data.get('items', []))} stock items...")
        for i, item in enumerate(data.get("items", [])):
            print(f"Filling stock item {i+1}...")
            # If not first item, add new row
            if i > 0:
                print("Adding new row...")
                add_button = self.driver.find_elements(By.CSS_SELECTOR, ".action-square.green-square")[0]
                add_button.click()
                print("New row added")
            
            # Get all stock item rows
            rows = self.driver.find_elements(By.CSS_SELECTOR, ".stock-item-row")
            row = rows[i]
            
            # Select stock code
            print("Selecting stock code...")
            stock_select = row.find_element(By.CSS_SELECTOR, "select[name='stockCode[]']")
            wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "select[name='stockCode[]'] option:nth-child(2)"))
            )
            options = stock_select.find_elements(By.TAG_NAME, "option")
            for option in options:
                if item.get("stockCode", "") in option.text:
                    option.click()
                    print(f"Selected stock code: {option.text}")
                    break
            else:
                # If not found, pick first non-empty
                for option in options:
                    if option.get_attribute("value"):
                        option.click()
                        print(f"Selected first available stock code: {option.text}")
                        break
            
            # Select project code
            print("Selecting project code...")
            wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "select[name='projectCode[]']"))
            )
            project_select = row.find_element(By.CSS_SELECTOR, "select[name='projectCode[]']")
            options = project_select.find_elements(By.TAG_NAME, "option")
            for option in options:
                if option.get_attribute("value"):
                    option.click()
                    print(f"Selected project code: {option.text}")
                    break
            
            # Select sub category (wait for it to populate)
            print("Waiting for subcategories to populate...")
            try:
                wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "select[name='subCategory[]'] option:nth-child(2)"))
                )
                subcat_select = row.find_element(By.CSS_SELECTOR, "select[name='subCategory[]']")
                options = subcat_select.find_elements(By.TAG_NAME, "option")
                if len(options) > 1:
                    options[1].click()
                    print(f"Selected subcategory: {options[1].text}")
            except Exception as e:
                print(f"Error selecting subcategory: {e}, continuing anyway...")
            
            # Fill units and price
            print("Setting units...")
            units_input = row.find_element(By.CSS_SELECTOR, "input[name='units[]']")
            units_input.clear()
            units_input.send_keys(str(item.get("units", 1)))
            print(f"Units set to {item.get('units', 1)}")
            
            print("Setting price...")
            price_input = row.find_element(By.CSS_SELECTOR, "input[name='price[]']")
            price_input.clear()
            price_input.send_keys(str(item.get("price", 100)))
            print(f"Price set to {item.get('price', 100)}")
            
        print("Form filling complete")
    
    def submit_form(self, expect_alert=True):
        """Submit the requisition form"""
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "#requisitionForm button[type='submit']")
        submit_button.click()
        
        if expect_alert:
            try:
                # Wait for alert and accept it
                WebDriverWait(self.driver, 10).until(EC.alert_is_present())
                alert = self.driver.switch_to.alert
                alert_text = alert.text
                alert.accept()
                return alert_text
            except TimeoutException:
                return None
        return None
    
    def check_session_active(self):
        """Check if user session is still active"""
        try:
            # Try to access currentUser element - should be visible if logged in
            current_user = self.driver.find_element(By.ID, "currentUser").text
            return len(current_user) > 0
        except:
            # If element not found, session likely ended
            return False
    
    def check_login_screen_visible(self):
        """Check if login screen is visible (user logged out)"""
        try:
            login_screen = self.driver.find_element(By.ID, "loginScreen")
            return login_screen.is_displayed()
        except:
            return False
    
    def check_transaction_in_audit_trail(self, order_number):
        """Check if a transaction appears in the audit trail tab"""
        # Navigate to audit trail tab
        self.driver.get(self.base_url)
        
        # Wait for page to fully load
        time.sleep(2)
        
        try:
            # Try explicit wait first
            audit_tab = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.tab-button[onclick=\"showTab('audit-trail')\"]"))
            )
            audit_tab.click()
        except:
            # If direct click fails, try JavaScript click as fallback
            try:
                audit_tab = self.driver.find_element(By.CSS_SELECTOR, "button.tab-button[onclick=\"showTab('audit-trail')\"]")
                self.driver.execute_script("arguments[0].click();", audit_tab)
            except:
                # Direct JavaScript call to the function as last resort
                self.driver.execute_script("showTab('audit-trail');")
        
        # Wait for data to load
        time.sleep(2)
        
        # Check if transaction is in table
        try:
            transactions_table = self.driver.find_element(By.ID, "transactionsTableBody")
            rows = transactions_table.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) > 1 and order_number in cells[1].text:
                    return True
            return False
        except:
            return False
    
    def test_standard_requisition_submission(self):
        """
        Test a standard requisition submission flow from end to end
        
        Validates:
        - Login works
        - Form submission succeeds
        - Requisition is saved to database
        - Items are saved to database
        - Transaction is created
        - Order number increments
        - Session remains active
        - Audit trail shows the transaction
        """
        test_result = TestResult("Standard Requisition Submission")
        
        try:
            # Login
            logged_in = self.login()
            test_result.add_assertion("Login successful", logged_in)
            
            if not logged_in:
                raise Exception("Failed to login, cannot continue test")
            
            # Get initial state
            next_order_number = self.db.get_next_order_number()
            formatted_order_number = f"ORD-{next_order_number}"
            req_count_before = self.db.get_requisition_count()
            txn_count_before = self.db.get_transaction_count()
            
            before_state = {
                "next_order_number": next_order_number,
                "requisition_count": req_count_before,
                "transaction_count": txn_count_before,
                "logged_in": True
            }
            test_result.set_before_state(before_state)
            
            # Fill form with test data
            test_data = {
                "requestDate": "12/04/2024",
                "requester": "Integration Test",
                "supplier": "Validation Supplier",
                "note": "End-to-end integration test",
                "items": [
                    {"stockCode": "AB", "units": 5, "price": 100},
                    {"stockCode": "CD", "units": 2, "price": 200}
                ]
            }
            self.fill_requisition_form(test_data)
            
            # Submit form
            alert_text = self.submit_form()
            form_submitted = alert_text and "success" in alert_text.lower()
            test_result.add_assertion("Form submitted successfully", form_submitted, 
                                     "Alert with success message", alert_text)
            
            # Wait for processing
            time.sleep(3)
            
            # Check if still logged in
            still_logged_in = self.check_session_active()
            logged_out = self.check_login_screen_visible()
            test_result.add_assertion("Session remained active", still_logged_in,
                                     "User still logged in", f"Logged in: {still_logged_in}, Login screen visible: {logged_out}")
            
            # Get updated state from database
            req_count_after = self.db.get_requisition_count()
            txn_count_after = self.db.get_transaction_count()
            current_order_number = self.db.get_next_order_number()
            
            # Check requisition in database
            requisitions = self.db.get_requisition_by_order_number(formatted_order_number)
            requisition_created = len(requisitions) > 0
            test_result.add_assertion("Requisition created in database", requisition_created,
                                     "One requisition record", len(requisitions))
            
            if requisition_created:
                requisition = requisitions[0]
                requisition_id = requisition["id"]
                
                # Check requisition fields
                test_result.add_assertion("Requisition has correct order number", 
                                         requisition["order_number"] == formatted_order_number,
                                         formatted_order_number, requisition["order_number"])
                
                test_result.add_assertion("Requisition has correct requester", 
                                         requisition["requester"] == test_data["requester"],
                                         test_data["requester"], requisition["requester"])
                
                test_result.add_assertion("Requisition has correct supplier", 
                                         requisition["supplier"] == test_data["supplier"],
                                         test_data["supplier"], requisition["supplier"])
                
                test_result.add_assertion("Requisition has correct note", 
                                         requisition["supplier_note"] == test_data["note"],
                                         test_data["note"], requisition["supplier_note"])
                
                # Check requisition items
                req_items = self.db.get_requisition_items(requisition_id)
                items_created = len(req_items) == len(test_data["items"])
                test_result.add_assertion("All requisition items created", items_created,
                                         len(test_data["items"]), len(req_items))
                
                # Calculate expected total value
                expected_total = sum(item["units"] * item["price"] for item in test_data["items"])
                test_result.add_assertion("Requisition has correct total value", 
                                         float(requisition["total_order_value"]) == expected_total,
                                         expected_total, float(requisition["total_order_value"]))
                
                # Check transaction in database
                transactions = self.db.get_transaction_by_order_number(formatted_order_number)
                transaction_created = len(transactions) > 0
                test_result.add_assertion("Transaction created in database", transaction_created,
                                         "One transaction record", len(transactions))
                
                if transaction_created:
                    transaction = transactions[0]
                    
                    # Check transaction fields
                    test_result.add_assertion("Transaction has correct order number", 
                                             transaction["order_number"] == formatted_order_number,
                                             formatted_order_number, transaction["order_number"])
                    
                    test_result.add_assertion("Transaction has correct type", 
                                             transaction["transaction_type"] == "Order Placed",
                                             "Order Placed", transaction["transaction_type"])
                    
                    test_result.add_assertion("Transaction has correct amount", 
                                             float(transaction["amount"]) == expected_total,
                                             expected_total, float(transaction["amount"]))
                    
                    test_result.add_assertion("Transaction has correct user", 
                                             transaction["user"] == test_data["requester"],
                                             test_data["requester"], transaction["user"])
                    
                    test_result.add_assertion("Transaction has correct status", 
                                             transaction["status"] in ["Pending", "pending"],
                                             "Pending", transaction["status"])
            
            # Check if order number incremented
            order_number_incremented = current_order_number == next_order_number + 1
            test_result.add_assertion("Order number incremented", order_number_incremented,
                                     next_order_number + 1, current_order_number)
            
            # Check if transaction appears in audit trail
            in_audit_trail = self.check_transaction_in_audit_trail(formatted_order_number)
            test_result.add_assertion("Transaction visible in audit trail", in_audit_trail,
                                     "Transaction in audit table", in_audit_trail)
            
            # Record final state
            after_state = {
                "next_order_number": current_order_number,
                "requisition_count": req_count_after,
                "transaction_count": txn_count_after,
                "requisition_count_delta": req_count_after - req_count_before,
                "transaction_count_delta": txn_count_after - txn_count_before,
                "still_logged_in": still_logged_in,
                "requisition": requisitions[0] if requisitions else None,
                "transaction": transactions[0] if transactions else None,
                "items_count": len(req_items) if 'req_items' in locals() else 0
            }
            test_result.set_after_state(after_state)
            
            # Determine overall test result
            test_passed = all(assertion["passed"] for assertion in test_result.assertions)
            test_result.finalize(test_passed)
            
        except Exception as e:
            # Capture full stacktrace for debugging
            error_trace = traceback.format_exc()
            test_result.set_error(e, error_trace)
            test_result.finalize(False)
        
        finally:
            # Add result to validation suite
            self.validation.add_result(test_result)
            
        return test_result
    
    def test_session_persistence(self):
        """
        Test that user session persists after form submission
        
        Validates:
        - User remains logged in after submission
        - No redirect to login screen
        - User can navigate to other tabs after submission
        """
        test_result = TestResult("Session Persistence")
        
        try:
            # Login
            logged_in = self.login()
            test_result.add_assertion("Login successful", logged_in)
            
            if not logged_in:
                raise Exception("Failed to login, cannot continue test")
            
            # Get user info before submission
            current_user_before = self.driver.find_element(By.ID, "currentUser").text
            
            before_state = {
                "logged_in": logged_in,
                "username": current_user_before
            }
            test_result.set_before_state(before_state)
            
            # Fill form
            test_data = {
                "requestDate": "12/04/2024",
                "requester": "Session Test",
                "supplier": "Persistence Co",
                "note": "Testing session persistence",
                "items": [
                    {"stockCode": "AB", "units": 1, "price": 25}
                ]
            }
            self.fill_requisition_form(test_data)
            
            # Submit form
            alert_text = self.submit_form()
            form_submitted = alert_text and "success" in alert_text.lower()
            test_result.add_assertion("Form submitted successfully", form_submitted)
            
            # Wait for processing
            time.sleep(3)
            
            # Check if still logged in
            is_logged_in = self.check_session_active()
            login_screen_visible = self.check_login_screen_visible()
            
            test_result.add_assertion("User still logged in after submission", is_logged_in,
                                     "User logged in", is_logged_in)
            
            test_result.add_assertion("Login screen not shown after submission", not login_screen_visible,
                                     "Login screen hidden", login_screen_visible)
            
            # Try navigating to another tab
            try:
                pending_tab = self.driver.find_element(By.CSS_SELECTOR, "button.tab-button[onclick=\"showTab('pending')\"]")
                pending_tab.click()
                
                # Wait for tab content to load
                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.ID, "pending"))
                )
                
                pending_tab_visible = True
            except:
                pending_tab_visible = False
            
            test_result.add_assertion("Can navigate to other tabs after submission", pending_tab_visible)
            
            # If still logged in, get current user info
            current_user_after = None
            if is_logged_in:
                try:
                    current_user_after = self.driver.find_element(By.ID, "currentUser").text
                except:
                    current_user_after = None
            
            test_result.add_assertion("Username preserved after submission", 
                                     current_user_after == current_user_before,
                                     current_user_before, current_user_after)
            
            after_state = {
                "logged_in": is_logged_in,
                "username": current_user_after,
                "login_screen_visible": login_screen_visible,
                "navigation_functional": pending_tab_visible
            }
            test_result.set_after_state(after_state)
            
            # Determine overall test result
            test_passed = all(assertion["passed"] for assertion in test_result.assertions)
            test_result.finalize(test_passed)
            
        except Exception as e:
            # Capture full stacktrace for debugging
            error_trace = traceback.format_exc()
            test_result.set_error(e, error_trace)
            test_result.finalize(False)
        
        finally:
            # Add result to validation suite
            self.validation.add_result(test_result)
            
        return test_result
    
    def run_all_tests(self):
        try:
            # Run all tests in sequence
            print("Starting Standard Requisition Submission test...")
            self.test_standard_requisition_submission()
            
            print("Starting Session Persistence test...")
            self.test_session_persistence()
            
            # Print summary
            self.validation.print_summary()
            
            return not self.validation.has_failures()
        finally:
            self.teardown()

if __name__ == "__main__":
    print("Starting Requisition System Integration Tests...")
    tests = RequisitionSystemTests()
    success = tests.run_all_tests()
    sys.exit(0 if success else 1) 