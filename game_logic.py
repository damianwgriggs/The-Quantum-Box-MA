def parse_input(user_input):
    """
    Converts a string string '101' into a list of integers [1, 0, 1].
    Returns None if input is invalid.
    """
    # Remove spaces and ensure input is only 0s and 1s
    clean_input = user_input.strip()
    
    if len(clean_input) != 3:
        return None
    
    if not all(char in '01' for char in clean_input):
        return None

    return [int(char) for char in clean_input]

def evaluate_guess(guess_list, secret_code):
    """
    Compares the user's guess list against the secret code list.
    Returns:
    - is_win (bool): True if exact match.
    - correct_count (int): Number of bits in the correct position.
    """
    correct_count = 0
    
    # Compare bit by bit
    for i in range(len(secret_code)):
        if guess_list[i] == secret_code[i]:
            correct_count += 1
            
    is_win = (correct_count == len(secret_code))
    
    return is_win, correct_count

# --- Quick Test Block ---
if __name__ == "__main__":
    # Simulate a secret code (e.g., derived from Quantum source)
    mock_secret = [1, 0, 1]
    
    # Test cases
    test_guesses = ["101", "000", "111", "abc"]
    
    print(f"Secret Code: {mock_secret}\n")
    
    for g in test_guesses:
        parsed = parse_input(g)
        if parsed:
            win, count = evaluate_guess(parsed, mock_secret)
            print(f"Guess: {g} -> Win: {win}, Correct Bits: {count}")
        else:
            print(f"Guess: {g} -> Invalid Input")