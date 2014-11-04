__author__ = 'yawen'

from flask import render_template

from . import es, admin


@admin.route('/admin')
def admin_page():
    return render_template('admin.html')