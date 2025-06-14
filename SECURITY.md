# Security Policy

## Overview

The Password Strength Checker Tool prioritizes security and privacy in its design and implementation.

## Security Features

- **No Password Storage**: Passwords are never stored or transmitted
- **Local Processing**: All analysis is performed locally
- **k-Anonymity Protocol**: HIBP integration uses privacy-preserving hash prefixes
- **Optional Features**: External services can be disabled (--no-hibp)
- **Secure Exports**: Passwords excluded from exports by default

## Privacy Protection

- Memory is cleared after analysis
- No logging of sensitive data
- All processing happens on your local machine
- User controls all data export options

## Vulnerability Reporting

If you discover a security issue:

1. **DO NOT** create a public GitHub issue
2. Email security concerns privately
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

## Best Practices

- Keep dependencies updated
- Run with minimal permissions
- Use in secure environments
- Enable HIBP checking for better security
- Never share analysis results containing passwords

## Supported Versions

| Version | Supported |
| ------- | --------- |
| 1.0.x   | ✅        |
| < 1.0   | ❌        |

## Security Updates

Security updates are provided as soon as vulnerabilities are confirmed and patches are available.
