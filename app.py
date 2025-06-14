#!/usr/bin/env python3
"""
Password Strength Checker Tool - Web Interface

A Flask-based web application that provides a modern, browser-accessible interface
for the Password Strength Checker Tool with real-time analysis and multi-language support.

Author: Password Security Tool
Date: June 2025
"""

from flask import Flask, render_template, request, jsonify, session
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# Import our core components
try:
    from enhanced_password_checker import PasswordStrengthChecker
    from i18n_manager import i18n, _
    WEB_READY = True
except ImportError as e:
    print(f"Warning: Could not import core components: {e}")
    WEB_READY = False

app = Flask(__name__)
app.secret_key = 'password_checker_secret_key_2025'  # Change in production

# Global password checker instance
if WEB_READY:
    checker = PasswordStrengthChecker()

@app.route('/')
def index():
    """Main page"""
    if not WEB_READY:
        return render_template('error.html', 
                             error="Application not ready. Please check dependencies.")
    
    # Get supported languages
    languages = i18n.get_supported_languages() if i18n else {'en': 'English'}
    
    # Force English as default for web interface unless explicitly set
    if 'language' not in session:
        session['language'] = 'en'
        if i18n:
            i18n.set_language('en')
    
    current_lang = session.get('language', 'en')
    
    return render_template('index.html', 
                         languages=languages, 
                         current_language=current_lang)

@app.route('/api/analyze', methods=['POST'])
def analyze_password():
    """API endpoint for password analysis"""
    if not WEB_READY:
        return jsonify({'error': 'Application not ready'}), 500
    
    try:
        data = request.get_json()
        password = data.get('password', '')
        language = data.get('language', 'en')
        include_hibp = data.get('include_hibp', True)
        
        if not password:
            return jsonify({'error': 'Password is required'}), 400
        
        # Create a temporary language context for this request
        from i18n_manager import SimpleTranslation
        temp_i18n = SimpleTranslation(language)
        
        # Temporarily replace the global translation function
        import i18n_manager
        original_gettext = i18n_manager.i18n.gettext
        i18n_manager.i18n.gettext = temp_i18n.gettext
        
        try:
            # Set session language for frontend
            session['language'] = language
            
            # Get analysis data with the correct language context
            analysis = checker.get_password_analysis_data(password, include_password=False)
            
            # Add web-specific formatting
            result = {
                'success': True,
                'analysis': analysis,
                'timestamp': datetime.now().isoformat(),
                'language': language
            }
        finally:
            # Restore original translation function
            i18n_manager.i18n.gettext = original_gettext# Add HIBP check if requested
        if include_hibp:
            if checker.hibp_checker:
                try:
                    is_compromised, breach_count, message = checker.hibp_checker.check_password(password)
                    result['hibp'] = {
                        'checked': True,
                        'compromised': is_compromised,
                        'count': breach_count,
                        'message': message
                    }
                except Exception as e:
                    result['hibp'] = {
                        'checked': False,
                        'error': str(e)
                    }
            else:
                result['hibp'] = {
                    'checked': False,
                    'message': 'Have I Been Pwned integration not available'
                }
        else:
            result['hibp'] = {'checked': False, 'message': 'HIBP check disabled by user'}
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/api/generate', methods=['POST'])
def generate_password():
    """API endpoint for password generation"""
    try:
        data = request.get_json()
        length = data.get('length', 16)
        include_upper = data.get('include_upper', True)
        include_lower = data.get('include_lower', True)
        include_numbers = data.get('include_numbers', True)
        include_symbols = data.get('include_symbols', True)
        
        # Validate inputs
        if length < 4 or length > 128:
            return jsonify({'error': 'Length must be between 4 and 128'}), 400
            
        if not any([include_upper, include_lower, include_numbers, include_symbols]):
            return jsonify({'error': 'At least one character type must be selected'}), 400
        
        # Build character set
        charset = ''
        if include_upper:
            charset += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if include_lower:
            charset += 'abcdefghijklmnopqrstuvwxyz'
        if include_numbers:
            charset += '0123456789'
        if include_symbols:
            charset += '!@#$%^&*()_+-=[]{}|;:,.<>?'
        
        # Generate secure password
        import secrets
        password = ''.join(secrets.choice(charset) for _ in range(length))
        
        # Analyze the generated password for quality feedback
        if WEB_READY:
            analysis = checker.get_password_analysis_data(password, include_password=False)
            strength_score = analysis.get('strength_score', 0)
            strength_level = analysis.get('strength_level', 'Unknown')
        else:
            strength_score = 0
            strength_level = 'Unknown'
        
        return jsonify({
            'success': True,
            'password': password,
            'length': length,
            'charset_size': len(charset),
            'strength_score': strength_score,
            'strength_level': strength_level,
            'entropy_bits': length * (len(charset).bit_length() - 1),
            'character_types': {
                'uppercase': include_upper,
                'lowercase': include_lower,
                'numbers': include_numbers,
                'symbols': include_symbols
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Password generation failed: {str(e)}'}), 500

@app.route('/api/languages')
def get_languages():
    """Get supported languages"""
    if i18n:
        languages = i18n.get_supported_languages()
    else:
        languages = {'en': 'English'}
    
    return jsonify({
        'success': True,
        'languages': languages,
        'current': session.get('language', 'en')
    })

@app.route('/api/language/<lang_code>', methods=['POST'])
def set_language(lang_code):
    """Set current language"""
    if i18n:
        supported = i18n.get_supported_languages()
        if lang_code in supported:
            # Only set session language, don't change global i18n state
            session['language'] = lang_code
            return jsonify({
                'success': True,
                'language': lang_code,
                'name': supported[lang_code]
            })
        else:
            return jsonify({'error': 'Unsupported language'}), 400
    else:
        return jsonify({'error': 'i18n not available'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy' if WEB_READY else 'error',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0',
        'features': {
            'enhanced_checker': WEB_READY,
            'hibp_integration': checker.hibp_checker is not None if WEB_READY else False,
            'zxcvbn': checker.use_zxcvbn if WEB_READY else False,
            'i18n': i18n is not None
        }
    })

if __name__ == '__main__':
    if not WEB_READY:
        print("❌ Error: Core components not available")
        exit(1)
    
    print("🌐 Password Strength Checker - Web Interface")
    print("� Server: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
