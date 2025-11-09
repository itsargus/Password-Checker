import string
import hashlib
import requests
from zxcvbn import zxcvbn
import time

# -------------------- Языковые словари --------------------
texts = {
    "ru": {
        "menu_intro": "Эта программа создана для оценки и создания безопасности ваших паролей.",
        "menu_options": ["1 - выход", "2 - проверка пароля", "3 - создание пароля", "4 - смена языка"],
        "choose_action": "Выберите действие: ",
        "invalid_choice": "Неверный ввод, попробуйте снова.",
        "exit": "Выход из программы.",
        "password_menu": "Введите пароль (или 'menu'): ",
        "create_password": "Создайте идеальный пароль (или введите 'menu'): ",
        "missing": "⚠️ Добавьте: ",
        "short_password": "⚠️ Пароль слишком короткий, минимум 8 символов.",
        "recommended_length": "⚠️ Рекомендуется использовать пароль 16+ символов.",
        "common_word": "⚠️ Пароль содержит распространённое слово/шаблон.",
        "spaces": "⚠️ Пароль не может содержать пробелы.",
        "pwned": "⚠️ Этот пароль встречался в утечках {} раз(а)!",
        "not_pwned": "Пароль не встречался в утечках",
        "perfect_password": "✅ Пароль идеален!",
        "improvable_password": "⚠️ Пароль можно улучшить.",
        "add_upper": "заглавные буквы",
        "add_lower": "маленькие буквы",
        "add_digit": "цифры",
        "add_special": "специальные символы"
    },
    "en": {
        "menu_intro": "This program helps you check and create secure passwords.",
        "menu_options": ["1 - exit", "2 - password check", "3 - create password", "4 - change language"],
        "choose_action": "Choose an action: ",
        "invalid_choice": "Invalid input, try again.",
        "exit": "Exiting program.",
        "password_menu": "Enter password (or 'menu'): ",
        "create_password": "Create a strong password (or type 'menu'): ",
        "missing": "⚠️ Add: ",
        "short_password": "⚠️ Password too short, minimum 8 characters.",
        "recommended_length": "⚠️ Recommended to use 16+ characters.",
        "common_word": "⚠️ Password contains common word/pattern.",
        "spaces": "⚠️ Password cannot contain spaces.",
        "pwned": "⚠️ This password has appeared in leaks {} times!",
        "not_pwned": "Password has not appeared in leaks",
        "perfect_password": "✅ Password is perfect!",
        "improvable_password": "⚠️ Password can be improved.",
        "add_upper": "uppercase letters",
        "add_lower": "lowercase letters",
        "add_digit": "digits",
        "add_special": "special characters"
    }
}

current_lang = "en"  # English by default

# -------------------- Общие переменные --------------------
common_patterns = [
    "password", "123456", "123456789", "qwerty", "abc123", "111111", "123123",
    "admin", "letmein", "welcome", "monkey", "login", "princess", "solo",
    "passw0rd", "starwars", "dragon", "football", "baseball", "shadow",
    "master", "hello", "freedom", "whatever", "qazwsx", "trustno1", "1234",
    "12345", "password1", "iloveyou", "sunshine", "flower", "hottie",
    "loveme", "zaq1zaq1", "batman", "superman", "pokemon"
]

# -------------------- Баннер --------------------
def print_animated_banner():
    banner = r"""
          _____                    _____                    _____                    _____                    _____          
         /\    \                  /\    \                  /\    \                  /\    \                  /\    \         
        /::\    \                /::\    \                /::\    \                /::\____\                /::\    \        
       /::::\    \              /::::\    \              /::::\    \              /:::/    /               /::::\    \       
      /::::::\    \            /::::::\    \            /::::::\    \            /:::/    /               /::::::\    \      
     /:::/\:::\    \          /:::/\:::\    \          /:::/\:::\    \          /:::/    /               /:::/\:::\    \     
    /:::/__\:::\    \        /:::/__\:::\    \        /:::/  \:::\    \        /:::/    /               /:::/__\:::\    \    
   /::::\   \:::\    \      /::::\   \:::\    \      /:::/    \:::\    \      /:::/    /                \:::\   \:::\    \   
  /::::::\   \:::\    \    /::::::\   \:::\    \    /:::/    / \:::\    \    /:::/    /      _____    ___\:::\   \:::\    \  
 /:::/\:::\   \:::\    \  /:::/\:::\   \:::\____\  /:::/    /   \:::\ ___\  /:::/____/      /\    \  /\   \:::\   \:::\    \ 
/:::/  \:::\   \:::\____\/:::/  \:::\   \:::|    |/:::/____/  ___\:::|    ||:::|    /      /::\____\/::\   \:::\   \:::\____\
\::/    \:::\  /:::/    /\::/   |::::\  /:::|____|\:::\    \ /\  /:::|____||:::|____\     /:::/    /\:::\   \:::\   \::/    /
 \/____/ \:::\/:::/    /  \/____|:::::\/:::/    /  \:::\    /::\ \::/    /  \:::\    \   /:::/    /  \:::\   \:::\   \/____/ 
          \::::::/    /         |:::::::::/    /    \:::\   \:::\ \/____/    \:::\    \ /:::/    /    \:::\   \:::\    \     
           \::::/    /          |::|\::::/    /      \:::\   \:::\____\       \:::\    /:::/    /      \:::\   \:::\____\    
           /:::/    /           |::| \::/____/        \:::\  /:::/    /        \:::\__/:::/    /        \:::\  /:::/    /    
          /:::/    /            |::|  ~|               \:::\/:::/    /          \::::::::/    /          \:::\/:::/    /     
         /:::/    /             |::|   |                \::::::/    /            \::::::/    /            \::::::/    /      
        /:::/    /              \::|   |                 \::::/    /              \::::/    /              \::::/    /       
        \::/    /                \:|   |                  \::/____/                \::/____/                \::/    /        
         \/____/                  \|___|                                            ~~                       \/____/     
"""
    green_color = "\033[92m"
    reset_color = "\033[0m"
    for line in banner.splitlines():
        print(green_color + line + reset_color)
        time.sleep(0.05)

