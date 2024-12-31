# Цифрова обробка сигналів

Репозиторій навчального курсу "Цифрова обробка сигналів"

## Налаштування середовища розробки

1. Клонуйте репозиторій:
```bash
git clone https://github.com/SZabolotnii/dsp-course.git
cd dsp-course
```

2. Створіть та активуйте віртуальне середовище:
```bash
# Створення віртуального середовища
python -m venv venv

# Активація для Linux/macOS
source venv/bin/activate

# Активація для Windows
venv\Scripts\activate
```

3. Встановіть залежності:
```bash
pip install -r requirements.txt
```

## Структура репозиторію

- `course-info/` - Інформація про курс
- `lectures/` - Матеріали лекцій
- `labs/` - Лабораторні роботи
- `resources/` - Додаткові матеріали
- `assessment/` - Матеріали для оцінювання
- `scripts/` - Скрипти для обслуговування репозиторію

## Використання

Для оновлення матеріалів з Moodle-бекапу:
```bash
# Активуйте віртуальне середовище, якщо воно не активне
source venv/bin/activate  # Linux/macOS
# або
venv\Scripts\activate     # Windows

# Запустіть скрипт міграції
python scripts/migrate.py <шлях_до_бекапу> <шлях_до_репозиторію>
```

## Розробка

Для додавання нових залежностей:
```bash
pip install <назва_пакету>
pip freeze > requirements.txt
```