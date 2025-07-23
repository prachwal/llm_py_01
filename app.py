"""
Główna aplikacja Streamlit z systemem logowania
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


def show_login_form():
    """Wyświetla formularz logowania"""
    st.title("🔐 Logowanie")
    
    with st.form("login_form"):
        username = st.text_input("Nazwa użytkownika")
        password = st.text_input("Hasło", type="password")
        submitted = st.form_submit_button("Zaloguj się")
        
        if submitted:
            if username and password:
                if AuthService.authenticate_user(username, password):
                    AuthService.login_user(username)
                    st.success("Pomyślnie zalogowano!")
                    st.rerun()
                else:
                    st.error("Nieprawidłowa nazwa użytkownika lub hasło")
            else:
                st.error("Wprowadź nazwę użytkownika i hasło")
    
    # Informacje dla developera
    if Config.get_debug():
        st.info("**Dane testowe:**\n\nUżytkownik: admin\nHasło: admin123")


def show_main_app():
    """Wyświetla główną aplikację po zalogowaniu"""
    # Nagłówek z informacjami o sesji
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.title(f"👋 Witaj, {AuthService.get_current_user()}!")
    
    with col2:
        if st.button("Wyloguj się"):
            AuthService.logout_user()
            st.rerun()
    
    # Informacje o sesji
    session_info = AuthService.get_session_info()
    if session_info:
        st.sidebar.markdown("### 📊 Informacje o sesji")
        st.sidebar.write(f"**Użytkownik:** {session_info['username']}")
        st.sidebar.write(f"**Czas pozostały:** {int(session_info['time_left'])} sekund")
        st.sidebar.write(f"**Czas trwania sesji:** {int(session_info['session_duration'])} sekund")
    
    # Główna zawartość aplikacji
    st.markdown("---")
    st.header("🚀 Główna aplikacja")
    
    # Przykładowa zawartość
    tab1, tab2, tab3 = st.tabs(["Dashboard", "Dane", "Ustawienia"])
    
    with tab1:
        st.subheader("Dashboard")
        st.write("To jest główny dashboard aplikacji.")
        
        # Przykładowe metryki
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Użytkownicy", "1", "0")
        with col2:
            st.metric("Sesje", "1", "1")
        with col3:
            st.metric("Uptime", "100%", "0%")
    
    with tab2:
        st.subheader("Dane")
        st.write("Tutaj można wyświetlać dane i analizy.")
        
        # Przykładowy wykres
        import numpy as np
        chart_data = np.random.randn(20, 3)
        st.line_chart(chart_data)
    
    with tab3:
        st.subheader("Ustawienia")
        st.write("Panel ustawień aplikacji.")
        
        if st.button("Test logowania"):
            logger.info("Test logowania wykonany przez użytkownika")
            st.success("Test logowania zapisany w logach")


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
            show_login_form()
            
    except ValueError as e:
        st.error(f"Błąd konfiguracji: {e}")
        logger.error(f"Błąd konfiguracji: {e}")
    except Exception as e:
        st.error(f"Wystąpił nieoczekiwany błąd: {e}")
        logger.error(f"Nieoczekiwany błąd: {e}")


if __name__ == "__main__":
    main()
