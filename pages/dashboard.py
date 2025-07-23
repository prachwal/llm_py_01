"""
Strona Dashboard - główny panel po zalogowaniu
"""
import streamlit as st
import time
from datetime import datetime
from src.auth_service import AuthService


def show_dashboard_page():
    """Wyświetla stronę dashboard"""
    st.header("📊 Dashboard")
    st.write("Główny panel aplikacji z przeglądem najważniejszych informacji.")

    # Metryki użytkownika
    session_info = AuthService.get_session_info()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Aktywni użytkownicy",
            "1",
            "0",
            help="Liczba aktualnie zalogowanych użytkowników"
        )

    with col2:
        if session_info:
            duration_minutes = int(session_info['session_duration'] / 60)
            st.metric(
                "Czas sesji",
                f"{duration_minutes} min",
                "aktywna",
                help="Czas trwania aktualnej sesji"
            )

    with col3:
        if session_info:
            time_left_minutes = int(session_info['time_left'] / 60)
            st.metric(
                "Pozostały czas",
                f"{time_left_minutes} min",
                help="Czas do automatycznego wylogowania"
            )

    with col4:
        st.metric(
            "Uptime aplikacji",
            "100%",
            "0%",
            help="Dostępność aplikacji"
        )

    st.markdown("---")

    # Aktywność użytkownika
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📈 Aktywność")

        # Przykładowy wykres aktywności
        import pandas as pd
        import numpy as np

        # Generuj przykładowe dane aktywności
        dates = pd.date_range('2025-07-01', '2025-07-23', freq='D')
        activity_data = pd.DataFrame({
            'Data': dates,
            'Logowania': np.random.randint(1, 10, len(dates)),
            'Sesje': np.random.randint(1, 8, len(dates))
        })

        st.line_chart(activity_data.set_index('Data'))

    with col2:
        st.subheader("ℹ️ Informacje o sesji")

        if session_info:
            st.write(f"**Użytkownik:** {session_info['username']}")

            login_time = datetime.fromtimestamp(session_info['login_time'])
            st.write(f"**Zalogowano:** {login_time.strftime('%H:%M:%S')}")

            st.write(f"**Czas sesji:** {int(session_info['session_duration'])}s")
            st.write(f"**Pozostały czas:** {int(session_info['time_left'])}s")

            # Pasek postępu dla czasu sesji
            progress = session_info['session_duration'] / (session_info['session_duration'] + session_info['time_left'])
            st.progress(progress, text="Postęp sesji")

    st.markdown("---")

    # Szybkie akcje
    st.subheader("⚡ Szybkie akcje")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🔄 Odśwież dashboard", use_container_width=True):
            st.rerun()

    with col2:
        if st.button("📊 Przejdź do danych", use_container_width=True):
            st.switch_page("pages/data.py")

    with col3:
        if st.button("⚙️ Ustawienia", use_container_width=True):
            st.switch_page("pages/settings.py")

    with col4:
        if st.button("🚪 Wyloguj się", use_container_width=True, type="secondary"):
            AuthService.logout_user()
            st.rerun()
