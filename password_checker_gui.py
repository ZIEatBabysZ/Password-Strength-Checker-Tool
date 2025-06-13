#!/usr/bin/env python3
"""
Password Strength Checker Tool - GUI Version

A comprehensive GUI application that analyzes password strength using multiple criteria
including zxcvbn scoring, length, character types, dictionary words, entropy, and common password detection.

Author: Password Security Tool
Date: June 2025
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import re
import math
import threading
from typing import Dict, List, Tuple, Optional
import os
import sys

# Import the enhanced password checker class
try:
    from enhanced_password_checker import PasswordStrengthChecker
except ImportError:
    # Fallback if import fails
    print("Warning: Could not import enhanced_password_checker. Using basic functionality.")
    from password_checker import PasswordStrengthChecker

class PasswordCheckerGUI:
    """GUI class for password strength checker"""
    
    def __init__(self, root):
        """Initialize the GUI"""
        self.root = root
        self.root.title("🔒 Password Strength Checker Tool")
        self.root.geometry("800x700")
        self.root.minsize(700, 600)
        
        # Initialize the password checker
        self.checker = PasswordStrengthChecker()
        
        # Color scheme
        self.colors = {
            'Very Strong': '#2e7d32',  # Dark green
            'Strong': '#388e3c',       # Green
            'Medium': '#f57c00',       # Orange
            'Weak': '#d32f2f',         # Red
            'Very Weak': '#b71c1c'     # Dark red
        }
        
        self.create_widgets()
        
        # Center the window
        self.center_window()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")
        
    def create_widgets(self):
        """Create and arrange GUI widgets"""
        # Configure styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🔒 Password Strength Checker", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Password input section
        input_frame = ttk.LabelFrame(main_frame, text="Password Input", padding="10")
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        # Password entry
        ttk.Label(input_frame, text="Password:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(input_frame, textvariable=self.password_var, 
                                      show="*", font=('Arial', 11))
        self.password_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        self.password_entry.bind('<KeyRelease>', self.on_password_change)
        
        # Show/Hide password button
        self.show_password_var = tk.BooleanVar()
        self.show_button = ttk.Checkbutton(input_frame, text="Show", 
                                         variable=self.show_password_var,
                                         command=self.toggle_password_visibility)
        self.show_button.grid(row=0, column=2)
        
        # Control buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=1, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Button(button_frame, text="Analyze Password", 
                  command=self.analyze_password).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Generate Strong Password", 
                  command=self.generate_password).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Clear", 
                  command=self.clear_analysis).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Batch Analysis", 
                  command=self.batch_analysis).pack(side=tk.LEFT)
        
        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="Analysis Results", padding="10")
        results_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(2, weight=1)
        
        # Strength meter
        meter_frame = ttk.Frame(results_frame)
        meter_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        meter_frame.columnconfigure(1, weight=1)
        
        ttk.Label(meter_frame, text="Strength:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        # Progress bar for strength
        self.strength_progress = ttk.Progressbar(meter_frame, length=300, mode='determinate')
        self.strength_progress.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.strength_label = ttk.Label(meter_frame, text="Enter a password to analyze", 
                                      font=('Arial', 10, 'bold'))
        self.strength_label.grid(row=0, column=2)
        
        # Score display
        score_frame = ttk.Frame(results_frame)
        score_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.score_label = ttk.Label(score_frame, text="Score: --/100", font=('Arial', 12, 'bold'))
        self.score_label.pack(side=tk.LEFT)
        
        # Results text area
        self.results_text = scrolledtext.ScrolledText(results_frame, height=20, width=80,
                                                    font=('Consolas', 10), wrap=tk.WORD)
        self.results_text.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure text tags for colored output
        self.results_text.tag_configure("header", font=('Arial', 12, 'bold'), foreground='blue')
        self.results_text.tag_configure("strong", font=('Arial', 10, 'bold'), foreground='green')
        self.results_text.tag_configure("medium", font=('Arial', 10, 'bold'), foreground='orange')
        self.results_text.tag_configure("weak", font=('Arial', 10, 'bold'), foreground='red')
        self.results_text.tag_configure("info", foreground='blue')
        self.results_text.tag_configure("warning", foreground='orange')
        self.results_text.tag_configure("error", foreground='red')
        self.results_text.tag_configure("success", foreground='green')
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        # Menu bar
        self.create_menu()
        
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Batch Analysis...", command=self.batch_analysis)
        file_menu.add_separator()
        file_menu.add_command(label="Export Results...", command=self.export_results)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Generate Password...", command=self.generate_password_dialog)
        tools_menu.add_command(label="Password Tips", command=self.show_password_tips)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="User Guide", command=self.show_user_guide)
        
    def toggle_password_visibility(self):
        """Toggle password visibility"""
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")
            
    def on_password_change(self, event=None):
        """Handle password input changes for real-time analysis"""
        password = self.password_var.get()
        if len(password) > 0:
            # Quick analysis for real-time feedback
            self.quick_analysis(password)
        else:
            self.reset_display()
            
    def quick_analysis(self, password):
        """Perform quick analysis for real-time feedback"""
        try:
            if hasattr(self.checker, 'calculate_score_builtin'):
                score, strength, _ = self.checker.calculate_score_builtin(password)
            else:
                score, strength, _ = self.checker.calculate_score(password)
            
            # Update progress bar
            self.strength_progress['value'] = score
            
            # Update strength label with color
            color = self.colors.get(strength, 'black')
            self.strength_label.config(text=strength, foreground=color)
            
            # Update score
            self.score_label.config(text=f"Score: {score}/100")
            
        except Exception as e:
            self.status_var.set(f"Error in quick analysis: {str(e)}")
            
    def reset_display(self):
        """Reset the display elements"""
        self.strength_progress['value'] = 0
        self.strength_label.config(text="Enter a password to analyze", foreground='black')
        self.score_label.config(text="Score: --/100")
        
    def analyze_password(self):
        """Perform full password analysis"""
        password = self.password_var.get().strip()
        
        if not password:
            messagebox.showwarning("Input Required", "Please enter a password to analyze.")
            return
            
        # Clear previous results
        self.results_text.delete(1.0, tk.END)
        self.status_var.set("Analyzing password...")
        
        # Run analysis in a separate thread to prevent GUI freezing
        thread = threading.Thread(target=self._perform_analysis, args=(password,))
        thread.daemon = True
        thread.start()
        
    def _perform_analysis(self, password):
        """Perform the actual analysis (runs in separate thread)"""
        try:
            # Capture the analysis output
            analysis_result = self._get_analysis_result(password)
            
            # Update GUI in main thread
            self.root.after(0, self._display_analysis_result, analysis_result)
            
        except Exception as e:
            error_msg = f"Error during analysis: {str(e)}"
            self.root.after(0, self._display_error, error_msg)
            
    def _get_analysis_result(self, password):
        """Get analysis result as formatted text"""
        if hasattr(self.checker, 'calculate_score_zxcvbn') and self.checker.use_zxcvbn:
            score, strength, suggestions, zxcvbn_result = self.checker.calculate_score_zxcvbn(password)
        else:
            if hasattr(self.checker, 'calculate_score_builtin'):
                score, strength, suggestions = self.checker.calculate_score_builtin(password)
            else:
                score, strength, suggestions = self.checker.calculate_score(password)
            zxcvbn_result = None
            
        # Format the analysis result
        result = []
        result.append("="*70)
        result.append("🔒 PASSWORD STRENGTH ANALYSIS 🔒")
        result.append("="*70)
        result.append("")
        
        # Algorithm info
        algorithm = "zxcvbn + Enhanced Analysis" if (hasattr(self.checker, 'use_zxcvbn') and self.checker.use_zxcvbn) else "Built-in Algorithm"
        result.append(f"Analysis Method: {algorithm}")
        result.append(f"Password Length: {len(password)} characters")
        result.append("")
        
        # Character types
        char_types = self.checker.check_character_types(password)
        result.append("Character Composition:")
        result.append(f"  • Lowercase letters: {'✓' if char_types['lowercase'] else '✗'}")
        result.append(f"  • Uppercase letters: {'✓' if char_types['uppercase'] else '✗'}")
        result.append(f"  • Numbers: {'✓' if char_types['digits'] else '✗'}")
        result.append(f"  • Special characters: {'✓' if char_types['special'] else '✗'}")
        result.append("")
        
        # Technical metrics
        entropy = self.checker.calculate_entropy(password)
        result.append("Technical Metrics:")
        result.append(f"  • Entropy: {entropy:.1f} bits")
        result.append(f"  • Unique characters: {len(set(password))}/{len(password)}")
        
        if zxcvbn_result:
            result.append(f"  • zxcvbn Score: {zxcvbn_result['score']}/4")
            result.append(f"  • Guesses needed: {zxcvbn_result['guesses']:,}")
            if 'entropy' in zxcvbn_result:
                result.append(f"  • zxcvbn Entropy: {zxcvbn_result['entropy']:.1f} bits")
        result.append("")
        
        # Overall assessment
        result.append("Overall Assessment:")
        result.append(f"  • Strength Score: {score}/100")
        result.append(f"  • Strength Level: {strength}")
        result.append("")
        
        # Progress bar representation
        bar_length = 50
        filled_length = int(bar_length * score // 100)
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        result.append(f"[{bar}] {score}%")
        result.append("")
        
        # Security issues
        issues = self.checker.check_common_patterns(password)
        if issues:
            result.append("⚠️  Security Issues Detected:")
            for i, issue in enumerate(issues, 1):
                result.append(f"  {i}. {issue}")
            result.append("")
              # zxcvbn specific patterns
        if zxcvbn_result and zxcvbn_result.get('sequence'):
            result.append("🔍 Pattern Analysis (zxcvbn):")
            for match in zxcvbn_result['sequence']:
                pattern_type = match.get('pattern', 'unknown')
                token = match.get('token', '')
                result.append(f"  • {pattern_type.title()}: '{token}'")
            result.append("")
        
        # Have I Been Pwned check
        if hasattr(self.checker, 'hibp_checker') and self.checker.hibp_checker:
            result.append("🛡️  Have I Been Pwned Check:")
            try:
                hibp_result = self.checker.hibp_checker.get_breach_info(password)
                if hibp_result['is_compromised']:
                    result.append(f"  ⚠️  PASSWORD COMPROMISED!")
                    result.append(f"  • Found in {hibp_result['breach_count']:,} data breaches")
                    result.append(f"  • Risk Level: {hibp_result['risk_level']}")
                    result.append(f"  • {hibp_result['recommendation']}")
                else:
                    result.append(f"  ✅ Password not found in known data breaches")
                    result.append(f"  • {hibp_result['recommendation']}")
            except Exception as e:
                result.append(f"  ⚠️  Unable to check breaches: {str(e)}")
            result.append("")
        else:
            result.append("🛡️  Have I Been Pwned Check:")
            result.append("  ⚠️  Breach checking unavailable")
            result.append("  • Install requests library for breach checking")
            result.append("")
            
        # Time to crack estimation
        if zxcvbn_result:
            result.append("🕐 Estimated Crack Time:")
            crack_times = zxcvbn_result['crack_times_display']
            result.append(f"  • Online attack (throttled): {crack_times['online_throttling_100_per_hour']}")
            result.append(f"  • Online attack (unthrottled): {crack_times['online_no_throttling_10_per_second']}")
            result.append(f"  • Offline attack (slow): {crack_times['offline_slow_hashing_1e4_per_second']}")
            result.append(f"  • Offline attack (fast): {crack_times['offline_fast_hashing_1e10_per_second']}")
        else:
            result.append("🕐 Estimated Crack Time:")
            guesses_per_second = 1e9
            total_combinations = 2 ** entropy
            seconds_to_crack = total_combinations / (2 * guesses_per_second)
            
            if seconds_to_crack < 1:
                time_str = "Instantly"
            elif seconds_to_crack < 60:
                time_str = f"{seconds_to_crack:.1f} seconds"
            elif seconds_to_crack < 3600:
                time_str = f"{seconds_to_crack/60:.1f} minutes"
            elif seconds_to_crack < 86400:
                time_str = f"{seconds_to_crack/3600:.1f} hours"
            elif seconds_to_crack < 31536000:
                time_str = f"{seconds_to_crack/86400:.1f} days"
            else:
                years = seconds_to_crack / 31536000
                if years > 1e6:
                    time_str = "Millions of years"
                else:
                    time_str = f"{years:.0f} years"
            result.append(f"  • Estimated time: {time_str}")
        result.append("")
        
        # Suggestions
        if suggestions:
            result.append("💡 Improvement Suggestions:")
            for i, suggestion in enumerate(suggestions, 1):
                result.append(f"  {i}. {suggestion}")
            result.append("")
            
        # Security recommendations
        result.append("🛡️  Security Recommendations:")
        if score < 40:
            result.append("  • Critical: This password is easily crackable")
            result.append("  • Use a password manager to generate strong passwords")
            result.append("  • Enable two-factor authentication (2FA) wherever possible")
        elif score < 60:
            result.append("  • Important: Consider strengthening this password")
            result.append("  • Add more character types and length")
        elif score < 80:
            result.append("  • Good: This is a reasonably strong password")
            result.append("  • Consider making it even longer for extra security")
        else:
            result.append("  • Excellent: This is a very strong password")
            
        result.append("  • Never reuse passwords across multiple accounts")
        result.append("  • Update passwords regularly, especially for sensitive accounts")
        result.append("  • Store passwords securely using a password manager")
        result.append("")
        result.append("="*70)
        
        return "\n".join(result), score, strength
        
    def _display_analysis_result(self, result_data):
        """Display analysis result in GUI (runs in main thread)"""
        result_text, score, strength = result_data
        
        # Update progress bar and labels
        self.strength_progress['value'] = score
        color = self.colors.get(strength, 'black')
        self.strength_label.config(text=strength, foreground=color)
        self.score_label.config(text=f"Score: {score}/100")
        
        # Display full analysis
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, result_text)
        
        # Apply some basic formatting
        self._format_results_text()
        
        self.status_var.set("Analysis complete")
        
    def _format_results_text(self):
        """Apply basic formatting to results text"""
        content = self.results_text.get(1.0, tk.END)
        lines = content.split('\n')
        
        self.results_text.delete(1.0, tk.END)
        
        for line in lines:
            if line.startswith('='):
                self.results_text.insert(tk.END, line + '\n', 'header')
            elif 'Very Strong' in line:
                self.results_text.insert(tk.END, line + '\n', 'strong')
            elif 'Strong' in line and 'Very Strong' not in line:
                self.results_text.insert(tk.END, line + '\n', 'strong')
            elif 'Medium' in line:
                self.results_text.insert(tk.END, line + '\n', 'medium')
            elif 'Weak' in line or 'Critical' in line:
                self.results_text.insert(tk.END, line + '\n', 'weak')
            elif line.startswith('⚠️') or line.startswith('🕐') or line.startswith('💡') or line.startswith('🛡️'):
                self.results_text.insert(tk.END, line + '\n', 'info')
            else:
                self.results_text.insert(tk.END, line + '\n')
                
    def _display_error(self, error_msg):
        """Display error message (runs in main thread)"""
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"Error: {error_msg}", 'error')
        self.status_var.set("Analysis failed")
        
    def generate_password(self):
        """Generate a strong password"""
        import random
        import string
        
        # Character sets
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Ensure at least one character from each set
        password = [
            random.choice(lowercase),
            random.choice(uppercase),
            random.choice(digits),
            random.choice(symbols)
        ]
        
        # Fill the rest randomly
        all_chars = lowercase + uppercase + digits + symbols
        for _ in range(12):  # Total length 16
            password.append(random.choice(all_chars))
            
        # Shuffle the password
        random.shuffle(password)
        generated_password = ''.join(password)
        
        # Set the password in the entry field
        self.password_var.set(generated_password)
        self.analyze_password()
        
        # Show password in a dialog
        messagebox.showinfo("Generated Password", 
                           f"Generated strong password:\n\n{generated_password}\n\n"
                           "The password has been copied to the input field.")
                           
    def generate_password_dialog(self):
        """Show password generation dialog with options"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Generate Password")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Password Generation Options", 
                 font=('Arial', 12, 'bold')).pack(pady=(0, 20))
        
        # Length selection
        length_frame = ttk.Frame(main_frame)
        length_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(length_frame, text="Length:").pack(side=tk.LEFT)
        length_var = tk.IntVar(value=16)
        ttk.Scale(length_frame, from_=8, to=32, variable=length_var, 
                 orient=tk.HORIZONTAL).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 10))
        length_label = ttk.Label(length_frame, text="16")
        length_label.pack(side=tk.LEFT)
        
        def update_length_label(val):
            length_label.config(text=str(int(float(val))))
        
        length_frame.winfo_children()[1].config(command=update_length_label)
        
        # Character type options
        options_frame = ttk.LabelFrame(main_frame, text="Include Characters", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 20))
        
        include_lowercase = tk.BooleanVar(value=True)
        include_uppercase = tk.BooleanVar(value=True)
        include_digits = tk.BooleanVar(value=True)
        include_symbols = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(options_frame, text="Lowercase letters (a-z)", 
                       variable=include_lowercase).pack(anchor=tk.W)
        ttk.Checkbutton(options_frame, text="Uppercase letters (A-Z)", 
                       variable=include_uppercase).pack(anchor=tk.W)
        ttk.Checkbutton(options_frame, text="Numbers (0-9)", 
                       variable=include_digits).pack(anchor=tk.W)
        ttk.Checkbutton(options_frame, text="Symbols (!@#$%^&*)", 
                       variable=include_symbols).pack(anchor=tk.W)
        
        # Generated password display
        result_frame = ttk.LabelFrame(main_frame, text="Generated Password", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        password_display = tk.Text(result_frame, height=3, wrap=tk.WORD, font=('Consolas', 11))
        password_display.pack(fill=tk.BOTH, expand=True)
        
        def generate_custom_password():
            import random
            import string
            
            char_sets = []
            if include_lowercase.get():
                char_sets.append(string.ascii_lowercase)
            if include_uppercase.get():
                char_sets.append(string.ascii_uppercase)
            if include_digits.get():
                char_sets.append(string.digits)
            if include_symbols.get():
                char_sets.append("!@#$%^&*()_+-=[]{}|;:,.<>?")
                
            if not char_sets:
                messagebox.showwarning("No Characters", "Please select at least one character type.")
                return
                
            length = length_var.get()
            password = []
            
            # Ensure at least one character from each selected set
            for char_set in char_sets:
                if len(password) < length:
                    password.append(random.choice(char_set))
                    
            # Fill the rest
            all_chars = ''.join(char_sets)
            while len(password) < length:
                password.append(random.choice(all_chars))
                
            # Shuffle
            random.shuffle(password)
            generated = ''.join(password)
            
            password_display.delete(1.0, tk.END)
            password_display.insert(1.0, generated)
            
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Generate", 
                  command=generate_custom_password).pack(side=tk.LEFT, padx=(0, 10))
        
        def use_password():
            password = password_display.get(1.0, tk.END).strip()
            if password:
                self.password_var.set(password)
                dialog.destroy()
                self.analyze_password()
            else:
                messagebox.showwarning("No Password", "Please generate a password first.")
                
        ttk.Button(button_frame, text="Use This Password", 
                  command=use_password).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Close", 
                  command=dialog.destroy).pack(side=tk.RIGHT)
                  
        # Generate initial password
        generate_custom_password()
        
    def batch_analysis(self):
        """Perform batch analysis from file"""
        file_path = filedialog.askopenfilename(
            title="Select Password File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                passwords = [line.strip() for line in f if line.strip()]
                
            if not passwords:
                messagebox.showwarning("Empty File", "The selected file contains no passwords.")
                return
                
            # Show batch analysis dialog
            self.show_batch_results(passwords)
            
        except Exception as e:
            messagebox.showerror("File Error", f"Error reading file: {str(e)}")
            
    def show_batch_results(self, passwords):
        """Show batch analysis results in a new window"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Batch Analysis Results")
        dialog.geometry("900x600")
        dialog.transient(self.root)
        
        main_frame = ttk.Frame(dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text=f"Batch Analysis Results ({len(passwords)} passwords)", 
                 font=('Arial', 12, 'bold')).pack(pady=(0, 10))
        
        # Results table
        columns = ('Password', 'Score', 'Strength', 'Issues')
        tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200)
            
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
        h_scrollbar = ttk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=tree.xview)
        tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Progress bar for batch processing
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=(10, 0))
        
        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(progress_frame, variable=progress_var, maximum=len(passwords))
        progress_bar.pack(fill=tk.X, pady=(0, 5))
        
        status_label = ttk.Label(progress_frame, text="Processing...")
        status_label.pack()
        
        def process_batch():
            for i, password in enumerate(passwords):
                try:
                    if hasattr(self.checker, 'calculate_score_builtin'):
                        score, strength, _ = self.checker.calculate_score_builtin(password)
                    else:
                        score, strength, _ = self.checker.calculate_score(password)
                    
                    issues = self.checker.check_common_patterns(password)
                    issue_count = len(issues)
                    
                    # Truncate password for display
                    display_password = password if len(password) <= 20 else password[:17] + "..."
                    
                    tree.insert('', tk.END, values=(display_password, f"{score}/100", strength, 
                                                  f"{issue_count} issues" if issue_count > 0 else "None"))
                    
                    progress_var.set(i + 1)
                    status_label.config(text=f"Processing {i+1}/{len(passwords)}...")
                    dialog.update()
                    
                except Exception as e:
                    tree.insert('', tk.END, values=(password[:20], "Error", "Error", str(e)[:30]))
                    
            status_label.config(text="Processing complete!")
            
        # Start processing
        thread = threading.Thread(target=process_batch)
        thread.daemon = True
        thread.start()
        
    def export_results(self):
        """Export current analysis results"""
        content = self.results_text.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("No Results", "No analysis results to export.")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Export Results",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("Export Successful", f"Results exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Error exporting results: {str(e)}")
                
    def clear_analysis(self):
        """Clear all analysis results"""
        self.password_var.set("")
        self.results_text.delete(1.0, tk.END)
        self.reset_display()
        self.status_var.set("Ready")
        
    def show_password_tips(self):
        """Show password security tips"""
        tips_window = tk.Toplevel(self.root)
        tips_window.title("Password Security Tips")
        tips_window.geometry("600x500")
        tips_window.transient(self.root)
        
        main_frame = ttk.Frame(tips_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="🛡️  Password Security Tips", 
                 font=('Arial', 14, 'bold')).pack(pady=(0, 20))
        
        tips_text = scrolledtext.ScrolledText(main_frame, height=20, wrap=tk.WORD, font=('Arial', 11))
        tips_text.pack(fill=tk.BOTH, expand=True)
        
        tips_content = """
Best Practices for Strong Passwords:

1. LENGTH MATTERS
   • Use at least 12 characters (16+ recommended)
   • Longer passwords are exponentially harder to crack

2. CHARACTER DIVERSITY
   • Mix uppercase and lowercase letters
   • Include numbers and special characters
   • Use symbols like !@#$%^&*()

3. AVOID COMMON PATTERNS
   • Don't use dictionary words
   • Avoid sequential characters (123, abc)
   • Don't use keyboard patterns (qwerty, asdf)
   • Never use personal information (name, birthday)

4. UNIQUE PASSWORDS
   • Use different passwords for every account
   • Never reuse passwords across sites
   • Especially important for sensitive accounts

5. PASSWORD MANAGERS
   • Use a reputable password manager
   • Generate random, strong passwords
   • Store passwords securely encrypted

6. TWO-FACTOR AUTHENTICATION (2FA)
   • Enable 2FA wherever possible
   • Use authenticator apps over SMS
   • Consider hardware security keys

7. REGULAR UPDATES
   • Change passwords regularly for sensitive accounts
   • Update immediately if a breach is suspected
   • Monitor for data breaches

8. PASSPHRASE ALTERNATIVE
   • Consider using passphrases (4+ random words)
   • Example: "correct horse battery staple"
   • Easier to remember, hard to crack

9. WHAT TO AVOID
   • Personal information (name, birthday, pet names)
   • Common substitutions (@ for a, 3 for e)
   • Common passwords (password123, admin)
   • Simple patterns or sequences

10. STORAGE SECURITY
    • Never write passwords in plain text
    • Don't store in browsers on shared computers
    • Use encrypted storage methods
    • Keep password manager secure

Remember: A strong password is your first line of defense against cyber attacks!
        """
        
        tips_text.insert(1.0, tips_content)
        tips_text.config(state=tk.DISABLED)
        
        ttk.Button(main_frame, text="Close", command=tips_window.destroy).pack(pady=(10, 0))
        
    def show_about(self):
        """Show about dialog"""
        about_text = """
🔒 Password Strength Checker Tool - GUI Version

A comprehensive password security analysis application with advanced 
pattern recognition and strength assessment capabilities.

Features:
• Real-time password strength analysis
• Multiple analysis algorithms (built-in + zxcvbn)
• Character composition analysis
• Common pattern detection
• Entropy calculation
• Crack time estimation
• Batch analysis capabilities
• Strong password generation
• Export functionality

Version: 1.0
Date: June 2025
        """
        
        messagebox.showinfo("About Password Strength Checker", about_text)
        
    def show_user_guide(self):
        """Show user guide"""
        guide_window = tk.Toplevel(self.root)
        guide_window.title("User Guide")
        guide_window.geometry("700x600")
        guide_window.transient(self.root)
        
        main_frame = ttk.Frame(guide_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="📖 User Guide", 
                 font=('Arial', 14, 'bold')).pack(pady=(0, 20))
        
        guide_text = scrolledtext.ScrolledText(main_frame, height=25, wrap=tk.WORD, font=('Arial', 11))
        guide_text.pack(fill=tk.BOTH, expand=True)
        
        guide_content = """
HOW TO USE PASSWORD STRENGTH CHECKER

1. BASIC ANALYSIS
   • Enter a password in the input field
   • Real-time analysis shows basic strength meter
   • Click "Analyze Password" for detailed analysis
   • Results show comprehensive security assessment

2. PASSWORD INPUT
   • Type directly in the password field
   • Use "Show" checkbox to toggle password visibility
   • Password analysis updates in real-time

3. ANALYSIS RESULTS
   • Strength meter shows overall password strength
   • Detailed analysis includes:
     - Character composition
     - Technical metrics (entropy, uniqueness)
     - Security issues and patterns
     - Crack time estimation
     - Improvement suggestions
     - Security recommendations

4. STRONG PASSWORD GENERATION
   • Click "Generate Strong Password" for quick generation
   • Use Tools → Generate Password for custom options
   • Adjust length, character types, and options
   • Generated passwords are automatically analyzed

5. BATCH ANALYSIS
   • Click "Batch Analysis" or File → Batch Analysis
   • Select a text file with passwords (one per line)
   • View results in a table format
   • See scores, strengths, and issue counts for all passwords

6. EXPORT RESULTS
   • Use File → Export Results to save analysis
   • Results saved as text file
   • Includes complete analysis details

7. UNDERSTANDING STRENGTH LEVELS
   • Very Weak (0-19): Easily crackable, immediate change needed
   • Weak (20-39): Poor security, vulnerable to attacks
   • Medium (40-59): Moderate security, room for improvement
   • Strong (60-79): Good security, minor improvements possible
   • Very Strong (80-100): Excellent security, hard to crack

8. SCORING FACTORS
   • Length: Longer passwords score higher
   • Character Types: Mix of uppercase, lowercase, numbers, symbols
   • Entropy: Mathematical measure of randomness
   • Patterns: Penalties for common patterns and words
   • Uniqueness: Ratio of unique to total characters

9. SECURITY ISSUES DETECTED
   • Dictionary words
   • Common passwords from database
   • Repeated characters
   • Sequential patterns (123, abc)
   • Keyboard patterns (qwerty, asdf)

10. IMPROVEMENT SUGGESTIONS
    • Add missing character types
    • Increase length
    • Remove common patterns
    • Avoid dictionary words
    • Make password more unique

TIPS FOR BEST RESULTS:
- Test multiple password variations
- Use the password generator for inspiration
- Check passwords for all your important accounts
- Enable 2FA wherever possible
- Use a password manager for unique passwords

Need help? Check Tools → Password Tips for security best practices!
        """
        
        guide_text.insert(1.0, guide_content)
        guide_text.config(state=tk.DISABLED)
        
        ttk.Button(main_frame, text="Close", command=guide_window.destroy).pack(pady=(10, 0))

def main():
    """Main function to run the GUI application"""
    try:
        root = tk.Tk()
        app = PasswordCheckerGUI(root)
        
        # Handle window closing
        def on_closing():
            root.quit()
            root.destroy()
            
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Start the GUI
        root.mainloop()
        
    except Exception as e:
        print(f"Error starting GUI: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
