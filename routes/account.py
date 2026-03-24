# Imports
from flask import Blueprint

from models.user import User
from extensions.login_manager import login_required

# Create Blueprint
page: Blueprint = Blueprint(name = 'account', 
                            import_name = __name__, 
                            template_folder = 'templates',
                            url_prefix = '',
                            static_folder = 'static')

@page.route('/me', methods = ['GET'])
@login_required
def me(current_user: User):
    return f'Welcome {current_user.name} !'