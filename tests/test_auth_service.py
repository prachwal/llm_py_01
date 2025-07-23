"""
Testy dla serwisu uwierzytelniania
"""
import pytest
import bcrypt
import time
from unittest.mock import patch, MagicMock
from src.auth_service import AuthService
from src.config import Config


class TestAuthService:
    """Testy klasy AuthService"""
    
    def test_hash_password(self):
        """Test hashowania hasła"""
        password = "test123"
        hashed = AuthService.hash_password(password)
        
        assert isinstance(hashed, str)
        assert hashed != password
        assert len(hashed) > 50  # bcrypt hash ma określoną długość
    
    def test_verify_password_correct(self):
        """Test weryfikacji poprawnego hasła"""
        password = "test123"
        hashed = AuthService.hash_password(password)
        
        assert AuthService.verify_password(password, hashed) is True
    
    def test_verify_password_incorrect(self):
        """Test weryfikacji niepoprawnego hasła"""
        password = "test123"
        wrong_password = "wrong123"
        hashed = AuthService.hash_password(password)
        
        assert AuthService.verify_password(wrong_password, hashed) is False
    
    def test_verify_password_invalid_hash(self):
        """Test weryfikacji z nieprawidłowym hashem"""
        password = "test123"
        invalid_hash = "invalid_hash"
        
        assert AuthService.verify_password(password, invalid_hash) is False
    
    @patch('src.auth_service.Config')
    def test_authenticate_user_success(self, mock_config):
        """Test pomyślnego uwierzytelnienia użytkownika"""
        mock_config.get_admin_user.return_value = "admin"
        mock_config.get_admin_password_hash.return_value = AuthService.hash_password("admin123")
        
        assert AuthService.authenticate_user("admin", "admin123") is True
    
    @patch('src.auth_service.Config')
    def test_authenticate_user_wrong_password(self, mock_config):
        """Test uwierzytelnienia z niepoprawnym hasłem"""
        mock_config.get_admin_user.return_value = "admin"
        mock_config.get_admin_password_hash.return_value = AuthService.hash_password("admin123")
        
        assert AuthService.authenticate_user("admin", "wrongpass") is False
    
    @patch('src.auth_service.Config')
    def test_authenticate_user_wrong_username(self, mock_config):
        """Test uwierzytelnienia z niepoprawną nazwą użytkownika"""
        mock_config.get_admin_user.return_value = "admin"
        mock_config.get_admin_password_hash.return_value = AuthService.hash_password("admin123")
        
        assert AuthService.authenticate_user("wronguser", "admin123") is False
    
    @patch('src.auth_service.st')
    @patch('src.auth_service.time')
    def test_login_user(self, mock_time, mock_st):
        """Test logowania użytkownika"""
        mock_time.time.return_value = 1000
        mock_st.session_state = {}
        
        AuthService.login_user("testuser")
        
        assert mock_st.session_state['authenticated'] is True
        assert mock_st.session_state['username'] == "testuser"
        assert mock_st.session_state['login_time'] == 1000
    
    @patch('src.auth_service.st')
    def test_logout_user(self, mock_st):
        """Test wylogowania użytkownika"""
        mock_st.session_state = {
            'authenticated': True,
            'username': 'testuser',
            'login_time': 1000
        }
        
        AuthService.logout_user()
        
        assert mock_st.session_state['authenticated'] is False
        assert mock_st.session_state['username'] is None
        assert mock_st.session_state['login_time'] is None
    
    @patch('src.auth_service.st')
    def test_is_authenticated_true(self, mock_st):
        """Test sprawdzenia uwierzytelnienia - pozytywny"""
        mock_st.session_state = {
            'authenticated': True,
            'login_time': time.time() - 100  # 100 sekund temu
        }
        
        with patch('src.auth_service.Config.get_session_timeout', return_value=3600):
            assert AuthService.is_authenticated() is True
    
    @patch('src.auth_service.st')
    def test_is_authenticated_false_not_logged(self, mock_st):
        """Test sprawdzenia uwierzytelnienia - nie zalogowany"""
        mock_st.session_state = {'authenticated': False}
        
        assert AuthService.is_authenticated() is False
    
    @patch('src.auth_service.st')
    @patch('src.auth_service.time')
    @patch('src.auth_service.AuthService.logout_user')
    def test_is_authenticated_timeout(self, mock_logout, mock_time, mock_st):
        """Test sprawdzenia uwierzytelnienia - timeout sesji"""
        mock_time.time.return_value = 5000
        mock_st.session_state = {
            'authenticated': True,
            'login_time': 1000  # 4000 sekund temu
        }
        
        with patch('src.auth_service.Config.get_session_timeout', return_value=3600):  # 1 godzina
            assert AuthService.is_authenticated() is False
            mock_logout.assert_called_once()
    
    @patch('src.auth_service.st')
    def test_get_current_user_authenticated(self, mock_st):
        """Test pobierania aktualnego użytkownika - zalogowany"""
        mock_st.session_state = {
            'authenticated': True,
            'username': 'testuser',
            'login_time': time.time() - 100
        }
        
        with patch('src.auth_service.Config.get_session_timeout', return_value=3600):
            assert AuthService.get_current_user() == 'testuser'
    
    @patch('src.auth_service.st')
    def test_get_current_user_not_authenticated(self, mock_st):
        """Test pobierania aktualnego użytkownika - nie zalogowany"""
        mock_st.session_state = {'authenticated': False}
        
        assert AuthService.get_current_user() is None
    
    @patch('src.auth_service.st')
    @patch('src.auth_service.time')
    def test_get_session_info(self, mock_time, mock_st):
        """Test pobierania informacji o sesji"""
        mock_time.time.return_value = 2000
        mock_st.session_state = {
            'authenticated': True,
            'username': 'testuser',
            'login_time': 1000
        }
        
        with patch('src.auth_service.Config.get_session_timeout', return_value=3600):
            session_info = AuthService.get_session_info()
            
            assert session_info['username'] == 'testuser'
            assert session_info['login_time'] == 1000
            assert session_info['session_duration'] == 1000
            assert session_info['time_left'] == 2600
    
    @patch('src.auth_service.st')
    def test_get_session_info_not_authenticated(self, mock_st):
        """Test pobierania informacji o sesji - nie zalogowany"""
        mock_st.session_state = {'authenticated': False}
        
        session_info = AuthService.get_session_info()
        assert session_info == {}
