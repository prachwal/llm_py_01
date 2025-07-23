"""
Testy dla modułu konfiguracji
"""
import pytest
import os
from unittest.mock import patch, mock_open
from src.config import Config


class TestConfig:
    """Testy klasy Config"""
    
    def test_default_values(self):
        """Test domyślnych wartości konfiguracji"""
        with patch.dict(os.environ, {}, clear=True):
            config = Config()
            assert config.APP_NAME == 'Streamlit App'
            assert config.DEBUG is False
            assert config.HOST == 'localhost'
            assert config.PORT == 8501
    
    def test_environment_variables(self):
        """Test odczytu zmiennych środowiskowych"""
        env_vars = {
            'APP_NAME': 'Test App',
            'DEBUG': 'true',
            'HOST': '0.0.0.0',
            'PORT': '8080',
            'SECRET_KEY': 'test-secret',
            'SESSION_TIMEOUT': '7200'
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            config = Config()
            assert config.APP_NAME == 'Test App'
            assert config.DEBUG is True
            assert config.HOST == '0.0.0.0'
            assert config.PORT == 8080
            assert config.SECRET_KEY == 'test-secret'
            assert config.SESSION_TIMEOUT == 7200
    
    def test_debug_flag_parsing(self):
        """Test parsowania flagi DEBUG"""
        test_cases = [
            ('true', True),
            ('True', True),
            ('TRUE', True),
            ('false', False),
            ('False', False),
            ('', False),
            ('anything', False)
        ]
        
        for debug_value, expected in test_cases:
            with patch.dict(os.environ, {'DEBUG': debug_value}, clear=True):
                config = Config()
                assert config.DEBUG is expected
    
    def test_validate_config_success(self):
        """Test pomyślnej walidacji konfiguracji"""
        env_vars = {
            'SECRET_KEY': 'valid-secret-key',
            'ADMIN_PASSWORD_HASH': 'valid-hash'
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            config = Config()
            assert config.validate_config() is True
    
    def test_validate_config_missing_secret_key(self):
        """Test walidacji z brakującym SECRET_KEY"""
        env_vars = {
            'ADMIN_PASSWORD_HASH': 'valid-hash'
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            config = Config()
            with pytest.raises(ValueError) as exc_info:
                config.validate_config()
            assert "SECRET_KEY" in str(exc_info.value)
    
    def test_validate_config_default_secret_key(self):
        """Test walidacji z domyślnym SECRET_KEY"""
        env_vars = {
            'SECRET_KEY': 'default-secret-key',
            'ADMIN_PASSWORD_HASH': 'valid-hash'
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            config = Config()
            with pytest.raises(ValueError) as exc_info:
                config.validate_config()
            assert "SECRET_KEY" in str(exc_info.value)
    
    def test_validate_config_missing_password_hash(self):
        """Test walidacji z brakującym ADMIN_PASSWORD_HASH"""
        env_vars = {
            'SECRET_KEY': 'valid-secret-key'
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            config = Config()
            with pytest.raises(ValueError) as exc_info:
                config.validate_config()
            assert "ADMIN_PASSWORD_HASH" in str(exc_info.value)
    
    @patch('logging.basicConfig')
    @patch('logging.getLogger')
    def test_setup_logging(self, mock_get_logger, mock_basic_config):
        """Test konfiguracji systemu logowania"""
        mock_logger = mock_get_logger.return_value
        
        logger = Config.setup_logging()
        
        # Sprawdź czy basicConfig został wywołany
        mock_basic_config.assert_called_once()
        
        # Sprawdź parametry wywołania
        args, kwargs = mock_basic_config.call_args
        assert 'level' in kwargs
        assert 'format' in kwargs
        assert 'handlers' in kwargs
        
        # Sprawdź czy zwrócono logger
        assert logger == mock_logger
