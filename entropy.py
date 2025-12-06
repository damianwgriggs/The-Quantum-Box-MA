import requests
import secrets

def get_true_random(length=3):
    """
    Generates a list of binary integers (0 or 1).
    Source: ANU Quantum Vacuum Fluctuations.
    Fallback: System Hardware Entropy (secrets).
    """
    source_used = "QUANTUM (Vacuum Fluctuations)"
    
    try:
        # Request 3 integers (0-255) from ANU Quantum API
        url = f"https://qrng.anu.edu.au/API/jsonI.php?length={length}&type=uint8"
        response = requests.get(url, timeout=3)
        
        if response.status_code == 200:
            data = response.json()
            if "data" in data and len(data["data"]) == length:
                # Convert uint8 (0-255) to binary bits (0 or 1) using modulo
                code = [num % 2 for num in data["data"]]
                return code, source_used
                
    except (requests.RequestException, ValueError):
        # Fail silently to fallback
        pass

    # Fallback: Cryptographically strong pseudo-randomness from OS kernel
    source_used = "HARDWARE (Kernel Entropy)"
    code = [secrets.choice([0, 1]) for _ in range(length)]
    return code, source_used

# --- Quick Test Block (Run this file directly to verify) ---
if __name__ == "__main__":
    code, source = get_true_random()
    print(f"Generated Code: {code}")
    print(f"Source: {source}")