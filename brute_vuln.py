import time
import hashlib

db = {"carlos": "supersecretpassword"}

def login(username, password_attempt):
    # 1. Write the IF statement to check if the username exists in 'db'
    if username == db.keys():
        
    
    # 2. If it DOES exist: 
    #    - Run the heavy hashlib.pbkdf2_hmac calculation here.
    #    - Then, check if password_attempt matches db[username].
    #    - Return "Login successful" or "Incorrect password" (VULNERABLE MESSAGE)
    
    # 3. If it DOES NOT exist:
    #    - Return "Invalid username" (VULNERABLE MESSAGE)

# --- PROOF OF VULNERABILITY ---
# Test 1: Invalid User (Should be fast)
start_time = time.time()
print(login("admin", "test"))
print(f"Time taken: {time.time() - start_time} seconds\n")

# Test 2: Valid User, Invalid Password (Should be slow)
# Write the code here to measure login("carlos", "wrongpassword")