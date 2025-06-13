#!/usr/bin/env python3
"""
Simple JSON-based translation system for Password Strength Checker Tool

This provides a fallback when gettext .mo files have encoding issues.
"""

import json
import os
import locale
from pathlib import Path
from typing import Dict, Optional

class SimpleTranslation:
    """Simple JSON-based translation system"""
    
    SUPPORTED_LANGUAGES = {
        'en': 'English',
        'es': 'Español', 
        'fr': 'Français',
        'de': 'Deutsch',
        'zh': '简体中文',
        'ja': '日本語'
    }
    
    def __init__(self, language: Optional[str] = None):
        self.current_language = language or self._detect_system_language()
        self.translations = {}
        self._load_translations()
    
    def _detect_system_language(self) -> str:
        """Detect system language"""
        try:
            system_locale = locale.getdefaultlocale()[0]
            if system_locale:
                lang_code = system_locale.split('_')[0].lower()
                if lang_code in self.SUPPORTED_LANGUAGES:
                    return lang_code
        except:
            pass
        return 'en'
    
    def _load_translations(self):
        """Load translations from JSON files or create them from PO files"""
        json_file = Path(__file__).parent / f"translations_{self.current_language}.json"
        
        if json_file.exists():
            with open(json_file, 'r', encoding='utf-8') as f:
                self.translations = json.load(f)
        else:
            # Create JSON from PO file
            self._create_json_from_po()
    
    def _create_json_from_po(self):
        """Create JSON translation from PO file"""
        po_file = Path(__file__).parent / f"locales/{self.current_language}/LC_MESSAGES/password_checker.po"
        
        if not po_file.exists():
            return
        
        translations = {}
        
        with open(po_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        msgid = None
        msgstr = None
        in_msgid = False
        in_msgstr = False
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('msgid '):
                msgid = line[6:].strip('"')
                in_msgid = True
                in_msgstr = False
            elif line.startswith('msgstr '):
                msgstr = line[7:].strip('"')
                in_msgid = False
                in_msgstr = True
            elif line.startswith('"') and (in_msgid or in_msgstr):
                content = line.strip('"')
                if in_msgid:
                    msgid += content
                elif in_msgstr:
                    msgstr += content
            elif line == "" or line.startswith('#'):
                if msgid is not None and msgstr is not None and msgid != "" and msgstr != "":
                    translations[msgid] = msgstr
                msgid = None
                msgstr = None
                in_msgid = False
                in_msgstr = False
        
        # Handle last entry
        if msgid is not None and msgstr is not None and msgid != "" and msgstr != "":
            translations[msgid] = msgstr
        
        self.translations = translations
        
        # Save as JSON for faster loading next time
        json_file = Path(__file__).parent / f"translations_{self.current_language}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(translations, f, ensure_ascii=False, indent=2)
    
    def gettext(self, text: str) -> str:
        """Get translated text"""
        return self.translations.get(text, text)
    
    def set_language(self, language: str) -> bool:
        """Change language"""
        if language not in self.SUPPORTED_LANGUAGES:
            return False
        
        self.current_language = language
        self._load_translations()
        return True
    
    def get_supported_languages(self) -> Dict[str, str]:
        return self.SUPPORTED_LANGUAGES.copy()
    
    def get_current_language(self) -> str:
        return self.current_language


# Global instances for compatibility
i18n = SimpleTranslation()

def _(text: str) -> str:
    """Translation function"""
    return i18n.gettext(text)
