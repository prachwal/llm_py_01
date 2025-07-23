#!/bin/bash

# setup.sh - Skrypt inicjalizacji środowiska dla aplikacji Streamlit
# Autor: System
# Data: $(date)

set -e  # Zatrzymaj wykonywanie przy błędzie

# Kolory dla outputu
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Inicjalizacja środowiska dla aplikacji Streamlit${NC}"
echo "=================================================="

# Funkcja logowania
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Sprawdź czy Python jest zainstalowany
check_python() {
    log_info "Sprawdzanie instalacji Python..."
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version)
        log_info "Znaleziono $PYTHON_VERSION"
    else
        log_error "Python3 nie jest zainstalowany. Zainstaluj Python 3.8+ przed kontynuowaniem."
        exit 1
    fi
}

# Sprawdź czy pip jest zainstalowany
check_pip() {
    log_info "Sprawdzanie instalacji pip..."
    if command -v pip3 &> /dev/null; then
        PIP_VERSION=$(pip3 --version)
        log_info "Znaleziono $PIP_VERSION"
    else
        log_error "pip3 nie jest zainstalowany. Zainstaluj pip przed kontynuowaniem."
        exit 1
    fi
}

# Utwórz środowisko wirtualne
create_venv() {
    log_info "Tworzenie środowiska wirtualnego..."
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        log_info "Środowisko wirtualne utworzone w katalogu 'venv'"
    else
        log_warning "Środowisko wirtualne już istnieje"
    fi
}

# Aktywuj środowisko wirtualne
activate_venv() {
    log_info "Aktywacja środowiska wirtualnego..."
    source venv/bin/activate
    log_info "Środowisko wirtualne aktywowane"
}

# Zainstaluj zależności
install_dependencies() {
    log_info "Instalowanie zależności z requirements.txt..."
    pip install --upgrade pip
    pip install -r requirements.txt
    log_info "Zależności zainstalowane pomyślnie"
}

# Skopiuj plik konfiguracyjny
setup_config() {
    log_info "Konfiguracja pliku środowiskowego..."
    if [ ! -f ".env" ]; then
        if [ -f ".env.example" ]; then
            cp .env.example .env
            log_info "Skopiowano .env.example do .env"
            log_warning "UWAGA: Zmień hasła i klucze w pliku .env przed uruchomieniem w produkcji!"
        else
            log_error "Plik .env.example nie istnieje"
            exit 1
        fi
    else
        log_warning "Plik .env już istnieje - pomijam kopiowanie"
    fi
}

# Wygeneruj nowy hash hasła dla admina
generate_admin_password() {
    log_info "Generowanie nowego hasha hasła dla admina..."
    ADMIN_PASSWORD="admin123"
    
    # Używamy Python do wygenerowania hasha
    ADMIN_HASH=$(python3 -c "
import bcrypt
password = '$ADMIN_PASSWORD'.encode('utf-8')
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
print(hashed.decode('utf-8'))
")
    
    # Aktualizuj plik .env
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s|ADMIN_PASSWORD_HASH=.*|ADMIN_PASSWORD_HASH=$ADMIN_HASH|" .env
    else
        # Linux
        sed -i "s|ADMIN_PASSWORD_HASH=.*|ADMIN_PASSWORD_HASH=$ADMIN_HASH|" .env
    fi
    
    log_info "Hash hasła zaktualizowany w pliku .env"
    log_info "Domyślne dane logowania: admin / $ADMIN_PASSWORD"
}

# Uruchom testy
run_tests() {
    log_info "Uruchamianie testów..."
    python -m pytest tests/ -v
    if [ $? -eq 0 ]; then
        log_info "Wszystkie testy przeszły pomyślnie"
    else
        log_error "Niektóre testy nie przeszły"
        exit 1
    fi
}

# Sprawdź składnię kodu
check_code_quality() {
    log_info "Sprawdzanie jakości kodu..."
    
    # Flake8 - sprawdzenie stylu kodu
    log_info "Uruchamianie flake8..."
    flake8 src/ app.py --max-line-length=88 --ignore=E203,W503
    
    # Black - formatowanie kodu
    log_info "Sprawdzanie formatowania z black..."
    black --check src/ app.py
    
    log_info "Sprawdzanie jakości kodu zakończone"
}

# Sprawdź czy wszystko działa
test_app() {
    log_info "Testowanie podstawowej funkcjonalności aplikacji..."
    python3 -c "
from src.config import Config
from src.auth_service import AuthService

# Test konfiguracji
try:
    Config.validate_config()
    print('✓ Konfiguracja jest poprawna')
except Exception as e:
    print(f'✗ Błąd konfiguracji: {e}')
    exit(1)

# Test serwisu uwierzytelniania
try:
    result = AuthService.hash_password('test')
    print('✓ Serwis uwierzytelniania działa')
except Exception as e:
    print(f'✗ Błąd serwisu uwierzytelniania: {e}')
    exit(1)

print('✓ Podstawowe testy przeszły pomyślnie')
"
}

# Wyświetl instrukcje uruchomienia
show_instructions() {
    echo ""
    log_info "🎉 Konfiguracja zakończona pomyślnie!"
    echo ""
    echo -e "${BLUE}Instrukcje uruchomienia:${NC}"
    echo "1. Aktywuj środowisko wirtualne:"
    echo -e "   ${YELLOW}source venv/bin/activate${NC}"
    echo ""
    echo "2. Uruchom aplikację:"
    echo -e "   ${YELLOW}streamlit run app.py${NC}"
    echo ""
    echo "3. Otwórz przeglądarkę i przejdź do:"
    echo -e "   ${YELLOW}http://localhost:8501${NC}"
    echo ""
    echo -e "${BLUE}Dane logowania:${NC}"
    echo -e "   Użytkownik: ${YELLOW}admin${NC}"
    echo -e "   Hasło: ${YELLOW}admin123${NC}"
    echo ""
    echo -e "${BLUE}Przydatne komendy:${NC}"
    echo -e "   Uruchom testy: ${YELLOW}python -m pytest tests/ -v${NC}"
    echo -e "   Sprawdź kod: ${YELLOW}flake8 src/ app.py${NC}"
    echo -e "   Formatuj kod: ${YELLOW}black src/ app.py${NC}"
    echo ""
}

# Główna funkcja
main() {
    log_info "Rozpoczynam konfigurację środowiska..."
    
    # Sprawdzenia podstawowe
    check_python
    check_pip
    
    # Konfiguracja środowiska
    create_venv
    activate_venv
    install_dependencies
    
    # Konfiguracja aplikacji
    setup_config
    generate_admin_password
    
    # Testy i walidacja
    run_tests
    check_code_quality
    test_app
    
    # Podsumowanie
    show_instructions
}

# Obsługa argumentów
case "${1:-}" in
    --skip-tests)
        log_warning "Pomijanie testów..."
        check_python
        check_pip
        create_venv
        activate_venv
        install_dependencies
        setup_config
        generate_admin_password
        test_app
        show_instructions
        ;;
    --tests-only)
        log_info "Uruchamianie tylko testów..."
        activate_venv
        run_tests
        check_code_quality
        ;;
    --help)
        echo "Użycie: $0 [OPCJA]"
        echo ""
        echo "Opcje:"
        echo "  --skip-tests    Pomiń uruchamianie testów"
        echo "  --tests-only    Uruchom tylko testy i sprawdzanie kodu"
        echo "  --help          Wyświetl tę pomoc"
        echo ""
        ;;
    *)
        main
        ;;
esac
