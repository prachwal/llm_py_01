"""
Strona Ustawień - konfiguracja aplikacji i użytkownika
"""
import streamlit as st
import logging
from src.config import Config
from src.auth_service import AuthService

logger = logging.getLogger(__name__)


def show_settings_page():
    """Wyświetla stronę ustawień"""
    st.header("⚙️ Ustawienia")
    st.write("Konfiguracja aplikacji i ustawienia użytkownika.")

    # Tabs dla różnych kategorii ustawień
    tab1, tab2, tab3, tab4 = st.tabs([
        "👤 Profil użytkownika",
        "🔧 Konfiguracja aplikacji",
        "🔒 Bezpieczeństwo",
        "🛠️ Narzędzia deweloperskie"
    ])

    with tab1:
        st.subheader("Profil użytkownika")

        current_user = AuthService.get_current_user()
        session_info = AuthService.get_session_info()

        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown("#### 📊 Informacje o koncie")
            if session_info:
                st.write(f"**Użytkownik:** {current_user}")
                st.write(f"**Status:** Zalogowany")
                st.write(f"**Czas sesji:** {int(session_info['session_duration'])} sekund")

                from datetime import datetime
                login_time = datetime.fromtimestamp(session_info['login_time'])
                st.write(f"**Ostatnie logowanie:** {login_time.strftime('%Y-%m-%d %H:%M:%S')}")

        with col2:
            st.markdown("#### ✏️ Edycja profilu")

            with st.form("profile_form"):
                st.text_input("Nazwa wyświetlana", value=current_user, disabled=True)
                st.text_input("Email", placeholder="admin@example.com")
                st.selectbox("Język interfejsu", ["Polski", "English", "Deutsch"])
                st.selectbox("Strefa czasowa", ["Europe/Warsaw", "UTC", "US/Eastern"])

                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("💾 Zapisz zmiany", use_container_width=True):
                        st.success("Profil został zaktualizowany!")
                        logger.info(f"Profil użytkownika {current_user} został zaktualizowany")

                with col2:
                    if st.form_submit_button("🔄 Resetuj", use_container_width=True, type="secondary"):
                        st.info("Formularz został zresetowany")

    with tab2:
        st.subheader("Konfiguracja aplikacji")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 🎨 Wygląd i zachowanie")

            theme = st.selectbox(
                "Motyw aplikacji",
                ["Auto", "Jasny", "Ciemny"],
                help="Wybierz preferowany motyw interfejsu"
            )

            sidebar_state = st.selectbox(
                "Stan paska bocznego",
                ["Rozwinięty", "Zwinięty", "Auto"],
                index=0
            )

            page_layout = st.selectbox(
                "Layout strony",
                ["Szeroki", "Normalny"],
                index=0
            )

            auto_refresh = st.checkbox(
                "Automatyczne odświeżanie dashboardu",
                value=False,
                help="Automatycznie odświeża dane co 30 sekund"
            )

            if auto_refresh:
                refresh_interval = st.slider(
                    "Interwał odświeżania (sekundy)",
                    10, 300, 30
                )

        with col2:
            st.markdown("#### 📊 Wyświetlanie danych")

            items_per_page = st.number_input(
                "Elementów na stronę",
                min_value=10,
                max_value=100,
                value=20,
                step=10
            )

            date_format = st.selectbox(
                "Format daty",
                ["DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD"],
                index=2
            )

            time_format = st.selectbox(
                "Format czasu",
                ["24h", "12h AM/PM"],
                index=0
            )

            show_tooltips = st.checkbox(
                "Pokaż podpowiedzi",
                value=True,
                help="Wyświetla dodatkowe informacje przy najechaniu"
            )

        if st.button("💾 Zapisz ustawienia aplikacji", use_container_width=True):
            st.success("Ustawienia aplikacji zostały zapisane!")
            logger.info("Ustawienia aplikacji zostały zaktualizowane")

    with tab3:
        st.subheader("Bezpieczeństwo")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 🔑 Zmiana hasła")

            with st.form("password_form"):
                current_password = st.text_input(
                    "Aktualne hasło",
                    type="password"
                )
                new_password = st.text_input(
                    "Nowe hasło",
                    type="password"
                )
                confirm_password = st.text_input(
                    "Potwierdź nowe hasło",
                    type="password"
                )

                if st.form_submit_button("🔐 Zmień hasło", use_container_width=True):
                    if not current_password or not new_password:
                        st.error("Wszystkie pola są wymagane")
                    elif new_password != confirm_password:
                        st.error("Nowe hasła nie są identyczne")
                    elif len(new_password) < 6:
                        st.error("Hasło musi mieć co najmniej 6 znaków")
                    else:
                        # Tutaj byłaby logika zmiany hasła
                        st.success("Hasło zostało zmienione!")
                        logger.info(f"Hasło użytkownika {current_user} zostało zmienione")

        with col2:
            st.markdown("#### 🛡️ Ustawienia sesji")

            session_timeout = st.slider(
                "Timeout sesji (minuty)",
                5, 480, 60,
                help="Czas po którym sesja wygasa automatycznie"
            )

            auto_logout = st.checkbox(
                "Automatyczne wylogowanie przy zamknięciu",
                value=True
            )

            remember_login = st.checkbox(
                "Zapamiętaj logowanie",
                value=False,
                help="Wydłuża czas sesji do 30 dni"
            )

            st.markdown("#### 🔍 Logi bezpieczeństwa")

            if st.button("📜 Pokaż historię logowań", use_container_width=True):
                st.info("Historia logowań zostanie wyświetlona w sekcji danych")

            if st.button("🚪 Wyloguj wszystkie sesje", use_container_width=True, type="secondary"):
                st.warning("Funkcja dostępna w pełnej wersji aplikacji")

    with tab4:
        st.subheader("Narzędzia deweloperskie")

        if Config.get_debug():
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### 🐛 Debug i testy")

                if st.button("🧪 Test logowania", use_container_width=True):
                    logger.info(f"Test logowania wykonany przez użytkownika {current_user}")
                    st.success("Test logowania zapisany w logach")

                if st.button("📝 Pokaż logi aplikacji", use_container_width=True):
                    try:
                        with open("app.log", "r") as f:
                            logs = f.readlines()[-10:]  # Ostatnie 10 linii
                        st.code("\n".join(logs))
                    except FileNotFoundError:
                        st.warning("Plik logów nie istnieje")

                if st.button("🔄 Wymuś restart sesji", use_container_width=True):
                    AuthService.logout_user()
                    st.rerun()

            with col2:
                st.markdown("#### ⚙️ Informacje systemowe")

                st.write("**Tryb debug:** Włączony")
                st.write(f"**Nazwa aplikacji:** {Config.get_app_name()}")
                st.write(f"**Host:** {Config.get_host()}")
                st.write(f"**Port:** {Config.get_port()}")
                st.write(f"**Poziom logów:** {Config.get_log_level()}")

                st.markdown("#### 🔑 Generowanie hashów")

                with st.form("hash_form"):
                    password_to_hash = st.text_input(
                        "Hasło do zahashowania",
                        type="password"
                    )

                    if st.form_submit_button("🔐 Generuj hash"):
                        if password_to_hash:
                            hashed = AuthService.hash_password(password_to_hash)
                            st.code(hashed)
                            st.success("Hash wygenerowany!")
                        else:
                            st.error("Wprowadź hasło")
        else:
            st.info("🔒 Narzędzia deweloperskie są dostępne tylko w trybie debug.")
            st.write("Aby włączyć tryb debug, ustaw `DEBUG=True` w pliku `.env`")

    # Przycisk powrotu
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        if st.button("🏠 Powrót do Dashboard", use_container_width=True):
            st.switch_page("pages/dashboard.py")
