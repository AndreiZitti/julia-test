"""
Gender Classification Module
Uses either OpenAI API (AI-first) or comprehensive name database to classify names by gender.
Returns: '1' for male, '2' for female, '?' for uncertain/unknown
"""

import re
import json
from openai import OpenAI

# Common male names database
MALE_NAMES = {
    'john', 'james', 'robert', 'michael', 'william', 'david', 'richard', 'charles', 
    'joseph', 'thomas', 'christopher', 'daniel', 'paul', 'mark', 'donald', 'steven',
    'andrew', 'joshua', 'kenneth', 'kevin', 'brian', 'george', 'edward', 'ronald',
    'timothy', 'jason', 'jeffrey', 'ryan', 'jacob', 'gary', 'nicholas', 'eric',
    'jonathan', 'stephen', 'larry', 'justin', 'scott', 'brandon', 'benjamin', 'samuel',
    'gregory', 'frank', 'raymond', 'alexander', 'patrick', 'jack', 'dennis', 'jerry',
    'tyler', 'aaron', 'jose', 'henry', 'adam', 'douglas', 'nathan', 'peter',
    'zachary', 'kyle', 'noah', 'alan', 'ethan', 'jeremy', 'lionel', 'andrew',
    'carl', 'harold', 'arthur', 'lawrence', 'sean', 'christian', 'albert', 'walter',
    'elijah', 'wayne', 'ralph', 'roy', 'eugene', 'louis', 'philip', 'bobby',
    'antonio', 'carlos', 'juan', 'miguel', 'luis', 'diego', 'sergio', 'jorge',
    'francisco', 'rafael', 'alberto', 'oscar', 'fernando', 'pedro', 'alejandro',
    'marco', 'ricardo', 'andres', 'gabriel', 'adrian', 'manuel', 'antonio',
    'mohammed', 'ahmad', 'hassan', 'ali', 'omar', 'ibrahim', 'yusuf', 'ahmed',
    'mustafa', 'abdul', 'malik', 'tariq', 'saeed', 'khalid', 'nasser', 'faisal',
    'alessandro', 'giovanni', 'lorenzo', 'francesco', 'marco', 'luca', 'andrea',
    'pierre', 'jean', 'michel', 'philippe', 'alain', 'bernard', 'claude', 'daniel',
    'raj', 'rahul', 'ravi', 'kumar', 'suresh', 'anil', 'sandeep', 'vijay',
    'chang', 'wei', 'ming', 'chen', 'zhang', 'wang', 'li', 'liu'
}

# Common female names database
FEMALE_NAMES = {
    'mary', 'patricia', 'jennifer', 'linda', 'elizabeth', 'barbara', 'susan', 'jessica',
    'sarah', 'karen', 'nancy', 'lisa', 'betty', 'helen', 'sandra', 'donna',
    'carol', 'ruth', 'sharon', 'michelle', 'laura', 'sarah', 'kimberly', 'deborah',
    'dorothy', 'lisa', 'nancy', 'karen', 'betty', 'helen', 'sandra', 'donna',
    'carol', 'ruth', 'sharon', 'michelle', 'laura', 'sarah', 'kimberly', 'deborah',
    'amy', 'angela', 'ashley', 'brenda', 'emma', 'olivia', 'cynthia', 'marie',
    'janet', 'catherine', 'frances', 'christine', 'samantha', 'debra', 'rachel', 'carolyn',
    'janet', 'virginia', 'maria', 'heather', 'diane', 'julie', 'joyce', 'victoria',
    'kelly', 'christina', 'joan', 'evelyn', 'lauren', 'judith', 'megan', 'cheryl',
    'andrea', 'hannah', 'jacqueline', 'martha', 'gloria', 'teresa', 'sara', 'janice',
    'marie', 'julia', 'heather', 'diane', 'ruth', 'julie', 'joyce', 'virginia',
    'anna', 'kathryn', 'gloria', 'teresa', 'doris', 'sara', 'janice', 'julia',
    'sophia', 'isabella', 'charlotte', 'amelia', 'evelyn', 'abigail', 'harper', 'emily',
    'elizabeth', 'avery', 'sofia', 'ella', 'madison', 'scarlett', 'victoria', 'aria',
    'grace', 'chloe', 'camila', 'penelope', 'riley', 'layla', 'lillian', 'nora',
    'zoey', 'mila', 'aubrey', 'hannah', 'lily', 'addison', 'eleanor', 'natalie',
    'luna', 'savannah', 'brooklyn', 'leah', 'zoe', 'stella', 'hazel', 'ellie',
    'maria', 'ana', 'lucia', 'carmen', 'rosa', 'elena', 'isabel', 'sofia',
    'claudia', 'adriana', 'lorena', 'patricia', 'laura', 'sandra', 'monica', 'alejandra',
    'fatima', 'aisha', 'zahra', 'noor', 'layla', 'amina', 'yasmin', 'sara',
    'mariam', 'zeinab', 'noura', 'hala', 'lina', 'rania', 'dina', 'maya',
    'chiara', 'giulia', 'francesca', 'alice', 'sofia', 'aurora', 'gioia', 'martina',
    'marie', 'claire', 'camille', 'lea', 'manon', 'chloe', 'sarah', 'emma',
    'priya', 'kavya', 'ananya', 'sneha', 'pooja', 'riya', 'shreya', 'nikita',
    'ling', 'mei', 'yan', 'jing', 'hui', 'xin', 'yu', 'na'
}

