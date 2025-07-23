# Streamlit App

Minimalna aplikacja Streamlit z systemem logowania, testami i pełną konfiguracją.

## 🚀 Szybki start

### Automatyczna instalacja
```bash
./setup.sh
```

### Manualna instalacja
```bash
# 1. Utwórz środowisko wirtualne
python3 -m venv venv
source venv/bin/activate

# 2. Zainstaluj zależności
pip install -r requirements.txt

# 3. Skopiuj konfigurację
cp .env.example .env

# 4. Uruchom testy
python -m pytest tests/ -v

# 5. Uruchom aplikację
streamlit run app.py
```

## 📁 Struktura projektu

```
├── app.py                 # Główna aplikacja Streamlit
├── requirements.txt       # Zależności Python
├── setup.sh              # Skrypt automatycznej instalacji
├── .env                  # Konfiguracja środowiska
├── .env.example          # Przykład konfiguracji
├── src/                  # Kod źródłowy
│   ├── __init__.py
│   ├── config.py         # Zarządzanie konfiguracją
│   └── auth_service.py   # Serwis uwierzytelniania
└── tests/                # Testy jednostkowe
    ├── __init__.py
    ├── test_config.py
    └── test_auth_service.py
```

## 🔐 System logowania

Aplikacja zawiera prosty system uwierzytelniania z:
- Hashowaniem haseł (bcrypt)
- Zarządzaniem sesjami
- Timeoutem sesji
- Logowaniem zdarzeń

### Domyślne dane logowania
- **Użytkownik:** `admin`
- **Hasło:** `admin123`

## ⚙️ Konfiguracja

Wszystkie ustawienia są w pliku `.env`:

```env
# Podstawowe ustawienia
APP_NAME=Streamlit App
DEBUG=True
HOST=localhost
PORT=8501

# Bezpieczeństwo
SECRET_KEY=your-secret-key
SESSION_TIMEOUT=3600

# Użytkownicy
ADMIN_USER=admin
ADMIN_PASSWORD_HASH=hash_hasła

# Logowanie
LOG_LEVEL=INFO
LOG_FILE=app.log
```

## 🔧 Zadania VS Code

Projekt zawiera skonfigurowane zadania (tasks) dla Visual Studio Code. Dostęp: `Ctrl+Shift+P` → "Tasks: Run Task"

### 🚀 Podstawowe zadania:
- **Uruchom aplikację Streamlit** - startuje serwer deweloperski
- **Uruchom testy** - wykonuje wszystkie testy jednostkowe
- **Uruchom testy z pokryciem** - testy + raport pokrycia kodu

### 🔍 Jakość kodu:
- **Sprawdź jakość kodu (flake8)** - analiza stylu i błędów
- **Formatuj kod (black)** - automatyczne formatowanie
- **Sprawdź formatowanie kodu** - sprawdzenie bez zmian

### ⚙️ Zarządzanie środowiskiem:
- **Zainstaluj zależności** - pip install -r requirements.txt
- **Utwórz środowisko wirtualne** - nowe venv
- **Aktywuj venv i zainstaluj zależności** - szybka konfiguracja
- **Pełna inicjalizacja projektu** - uruchomienie setup.sh

### 🛠️ Narzędzia pomocnicze:
- **Wygeneruj hash hasła** - do konfiguracji użytkowników
- **Wyczyść pliki cache** - usuwa __pycache__
- **Sprawdź logi aplikacji** - tail -f app.log

## 🐛 Debugowanie

Konfiguracje debugowania dostępne w Run & Debug (F5):
- **Debug Streamlit App** - debugowanie głównej aplikacji
- **Debug Tests** - debugowanie testów
- **Debug Single Test File** - debugowanie pojedynczego pliku testów
- **Python: Current File** - debugowanie aktualnego pliku

## 📝 Ustawienia VS Code

Projekt zawiera automatyczną konfigurację:
- Python interpreter: `./venv/bin/python`
- Formatowanie przy zapisie (Black)
- Automatyczne sortowanie importów
- Lint z flake8
- Wykluczenie plików cache z eksploratora

### Zalecane rozszerzenia:
- Python (ms-python.python)
- Black Formatter (ms-python.black-formatter)
- Flake8 (ms-python.flake8)
- Pylint (ms-python.pylint)
- Jupyter (ms-toolsai.jupyter)

## 🧪 Testy

```bash
# Uruchom wszystkie testy
python -m pytest tests/ -v

# Uruchom testy z pokryciem
python -m pytest tests/ --cov=src

# Sprawdź jakość kodu
flake8 src/ app.py
black src/ app.py
```

## 📊 Funkcjonalności

### Zaimplementowane
- ✅ System logowania z hashowaniem haseł
- ✅ Zarządzanie sesjami z timeoutem
- ✅ Konfiguracja przez zmienne środowiskowe
- ✅ Kompleksowe testy jednostkowe
- ✅ Logowanie zdarzeń
- ✅ Automatyczny skrypt setup.sh
- ✅ Walidacja konfiguracji

### Interfejs użytkownika
- 🔐 Formularz logowania
- 📊 Dashboard z metrykami
- 📈 Przykładowe wykresy
- ⚙️ Panel ustawień
- 📋 Informacje o sesji w sidebarze

## 🔧 Opcje skryptu setup.sh

```bash
./setup.sh              # Pełna instalacja
./setup.sh --skip-tests # Instalacja bez testów
./setup.sh --tests-only # Tylko testy i sprawdzanie kodu
./setup.sh --help       # Pomoc
```

## 🚀 Uruchomienie

Po zakończeniu instalacji:

1. **Aktywuj środowisko wirtualne:**
   ```bash
   source venv/bin/activate
   ```

2. **Uruchom aplikację:**
   ```bash
   streamlit run app.py
   ```

3. **Otwórz w przeglądarce:**
   ```
   http://localhost:8501
   ```

## 🛡️ Bezpieczeństwo

⚠️ **Ważne dla produkcji:**
- Zmień `SECRET_KEY` w pliku `.env`
- Wygeneruj nowy hash hasła dla admina
- Ustaw `DEBUG=False`
- Użyj zewnętrznej bazy danych dla użytkowników
- Skonfiguruj HTTPS

## 📝 Logowanie

Aplikacja loguje zdarzenia do:
- Pliku `app.log`
- Konsoli (podczas developmentu)

Poziomy logowania: DEBUG, INFO, WARNING, ERROR

## 🤝 Development

### Dodawanie nowych funkcji
1. Umieść logikę biznesową w `src/`
2. Dodaj odpowiednie testy w `tests/`
3. Aktualizuj dokumentację
4. Uruchom testy przed commitem

### Code Quality
Projekt używa:
- `black` do formatowania kodu
- `flake8` do sprawdzania stylu
- `pytest` do testowania

---

**Autor:** System
**Data:** 2025-07-23
