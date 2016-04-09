# -*- coding: utf-8 -*
from flask import render_template, redirect, request, url_for, flash, current_app
from flask.ext.login import login_user, logout_user, login_required, \
    current_user
from .. import db
from ..models import Material
from . import material
from datetime import datetime
from .forms import MaterialForm, EditMaterialForm


@material.route('/show_material/<int:id>', methods=['GET', 'POST'])
def show_material(id):
    material = Material.query.filter_by(id=id).first_or_404()
    return render_template('material/show.html', material=material)

    
@material.route('/materials', methods=['GET', 'POST'])
def materials():
    page = request.args.get('page', 1, type=int)
    pagination = Material.query.order_by(Material.timestamp.desc()).paginate(
        page, per_page=current_app.config['INDEX_MATERIALS_PER_PAGE'],
        error_out=False)
    materials = pagination.items
    return render_template('material/materials.html', materials=materials,
                           pagination=pagination)


"""
@material.route('/add', methods=['GET', 'POST'])
总是无法正常工作，因为 material 对象本身有 add 属性或者方法
"""
@material.route('/add_material', methods=['GET', 'POST'])
@login_required
def add_material():
    form = MaterialForm()
    if form.validate_on_submit():
        material = Material(contents=form.body.data,
                      title = form.title.data)
        db.session.add(material)
        db.session.commit()
        """ only insert data to sql table can trigger the action to generate an unique ID"""
        id = Material.query.order_by(Material.timestamp.desc()).first().id
        return redirect(url_for('material.show_material', id=id))
    return render_template("material/add.html", form=form)

@material.route('/edit_material/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_material(id):
    material = Material.query.filter_by(id=id).first_or_404()
    form = EditMaterialForm()

    if form.validate_on_submit():
        material.contents=form.body.data
        material.lastupdate_timestamp = datetime.utcnow()        
        db.session.add(material)
        db.session.commit()
        return redirect(url_for('material.show_material', id=material.id))
    
    form.body.data = material.contents
    
    return render_template("material/edit.html", form=form)