# -------------------- Проверка утечек --------------------
def check_pwned(password: str) -> int:
    sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    try:
        res = requests.get(url, timeout=5)
        res.raise_for_status()
    except requests.RequestException:
        return 0
    hashes = (line.split(':') for line in res.text.splitlines())
    for h, count in hashes:
        if h == suffix:
            return int(count)
    return 0

# -------------------- Визуальная шкала --------------------
def print_strength_bar(points, max_points=12):
    bar_length = 12
    filled_length = int(bar_length * points / max_points)
    empty_length = bar_length - filled_length
    if points <= 4:
        color = "\033[91m"
        label = texts[current_lang]["improvable_password"]
    elif points <= 8:
        color = "\033[93m"
        label = texts[current_lang]["improvable_password"]
    else:
        color = "\033[92m"
        label = texts[current_lang]["perfect_password"]
    reset = "\033[0m"
    bar = color + "█" * filled_length + "-" * empty_length + reset
    print(f"{bar} {label}")

# -------------------- Создание пароля --------------------
def create_password():
    t = texts[current_lang]
    while True:
        password = input("\n" + t["create_password"])
        if password.lower() == "menu":
            break

        missing = []
        if not any(ch.isupper() for ch in password):
            missing.append(t["add_upper"])
        if not any(ch.islower() for ch in password):
            missing.append(t["add_lower"])
        if not any(ch.isdigit() for ch in password):
            missing.append(t["add_digit"])
        if not any(ch in string.punctuation for ch in password):
            missing.append(t["add_special"])
        if missing:
            print(t["missing"] + ", ".join(missing))

        if len(password) < 8:
            print(t["short_password"])
        elif len(password) < 16:
            print(t["recommended_length"])

        if any(word in password.lower() for word in common_patterns):
            print(t["common_word"])

        if " " in password:
            print(t["spaces"])
            continue

        leaks = check_pwned(password)
        if leaks > 0:
            print(t["pwned"].format(leaks))
        else:
            print(t["not_pwned"])

        if not missing and len(password) >= 16 and leaks == 0 and " " not in password and not any(word in password.lower() for word in common_patterns):
            print(t["perfect_password"])
        else:
            print(t["improvable_password"])

# -------------------- Проверка пароля --------------------
def password_check():
    t = texts[current_lang]
    while True:
        password = input("\n" + t["password_menu"])
        if password.lower() == "menu":
            break

        result = zxcvbn(password)
        password_point = result["score"]

        length = len(password)
        for limit in [5, 7, 11, 15]:
            if length > limit:
                password_point += 1

        if any(ch.isupper() for ch in password):
            password_point += 1
        if any(ch.islower() for ch in password):
            password_point += 1
        if any(ch.isdigit() for ch in password):
            password_point += 1
        if any(ch in string.punctuation for ch in password):
            password_point += 1

        if any(word in password.lower() for word in common_patterns):
            password_point -= 2
            print(t["common_word"])

        if " " in password:
            print(t["spaces"])
            continue

        leaks = check_pwned(password)
        if leaks > 0:
            print(t["pwned"].format(leaks))
            password_point = max(password_point - 2, 0)

        print_strength_bar(password_point)

# -------------------- Главное меню --------------------
def main_menu():
    global current_lang
    while True:
        t = texts[current_lang]
        print("\n" + t["menu_intro"])
        for option in t["menu_options"]:
            print(option)
        choice = input(t["choose_action"]).strip()
        if choice == "2":
            password_check()
        elif choice == "3":
            create_password()
        elif choice == "4":
            current_lang = "en" if current_lang == "ru" else "ru"
        elif choice == "1":
            print(t["exit"])
            break
        else:
            print(t["invalid_choice"])

# -------------------- Запуск программы --------------------
if __name__ == "__main__":
    print_animated_banner()
    main_menu()

