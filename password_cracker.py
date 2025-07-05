import subprocess
import tempfile
import os
from passlib.hash import bcrypt

def simulate_cracking(password):
    """
    Simulate password cracking using John the Ripper
    """
    # Create a temporary file to store the hash
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        # Generate bcrypt hash
        password_hash = bcrypt.hash(password)
        temp_file.write(f"test:{password_hash}\n")
        temp_filename = temp_file.name

    try:
        # Run John the Ripper in --show mode first to avoid actual cracking
        show_cmd = ["john", "--show", temp_filename]
        show_result = subprocess.run(show_cmd, capture_output=True, text=True)

        # If password is in John's database, it's considered weak
        if "test" in show_result.stdout:
            return {
                "cracked": True,
                "method": "Known password (found in database)",
                "time": "Instant"
            }

        # Run John with limited rules to estimate cracking difficulty
        crack_cmd = [
            "john",
            "--format=bcrypt",
            "--wordlist=/usr/share/john/password.lst",
            "--rules=Single",
            "--max-run-time=10",
            temp_filename
        ]
        
        crack_result = subprocess.run(crack_cmd, capture_output=True, text=True)
        
        # Check if password was cracked
        show_result = subprocess.run(show_cmd, capture_output=True, text=True)
        cracked = "test" in show_result.stdout

        return {
            "cracked": cracked,
            "method": "Dictionary attack with rules" if cracked else "Not cracked in simulation",
            "time": "< 10 seconds" if cracked else "> 10 seconds"
        }

    except Exception as e:
        return {
            "error": "Failed to simulate cracking",
            "details": str(e)
        }
    
    finally:
        # Clean up
        try:
            os.unlink(temp_filename)
            os.unlink(f"{temp_filename}.pot")
        except:
            pass 