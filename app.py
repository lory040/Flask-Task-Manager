from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    when = db.Column(db.String(100), nullable=False)  # Aici salvăm timpul ales de tine


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        task_when = request.form['when']

        new_task = Todo(content=task_content, when=task_when)
        db.session.add(new_task)
        db.session.commit()
        return redirect('/')

    tasks = Todo.query.all()
    return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)