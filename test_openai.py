#!/usr/bin/env python3
"""
Test script to verify OpenAI API integration
"""

import sys
from gender_classifier import classify_gender_with_ai

def test_openai_integration():
    """Test the OpenAI API integration with sample names"""
    
    # Get API key from user
    api_key = input("Enter your OpenAI API key (sk-...): ").strip()
    
    if not api_key:
        print("❌ No API key provided!")
        return False
    
    if not api_key.startswith('sk-'):
        print("❌ Invalid API key format! Should start with 'sk-'")
        return False
    
    # Test with sample names
    test_names = ['John', 'Mary', 'Alex', 'Jennifer', 'Michael']
    
    print(f"\n🔄 Testing OpenAI API with names: {test_names}")
    print("This will cost approximately $0.001-0.002...")
    
    try:
        # Call the AI classification function
        results = classify_gender_with_ai(test_names, api_key)
        
        print("\n✅ OpenAI API Test Results:")
        print("-" * 40)
        for name, gender_code in results.items():
            gender_desc = {
                '1': 'Male',
                '2': 'Female', 
                '?': 'Uncertain'
            }.get(gender_code, 'Unknown')
            print(f"{name:<10} → {gender_code} ({gender_desc})")
        
        print(f"\n✅ SUCCESS! OpenAI API is working correctly.")
        print(f"📊 Processed {len(results)} names successfully.")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: OpenAI API failed!")
        print(f"Error details: {str(e)}")
        
        # Common error hints
        if "Incorrect API key" in str(e):
            print("\n💡 Hints:")
            print("- Make sure your API key is correct")
            print("- Check if your API key is active at https://platform.openai.com/api-keys")
        
        elif "billing" in str(e).lower() or "quota" in str(e).lower():
            print("\n💡 Hints:")
            print("- Add credits to your OpenAI account at https://platform.openai.com/account/billing")
            print("- Make sure you have at least $5 in credits")
        
        elif "rate limit" in str(e).lower():
            print("\n💡 Hints:")
            print("- You're making requests too quickly")
            print("- Wait a moment and try again")
        
        return False

if __name__ == "__main__":
    print("🤖 OpenAI API Integration Test")
    print("=" * 40)
    success = test_openai_integration()
    
    if success:
        print("\n🎉 Your OpenAI API integration is ready to use!")
    else:
        print("\n🔧 Please fix the issues above and try again.")
    
    sys.exit(0 if success else 1) 