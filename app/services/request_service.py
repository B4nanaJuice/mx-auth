# Imports
from flask import url_for
import logging
import re

from config.settings import config

logger = logging.getLogger(__name__)

class RequestService:

    # Verify url (protection)
    @staticmethod
    def verify_url(url: str) -> str:
        default_url: str = url_for('auth.login')
        return url