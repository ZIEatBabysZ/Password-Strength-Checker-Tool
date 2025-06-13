#!/usr/bin/env python3
"""
Password Strength Checker Tool

A comprehensive command-line tool that analyzes password strength using multiple criteria
including length, character types, dictionary words, entropy, and common password detection.

Author: Password Security Tool
Date: June 2025
"""

import re
import math
import argparse
import sys
import os
from typing import Dict, List, Tuple
from colorama import Fore, Style, init

# Initialize colorama for cross-platform color support
init(autoreset=True)

class PasswordStrengthChecker:
    """Main class for password strength analysis"""
    
    def __init__(self):
        """Initialize the password checker with common passwords and dictionary words"""
        self.common_passwords = self._load_common_passwords()
        self.dictionary_words = self._load_dictionary_words()
        
    def _load_common_passwords(self) -> set:
        """Load common passwords from file or use built-in list"""
        common_passwords_file = "common_passwords.txt"
        
        # Built-in list of most common passwords
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
            "2010", "kitten", "gosox", "love123", "princess"
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
            "monkey", "bear", "wolf", "fox", "rabbit", "mouse", "snake"
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
                           'asdfghjkl', 'zxcvbnm', '1qaz', '2wsx', '3edc']
        
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
    
    def calculate_score(self, password: str) -> Tuple[int, str, List[str]]:
        """Calculate overall password strength score and provide recommendations"""
        score = 0
        suggestions = []
        
        # Length scoring (0-25 points)
        length = len(password)
        if length >= 12:
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
        if entropy >= 60:
            score += 25
        elif entropy >= 50:
            score += 20
        elif entropy >= 40:
            score += 15
        elif entropy >= 30:
            score += 10
        else:
            score += 5
        
        # Pattern and common password penalties (0-25 points deduction)
        issues = self.check_common_patterns(password)
        penalty = min(len(issues) * 5, 25)
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
        
        score, strength, suggestions = self.calculate_score(password)
        color = self.get_color_for_strength(strength)
        
        print("\n" + "="*60)
        print(f"{Fore.CYAN + Style.BRIGHT}PASSWORD STRENGTH ANALYSIS{Style.RESET_ALL}")
        print("="*60)
        
        # Basic info
        print(f"\n{Fore.CYAN}Password Length:{Style.RESET_ALL} {len(password)} characters")
        
        # Character types
        char_types = self.check_character_types(password)
        print(f"\n{Fore.CYAN}Character Types:{Style.RESET_ALL}")
        print(f"  - Lowercase letters: {Fore.GREEN + '[YES]' if char_types['lowercase'] else Fore.RED + '[NO]'}{Style.RESET_ALL}")
        print(f"  - Uppercase letters: {Fore.GREEN + '[YES]' if char_types['uppercase'] else Fore.RED + '[NO]'}{Style.RESET_ALL}")
        print(f"  - Numbers: {Fore.GREEN + '[YES]' if char_types['digits'] else Fore.RED + '[NO]'}{Style.RESET_ALL}")
        print(f"  - Special characters: {Fore.GREEN + '[YES]' if char_types['special'] else Fore.RED + '[NO]'}{Style.RESET_ALL}")
        
        # Entropy
        entropy = self.calculate_entropy(password)
        print(f"\n{Fore.CYAN}Entropy:{Style.RESET_ALL} {entropy:.1f} bits")
        
        # Score and strength
        print(f"\n{Fore.CYAN}Strength Score:{Style.RESET_ALL} {score}/100")
        print(f"{Fore.CYAN}Strength Level:{Style.RESET_ALL} {color}{strength}{Style.RESET_ALL}")
        
        # Progress bar
        bar_length = 40
        filled_length = int(bar_length * score // 100)
        bar = "#" * filled_length + "-" * (bar_length - filled_length)
        print(f"\n{color}[{bar}] {score}%{Style.RESET_ALL}")
        
        # Security issues
        issues = self.check_common_patterns(password)
        if issues:
            print(f"\n{Fore.YELLOW}[!] Security Issues:{Style.RESET_ALL}")
            for issue in issues:
                print(f"  - {issue}")
        
        # Suggestions
        if suggestions:
            print(f"\n{Fore.CYAN}[+] Improvement Suggestions:{Style.RESET_ALL}")
            for suggestion in suggestions:
                print(f"  - {suggestion}")
        
        # Time to crack estimation
        self._display_crack_time(entropy)
        
        print("\n" + "="*60)
    
    def _display_crack_time(self, entropy: float) -> None:
        """Display estimated time to crack the password"""
        # Assume 1 billion guesses per second (modern hardware)
        guesses_per_second = 1e9
        total_combinations = 2 ** entropy
        seconds_to_crack = total_combinations / (2 * guesses_per_second)  # Average case
        
        print(f"\n{Fore.CYAN}[TIME] Estimated Crack Time:{Style.RESET_ALL}")
        
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


def main():
    """Main function to run the password strength checker"""
    parser = argparse.ArgumentParser(
        description="Password Strength Checker Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python password_checker.py -p "MyPassword123!"
  python password_checker.py --interactive
  python password_checker.py --help
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
    
    args = parser.parse_args()
    
    # Initialize the checker
    checker = PasswordStrengthChecker()
    
    # Display header
    print(f"\n{Fore.CYAN + Style.BRIGHT}[*] PASSWORD STRENGTH CHECKER TOOL [*]{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Analyze your password security with comprehensive checks{Style.RESET_ALL}")
    
    try:
        if args.password:
            # Analyze provided password
            checker.analyze_password(args.password)
        elif args.interactive or len(sys.argv) == 1:
            # Interactive mode
            print(f"\n{Fore.YELLOW}Interactive Mode - Enter 'quit' to exit{Style.RESET_ALL}")
            while True:
                try:
                    password = input(f"\n{Fore.CYAN}Enter password to analyze: {Style.RESET_ALL}")
                    if password.lower() in ['quit', 'exit', 'q']:
                        print(f"{Fore.GREEN}Thank you for using Password Strength Checker!{Style.RESET_ALL}")
                        break
                    if password:
                        checker.analyze_password(password)
                    else:
                        print(f"{Fore.RED}Please enter a password{Style.RESET_ALL}")
                except KeyboardInterrupt:
                    print(f"\n{Fore.GREEN}Thank you for using Password Strength Checker!{Style.RESET_ALL}")
                    break
        else:
            parser.print_help()
            
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    main()
