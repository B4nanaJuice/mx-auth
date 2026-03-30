# Imports
from flask import request, redirect, url_for, flash
from functools import wraps
import jwt

from config.settings import config
from app.models.user import User
from app.services.auth_service import AuthService



