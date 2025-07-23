"""
Strona logowania - formularz uwierzytelniania
"""
import streamlit as st
from src.config import Config
from src.auth_service import AuthService


def show_login_page():
    """Wyświetla stronę logowania"""
    st.title("🔐 Logowanie")

    # Centrowanie formularza
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        with st.form("login_form"):
            st.markdown("### Zaloguj się do aplikacji")

            username = st.text_input(
                "Nazwa użytkownika",
                placeholder="Wprowadź nazwę użytkownika"
            )
            password = st.text_input(
                "Hasło",
                type="password",
                placeholder="Wprowadź hasło"
            )

            submitted = st.form_submit_button(
                "Zaloguj się",
                use_container_width=True,
                type="primary"
            )

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
        st.info("**🔧 Dane testowe (tryb debug):**\n\n👤 **Użytkownik:** admin\n🔑 **Hasło:** admin123")

    # Dodatkowe informacje
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ℹ️ Informacje")
        st.write("Ta aplikacja używa bezpiecznego systemu uwierzytelniania z hashowaniem haseł.")

    with col2:
        st.markdown("### 🔒 Bezpieczeństwo")
        st.write("Sesje są automatycznie wylogowywane po okresie nieaktywności.")
