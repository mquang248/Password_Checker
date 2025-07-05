import re
from zxcvbn import zxcvbn
from concurrent.futures import ThreadPoolExecutor
import math

def calculate_entropy(password):
    """
    Calculate password entropy based on character set complexity
    """
    char_sets = {
        'lowercase': len(re.findall(r'[a-z]', password)),
        'uppercase': len(re.findall(r'[A-Z]', password)),
        'numbers': len(re.findall(r'\d', password)),
        'symbols': len(re.findall(r'[!@#$%^&*(),.?":{}|<>]', password))
    }
    
    char_set_size = 0
    if char_sets['lowercase']: char_set_size += 26
    if char_sets['uppercase']: char_set_size += 26
    if char_sets['numbers']: char_set_size += 10
    if char_sets['symbols']: char_set_size += 32
    
    if char_set_size == 0:
        return 0
    
    entropy = math.log2(char_set_size ** len(password))
    return entropy

def check_common_patterns(password):
    """
    Check for common patterns that weaken passwords
    """
    patterns = {
        'sequential_numbers': r'(?:\d{3,})',
        'sequential_letters': r'(?:abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)',
        'repeated_chars': r'(.)\1{2,}',
        'common_years': r'(?:19[0-9]{2}|20[0-2][0-9])',
        'keyboard_patterns': r'(?:qwer|asdf|zxcv|wasd|1234|7890)'
    }
    
    found_patterns = []
    for pattern_name, pattern in patterns.items():
        if re.search(pattern, password.lower()):
            found_patterns.append(pattern_name)
    
    return found_patterns

def analyze_structure(password):
    """
    Analyze password structure for better strength assessment
    """
    structure = {
        'length': len(password),
        'unique_chars': len(set(password)),
        'char_diversity': len(set(password)) / len(password) if password else 0,
        'patterns': check_common_patterns(password)
    }
    return structure

def calculate_strength_score(password, entropy, structure):
    """
    Calculate final strength score based on multiple factors
    """
    base_score = min(4, entropy / 32)  # Normalize entropy to 0-4 scale
    
    # Penalty factors
    penalties = 0
    
    # Penalize for patterns
    if structure['patterns']:
        penalties += 0.5 * len(structure['patterns'])
    
    # Penalize for low character diversity
    if structure['char_diversity'] < 0.5:
        penalties += 0.5
    
    # Penalize for short length
    if structure['length'] < 12:
        penalties += (12 - structure['length']) * 0.1
    
    # Calculate final score
    final_score = max(0, min(4, base_score - penalties))
    return round(final_score)

def check_password_strength(password):
    """
    Enhanced password strength analysis using multiple criteria and parallel processing
    """
    with ThreadPoolExecutor() as executor:
        # Run analyses in parallel
        entropy_future = executor.submit(calculate_entropy, password)
        structure_future = executor.submit(analyze_structure, password)
        zxcvbn_future = executor.submit(zxcvbn, password)
        
        # Gather results
        entropy = entropy_future.result()
        structure = structure_future.result()
        zxcvbn_result = zxcvbn_future.result()
    
    # Calculate comprehensive score
    score = calculate_strength_score(password, entropy, structure)
    
    # Basic checks
    length_check = len(password) >= 12
    has_upper = bool(re.search(r'[A-Z]', password))
    has_lower = bool(re.search(r'[a-z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
    
    # Enhanced feedback
    feedback = {
        'score': score,
        'entropy': round(entropy, 2),
        'estimated_crack_time': zxcvbn_result['crack_times_display']['offline_slow_hashing_1e4_per_second'],
        'checks': {
            'length': length_check,
            'uppercase': has_upper,
            'lowercase': has_lower,
            'numbers': has_digit,
            'special_chars': has_special,
            'no_common_patterns': len(structure['patterns']) == 0
        },
        'suggestions': []
    }
    
    # Dynamic suggestions based on comprehensive analysis
    if not length_check:
        feedback['suggestions'].append("Increase length to at least 12 characters")
    if not has_upper:
        feedback['suggestions'].append("Add uppercase letters")
    if not has_lower:
        feedback['suggestions'].append("Add lowercase letters")
    if not has_digit:
        feedback['suggestions'].append("Add numbers")
    if not has_special:
        feedback['suggestions'].append("Add special characters")
    
    if structure['patterns']:
        feedback['suggestions'].append("Avoid common patterns: " + ", ".join(structure['patterns']))
    
    if structure['char_diversity'] < 0.5:
        feedback['suggestions'].append("Use more unique characters")
    
    # Add zxcvbn suggestions if available
    if zxcvbn_result['feedback']['suggestions']:
        feedback['suggestions'].extend(zxcvbn_result['feedback']['suggestions'])
    
    return feedback 