from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'



db = SQLAlchemy(app)

class Todo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	task = db.Column(db.String(200), nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return f"Todo('{self.task}', '{self.date_created}')"

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/tasks', methods=['POST', 'GET'])
def tasks():
	if request.method == 'POST':
		get_task_content = request.form['task']
		add_task_to_db = Todo(task=get_task_content)
		db.session.add(add_task_to_db)
		db.session.commit()
		return redirect('tasks')

	else:
		tasks = Todo.query.all()
		return render_template('tasks.html', tasks=tasks)

@app.route('/tasks/delete/<int:id>', methods=['POST', 'GET'])
def delete(id):
	task_obj = Todo.query.get_or_404(id)
	db.session.delete(task_obj)
	db.session.commit()
	return redirect(url_for('tasks'))

@app.route('/tasks/update/<int:id>', methods=['POST', 'GET'])
def update(id):
	task_obj = Todo.query.get_or_404(id)
	if request.method == 'POST':
		task_obj.task = request.form['task']
		db.session.commit()
		return redirect(url_for('tasks'))	
	else:
		return render_template('update_task.html', task=task_obj)


if __name__ == '__main__':
	app.run(debug=True)