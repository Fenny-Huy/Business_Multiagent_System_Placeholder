# config/api_keys.py
import os
import json
import keyring
import logging
from typing import Optional, Dict, Any
from pathlib import Path
from cryptography.fernet import Fernet
import base64


def load_dotenv(env_file=".env"):
    """Load environment variables from .env file
    
    Args:
        env_file: Path to .env file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        if not os.path.exists(env_file):
            logging.info(f".env file not found at {env_file}")
            return False
        
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                    
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip().strip("'").strip('"')
        
        logging.info(f"Loaded environment variables from {env_file}")
        return True
    except Exception as e:
        logging.error(f"Failed to load .env file: {e}")
        return False


class APIKeyManager:
    """Secure API key management system with multiple storage options"""
    
    def __init__(self, use_keyring: bool = True, encryption_key: Optional[str] = None, load_env: bool = True):
        """Initialize API key manager
        
        Args:
            use_keyring: Whether to use system keyring for storage
            encryption_key: Optional encryption key for file-based storage
            load_env: Whether to try loading from .env file
        """
        self.use_keyring = use_keyring
        self.config_dir = Path("config")
        self.config_dir.mkdir(exist_ok=True)
        self.key_file = self.config_dir / ".api_keys.enc"
        
        # Try to load from .env file
        if load_env:
            # Try project root .env first, then config dir .env
            load_dotenv(".env") or load_dotenv("config/.env")
        
        # Initialize encryption
        if encryption_key:
            self.encryption_key = encryption_key.encode()
        else:
            self.encryption_key = self._get_or_create_encryption_key()
        
        self.cipher = Fernet(base64.urlsafe_b64encode(self.encryption_key.ljust(32)[:32]))
    
    def _get_or_create_encryption_key(self) -> bytes:
        """Get or create encryption key for file storage"""
        key_path = self.config_dir / ".enc_key"
        
        if key_path.exists():
            with open(key_path, 'rb') as f:
                return f.read()
        else:
            # Generate new key
            key = os.urandom(32)
            with open(key_path, 'wb') as f:
                f.write(key)
            # Set restrictive permissions
            os.chmod(key_path, 0o600)
            return key
    
    def get_api_key(self, service: str) -> Optional[str]:
        """Get API key for service
        
        Args:
            service: Service name
            
        Returns:
            API key if found, None otherwise
        """
        # Try environment variable first
        env_key = f"{service.upper()}_API_KEY"
        if env_key in os.environ:
            return os.environ[env_key]
        
        # Try keyring
        if self.use_keyring:
            try:
                key = keyring.get_password("langgraph_multiagent", service)
                if key:
                    return key
            except Exception as e:
                logging.warning(f"Failed to get key from keyring: {e}")
        
        return None
    
    def save_api_key(self, service: str, key: str) -> bool:
        """Save API key securely
        
        Args:
            service: Service name (e.g., 'gemini', 'openai')
            key: API key to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if self.use_keyring:
                keyring.set_password("langgraph_multiagent", service, key)
                logging.info(f"API key for {service} saved to system keyring")
                return True
        except Exception as e:
            logging.error(f"Failed to save API key: {e}")
            return False