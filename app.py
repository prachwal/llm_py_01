"""
Główna aplikacja Streamlit z modularną strukturą stron
"""
import streamlit as st
import logging
from src.config import Config
from src.auth_service import AuthService

# Inicjalizacja konfiguracji i logowania
Config.setup_logging()
logger = logging.getLogger(__name__)


def init_session_state():
    """Inicjalizacja stanu sesji"""
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    if 'username' not in st.session_state:
        st.session_state['username'] = None
    if 'login_time' not in st.session_state:
        st.session_state['login_time'] = None


def show_navigation():
    """Wyświetla nawigację aplikacji w sidebarze"""
    st.sidebar.markdown("## 🧭 Nawigacja")

    # Informacje o użytkowniku
    current_user = AuthService.get_current_user()
    if current_user:
        st.sidebar.success(f"Zalogowany: **{current_user}**")

        # Informacje o sesji
        session_info = AuthService.get_session_info()
        if session_info:
            time_left_min = int(session_info['time_left'] / 60)
            st.sidebar.info(f"⏱️ Pozostały czas: {time_left_min} min")

        st.sidebar.markdown("---")

        # Menu nawigacyjne
        pages = {
            "📊 Dashboard": "pages/dashboard.py",
            "📈 Dane i Analizy": "pages/data.py",
            "⚙️ Ustawienia": "pages/settings.py"
        }

        st.sidebar.markdown("### 📋 Strony")
        for page_name, page_path in pages.items():
            if st.sidebar.button(page_name, use_container_width=True):
                st.switch_page(page_path)

        st.sidebar.markdown("---")

        # Przycisk wylogowania
        if st.sidebar.button("🚪 Wyloguj się", use_container_width=True, type="secondary"):
            AuthService.logout_user()
            st.rerun()

        # Dodatkowe informacje
        st.sidebar.markdown("---")
        st.sidebar.markdown("### ℹ️ Informacje")
        st.sidebar.markdown(f"**Aplikacja:** {Config.get_app_name()}")
        if Config.get_debug():
            st.sidebar.warning("🐛 Tryb DEBUG")


def show_main_app():
    """Wyświetla główną aplikację po zalogowaniu"""
    # Nawigacja w sidebarze
    show_navigation()

    # Domyślnie pokazuj dashboard
    st.switch_page("pages/dashboard.py")


def show_login_page():
    """Wyświetla stronę logowania"""
    # Import tutaj, żeby uniknąć cyklicznych importów
    from pages.login import show_login_page
    show_login_page()


def main():
    """Główna funkcja aplikacji"""
    # Konfiguracja strony
    st.set_page_config(
        page_title=Config.get_app_name(),
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Inicjalizacja
    init_session_state()

    try:
        # Walidacja konfiguracji
        Config.validate_config()

        # Sprawdzenie uwierzytelnienia
        if AuthService.is_authenticated():
            show_main_app()
        else:
            show_login_page()

    except ValueError as e:
        st.error(f"Błąd konfiguracji: {e}")
        logger.error(f"Błąd konfiguracji: {e}")
    except Exception as e:
        st.error(f"Wystąpił nieoczekiwany błąd: {e}")
        logger.error(f"Nieoczekiwany błąd: {e}")


if __name__ == "__main__":
    main()
