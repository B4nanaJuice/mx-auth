# Imports
from flask import Flask, Blueprint, render_template, flash, request, redirect, url_for, make_response, Response, jsonify

from app.decorators import access_token_required
from app.data.models.user import User
from app.services.oauth_service import OAuthService, OAuthException

# Create blueprint
bp: Blueprint = Blueprint('oauth', 'oauth', url_prefix = '/oauth')

@bp.get('/authorize')
@access_token_required
def authorize(user: User):
    
    oauth_client_id: str = request.args.get('client', None)
    if not oauth_client_id:
        return redirect(url_for('auth.login'))
    
    try:
        auth_code = OAuthService.generate_authorization_code(
            user_id = user.id,
            oauth_client_id = oauth_client_id
        )

        callback: str = request.args.get('callback', None)
        return redirect(f'{callback}?code={auth_code.code}' if callback else url_for('auth.login'))

    except OAuthException as e:
        flash (e.message, 'error')
        return redirect(url_for('auth.login'))
    
@bp.post('/token')
def exchange_token():
    
    code: str = request.form.get('code', None)
    if not code:
        return jsonify({'message': 'You must provide an authorization code.'}), 404
    
    try:
        token_pair = OAuthService.exchange_authorization_code(code = code)

        return jsonify({
            'access_token': token_pair.access_token,
            'refresh_token': token_pair.refresh_token
        }), 200
    
    except OAuthException as e:
        return jsonify({'message': e.message}), 404

