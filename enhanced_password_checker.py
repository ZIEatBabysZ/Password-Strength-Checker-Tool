#!/usr/bin/env python3
"""
Enhanced Password Strength Checker Tool
Comprehensive password analysis with multi-language support
"""

import re
import math
import argparse
import sys
import os
import json
import csv
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from colorama import Fore, Style, init
import importlib.util

# Initialize colorama for cross-platform color support
init(autoreset=True)

# Import internationalization support
try:
    from i18n_manager import i18n, _
except ImportError:
    # Fallback if i18n not available
    print("Warning: Internationalization not available. Using English only.")
    def _(text): return text
    i18n = None

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
            print(f"{Fore.YELLOW}{_('Note: zxcvbn library not found. Using built-in scoring algorithm.')}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}{_('Install it with: pip install zxcvbn')}{Style.RESET_ALL}\n")
        
        if not HIBP_AVAILABLE:
            print(f"{Fore.YELLOW}{_('Note: Have I Been Pwned integration not available.')}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}{_('Install requests with: pip install requests')}{Style.RESET_ALL}\n")
    
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
            issues.append(_("Contains repeated characters"))
        
        # Check for sequential patterns
        sequences = ['123', '234', '345', '456', '567', '678', '789', '890',
                    'abc', 'bcd', 'cde', 'def', 'efg', 'fgh', 'ghi', 'hij',
                    'ijk', 'jkl', 'klm', 'lmn', 'mno', 'nop', 'opq', 'pqr',
                    'qrs', 'rst', 'stu', 'tuv', 'uvw', 'vwx', 'wxy', 'xyz']        
        for seq in sequences:
            if seq in password_lower or seq[::-1] in password_lower:
                issues.append(_("Contains sequential characters"))
                break
          # Check for keyboard patterns
        keyboard_patterns = ['qwerty', 'asdf', 'zxcv', '1234', 'qwertyuiop',
                           'asdfghjkl', 'zxcvbnm', '1qaz', '2wsx', '3edc',
                           'qwe', 'asd', 'zxc', 'wer', 'sdf', 'xcv']
        
        for pattern in keyboard_patterns:
            if pattern in password_lower:
                issues.append(_("Contains keyboard patterns"))
                break
        
        # Check for common words
        for word in self.dictionary_words:
            if len(word) > 3 and word in password_lower:
                issues.append(_("Contains dictionary word: '{}'").format(word))
        
        # Check against common passwords
        if password_lower in self.common_passwords:
            issues.append(_("Password is in common passwords list"))
        
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
            suggestions.append(_("Use at least 8 characters"))
        
        if length < 8:
            suggestions.append(_("Increase password length for better security"))
        
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
            suggestions.append(_("Add lowercase letters"))
        if not char_types['uppercase']:
            suggestions.append(_("Add uppercase letters"))
        if not char_types['digits']:
            suggestions.append(_("Add numbers"))
        if not char_types['special']:
            suggestions.append(_("Add special characters"))
        
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
                suggestions.append(_("Avoid using dictionary words"))
            elif "common passwords" in issue:
                suggestions.append(_("This password is too common - choose a unique one"))
            elif "repeated characters" in issue:
                suggestions.append(_("Avoid repeating the same character"))
            elif "sequential characters" in issue:
                suggestions.append(_("Avoid sequential characters (123, abc)"))
            elif "keyboard patterns" in issue:
                suggestions.append(_("Avoid keyboard patterns (qwerty, asdf)"))
        
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
            suggestions.append(_("Use more unique characters"))
        
        # Ensure score is between 0 and 100
        score = max(0, min(100, score))
        
        # Determine strength label
        if score >= 80:
            strength = _("Very Strong")
        elif score >= 60:
            strength = _("Strong")
        elif score >= 40:
            strength = _("Medium")
        elif score >= 20:
            strength = _("Weak")
        else:
            strength = _("Very Weak")
        
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
        strength_mapping = {0: _("Very Weak"), 1: _("Weak"), 2: _("Medium"), 3: _("Strong"), 4: _("Very Strong")}
        strength = strength_mapping.get(zxcvbn_score, _("Very Weak"))          # Generate suggestions
        suggestions = []
        if result['feedback']['warning']:
            suggestions.append(_(result['feedback']['warning']))
        for suggestion in result['feedback']['suggestions']:
            suggestions.append(_(suggestion))
        
        # Add our own suggestions
        char_types = self.check_character_types(password)
        if not char_types['uppercase']:
            suggestions.append(_("Add uppercase letters"))
        if not char_types['lowercase']:
            suggestions.append(_("Add lowercase letters"))
        if not char_types['digits']:
            suggestions.append(_("Add numbers"))
        if not char_types['special']:
            suggestions.append(_("Add special characters"))
        
        if len(password) < 8:
            suggestions.append(_("Use at least 8 characters"))
        if len(password) < 12:
            suggestions.append(_("Consider using 12+ characters for better security"))
        
        return int(final_score), strength, suggestions, result
    
    def get_color_for_strength(self, strength: str) -> str:
        """Get color code for password strength"""
        colors = {
            _("Very Strong"): Fore.GREEN + Style.BRIGHT,
            _("Strong"): Fore.GREEN,
            _("Medium"): Fore.YELLOW,
            _("Weak"): Fore.RED,
            _("Very Weak"): Fore.RED + Style.BRIGHT
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
        print(f"{Fore.CYAN + Style.BRIGHT}[*] {_('PASSWORD STRENGTH ANALYSIS')} [*]{Style.RESET_ALL}")
        print("="*70)
        
        # Algorithm info
        algorithm = _("zxcvbn + Enhanced Analysis") if self.use_zxcvbn else _("Built-in Algorithm")
        print(f"\n{Fore.CYAN}{_('Analysis Method')}:{Style.RESET_ALL} {algorithm}")
        
        # Basic info
        print(f"{Fore.CYAN}{_('Password Length')}:{Style.RESET_ALL} {len(password)} {_('characters')}")
        
        # Character types
        char_types = self.check_character_types(password)
        print(f"\n{Fore.CYAN}{_('Character Composition')}:{Style.RESET_ALL}")
        print(f"  - {_('Lowercase letters')}: {Fore.GREEN + '[YES]' if char_types['lowercase'] else Fore.RED + '[NO]'}{Style.RESET_ALL}")
        print(f"  - {_('Uppercase letters')}: {Fore.GREEN + '[YES]' if char_types['uppercase'] else Fore.RED + '[NO]'}{Style.RESET_ALL}")
        print(f"  - {_('Numbers')}: {Fore.GREEN + '[YES]' if char_types['digits'] else Fore.RED + '[NO]'}{Style.RESET_ALL}")
        print(f"  - {_('Special characters')}: {Fore.GREEN + '[YES]' if char_types['special'] else Fore.RED + '[NO]'}{Style.RESET_ALL}")
        
        # Entropy and zxcvbn specific info
        entropy = self.calculate_entropy(password)
        print(f"\n{Fore.CYAN}{_('Technical Metrics')}:{Style.RESET_ALL}")
        print(f"  - {_('Entropy')}: {entropy:.1f} {_('bits')}")
        print(f"  - {_('Unique characters')}: {len(set(password))}/{len(password)}")
        if zxcvbn_result:
            print(f"  - {_('zxcvbn Score')}: {zxcvbn_result['score']}/4")
            print(f"  - {_('Guesses needed')}: {zxcvbn_result['guesses']:,}")
            if 'entropy' in zxcvbn_result:
                print(f"  - {_('zxcvbn Entropy')}: {zxcvbn_result['entropy']:.1f} {_('bits')}")
        
        # Score and strength
        print(f"\n{Fore.CYAN}{_('Overall Assessment')}:{Style.RESET_ALL}")
        print(f"  - {_('Strength Score')}: {score}/100")
        print(f"  - {_('Strength Level')}: {color}{strength}{Style.RESET_ALL}")
        
        # Progress bar
        bar_length = 50
        filled_length = int(bar_length * score // 100)
        bar = "#" * filled_length + "-" * (bar_length - filled_length)
        print(f"\n{color}[{bar}] {score}%{Style.RESET_ALL}")
        
        # Security issues
        issues = self.check_common_patterns(password)
        if issues:
            print(f"\n{Fore.YELLOW}[!] {_('Security Issues Detected')}:{Style.RESET_ALL}")
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
            print(f"\n{Fore.CYAN}[HIBP] {_('Have I Been Pwned Check')}:{Style.RESET_ALL}")
            try:
                hibp_result = self.hibp_checker.get_breach_info(password)
                if hibp_result['is_compromised']:
                    print(f"  - {Fore.RED}⚠️  {_('PASSWORD COMPROMISED!')}{Style.RESET_ALL}")
                    print(f"  - {_('Found in')} {hibp_result['breach_count']:,} {_('data breaches')}")
                    print(f"  - {_('Risk Level')}: {Fore.RED}{_(hibp_result['risk_level'])}{Style.RESET_ALL}")
                    print(f"  - {Fore.YELLOW}{hibp_result['recommendation']}{Style.RESET_ALL}")
                else:
                    print(f"  - {Fore.GREEN}✓ {_('Password not found in known data breaches')}{Style.RESET_ALL}")
                    print(f"  - {hibp_result['recommendation']}")
            except Exception as e:
                print(f"  - {Fore.YELLOW}{_('Unable to check breaches')}: {str(e)}{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.YELLOW}[HIBP] {_('Have I Been Pwned check unavailable')}{Style.RESET_ALL}")
            print(f"  - {_('Install requests library for breach checking')}: pip install requests")
        
        # Suggestions
        if suggestions:
            print(f"\n{Fore.CYAN}[+] {_('Improvement Suggestions')}:{Style.RESET_ALL}")
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
        print(f"\n{Fore.CYAN}[SECURITY] {_('Security Recommendations')}:{Style.RESET_ALL}")
        
        if score < 40:
            print(f"  - {Fore.RED}{_('Critical')}: {_('This password is easily crackable')}{Style.RESET_ALL}")
            print(f"  - {_('Use a password manager to generate strong passwords')}")
            print(f"  - {_('Enable two-factor authentication (2FA) wherever possible')}")
        elif score < 60:
            print(f"  - {Fore.YELLOW}{_('Important')}: {_('Consider strengthening this password')}{Style.RESET_ALL}")
            print(f"  - {_('Add more character types and length')}")
        elif score < 80:
            print(f"  - {Fore.GREEN}{_('Good')}: {_('This is a reasonably strong password')}{Style.RESET_ALL}")
            print(f"  - {_('Consider making it even longer for extra security')}")
        else:
            print(f"  - {Fore.GREEN}{_('Excellent')}: {_('This is a very strong password')}{Style.RESET_ALL}")
        
        print(f"  - {_('Never reuse passwords across multiple accounts')}")
        print(f"  - {_('Update passwords regularly, especially for sensitive accounts')}")
        print(f"  - {_('Store passwords securely using a password manager')}")
    
    def get_password_analysis_data(self, password: str, include_password: bool = False) -> Dict:
        """
        Analyze password and return structured data for export
        
        Args:
            password: Password to analyze
            include_password: Whether to include the actual password in results (security consideration)
            
        Returns:
            Dictionary containing all analysis results
        """
        if not password:
            return {"error": "Password cannot be empty"}
        
        # Use zxcvbn if available, otherwise use built-in algorithm
        if self.use_zxcvbn:
            score, strength, suggestions, zxcvbn_result = self.calculate_score_zxcvbn(password)
        else:
            score, strength, suggestions = self.calculate_score_builtin(password)
            zxcvbn_result = None
        
        # Get basic analysis data
        char_types = self.check_character_types(password)
        entropy = self.calculate_entropy(password)
        issues = self.check_common_patterns(password)
        
        # Analyze HIBP if available
        hibp_result = None
        if self.hibp_checker:
            try:
                hibp_result = self.hibp_checker.get_breach_info(password)
            except Exception as e:
                hibp_result = {"error": f"HIBP check failed: {str(e)}"}
        
        # Build structured result
        result = {
            "timestamp": datetime.now().isoformat(),
            "analysis_method": "zxcvbn + Enhanced Analysis" if self.use_zxcvbn else "Built-in Algorithm",
            "password_length": len(password),
            "character_composition": {
                "lowercase_letters": char_types['lowercase'],
                "uppercase_letters": char_types['uppercase'],
                "numbers": char_types['digits'],
                "special_characters": char_types['special'],
                "character_types_count": sum(char_types.values())
            },
            "technical_metrics": {
                "entropy_bits": round(entropy, 2),
                "unique_characters": len(set(password)),
                "uniqueness_ratio": round(len(set(password)) / len(password), 3) if len(password) > 0 else 0
            },
            "strength_assessment": {
                "score": score,
                "max_score": 100,
                "strength_level": strength,
                "percentage": score
            },
            "security_issues": {
                "issues_found": len(issues),
                "issue_list": issues
            },
            "improvement_suggestions": suggestions,
            "breach_check": hibp_result if hibp_result else {"status": "unavailable", "reason": "HIBP integration not available"}
        }
        
        # Add zxcvbn specific data if available
        if zxcvbn_result:
            result["zxcvbn_analysis"] = {
                "score": zxcvbn_result['score'],
                "guesses": zxcvbn_result['guesses'],
                "crack_times": zxcvbn_result.get('crack_times_seconds', {}),
                "feedback": {
                    "warning": zxcvbn_result['feedback'].get('warning', ''),
                    "suggestions": zxcvbn_result['feedback'].get('suggestions', [])
                }
            }
            if 'entropy' in zxcvbn_result:
                result["technical_metrics"]["zxcvbn_entropy_bits"] = round(zxcvbn_result['entropy'], 2)
        
        # Optionally include password (security consideration)
        if include_password:
            result["password"] = password
        else:
            result["password_hash"] = hash(password)  # For identification without exposing password
        
        return result

    def export_analysis_to_json(self, analysis_data: Dict, filename: str) -> bool:
        """
        Export analysis data to JSON format
        
        Args:
            analysis_data: Analysis result from get_password_analysis_data
            filename: Output filename
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Convert any non-serializable objects to strings
            def json_serializer(obj):
                from decimal import Decimal
                if isinstance(obj, Decimal):
                    return float(obj)
                raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(analysis_data, f, indent=2, ensure_ascii=False, default=json_serializer)
            return True
        except Exception as e:
            print(f"{Fore.RED}Error exporting to JSON: {str(e)}{Style.RESET_ALL}")
            return False

    def export_batch_to_csv(self, batch_results: List[Dict], filename: str) -> bool:
        """
        Export batch analysis results to CSV format
        
        Args:
            batch_results: List of analysis results
            filename: Output filename
            
        Returns:
            True if successful, False otherwise
        """
        if not batch_results:
            print(f"{Fore.RED}No results to export{Style.RESET_ALL}")
            return False
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                # Define CSV columns
                fieldnames = [
                    'timestamp', 'password_length', 'score', 'strength_level',
                    'lowercase_letters', 'uppercase_letters', 'numbers', 'special_characters',
                    'character_types_count', 'entropy_bits', 'unique_characters',
                    'uniqueness_ratio', 'issues_found', 'issue_list', 'improvement_suggestions',
                    'breach_status', 'breach_count', 'analysis_method'
                ]
                
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for result in batch_results:
                    # Flatten the nested structure for CSV
                    row = {
                        'timestamp': result.get('timestamp', ''),
                        'password_length': result.get('password_length', 0),
                        'score': result.get('strength_assessment', {}).get('score', 0),
                        'strength_level': result.get('strength_assessment', {}).get('strength_level', ''),
                        'lowercase_letters': result.get('character_composition', {}).get('lowercase_letters', False),
                        'uppercase_letters': result.get('character_composition', {}).get('uppercase_letters', False),
                        'numbers': result.get('character_composition', {}).get('numbers', False),
                        'special_characters': result.get('character_composition', {}).get('special_characters', False),
                        'character_types_count': result.get('character_composition', {}).get('character_types_count', 0),
                        'entropy_bits': result.get('technical_metrics', {}).get('entropy_bits', 0),
                        'unique_characters': result.get('technical_metrics', {}).get('unique_characters', 0),
                        'uniqueness_ratio': result.get('technical_metrics', {}).get('uniqueness_ratio', 0),
                        'issues_found': result.get('security_issues', {}).get('issues_found', 0),
                        'issue_list': '; '.join(result.get('security_issues', {}).get('issue_list', [])),
                        'improvement_suggestions': '; '.join(result.get('improvement_suggestions', [])),
                        'breach_status': 'compromised' if result.get('breach_check', {}).get('is_compromised') else 'safe',
                        'breach_count': result.get('breach_check', {}).get('breach_count', 0),                        'analysis_method': result.get('analysis_method', '')
                    }
                    writer.writerow(row)
            return True
        except Exception as e:
            print(f"{Fore.RED}Error exporting to CSV: {str(e)}{Style.RESET_ALL}")
            return False

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
  • Multiple attack scenario time estimations
  • Color-coded output for better visualization
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
        action='store_true',        help='Force use of built-in algorithm instead of zxcvbn'
    )
    
    parser.add_argument(
        '--no-hibp',
        action='store_true',
        help='Skip Have I Been Pwned breach checking'
    )
    
    parser.add_argument(
        '--export-json',
        type=str,
        help='Export analysis results to JSON file (single password analysis only)'
    )
    
    parser.add_argument(
        '--export-csv',
        type=str,
        help='Export batch analysis results to CSV file (batch mode only)'
    )
    
    parser.add_argument(
        '--include-passwords',
        action='store_true',
        help='Include actual passwords in export (SECURITY RISK - use with caution)'
    )
    
    parser.add_argument(
        '--language', '-l',
        type=str,
        choices=['en', 'es', 'fr', 'de', 'zh', 'ja'],
        help='Language for output (en=English, es=Spanish, fr=French, de=German, zh=Chinese, ja=Japanese)'
    )
    
    args = parser.parse_args()
    
    # Set language if specified
    if args.language and i18n:
        if not i18n.set_language(args.language):
            print(f"{Fore.YELLOW}Warning: Language '{args.language}' not fully supported. Using English.{Style.RESET_ALL}")
    
    # Initialize the checker
    checker = PasswordStrengthChecker()
    
    # Force built-in algorithm if requested
    if args.no_zxcvbn:
        checker.use_zxcvbn = False
      # Disable HIBP checking if requested
    if args.no_hibp:
        checker.hibp_checker = None
      # Display header
    print(f"\n{Fore.CYAN + Style.BRIGHT}[*] {_('ENHANCED PASSWORD STRENGTH CHECKER')} [*]{Style.RESET_ALL}")
    
    try:
        if args.batch:
            # Batch mode
            try:
                with open(args.batch, 'r', encoding='utf-8') as f:
                    passwords = [line.strip() for line in f if line.strip()]
                
                print(f"\n{Fore.YELLOW}Batch Mode - Analyzing {len(passwords)} passwords{Style.RESET_ALL}")
                
                # Collect results for export if requested
                batch_results = []
                
                for i, password in enumerate(passwords, 1):
                    print(f"\n{Fore.CYAN}--- Password {i}/{len(passwords)} ---{Style.RESET_ALL}")
                    
                    # Get analysis data for export
                    if args.export_csv:
                        analysis_data = checker.get_password_analysis_data(password, args.include_passwords)
                        batch_results.append(analysis_data)
                    
                    # Display analysis
                    checker.analyze_password(password)
                    
                    if i < len(passwords) and not args.export_csv:
                        input(f"\n{Fore.YELLOW}Press Enter to continue to next password...{Style.RESET_ALL}")
                
                # Export to CSV if requested
                if args.export_csv and batch_results:
                    print(f"\n{Fore.CYAN}Exporting results to CSV...{Style.RESET_ALL}")
                    if checker.export_batch_to_csv(batch_results, args.export_csv):
                        print(f"{Fore.GREEN}✓ Results exported to {args.export_csv}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}✗ Failed to export results{Style.RESET_ALL}")
                        
            except FileNotFoundError:
                print(f"{Fore.RED}Error: File '{args.batch}' not found{Style.RESET_ALL}")
                sys.exit(1)
            except Exception as e:
                print(f"{Fore.RED}Error reading file: {str(e)}{Style.RESET_ALL}")
                sys.exit(1)
                
        elif args.password:
            # Analyze provided password
            checker.analyze_password(args.password)
            
            # Export to JSON if requested
            if args.export_json:
                print(f"\n{Fore.CYAN}Exporting results to JSON...{Style.RESET_ALL}")
                analysis_data = checker.get_password_analysis_data(args.password, args.include_passwords)
                if checker.export_analysis_to_json(analysis_data, args.export_json):
                    print(f"{Fore.GREEN}✓ Results exported to {args.export_json}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}✗ Failed to export results{Style.RESET_ALL}")
            
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
