# Password Checker

A Python program for **checking and creating strong passwords**.  
Also checks whether a password has appeared in known leaks using the [Have I Been Pwned API](https://haveibeenpwned.com/).

---

## Description

Password Checker is a console application that helps the user evaluate password strength, check it against breach databases, and create a secure alternative.  
The strength assessment is based on the `zxcvbn` library extended with custom rules, and leak checks use the `k-anonymity` method for privacy.

---

## Features

### Password checking
- Strength assessment with `zxcvbn` and additional rules:
  - Length
  - Uppercase and lowercase letters, digits, special characters
  - Common words and patterns
  - Leak checking via the Have I Been Pwned API
- Visual strength bar display

### Password creation
- Help to create a strong password with tips:
  - Which characters to add
  - Avoid common words
  - Length recommendations
  - Leak check

### Language support
- Ability to switch between English and Russian.

### Animated banner
- ASCII banner on program startup

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/itsargus/password-checker.git
   cd password-checker
2. Installation of vulnerabilities:
   ```bash
   pip install requests zxcvbn
   pip install requests zxcvbn-python

## Screenshots
<img width="1271" height="651" alt="image" src="https://github.com/user-attachments/assets/22512f4a-e1ac-4f3d-992b-e7ee033e1b7a" />





