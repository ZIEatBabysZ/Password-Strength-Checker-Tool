#!/usr/bin/env python3
"""
Have I Been Pwned API Integration for Password Strength Checker Tool
Checks if passwords have been compromised in known data breaches

Uses the HaveIBeenPwned Passwords API v3:
https://haveibeenpwned.com/API/v3#PwnedPasswords

This implementation uses k-anonymity to protect user privacy:
- Only the first 5 characters of the SHA-1 hash are sent to the API
- The full password never leaves your system
"""

import hashlib
import requests
import time
from typing import Tuple, Optional

class HaveIBeenPwnedChecker:
    """
    Check passwords against the Have I Been Pwned database
    using k-anonymity for privacy protection
    """
    
    API_URL = "https://api.pwnedpasswords.com/range/"
    REQUEST_TIMEOUT = 10
    MAX_RETRIES = 3
    RETRY_DELAY = 1
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Password-Strength-Checker-Tool/1.0',
            'Add-Padding': 'true'  # Helps protect against timing attacks
        })
    
    def check_password(self, password: str) -> Tuple[bool, int, str]:
        """
        Check if a password has been compromised in data breaches.
        
        Args:
            password (str): The password to check
            
        Returns:
            Tuple[bool, int, str]: (is_compromised, breach_count, status_message)
        """
        try:
            # Generate SHA-1 hash of the password
            sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
            
            # Use k-anonymity: send only first 5 characters
            hash_prefix = sha1_hash[:5]
            hash_suffix = sha1_hash[5:]
            
            # Make API request with retries
            response_data = self._make_api_request(hash_prefix)
            if response_data is None:
                return False, 0, "API request failed - unable to check password"
            
            # Parse response to find our hash
            breach_count = self._parse_response(response_data, hash_suffix)
            
            if breach_count > 0:
                return True, breach_count, f"Password found in {breach_count:,} data breaches"
            else:
                return False, 0, "Password not found in known data breaches"
                
        except Exception as e:
            return False, 0, f"Error checking password: {str(e)}"
    
    def _make_api_request(self, hash_prefix: str) -> Optional[str]:
        """
        Make API request to Have I Been Pwned with retries
        
        Args:
            hash_prefix (str): First 5 characters of SHA-1 hash
            
        Returns:
            Optional[str]: API response text or None if failed
        """
        for attempt in range(self.MAX_RETRIES):
            try:
                response = self.session.get(
                    f"{self.API_URL}{hash_prefix}",
                    timeout=self.REQUEST_TIMEOUT
                )
                
                if response.status_code == 200:
                    return response.text
                elif response.status_code == 404:
                    # No matches found
                    return ""
                elif response.status_code == 429:
                    # Rate limited - wait longer
                    time.sleep(self.RETRY_DELAY * (attempt + 1) * 2)
                    continue
                else:
                    print(f"API request failed with status {response.status_code}")
                    
            except requests.exceptions.Timeout:
                print(f"API request timeout (attempt {attempt + 1}/{self.MAX_RETRIES})")
            except requests.exceptions.ConnectionError:
                print(f"Connection error (attempt {attempt + 1}/{self.MAX_RETRIES})")
            except Exception as e:
                print(f"Unexpected error: {e}")
            
            if attempt < self.MAX_RETRIES - 1:
                time.sleep(self.RETRY_DELAY * (attempt + 1))
        
        return None
    
    def _parse_response(self, response_data: str, hash_suffix: str) -> int:
        """
        Parse API response to find breach count for our password
        
        Args:
            response_data (str): API response containing hash suffixes and counts
            hash_suffix (str): The remaining part of our SHA-1 hash
            
        Returns:
            int: Number of times password was found in breaches (0 if not found)
        """
        if not response_data:
            return 0
        
        for line in response_data.strip().split('\n'):
            if ':' in line:
                suffix, count = line.split(':', 1)
                if suffix.strip().upper() == hash_suffix:
                    return int(count.strip())
        
        return 0
    
    def check_password_simple(self, password: str) -> bool:
        """
        Simple boolean check if password is compromised
        
        Args:
            password (str): Password to check
            
        Returns:
            bool: True if compromised, False if safe or check failed
        """
        is_compromised, _, _ = self.check_password(password)
        return is_compromised
    
    def get_breach_info(self, password: str) -> dict:
        """
        Get detailed breach information for a password
        
        Args:
            password (str): Password to check
            
        Returns:
            dict: Detailed information about the password breach status
        """
        is_compromised, breach_count, message = self.check_password(password)
        
        return {
            'is_compromised': is_compromised,
            'breach_count': breach_count,
            'message': message,
            'risk_level': self._get_risk_level(breach_count),
            'recommendation': self._get_recommendation(is_compromised, breach_count)
        }
    
    def _get_risk_level(self, breach_count: int) -> str:
        """
        Determine risk level based on breach count
        
        Args:
            breach_count (int): Number of breaches
            
        Returns:
            str: Risk level description
        """
        if breach_count == 0:
            return "Safe"
        elif breach_count < 10:
            return "Low Risk"
        elif breach_count < 100:
            return "Medium Risk"
        elif breach_count < 1000:
            return "High Risk"
        else:
            return "Very High Risk"
    
    def _get_recommendation(self, is_compromised: bool, breach_count: int) -> str:
        """
        Get security recommendation based on breach status
        
        Args:
            is_compromised (bool): Whether password is compromised
            breach_count (int): Number of breaches
            
        Returns:
            str: Security recommendation
        """
        if not is_compromised:
            return "This password appears safe, but consider using a unique password for each account."
        
        if breach_count < 10:
            return "This password has been compromised. Consider changing it immediately."
        elif breach_count < 100:
            return "This password is commonly breached. Change it immediately and use a password manager."
        else:
            return "This password is extremely common in breaches. Never use this password anywhere!"


def test_hibp_checker():
    """
    Test function for the Have I Been Pwned checker
    """
    print("Testing Have I Been Pwned API Integration...")
    print("=" * 50)
    
    checker = HaveIBeenPwnedChecker()
    
    # Test with a known compromised password
    test_passwords = [
        ("password", "Known bad password"),
        ("P@ssw0rd123!", "Common variation"),
        ("ThisIsAVeryUniquePasswordThatShouldNotBeInBreaches2024!", "Likely safe password")
    ]
    
    for password, description in test_passwords:
        print(f"\nTesting: {description}")
        print(f"Password: {'*' * len(password)}")
        
        result = checker.get_breach_info(password)
        print(f"Compromised: {result['is_compromised']}")
        print(f"Breach Count: {result['breach_count']:,}")
        print(f"Risk Level: {result['risk_level']}")
        print(f"Message: {result['message']}")
        print(f"Recommendation: {result['recommendation']}")


if __name__ == "__main__":
    test_hibp_checker()
