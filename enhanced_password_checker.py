#!/usr/bin/env python3
"""
Enhanced Password Strength Checker Tool with zxcvbn Integration

A comprehensive command-line tool that analyzes password strength using multiple criteria
including zxcvbn scoring, length, character types, dictionary words, entropy, and common password detection.

Author: Password Security Tool
Date: June 2025
"""

import re
import math
import argparse
import sys
import os
from typing import Dict, List, Tuple, Optional
from colorama import Fore, Style, init
import importlib.util

# Initialize colorama for cross-platform color support
init(autoreset=True)

# Try to import zxcvbn
try:
    from zxcvbn import zxcvbn
    ZXCVBN_AVAILABLE = True
except ImportError:
    ZXCVBN_AVAILABLE = False

# Try to import Have I Been Pwned checker
try:
    from hibp_checker import HaveIBeenPwnedChecker
    HIBP_AVAILABLE = True
except ImportError:
    HIBP_AVAILABLE = False

class PasswordStrengthChecker:
    """Enhanced password strength checker with zxcvbn integration"""
    
    def __init__(self):
        """Initialize the password checker with common passwords and dictionary words"""
        self.common_passwords = self._load_common_passwords()
        self.dictionary_words = self._load_dictionary_words()
        self.use_zxcvbn = ZXCVBN_AVAILABLE
        self.hibp_checker = HaveIBeenPwnedChecker() if HIBP_AVAILABLE else None
        
        if not self.use_zxcvbn:
            print(f"{Fore.YELLOW}Note: zxcvbn library not found. Using built-in scoring algorithm.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Install it with: pip install zxcvbn{Style.RESET_ALL}\n")
        
        if not HIBP_AVAILABLE:
            print(f"{Fore.YELLOW}Note: Have I Been Pwned integration not available.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Install requests with: pip install requests{Style.RESET_ALL}\n")
    
    def _load_common_passwords(self) -> set:
        """Load common passwords from file or use built-in list"""
        common_passwords_file = "common_passwords.txt"
        
        # Built-in list of most common passwords (top 500)
        builtin_common = {
            "123456", "password", "12345678", "qwerty", "123456789", "12345",
            "1234", "111111", "1234567", "dragon", "123123", "baseball",
            "abc123", "football", "monkey", "letmein", "696969", "shadow",
            "master", "666666", "qwertyuiop", "123321", "mustang", "1234567890",
            "michael", "654321", "pussy", "superman", "1qaz2wsx", "7777777",
            "fuckyou", "121212", "000000", "qazwsx", "123qwe", "killer",
            "trustno1", "jordan", "jennifer", "zxcvbnm", "asdfgh", "hunter",
            "buster", "soccer", "harley", "batman", "andrew", "tigger",
            "sunshine", "iloveyou", "fuckme", "2000", "charlie", "robert",
            "thomas", "hockey", "ranger", "daniel", "starwars", "klaster",
            "112233", "george", "asshole", "computer", "michelle", "jessica",
            "pepper", "1111", "zxcvbn", "555555", "11111111", "131313",
            "freedom", "777777", "pass", "fuck", "maggie", "159753",
            "aaaaaa", "ginger", "princess", "joshua", "cheese", "amanda",
            "summer", "love", "ashley", "6969", "nicole", "chelsea",
            "biteme", "matthew", "access", "yankees", "987654321", "dallas",
            "austin", "thunder", "taylor", "matrix", "william", "corvette",
            "hello", "martin", "heather", "secret", "fucker", "merlin",
            "diamond", "1234qwer", "gfhjkm", "hammer", "silver", "222222",
            "88888888", "anthony", "justin", "test", "bailey", "q1w2e3r4t5",
            "patrick", "internet", "scooter", "orange", "11111", "golfer",
            "cookie", "richard", "samantha", "bigdog", "guitar", "jackson",
            "whatever", "mickey", "chicken", "sparky", "snoopy", "maverick",
            "phoenix", "camaro", "sexy", "peanut", "morgan", "welcome",
            "falcon", "cowboy", "ferrari", "samsung", "andrea", "smokey",
            "steelers", "joseph", "mercedes", "dakota", "arsenal", "eagles",
            "melissa", "boomer", "booboo", "spider", "nascar", "monster",
            "tigers", "yellow", "xxxxxx", "123123123", "gateway", "marina",
            "diablo", "bulldog", "qwer1234", "compaq", "purple", "hardcore",
            "banana", "junior", "hannah", "123654", "porsche", "lakers",
            "iceman", "money", "cowboys", "987654", "london", "tennis",
            "999999", "ncc1701", "coffee", "scooby", "0000", "miller",
            "boston", "q1w2e3r4", "fuckoff", "brandon", "yamaha", "chester",
            "mother", "forever", "johnny", "edward", "333333", "oliver",
            "redsox", "player", "nikita", "knight", "fender", "barney",
            "midnight", "please", "brandy", "chicago", "badboy", "iwantu",
            "slayer", "rangers", "charles", "angel", "flower", "bigdaddy",
            "rabbit", "wizard", "bigdick", "jasper", "enter", "rachel",
            "chris", "steven", "winner", "adidas", "victoria", "natasha",
            "1q2w3e4r", "jasmine", "winter", "prince", "panties", "marine",
            "ghbdtn", "fishing", "cocacola", "casper", "james", "232323",
            "raiders", "888888", "marlboro", "gandalf", "asdfasdf", "crystal",
            "87654321", "12344321", "sexsex", "golden", "blowme", "bigtits",
            "8675309", "panther", "lauren", "angela", "bitch", "spanky",
            "thx1138", "angels", "madison", "winston", "shannon", "mike",
            "toyota", "blowjob", "jordan23", "canada", "sophie", "Password",
            "apples", "dick", "tiger", "razz", "123abc", "pokemon", "qazxsw",
            "55555", "qwaszx", "muffin", "johnson", "murphy", "cooper",
            "jonathan", "liverpoo", "david", "danielle", "159357", "jackie",
            "1990", "123456a", "789456", "turtle", "horny", "abcd1234",
            "scorpion", "qazwsxedc", "101010", "butter", "carlos", "password1",
            "dennis", "slipknot", "qwerty123", "booger", "asdf", "1991",
            "black", "startrek", "12341234", "cameron", "newyork", "rainbow",
            "nathan", "john", "1992", "rocket", "viking", "redskins",
            "butthead", "asdfghj", "1212", "sierra", "peaches", "gemini",
            "doctor", "wilson", "sandra", "helpme", "qwertyui", "victor",
            "florida", "dolphin", "pookie", "captain", "tucker", "blue",
            "liverpool", "theman", "bandit", "dolphins", "maddog", "packers",
            "jaguar", "lovers", "nicholas", "united", "tiffany", "maxwell",
            "zzzzzz", "nirvana", "jeremy", "suckit", "stupid", "porn",
            "monica", "elephant", "giants", "jackass", "hotdog", "rosebud",
            "success", "debbie", "mountain", "444444", "xxxxxxxx", "warrior",
            "1q2w3e4r5t", "q1w2e3", "123456q", "albert", "metallic", "lucky",
            "azerty", "7777", "shithead", "alex", "bond007", "alexis",
            "1111111", "samson", "5150", "willie", "scorpio", "bonnie",
            "gators", "benjamin", "voodoo", "driver", "dexter", "2112",
            "jason", "calvin", "freddy", "212121", "creative", "12345a",
            "sydney", "rush2112", "1989", "asdfghjkl", "red123", "bubba",
            "4815162342", "passw0rd", "trouble", "gunner", "happy",
            "fucking", "gordon", "legend", "jessie", "stella", "qwert",
            "eminem", "arthur", "apple", "nissan", "bullshit", "bear",
            "america", "1qazxsw2", "nothing", "parker", "4444", "rebecca",
            "qweqwe", "garfield", "01012011", "beavis", "69696969", "jack",
            "asdasd", "december", "2222", "102030", "252525", "11223344",
            "magic", "apollo", "skippy", "315475", "girls", "kitten",
            "golf", "copper", "braves", "shelby", "godzilla", "beaver",
            "fred", "tomcat", "august", "buddy", "airborne", "1993",
            "1988", "lifehack", "qqqqqq", "brooklyn", "animal", "platinum",
            "phantom", "online", "xavier", "darkness", "blink182", "power",
            "fish", "green", "789456123", "voyager", "police", "travis",
            "12qwaszx", "heaven", "snowball", "lover", "abcdef", "00000",
            "pakistan", "007007", "walter", "playboy", "blazer", "cricket",
            "sniper", "hooters", "donkey", "willow", "loveme", "saturn",
            "therock", "redwings", "bigboy", "pumpkin", "trinity", "williams",
            "tits", "nintendo", "digital", "destiny", "topgun", "runner",
            "marvin", "guinness", "chance", "bubbles", "testing", "fire",
            "november", "minecraft", "asdf1234", "lasvegas", "sergey",
            "broncos", "cartman", "private", "celtic", "birdie", "little",
            "cassie", "babygirl", "donald", "beatles", "1313", "dickhead",
            "family", "12345q", "zxc123", "chemistry", "spring", "bruce",
            "eclipse", "bottom", "billybob", "7654321", "1994", "1987",
            "0987654321", "98765432", "9876543210", "asd123", "picard",
            "2010", "gosox", "love123", "princess1", "admin", "god",
            "1234qwer", "Administrator", "root", "1234567890", "pass123",
            "temp", "guest", "demo", "test123", "user", "welcome1",
            "backup", "system", "super", "service", "support", "sales",
            "mysql", "oracle", "postgres", "database", "server", "apache",
            "web", "www", "mail", "email", "ftp", "ssh", "telnet",
            "router", "switch", "firewall", "vpn", "security", "monitor"
        }
        
        try:
            if os.path.exists(common_passwords_file):
                with open(common_passwords_file, 'r', encoding='utf-8') as f:
                    file_passwords = {line.strip().lower() for line in f if line.strip()}
                return builtin_common.union(file_passwords)
        except Exception:
            pass
            
        return builtin_common
    
    def _load_dictionary_words(self) -> set:
        """Load dictionary words from file or use built-in list"""
        dictionary_file = "dictionary_words.txt"
        
        # Built-in list of common dictionary words
        builtin_words = {
            "password", "computer", "internet", "security", "welcome", "admin",
            "user", "login", "system", "server", "network", "database",
            "website", "email", "account", "profile", "settings", "config",
            "backup", "recovery", "download", "upload", "file", "folder",
            "document", "picture", "image", "video", "music", "game",
            "player", "winner", "loser", "master", "expert", "professional",
            "business", "company", "office", "home", "house", "family",
            "friend", "love", "heart", "soul", "mind", "body", "health",
            "money", "cash", "bank", "credit", "card", "payment", "price",
            "value", "cost", "budget", "finance", "investment", "profit",
            "market", "trade", "sale", "buy", "sell", "customer", "client",
            "service", "support", "help", "guide", "tutorial", "lesson",
            "course", "school", "student", "teacher", "education", "learning",
            "knowledge", "skill", "ability", "talent", "gift", "power",
            "strength", "energy", "force", "speed", "time", "space",
            "world", "earth", "planet", "universe", "galaxy", "star",
            "moon", "sun", "light", "dark", "bright", "color", "blue",
            "red", "green", "yellow", "orange", "purple", "pink", "black",
            "white", "gray", "brown", "silver", "gold", "diamond", "metal",
            "rock", "stone", "mountain", "valley", "river", "ocean",
            "sea", "lake", "beach", "island", "forest", "tree", "flower",
            "grass", "animal", "bird", "fish", "cat", "dog", "horse",
            "cow", "pig", "sheep", "chicken", "tiger", "lion", "elephant",
            "monkey", "bear", "wolf", "fox", "rabbit", "mouse", "snake",
            "january", "february", "march", "april", "may", "june",
            "july", "august", "september", "october", "november", "december",
            "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
            "spring", "summer", "autumn", "winter", "year", "month", "week", "day"
        }
        
        try:
            if os.path.exists(dictionary_file):
                with open(dictionary_file, 'r', encoding='utf-8') as f:
                    file_words = {line.strip().lower() for line in f if line.strip()}
                return builtin_words.union(file_words)
        except Exception:
            pass
            
        return builtin_words
    
    def calculate_entropy(self, password: str) -> float:
        """Calculate password entropy in bits"""
        charset_size = 0
        
        # Determine character set size
        if re.search(r'[a-z]', password):
            charset_size += 26  # lowercase letters
        if re.search(r'[A-Z]', password):
            charset_size += 26  # uppercase letters
        if re.search(r'[0-9]', password):
            charset_size += 10  # digits
        if re.search(r'[^a-zA-Z0-9]', password):
            charset_size += 32  # special characters (approximation)
        
        if charset_size == 0:
            return 0
        
        # Entropy = log2(charset_size^length)
        entropy = len(password) * math.log2(charset_size)
        return entropy
    
    def check_character_types(self, password: str) -> Dict[str, bool]:
        """Check what types of characters are present in the password"""
        return {
            'lowercase': bool(re.search(r'[a-z]', password)),
            'uppercase': bool(re.search(r'[A-Z]', password)),
            'digits': bool(re.search(r'[0-9]', password)),
            'special': bool(re.search(r'[^a-zA-Z0-9]', password))
        }
    
    def check_common_patterns(self, password: str) -> List[str]:
        """Check for common weak patterns in the password"""
        issues = []
        password_lower = password.lower()
        
        # Check for consecutive characters
        if re.search(r'(.)\1{2,}', password):
            issues.append("Contains repeated characters")
        
        # Check for sequential patterns
        sequences = ['123', '234', '345', '456', '567', '678', '789', '890',
                    'abc', 'bcd', 'cde', 'def', 'efg', 'fgh', 'ghi', 'hij',
                    'ijk', 'jkl', 'klm', 'lmn', 'mno', 'nop', 'opq', 'pqr',
                    'qrs', 'rst', 'stu', 'tuv', 'uvw', 'vwx', 'wxy', 'xyz']
        
        for seq in sequences:
            if seq in password_lower or seq[::-1] in password_lower:
                issues.append("Contains sequential characters")
                break
        
        # Check for keyboard patterns
        keyboard_patterns = ['qwerty', 'asdf', 'zxcv', '1234', 'qwertyuiop',
                           'asdfghjkl', 'zxcvbnm', '1qaz', '2wsx', '3edc',
                           'qwe', 'asd', 'zxc', 'wer', 'sdf', 'xcv']
        
        for pattern in keyboard_patterns:
            if pattern in password_lower:
                issues.append("Contains keyboard patterns")
                break
        
        # Check for common words
        for word in self.dictionary_words:
            if len(word) > 3 and word in password_lower:
                issues.append(f"Contains dictionary word: '{word}'")
        
        # Check against common passwords
        if password_lower in self.common_passwords:
            issues.append("Password is in common passwords list")
        
        return issues
    
    def calculate_score_builtin(self, password: str) -> Tuple[int, str, List[str]]:
        """Calculate password strength using built-in algorithm"""
        score = 0
        suggestions = []
        
        # Length scoring (0-30 points)
        length = len(password)
        if length >= 16:
            score += 30
        elif length >= 12:
            score += 25
        elif length >= 8:
            score += 20
        elif length >= 6:
            score += 15
        elif length >= 4:
            score += 10
        else:
            score += 5
            suggestions.append("Use at least 8 characters (12+ recommended)")
        
        if length < 8:
            suggestions.append("Increase password length for better security")
        
        # Character type diversity (0-25 points)
        char_types = self.check_character_types(password)
        type_count = sum(char_types.values())
        
        if type_count == 4:
            score += 25
        elif type_count == 3:
            score += 20
        elif type_count == 2:
            score += 15
        elif type_count == 1:
            score += 10
        else:
            score += 0
        
        # Add suggestions for missing character types
        if not char_types['lowercase']:
            suggestions.append("Add lowercase letters")
        if not char_types['uppercase']:
            suggestions.append("Add uppercase letters")
        if not char_types['digits']:
            suggestions.append("Add numbers")
        if not char_types['special']:
            suggestions.append("Add special characters (!@#$%^&*)")
        
        # Entropy scoring (0-25 points)
        entropy = self.calculate_entropy(password)
        if entropy >= 70:
            score += 25
        elif entropy >= 60:
            score += 20
        elif entropy >= 50:
            score += 15
        elif entropy >= 40:
            score += 10
        else:
            score += 5
        
        # Pattern and common password penalties (0-25 points deduction)
        issues = self.check_common_patterns(password)
        penalty = min(len(issues) * 7, 25)
        score -= penalty
        
        # Add issues as suggestions
        for issue in issues:
            if "dictionary word" in issue:
                suggestions.append("Avoid using dictionary words")
            elif "common passwords" in issue:
                suggestions.append("This password is too common - choose a unique one")
            elif "repeated characters" in issue:
                suggestions.append("Avoid repeating the same character")
            elif "sequential characters" in issue:
                suggestions.append("Avoid sequential characters (123, abc)")
            elif "keyboard patterns" in issue:
                suggestions.append("Avoid keyboard patterns (qwerty, asdf)")
        
        # Uniqueness bonus (0-20 points)
        unique_chars = len(set(password))
        uniqueness_ratio = unique_chars / len(password)
        if uniqueness_ratio >= 0.8:
            score += 20
        elif uniqueness_ratio >= 0.6:
            score += 15
        elif uniqueness_ratio >= 0.4:
            score += 10
        else:
            score += 5
            suggestions.append("Use more unique characters")
        
        # Ensure score is between 0 and 100
        score = max(0, min(100, score))
        
        # Determine strength label
        if score >= 80:
            strength = "Very Strong"
        elif score >= 60:
            strength = "Strong"
        elif score >= 40:
            strength = "Medium"
        elif score >= 20:
            strength = "Weak"
        else:
            strength = "Very Weak"
        
        return score, strength, suggestions
    
    def calculate_score_zxcvbn(self, password: str) -> Tuple[int, str, List[str], Dict]:
        """Calculate password strength using zxcvbn library"""
        result = zxcvbn(password)
        
        # Convert zxcvbn score (0-4) to our scale (0-100)
        zxcvbn_score = result['score']
        score_mapping = {0: 10, 1: 25, 2: 50, 3: 75, 4: 95}
        base_score = score_mapping.get(zxcvbn_score, 10)
          # Adjust score based on additional factors
        length_bonus = min(len(password) * 2, 20)
        entropy_bonus = min(result.get('entropy', 0) / 4, 15)
        
        final_score = min(100, base_score + length_bonus + entropy_bonus)
        
        # Determine strength label
        strength_mapping = {0: "Very Weak", 1: "Weak", 2: "Medium", 3: "Strong", 4: "Very Strong"}
        strength = strength_mapping.get(zxcvbn_score, "Very Weak")
        
        # Generate suggestions
        suggestions = []
        if result['feedback']['warning']:
            suggestions.append(result['feedback']['warning'])
        
        for suggestion in result['feedback']['suggestions']:
            suggestions.append(suggestion)
        
        # Add our own suggestions
        char_types = self.check_character_types(password)
        if not char_types['uppercase']:
            suggestions.append("Add uppercase letters")
        if not char_types['lowercase']:
            suggestions.append("Add lowercase letters")
        if not char_types['digits']:
            suggestions.append("Add numbers")
        if not char_types['special']:
            suggestions.append("Add special characters")
        
        if len(password) < 8:
            suggestions.append("Use at least 8 characters")
        if len(password) < 12:
            suggestions.append("Consider using 12+ characters for better security")
        
        return int(final_score), strength, suggestions, result
    
    def get_color_for_strength(self, strength: str) -> str:
        """Get color code for password strength"""
        colors = {
            "Very Strong": Fore.GREEN + Style.BRIGHT,
            "Strong": Fore.GREEN,
            "Medium": Fore.YELLOW,
            "Weak": Fore.RED,
            "Very Weak": Fore.RED + Style.BRIGHT
        }
        return colors.get(strength, Fore.WHITE)
    
    def analyze_password(self, password: str) -> None:
        """Analyze password and display results"""
        if not password:
            print(f"{Fore.RED}Error: Password cannot be empty{Style.RESET_ALL}")
            return
        
        # Use zxcvbn if available, otherwise use built-in algorithm
        if self.use_zxcvbn:
            score, strength, suggestions, zxcvbn_result = self.calculate_score_zxcvbn(password)
        else:
            score, strength, suggestions = self.calculate_score_builtin(password)
            zxcvbn_result = None
        
        color = self.get_color_for_strength(strength)
        
        print("\n" + "="*70)
        print(f"{Fore.CYAN + Style.BRIGHT}[*] PASSWORD STRENGTH ANALYSIS [*]{Style.RESET_ALL}")
        print("="*70)
        
        # Algorithm info
        algorithm = "zxcvbn + Enhanced Analysis" if self.use_zxcvbn else "Built-in Algorithm"
        print(f"\n{Fore.CYAN}Analysis Method:{Style.RESET_ALL} {algorithm}")
        
        # Basic info
        print(f"{Fore.CYAN}Password Length:{Style.RESET_ALL} {len(password)} characters")
        
        # Character types
        char_types = self.check_character_types(password)
        print(f"\n{Fore.CYAN}Character Composition:{Style.RESET_ALL}")
        print(f"  - Lowercase letters: {Fore.GREEN + '[YES]' if char_types['lowercase'] else Fore.RED + '[NO]'}{Style.RESET_ALL}")
        print(f"  - Uppercase letters: {Fore.GREEN + '[YES]' if char_types['uppercase'] else Fore.RED + '[NO]'}{Style.RESET_ALL}")
        print(f"  - Numbers: {Fore.GREEN + '[YES]' if char_types['digits'] else Fore.RED + '[NO]'}{Style.RESET_ALL}")
        print(f"  - Special characters: {Fore.GREEN + '[YES]' if char_types['special'] else Fore.RED + '[NO]'}{Style.RESET_ALL}")
          # Entropy and zxcvbn specific info
        entropy = self.calculate_entropy(password)
        print(f"\n{Fore.CYAN}Technical Metrics:{Style.RESET_ALL}")
        print(f"  - Entropy: {entropy:.1f} bits")
        print(f"  - Unique characters: {len(set(password))}/{len(password)}")
        
        if zxcvbn_result:
            print(f"  - zxcvbn Score: {zxcvbn_result['score']}/4")
            print(f"  - Guesses needed: {zxcvbn_result['guesses']:,}")
            if 'entropy' in zxcvbn_result:
                print(f"  - zxcvbn Entropy: {zxcvbn_result['entropy']:.1f} bits")
        
        # Score and strength
        print(f"\n{Fore.CYAN}Overall Assessment:{Style.RESET_ALL}")
        print(f"  - Strength Score: {score}/100")
        print(f"  - Strength Level: {color}{strength}{Style.RESET_ALL}")
        
        # Progress bar
        bar_length = 50
        filled_length = int(bar_length * score // 100)
        bar = "#" * filled_length + "-" * (bar_length - filled_length)
        print(f"\n{color}[{bar}] {score}%{Style.RESET_ALL}")
        
        # Security issues
        issues = self.check_common_patterns(password)
        if issues:
            print(f"\n{Fore.YELLOW}[!] Security Issues Detected:{Style.RESET_ALL}")
            for i, issue in enumerate(issues, 1):
                print(f"  {i}. {issue}")
          # zxcvbn specific patterns
        if zxcvbn_result and zxcvbn_result.get('sequence'):
            print(f"\n{Fore.YELLOW}[PATTERN] Pattern Analysis (zxcvbn):{Style.RESET_ALL}")
            for match in zxcvbn_result['sequence']:
                pattern_type = match.get('pattern', 'unknown')
                token = match.get('token', '')
                print(f"  - {pattern_type.title()}: '{token}'")
        
        # Have I Been Pwned check
        if self.hibp_checker:
            print(f"\n{Fore.CYAN}[HIBP] Have I Been Pwned Check:{Style.RESET_ALL}")
            try:
                hibp_result = self.hibp_checker.get_breach_info(password)
                if hibp_result['is_compromised']:
                    print(f"  - {Fore.RED}⚠️  PASSWORD COMPROMISED!{Style.RESET_ALL}")
                    print(f"  - Found in {hibp_result['breach_count']:,} data breaches")
                    print(f"  - Risk Level: {Fore.RED}{hibp_result['risk_level']}{Style.RESET_ALL}")
                    print(f"  - {Fore.YELLOW}{hibp_result['recommendation']}{Style.RESET_ALL}")
                else:
                    print(f"  - {Fore.GREEN}✓ Password not found in known data breaches{Style.RESET_ALL}")
                    print(f"  - {hibp_result['recommendation']}")
            except Exception as e:
                print(f"  - {Fore.YELLOW}Unable to check breaches: {str(e)}{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.YELLOW}[HIBP] Have I Been Pwned check unavailable{Style.RESET_ALL}")
            print(f"  - Install requests library for breach checking: pip install requests")
        
        # Suggestions
        if suggestions:
            print(f"\n{Fore.CYAN}[+] Improvement Suggestions:{Style.RESET_ALL}")
            for i, suggestion in enumerate(suggestions, 1):
                print(f"  {i}. {suggestion}")
        
        # Time to crack estimation
        if zxcvbn_result:
            self._display_crack_time_zxcvbn(zxcvbn_result)
        else:
            self._display_crack_time_builtin(entropy)
        
        # Additional security tips
        self._display_security_tips(score)
        
        print("\n" + "="*70)
    
    def _display_crack_time_zxcvbn(self, result: Dict) -> None:
        """Display crack time using zxcvbn data"""
        print(f"\n{Fore.CYAN}[TIME] Estimated Crack Time:{Style.RESET_ALL}")
        
        # Online attack (throttled)
        online_throttled = result['crack_times_display']['online_throttling_100_per_hour']
        print(f"  - Online attack (throttled): {Fore.RED}{online_throttled}{Style.RESET_ALL}")
        
        # Online attack (no throttling)
        online_no_throttling = result['crack_times_display']['online_no_throttling_10_per_second']
        print(f"  - Online attack (unthrottled): {Fore.YELLOW}{online_no_throttling}{Style.RESET_ALL}")
        
        # Offline attack (slow)
        offline_slow = result['crack_times_display']['offline_slow_hashing_1e4_per_second']
        print(f"  - Offline attack (slow): {Fore.YELLOW}{offline_slow}{Style.RESET_ALL}")
        
        # Offline attack (fast)
        offline_fast = result['crack_times_display']['offline_fast_hashing_1e10_per_second']
        print(f"  - Offline attack (fast): {Fore.GREEN}{offline_fast}{Style.RESET_ALL}")
    
    def _display_crack_time_builtin(self, entropy: float) -> None:
        """Display estimated time to crack using entropy"""
        # Assume 1 billion guesses per second (modern hardware)
        guesses_per_second = 1e9
        total_combinations = 2 ** entropy
        seconds_to_crack = total_combinations / (2 * guesses_per_second)  # Average case
        
        print(f"\n{Fore.CYAN}[TIME] Estimated Crack Time (Offline Attack):{Style.RESET_ALL}")
        
        if seconds_to_crack < 1:
            print(f"  {Fore.RED}Instantly{Style.RESET_ALL}")
        elif seconds_to_crack < 60:
            print(f"  {Fore.RED}{seconds_to_crack:.1f} seconds{Style.RESET_ALL}")
        elif seconds_to_crack < 3600:
            minutes = seconds_to_crack / 60
            print(f"  {Fore.RED}{minutes:.1f} minutes{Style.RESET_ALL}")
        elif seconds_to_crack < 86400:
            hours = seconds_to_crack / 3600
            print(f"  {Fore.YELLOW}{hours:.1f} hours{Style.RESET_ALL}")
        elif seconds_to_crack < 31536000:
            days = seconds_to_crack / 86400
            print(f"  {Fore.YELLOW}{days:.1f} days{Style.RESET_ALL}")
        elif seconds_to_crack < 31536000000:
            years = seconds_to_crack / 31536000
            print(f"  {Fore.GREEN}{years:.1f} years{Style.RESET_ALL}")
        else:
            years = seconds_to_crack / 31536000
            if years > 1e6:
                print(f"  {Fore.GREEN}Millions of years{Style.RESET_ALL}")
            else:
                print(f"  {Fore.GREEN}{years:.0f} years{Style.RESET_ALL}")
    
    def _display_security_tips(self, score: int) -> None:
        """Display security tips based on password score"""
        print(f"\n{Fore.CYAN}[SECURITY] Security Recommendations:{Style.RESET_ALL}")
        
        if score < 40:
            print(f"  - {Fore.RED}Critical:{Style.RESET_ALL} This password is easily crackable")
            print(f"  - Use a password manager to generate strong passwords")
            print(f"  - Enable two-factor authentication (2FA) wherever possible")
        elif score < 60:
            print(f"  - {Fore.YELLOW}Important:{Style.RESET_ALL} Consider strengthening this password")
            print(f"  - Add more character types and length")
        elif score < 80:
            print(f"  - {Fore.GREEN}Good:{Style.RESET_ALL} This is a reasonably strong password")
            print(f"  - Consider making it even longer for extra security")
        else:
            print(f"  - {Fore.GREEN}Excellent:{Style.RESET_ALL} This is a very strong password")
        
        print(f"  - Never reuse passwords across multiple accounts")
        print(f"  - Update passwords regularly, especially for sensitive accounts")
        print(f"  - Store passwords securely using a password manager")


def main():
    """Main function to run the password strength checker"""
    parser = argparse.ArgumentParser(
        description="Enhanced Password Strength Checker Tool with zxcvbn Integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python enhanced_password_checker.py -p "MyPassword123!"
  python enhanced_password_checker.py --interactive
  python enhanced_password_checker.py --batch passwords.txt
  python enhanced_password_checker.py --help

Features:
  • Integrates with zxcvbn library for advanced analysis
  • Comprehensive pattern detection
  • Multiple attack scenario time estimations  • Color-coded output for better visualization
  • Detailed security recommendations
        """
    )
    
    parser.add_argument(
        '-p', '--password',
        type=str,
        help='Password to analyze'
    )
    
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Run in interactive mode'
    )
    
    parser.add_argument(
        '-b', '--batch',
        type=str,
        help='Analyze passwords from a file (one per line)'
    )
    
    parser.add_argument(
        '--no-zxcvbn',
        action='store_true',
        help='Force use of built-in algorithm instead of zxcvbn'
    )
    
    parser.add_argument(
        '--no-hibp',
        action='store_true',
        help='Skip Have I Been Pwned breach checking'
    )
    
    args = parser.parse_args()
    
    # Initialize the checker
    checker = PasswordStrengthChecker()
    
    # Force built-in algorithm if requested
    if args.no_zxcvbn:
        checker.use_zxcvbn = False
    
    # Disable HIBP checking if requested
    if args.no_hibp:
        checker.hibp_checker = None
    
    # Display header
    print(f"\n{Fore.CYAN + Style.BRIGHT}[*] ENHANCED PASSWORD STRENGTH CHECKER [*]{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Advanced password security analysis with comprehensive checks{Style.RESET_ALL}")
    
    try:
        if args.batch:
            # Batch mode
            try:
                with open(args.batch, 'r', encoding='utf-8') as f:
                    passwords = [line.strip() for line in f if line.strip()]
                
                print(f"\n{Fore.YELLOW}Batch Mode - Analyzing {len(passwords)} passwords{Style.RESET_ALL}")
                
                for i, password in enumerate(passwords, 1):
                    print(f"\n{Fore.CYAN}--- Password {i}/{len(passwords)} ---{Style.RESET_ALL}")
                    checker.analyze_password(password)
                    
                    if i < len(passwords):
                        input(f"\n{Fore.YELLOW}Press Enter to continue to next password...{Style.RESET_ALL}")
                        
            except FileNotFoundError:
                print(f"{Fore.RED}Error: File '{args.batch}' not found{Style.RESET_ALL}")
                sys.exit(1)
            except Exception as e:
                print(f"{Fore.RED}Error reading file: {str(e)}{Style.RESET_ALL}")
                sys.exit(1)
                
        elif args.password:
            # Analyze provided password
            checker.analyze_password(args.password)
            
        elif args.interactive or len(sys.argv) == 1:
            # Interactive mode
            print(f"\n{Fore.YELLOW}Interactive Mode - Enter 'quit' to exit{Style.RESET_ALL}")
            while True:
                try:
                    password = input(f"\n{Fore.CYAN}Enter password to analyze: {Style.RESET_ALL}")
                    if password.lower() in ['quit', 'exit', 'q']:
                        print(f"{Fore.GREEN}Thank you for using Enhanced Password Strength Checker!{Style.RESET_ALL}")
                        break
                    if password:
                        checker.analyze_password(password)
                    else:
                        print(f"{Fore.RED}Please enter a password{Style.RESET_ALL}")
                except KeyboardInterrupt:
                    print(f"\n{Fore.GREEN}Thank you for using Enhanced Password Strength Checker!{Style.RESET_ALL}")
                    break
        else:
            parser.print_help()
            
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    main()
