from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



# flask can be used for webapp
# initialization by variable app
app=Flask(__name__)

# SQl Alchemy initialization
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

# defining db schema through class
class Todo(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(500), nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/', methods=['GET','POST'])
def hello_world():
    if request.method=="POST":
        title=request.form['title']
        todo=Todo(title=title)
        db.session.add(todo) # to add new title
        db.session.commit() # to commit the change
    allTodo=Todo.query.all()
    # print(allTodo)
    return render_template("index.html",allTodo=allTodo)
    # return "Hello, World!"

@app.route('/show')
def products():
    allTodo=Todo.query.all()
    print(allTodo)
    return "this is a new product page"

@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title=request.form['title']
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo=Todo.query.filter_by(sno=sno).first()
    return render_template("update.html", todo=todo)

@app.route('/delete/<int:sno>') 
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route('/about')
def about():
    return render_template('about.html')



if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

