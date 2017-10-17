"""Views for self-user management

TODO : before we can make it here, we need to implement permissions
"""
import logging
from flask_login import login_required, current_user
from flask import Blueprint, request, flash, render_template

from extrapypi.extensions import db
from extrapypi.forms.user import UserForm

log = logging.getLogger("extrapypi")


blueprint = Blueprint('user', __name__, url_prefix='/user')


@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def update_user():
    """Update current logged user
    """
    user = current_user
    form = UserForm(request.form, obj=user)
    del form.role

    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        flash("Informations updated")
    return render_template("dashboard/user_detail.html", form=form, user=current_user)


@blueprint.route('/password', methods=['GET', 'POST'])
def update_password():
    pass
