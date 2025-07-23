"""
Serwis uwierzytelniania - obsługa logowania i sesji użytkowników
"""
import bcrypt
import streamlit as st
import time
import logging
from typing import Optional, Dict, Any
from .config import Config

logger = logging.getLogger(__name__)


class AuthService:
    """Serwis obsługi uwierzytelniania"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hashuje hasło używając bcrypt
        
        Args:
            password: Hasło do zahashowania
            
        Returns:
            Zahashowane hasło jako string
        """
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """
        Weryfikuje hasło względem hasha
        
        Args:
            password: Hasło do sprawdzenia
            hashed: Hash do porównania
            
        Returns:
            True jeśli hasło jest poprawne, False w przeciwnym razie
        """
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except Exception as e:
            logger.error(f"Błąd weryfikacji hasła: {e}")
            return False
    
    @staticmethod
    def authenticate_user(username: str, password: str) -> bool:
        """
        Uwierzytelnia użytkownika
        
        Args:
            username: Nazwa użytkownika
            password: Hasło
            
        Returns:
            True jeśli uwierzytelnienie się powiodło, False w przeciwnym razie
        """
        if username == Config.get_admin_user():
            if AuthService.verify_password(password, Config.get_admin_password_hash()):
                logger.info(f"Pomyślne logowanie użytkownika: {username}")
                return True
            else:
                logger.warning(f"Nieudana próba logowania użytkownika: {username}")
                return False
        
        logger.warning(f"Nieznany użytkownik: {username}")
        return False
    
    @staticmethod
    def login_user(username: str) -> None:
        """
        Loguje użytkownika - ustawia sesję
        
        Args:
            username: Nazwa użytkownika do zalogowania
        """
        st.session_state['authenticated'] = True
        st.session_state['username'] = username
        st.session_state['login_time'] = time.time()
        logger.info(f"Użytkownik {username} został zalogowany")
    
    @staticmethod
    def logout_user() -> None:
        """Wylogowuje użytkownika - czyści sesję"""
        username = st.session_state.get('username', 'Unknown')
        st.session_state['authenticated'] = False
        st.session_state['username'] = None
        st.session_state['login_time'] = None
        logger.info(f"Użytkownik {username} został wylogowany")
    
    @staticmethod
    def is_authenticated() -> bool:
        """
        Sprawdza czy użytkownik jest uwierzytelniony
        
        Returns:
            True jeśli użytkownik jest zalogowany, False w przeciwnym razie
        """
        if not st.session_state.get('authenticated', False):
            return False
        
        # Sprawdź timeout sesji
        login_time = st.session_state.get('login_time', 0)
        if time.time() - login_time > Config.get_session_timeout():
            AuthService.logout_user()
            return False
        
        return True
    
    @staticmethod
    def get_current_user() -> Optional[str]:
        """
        Zwraca nazwę aktualnie zalogowanego użytkownika
        
        Returns:
            Nazwa użytkownika lub None jeśli nikt nie jest zalogowany
        """
        if AuthService.is_authenticated():
            return st.session_state.get('username')
        return None
    
    @staticmethod
    def get_session_info() -> Dict[str, Any]:
        """
        Zwraca informacje o sesji
        
        Returns:
            Słownik z informacjami o sesji
        """
        if not AuthService.is_authenticated():
            return {}
        
        login_time = st.session_state.get('login_time', 0)
        session_duration = time.time() - login_time
        time_left = Config.get_session_timeout() - session_duration
        
        return {
            'username': st.session_state.get('username'),
            'login_time': login_time,
            'session_duration': session_duration,
            'time_left': max(0, time_left)
        }
