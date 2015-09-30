# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect, url_for, make_response, request, flash, jsonify
from flask.ext.login import login_required, current_user

from ..extensions import db
from ..decorators import admin_required

from ..user.models import User, Event, Project, Category
from .forms import UserForm, EventForm, ProjectForm, CategoryForm

import json

blueprint = Blueprint('admin', __name__, url_prefix='/admin')


@blueprint.route('/')
@login_required
@admin_required
def index():
    users = User.query.all()
    return render_template('admin/index.html', users=users, active='index')


@blueprint.route('/users')
@login_required
@admin_required
def users():
    users = User.query.all()
    return render_template('admin/users.html', users=users, active='users')


@blueprint.route('/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def user(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    form = UserForm(obj=user, next=request.args.get('next'))

    if form.validate_on_submit():
        originalhash = user.password
        form.populate_obj(user)
        if form.password.data:
            user.set_password(form.password.data)
        else:
            user.password = originalhash
        db.session.add(user)
        db.session.commit()

        flash('User updated.', 'success')

    return render_template('admin/user.html', user=user, form=form)

@blueprint.route('/user/new', methods=['GET', 'POST'])
@login_required
@admin_required
def user_new():
    user = User()
    form = UserForm(obj=user, next=request.args.get('next'))

    if form.validate_on_submit():
        form.populate_obj(user)

        db.session.add(user)
        db.session.commit()

        flash('User added.', 'success')

    return render_template('admin/usernew.html', form=form)

##############
##############
##############

@blueprint.route('/events')
@login_required
@admin_required
def events():
    events = Event.query.all()
    return render_template('admin/events.html', events=events, active='events')


@blueprint.route('/event/<int:event_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def event(event_id):
    event = Event.query.filter_by(id=event_id).first_or_404()
    form = EventForm(obj=event, next=request.args.get('next'))

    if form.validate_on_submit():
        form.populate_obj(event)

        db.session.add(event)
        db.session.commit()

        flash('Event updated.', 'success')

    return render_template('admin/event.html', event=event, form=form)

@blueprint.route('/event/new', methods=['GET', 'POST'])
@login_required
@admin_required
def event_new():
    event = Event()
    form = EventForm(obj=event, next=request.args.get('next'))

    if form.validate_on_submit():
        form.populate_obj(event)

        db.session.add(event)
        db.session.commit()

        flash('Event added.', 'success')

    return render_template('admin/eventnew.html', form=form)

##############
##############
##############


@blueprint.route('/projects')
@login_required
@admin_required
def projects():
    projects = Project.query.all()
    return render_template('admin/projects.html', projects=projects, active='projects')


@blueprint.route('/project/<int:project_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def project(project_id):
    project = Project.query.filter_by(id=project_id).first_or_404()
    form = ProjectForm(obj=project, next=request.args.get('next'))
    form.user_id.choices = [(e.id, "%s (%s)" % (e.username, e.teamname)) for e in User.query.order_by('username')]
    form.event_id.choices = [(e.id, e.name) for e in Event.query.order_by('name')]
    form.category_id.choices = [(c.id, c.name) for c in project.categories_all()]

    if form.validate_on_submit():
        form.populate_obj(project)

        db.session.add(project)
        db.session.commit()

        flash('Project updated.', 'success')

    return render_template('admin/project.html', project=project, form=form)

@blueprint.route('/project/new', methods=['GET', 'POST'])
@login_required
@admin_required
def project_new():
    project = Project()
    form = ProjectForm(obj=project, next=request.args.get('next'))
    form.user_id.choices = [(e.id, "%s (%s)" % (e.username, e.teamname)) for e in User.query.order_by('username')]
    form.event_id.choices = [(e.id, e.name) for e in Event.query.order_by('name')]
    form.category_id.choices = [(c.id, c.name) for c in project.categories_all()]

    if form.validate_on_submit():
        form.populate_obj(project)

        db.session.add(project)
        db.session.commit()

        flash('Project added.', 'success')

    return render_template('admin/projectnew.html', form=form)

##############
##############
##############

@blueprint.route('/categories')
@login_required
@admin_required
def categories():
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories, active='categories')


@blueprint.route('/category/<int:category_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def category(category_id):
    category = Category.query.filter_by(id=category_id).first_or_404()
    form = CategoryForm(obj=category, next=request.args.get('next'))
    form.event_id.choices = [(e.id, e.name) for e in Event.query.order_by('name')]
    form.event_id.choices.insert(0, (-1, ''))

    if form.validate_on_submit():
        form.populate_obj(category)
        if category.event_id == -1: category.event_id = None
        if category.promote_id == -1: category.promote_id = None

        db.session.add(category)
        db.session.commit()

        flash('Category updated.', 'success')

    return render_template('admin/category.html', category=category, form=form)

@blueprint.route('/category/new', methods=['GET', 'POST'])
@login_required
@admin_required
def category_new():
    category = Category()
    form = CategoryForm(obj=category, next=request.args.get('next'))
    form.event_id.choices = [(e.id, e.name) for e in Event.query.order_by('name')]
    form.event_id.choices.insert(0, (-1, ''))

    if form.validate_on_submit():
        form.populate_obj(category)
        if category.event_id == -1: category.event_id = None
        if category.promote_id == -1: category.promote_id = None

        db.session.add(category)
        db.session.commit()

        flash('Category added.', 'success')

    return render_template('admin/categorynew.html', form=form)
