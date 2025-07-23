"""
Strona Dane - analiza i wizualizacja danych
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta


def show_data_page():
    """Wyświetla stronę z danymi i analizami"""
    st.header("📈 Analiza danych")
    st.write("Strona do analizy i wizualizacji danych aplikacji.")

    # Sidebar z opcjami filtrowania
    st.sidebar.markdown("### 🔍 Filtry danych")

    # Wybór zakresu dat
    date_range = st.sidebar.date_input(
        "Zakres dat",
        value=[datetime.now() - timedelta(days=30), datetime.now()],
        help="Wybierz zakres dat do analizy"
    )

    # Wybór typu danych
    data_type = st.sidebar.selectbox(
        "Typ danych",
        ["Aktywność użytkowników", "Wydajność systemu", "Logi aplikacji"],
        help="Wybierz typ danych do wyświetlenia"
    )

    # Tabs dla różnych analiz
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Wykresy",
        "📋 Tabele",
        "🔍 Szczegóły",
        "📤 Eksport"
    ])

    with tab1:
        st.subheader("Wizualizacje danych")

        # Generuj przykładowe dane
        dates = pd.date_range('2025-07-01', '2025-07-23', freq='D')

        if data_type == "Aktywność użytkowników":
            data = pd.DataFrame({
                'Data': dates,
                'Logowania': np.random.randint(5, 25, len(dates)),
                'Aktywni użytkownicy': np.random.randint(1, 15, len(dates)),
                'Czas sesji (min)': np.random.randint(10, 120, len(dates))
            })

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### 👥 Logowania dzienne")
                fig = px.bar(data, x='Data', y='Logowania',
                           title="Liczba logowań dziennie")
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.markdown("#### ⏱️ Średni czas sesji")
                fig = px.line(data, x='Data', y='Czas sesji (min)',
                            title="Średni czas sesji (minuty)")
                st.plotly_chart(fig, use_container_width=True)

        elif data_type == "Wydajność systemu":
            data = pd.DataFrame({
                'Czas': pd.date_range('2025-07-23 00:00', '2025-07-23 23:59', freq='H'),
                'CPU (%)': np.random.randint(10, 80, 24),
                'RAM (%)': np.random.randint(20, 70, 24),
                'Odpowiedź (ms)': np.random.randint(50, 300, 24)
            })

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### 💻 Wykorzystanie zasobów")
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=data['Czas'], y=data['CPU (%)'],
                                       name='CPU', line=dict(color='red')))
                fig.add_trace(go.Scatter(x=data['Czas'], y=data['RAM (%)'],
                                       name='RAM', line=dict(color='blue')))
                fig.update_layout(title="Wykorzystanie CPU i RAM", yaxis_title="Procent (%)")
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.markdown("#### ⚡ Czas odpowiedzi")
                fig = px.area(data, x='Czas', y='Odpowiedź (ms)',
                            title="Czas odpowiedzi aplikacji")
                st.plotly_chart(fig, use_container_width=True)

        else:  # Logi aplikacji
            # Wykresy logów
            log_data = pd.DataFrame({
                'Godzina': pd.date_range('2025-07-23 00:00', '2025-07-23 23:59', freq='H'),
                'INFO': np.random.randint(10, 50, 24),
                'WARNING': np.random.randint(0, 10, 24),
                'ERROR': np.random.randint(0, 5, 24)
            })

            st.markdown("#### 📝 Logi aplikacji wg poziomu")
            fig = px.bar(log_data, x='Godzina', y=['INFO', 'WARNING', 'ERROR'],
                        title="Liczba logów wg poziomu i godziny")
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Tabele danych")

        if data_type == "Aktywność użytkowników":
            st.markdown("#### 👥 Szczegóły aktywności użytkowników")
            user_data = pd.DataFrame({
                'Użytkownik': ['admin', 'user1', 'user2', 'user3'],
                'Ostatnie logowanie': [
                    '2025-07-23 14:30:00',
                    '2025-07-23 12:15:00',
                    '2025-07-22 16:45:00',
                    '2025-07-21 09:20:00'
                ],
                'Liczba sesji': [25, 18, 12, 8],
                'Średni czas sesji (min)': [45, 32, 28, 52],
                'Status': ['Aktywny', 'Nieaktywny', 'Nieaktywny', 'Nieaktywny']
            })
            st.dataframe(user_data, use_container_width=True)

        elif data_type == "Wydajność systemu":
            st.markdown("#### 💻 Metryki systemu")
            system_data = pd.DataFrame({
                'Metryka': ['CPU średnie', 'RAM średnie', 'Dysk wolne', 'Połączenia'],
                'Wartość': ['45%', '62%', '25 GB', '128'],
                'Status': ['OK', 'Ostrzeżenie', 'OK', 'OK'],
                'Limit': ['80%', '85%', '5 GB', '1000']
            })
            st.dataframe(system_data, use_container_width=True)

        else:
            st.markdown("#### 📝 Ostatnie logi")
            log_entries = pd.DataFrame({
                'Czas': [
                    '2025-07-23 14:35:22',
                    '2025-07-23 14:34:15',
                    '2025-07-23 14:33:08',
                    '2025-07-23 14:32:45',
                    '2025-07-23 14:31:30'
                ],
                'Poziom': ['INFO', 'INFO', 'WARNING', 'INFO', 'ERROR'],
                'Moduł': ['auth_service', 'config', 'auth_service', 'app', 'database'],
                'Wiadomość': [
                    'Pomyślne logowanie użytkownika: admin',
                    'Konfiguracja załadowana pomyślnie',
                    'Próba logowania z nieprawidłowym hasłem',
                    'Aplikacja uruchomiona pomyślnie',
                    'Błąd połączenia z bazą danych'
                ]
            })
            st.dataframe(log_entries, use_container_width=True)

    with tab3:
        st.subheader("Szczegółowe informacje")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 📊 Statystyki ogólne")
            stats = {
                "Całkowita liczba logowań": "1,247",
                "Średni czas sesji": "42 min",
                "Najdłuższa sesja": "3h 25min",
                "Najczęstszy użytkownik": "admin",
                "Błędy w tym miesiącu": "3",
                "Uptime aplikacji": "99.8%"
            }

            for key, value in stats.items():
                st.metric(key, value)

        with col2:
            st.markdown("#### 🔍 Filtry zaawansowane")

            # Dodatkowe opcje filtrowania
            st.selectbox("Grupa użytkowników", ["Wszyscy", "Administratorzy", "Użytkownicy"])
            st.slider("Minimalny czas sesji (min)", 0, 180, 5)
            st.multiselect("Poziomy logów", ["DEBUG", "INFO", "WARNING", "ERROR"], ["INFO", "WARNING", "ERROR"])

            if st.button("Zastosuj filtry", use_container_width=True):
                st.success("Filtry zastosowane!")

    with tab4:
        st.subheader("Eksport danych")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 📤 Opcje eksportu")

            export_format = st.selectbox(
                "Format eksportu",
                ["CSV", "Excel", "JSON", "PDF raport"]
            )

            export_range = st.selectbox(
                "Zakres danych",
                ["Aktualny widok", "Wszystkie dane", "Ostatnie 30 dni", "Niestandardowy"]
            )

            include_charts = st.checkbox("Uwzględnij wykresy", value=True)

            if st.button("🔽 Pobierz dane", use_container_width=True, type="primary"):
                # Symulacja eksportu
                with st.spinner("Przygotowywanie eksportu..."):
                    import time
                    time.sleep(2)
                st.success(f"Dane wyeksportowane do formatu {export_format}!")

        with col2:
            st.markdown("#### 📋 Automatyczne raporty")

            st.checkbox("Dzienny raport email", value=False)
            st.checkbox("Tygodniowy raport PDF", value=False)
            st.checkbox("Alerty o błędach", value=True)

            st.time_input("Godzina wysyłki", value=None)
            st.text_input("Email odbiorcy", placeholder="admin@example.com")

            if st.button("💾 Zapisz ustawienia", use_container_width=True):
                st.success("Ustawienia automatycznych raportów zapisane!")

    # Informacja na dole strony
    st.markdown("---")
    st.info("💡 **Wskazówka:** Użyj filtrów w pasku bocznym, aby dostosować wyświetlane dane do swoich potrzeb.")
