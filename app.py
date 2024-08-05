from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///work_management.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    assignee = db.Column(db.String(150), nullable=False)

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=150)])
    description = TextAreaField('Description', validators=[DataRequired()])
    status = SelectField('Status', choices=[('To Do', 'To Do'), ('In Progress', 'In Progress'), ('Done', 'Done')], validators=[DataRequired()])
    assignee = StringField('Assignee', validators=[DataRequired(), Length(min=2, max=150)])
    submit = SubmitField('Add Task')

db.create_all()

@app.route('/')
def home():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        new_task = Task(
            title=form.title.data,
            description=form.description.data,
            status=form.status.data,
            assignee=form.assignee.data
        )
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('add_task.html', form=form)

@app.route('/update_task/<int:id>', methods=['GET', 'POST'])
def update_task(id):
    task = Task.query.get_or_404(id)
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.status = form.status.data
        task.assignee = form.assignee.data
        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('update_task.html', form=form, task=task)

@app.route('/delete_task/<int:id>', methods=['POST'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