# Ambiguous names that could be either gender
AMBIGUOUS_NAMES = {
    'alex', 'alexis', 'avery', 'blake', 'casey', 'cameron', 'charlie', 'drew',
    'ellis', 'emery', 'jordan', 'kelly', 'kendall', 'kennedy', 'logan', 'morgan',
    'parker', 'peyton', 'quinn', 'reese', 'riley', 'river', 'rowan', 'sage',
    'sam', 'skyler', 'taylor', 'terry', 'toni', 'tracy', 'valencia', 'whitney',
    'chris', 'pat', 'dana', 'jamie', 'lee', 'lynn', 'robin', 'sydney',
    'angel', 'ash', 'aubrey', 'august', 'autumn', 'blue', 'brook', 'cedar',
    'cloud', 'dakota', 'denver', 'echo', 'emerson', 'francis', 'gray', 'haven',
    'hunter', 'indigo', 'justice', 'kai', 'lane', 'london', 'lux', 'mason',
    'nevada', 'ocean', 'phoenix', 'rain', 'scout', 'storm', 'true', 'vale'
}

# Name endings that typically indicate gender
MALE_ENDINGS = {'son', 'sen', 'sson', 'ovich', 'evich', 'ski', 'sky', 'ez', 'az'}
FEMALE_ENDINGS = {'daughter', 'dottir', 'ova', 'eva', 'ina', 'ska', 'a'}

def clean_name(name):
    """Clean and normalize a name for comparison."""
    if not name or str(name).strip() == '' or str(name).lower() == 'nan':
        return ""
    
    # Convert to string and clean
    name_str = str(name).strip().lower()
    
    # Remove titles, prefixes, and common suffixes
    prefixes_to_remove = ['mr.', 'mrs.', 'ms.', 'dr.', 'prof.', 'sir', 'miss', 'mme.', 'mlle.']
    suffixes_to_remove = ['jr.', 'sr.', 'ii', 'iii', 'iv', 'phd', 'md', 'esq.']
    
    for prefix in prefixes_to_remove:
        if name_str.startswith(prefix):
            name_str = name_str[len(prefix):].strip()
            break
    
    for suffix in suffixes_to_remove:
        if name_str.endswith(suffix):
            name_str = name_str[:-len(suffix)].strip()
            break
    
    # Remove special characters and numbers
    name_str = re.sub(r'[^a-zA-Z\s\-\']', '', name_str)
    
    # Extract first name (assume it's the first word)
    first_name = name_str.split()[0] if name_str.split() else ""
    
    return first_name

