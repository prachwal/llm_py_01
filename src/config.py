"""
Konfiguracja aplikacji - centralne zarządzanie ustawieniami z pliku .env
"""
import os
from dotenv import load_dotenv
import logging

# Załaduj zmienne środowiskowe z pliku .env
load_dotenv()


class Config:
    """Klasa konfiguracyjna aplikacji"""
    
    @classmethod
    def get_app_name(cls):
        return os.getenv('APP_NAME', 'Streamlit App')
    
    @classmethod
    def get_debug(cls):
        return os.getenv('DEBUG', 'False').lower() == 'true'
    
    @classmethod
    def get_host(cls):
        return os.getenv('HOST', 'localhost')
    
    @classmethod
    def get_port(cls):
        return int(os.getenv('PORT', 8501))
    
    @classmethod
    def get_secret_key(cls):
        return os.getenv('SECRET_KEY', 'default-secret-key')
    
    @classmethod
    def get_session_timeout(cls):
        return int(os.getenv('SESSION_TIMEOUT', 3600))
    
    @classmethod
    def get_admin_user(cls):
        return os.getenv('ADMIN_USER', 'admin')
    
    @classmethod
    def get_admin_password_hash(cls):
        return os.getenv('ADMIN_PASSWORD_HASH', '')
    
    @classmethod
    def get_log_level(cls):
        return os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def get_log_file(cls):
        return os.getenv('LOG_FILE', 'app.log')
    
    # Właściwości dla kompatybilności wstecznej
    @property
    def APP_NAME(self):
        return self.get_app_name()
    
    @property
    def DEBUG(self):
        return self.get_debug()
    
    @property
    def HOST(self):
        return self.get_host()
    
    @property
    def PORT(self):
        return self.get_port()
    
    @property
    def SECRET_KEY(self):
        return self.get_secret_key()
    
    @property
    def SESSION_TIMEOUT(self):
        return self.get_session_timeout()
    
    @property
    def ADMIN_USER(self):
        return self.get_admin_user()
    
    @property
    def ADMIN_PASSWORD_HASH(self):
        return self.get_admin_password_hash()
    
    @property
    def LOG_LEVEL(self):
        return self.get_log_level()
    
    @property
    def LOG_FILE(self):
        return self.get_log_file()
    
    @classmethod
    def setup_logging(cls):
        """Konfiguracja systemu logowania"""
        logging.basicConfig(
            level=getattr(logging, cls.get_log_level()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(cls.get_log_file()),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    @classmethod
    def validate_config(cls):
        """Walidacja konfiguracji aplikacji"""
        errors = []
        
        secret_key = cls.get_secret_key()
        if not secret_key or secret_key == 'default-secret-key':
            errors.append("SECRET_KEY nie jest ustawiony lub używa wartości domyślnej")
        
        admin_password_hash = cls.get_admin_password_hash()
        if not admin_password_hash:
            errors.append("ADMIN_PASSWORD_HASH nie jest ustawiony")
        
        if errors:
            raise ValueError(f"Błędy konfiguracji: {'; '.join(errors)}")
        
        return True
