"""
Testy dla modułów stron
"""
import pytest
from unittest.mock import patch, MagicMock
import streamlit as st


class TestPagesModules:
    """Testy dla modułów stron"""

    @patch('streamlit.title')
    @patch('streamlit.form')
    @patch('src.config.Config.get_debug')
    def test_login_page_import(self, mock_debug, mock_form, mock_title):
        """Test importu strony logowania"""
        mock_debug.return_value = True
        mock_form.return_value.__enter__ = MagicMock()
        mock_form.return_value.__exit__ = MagicMock()

        # Test importu
        from pages.login import show_login_page
        assert callable(show_login_page)

    @patch('streamlit.header')
    @patch('streamlit.write')
    def test_dashboard_page_import(self, mock_write, mock_header):
        """Test importu strony dashboard"""
        from pages.dashboard import show_dashboard_page
        assert callable(show_dashboard_page)

    @patch('streamlit.header')
    @patch('streamlit.write')
    def test_data_page_import(self, mock_write, mock_header):
        """Test importu strony danych"""
        from pages.data import show_data_page
        assert callable(show_data_page)

    @patch('streamlit.header')
    @patch('streamlit.write')
    def test_settings_page_import(self, mock_write, mock_header):
        """Test importu strony ustawień"""
        from pages.settings import show_settings_page
        assert callable(show_settings_page)

    def test_pages_package_structure(self):
        """Test struktury pakietu pages"""
        import pages
        assert hasattr(pages, '__init__')

        # Test czy wszystkie moduły są dostępne
        import pages.login
        import pages.dashboard
        import pages.data
        import pages.settings

        assert hasattr(pages.login, 'show_login_page')
        assert hasattr(pages.dashboard, 'show_dashboard_page')
        assert hasattr(pages.data, 'show_data_page')
        assert hasattr(pages.settings, 'show_settings_page')