def classify_gender_with_ai(names_batch, api_key):
    """
    Classify a batch of names using OpenAI API for better accuracy.
    
    Args:
        names_batch (list): List of names to classify
        api_key (str): OpenAI API key
        
    Returns:
        dict: Dictionary with 'success', 'results', 'model_used', and 'error' keys
    """
    if not api_key or not names_batch:
        return {
            'success': False,
            'error': 'No API key or names provided',
            'results': {}
        }
    
    # Clean the names first
    cleaned_names = []
    name_mapping = {}
    for name in names_batch:
        cleaned = clean_name(name) if name else ""
        if cleaned:
            cleaned_names.append(cleaned)
            name_mapping[cleaned] = name
    
    if not cleaned_names:
        return {
            'success': True,
            'results': {name: '?' for name in names_batch},
            'model_used': 'None (empty names)',
            'error': None
        }
    
    # Create prompt for batch processing
    batch_size = min(50, len(cleaned_names))
    current_batch = cleaned_names[:batch_size]
    
    prompt = f"""Classify the following names by gender. Return only a JSON object where each name maps to:
- "1" for male names
- "2" for female names  
- "?" for ambiguous, uncertain, or unknown names

Names to classify: {current_batch}

Respond with only the JSON object, no additional text:"""

    # Try models in order of preference
    models_to_try = [
        ("gpt-3.5-turbo", "GPT-3.5 Turbo"),
        ("gpt-4o-mini", "GPT-4o Mini"),
        ("gpt-4o", "GPT-4o"),
        ("gpt-4", "GPT-4")
    ]
    
    print(f"🤖 Initializing OpenAI client with API key: {api_key[:12]}...")
    
    for model_id, model_name in models_to_try:
        try:
            client = OpenAI(api_key=api_key)
            
            print(f"🔄 Trying model: {model_name}")
            
            response = client.chat.completions.create(
                model=model_id,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a precise name classification assistant. Return only valid JSON with no additional commentary."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                temperature=0.1,
                max_tokens=1000
            )
            
            # Parse the response
            response_text = response.choices[0].message.content.strip()
            
            # Try to extract JSON from response
            try:
                # Remove any markdown formatting
                if '```json' in response_text:
                    response_text = response_text.split('```json')[1].split('```')[0]
                elif '```' in response_text:
                    response_text = response_text.split('```')[1].split('```')[0]
                
                ai_results = json.loads(response_text)
                
                # Map back to original names and validate results
                final_results = {}
                for name in names_batch:
                    cleaned = clean_name(name) if name else ""
                    if cleaned in ai_results:
                        result = ai_results[cleaned]
                        # Validate result
                        if result in ['1', '2', '?']:
                            final_results[name] = result
                        else:
                            final_results[name] = '?'
                    else:
                        final_results[name] = '?'
                
                print(f"✅ Success with {model_name}")
                return {
                    'success': True,
                    'results': final_results,
                    'model_used': model_name,
                    'error': None
                }
                
            except json.JSONDecodeError as json_error:
                print(f"❌ JSON parsing failed for {model_name}: {json_error}")
                continue  # Try next model
        
        except Exception as e:
            error_str = str(e)
            print(f"❌ Model {model_name} failed: {error_str}")
            
            # Check for specific errors that mean we should stop trying
            if "Incorrect API key" in error_str:
                return {
                    'success': False,
                    'error': 'Invalid API key. Please check your OpenAI API key.',
                    'results': {}
                }
            elif "billing" in error_str.lower() or "quota" in error_str.lower():
                return {
                    'success': False,
                    'error': 'Insufficient OpenAI credits. Please add credits to your account.',
                    'results': {}
                }
            elif "rate limit" in error_str.lower():
                return {
                    'success': False,
                    'error': 'Rate limit exceeded. Please wait a moment and try again.',
                    'results': {}
                }
            # For model not found errors, continue to try next model
            elif "model" in error_str.lower() and "not found" in error_str.lower():
                continue
            else:
                # For other errors, continue trying other models
                continue
    
    # If we get here, all models failed
    return {
        'success': False,
        'error': 'All OpenAI models failed. Your account may not have access to any compatible models.',
        'results': {}
    }

def classify_gender(name):
    """
    Classify a name as male (1), female (2), or uncertain (?) using rule-based approach.
    
    Args:
        name (str): The name to classify
        
    Returns:
        str: '1' for male, '2' for female, '?' for uncertain
    """
    if not name or str(name).strip() == '' or str(name).lower() == 'nan':
        return '?'
    
    # Clean the name
    clean_first_name = clean_name(name)
    
    if not clean_first_name:
        return '?'
    
    # Check exact matches first
    if clean_first_name in MALE_NAMES:
        return '1'
    elif clean_first_name in FEMALE_NAMES:
        return '2'
    elif clean_first_name in AMBIGUOUS_NAMES:
        return '?'
    
    # Check name endings for patterns
    for ending in MALE_ENDINGS:
        if clean_first_name.endswith(ending):
            return '1'
    
    for ending in FEMALE_ENDINGS:
        if clean_first_name.endswith(ending):
            return '2'
    
    # Additional heuristics
    # Names ending in 'a' are often female (but not always)
    if clean_first_name.endswith('a') and len(clean_first_name) > 2:
        # Check if it's not a known male name ending in 'a'
        male_a_exceptions = {'joshua', 'luca', 'andrea', 'elijah', 'dakota', 'montana'}
        if clean_first_name not in male_a_exceptions:
            return '2'
    
    # Names ending in consonants often male
    if clean_first_name.endswith(('er', 'on', 'en', 'in', 'an', 'el', 'al')):
        return '1'
    
    # If we can't determine, return uncertain
    return '?'

# Test function to validate the classifier
def test_classifier():
    """Test the classifier with known examples."""
    test_cases = [
        ('John', '1'), ('Mary', '2'), ('Alex', '?'),
        ('Jennifer', '2'), ('Michael', '1'), ('Taylor', '?'),
        ('Dr. John Smith', '1'), ('Ms. Sarah Johnson', '2'),
        ('', '?'), ('123', '?'), ('Unknown', '?')
    ]
    
    print("Testing Gender Classifier:")
    for name, expected in test_cases:
        result = classify_gender(name)
        status = "✓" if result == expected else "✗"
        print(f"{status} {name} -> {result} (expected {expected})")

if __name__ == "__main__":
    test_classifier() 