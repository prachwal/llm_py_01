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
├── app.py                 # Główna aplikacja Streamlit (router)
├── requirements.txt       # Zależności Python
├── setup.sh              # Skrypt automatycznej instalacji
├── .env                  # Konfiguracja środowiska
├── .env.example          # Przykład konfiguracji
├── src/                  # Kod źródłowy (logika biznesowa)
│   ├── __init__.py
│   ├── config.py         # Zarządzanie konfiguracją
│   └── auth_service.py   # Serwis uwierzytelniania
├── pages/                # Moduły stron aplikacji
│   ├── __init__.py
│   ├── login.py          # Strona logowania
│   ├── dashboard.py      # Dashboard główny
│   ├── data.py          # Analiza i wizualizacja danych
│   └── settings.py       # Ustawienia aplikacji
├── tests/                # Testy jednostkowe
│   ├── __init__.py
│   ├── test_config.py
│   ├── test_auth_service.py
│   └── test_pages.py     # Testy modułów stron
└── .vscode/              # Konfiguracja VS Code
    ├── tasks.json        # Zadania deweloperskie
    ├── launch.json       # Konfiguracje debugowania
    ├── settings.json     # Ustawienia projektu
    └── extensions.json   # Zalecane rozszerzenia
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
- ✅ **Modularna struktura stron (pages/)**
- ✅ **Interaktywne wykresy (Plotly)**
- ✅ **Zaawansowana nawigacja**
- ✅ **Responsywny UI design**

### Interfejs użytkownika
- 🔐 Strona logowania z ulepszonym interfejsem
- 📊 Dashboard z metrykami i wykresami aktywności
- 📈 Strona analizy danych z interaktywnymi wykresami (Plotly)
- ⚙️ Kompleksowa strona ustawień z konfiguracją profilu
- 🧭 Intuicyjna nawigacja w sidebarze
- 📱 Responsywny design i moderne UI components

## 🎯 **Architektura modularna**

Aplikacja została przeprojektowana z myślą o skalowalności:

### **📱 Struktura stron:**
- **`app.py`** - główny router i zarządzanie nawigacją
- **`pages/login.py`** - zaawansowana strona logowania
- **`pages/dashboard.py`** - dashboard z metrykami i wykresami
- **`pages/data.py`** - analiza danych z Plotly charts
- **`pages/settings.py`** - konfiguracja użytkownika i aplikacji

### **⚡ Funkcjonalności stron:**

#### **🔐 Login (`pages/login.py`):**
- Centrum formularza logowania
- Informacje debug dla deweloperów
- Dodatkowe sekcje informacyjne
- Responsywny design

#### **📊 Dashboard (`pages/dashboard.py`):**
- Metryki użytkownika w czasie rzeczywistym
- Wykresy aktywności (pandas + plotly)
- Informacje o sesji z paskiem postępu
- Szybkie akcje nawigacyjne

#### **📈 Dane (`pages/data.py`):**
- Interaktywne wykresy (Plotly Express)
- Filtry w sidebarze
- Tabs: Wykresy, Tabele, Szczegóły, Eksport
- Symulacja różnych typów danych
- Funkcje eksportu danych

#### **⚙️ Ustawienia (`pages/settings.py`):**
- Tabs: Profil, Konfiguracja, Bezpieczeństwo, Dev Tools
- Edycja profilu użytkownika
- Konfiguracja wyglądu aplikacji
- Zmiana hasła i ustawienia sesji
- Narzędzia deweloperskie (debug mode)

### **� Nawigacja:**
- Sidebar z menu stron
- Informacje o użytkowniku i sesji
- Przycisk wylogowania
- Wskaźniki stanu (debug mode)

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
