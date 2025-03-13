from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
import os


app = Flask(__name__)

# all_books = []

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")

db.init_app(app)

class Books(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    #Read All Records
    result = db.session.execute(db.select(Books).order_by(Books.title))
    all_books = result.scalars()

    # return render_template("index.html", books=all_books)
    return render_template("index.html", books=all_books)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":

        # new_book = {
        #     "title": request.form['title'],
        #     "author": request.form['author'],
        #     "rating": request.form['rating'],
        # }
        # all_books.append(new_book)

        new_book = Books(title=request.form['title'], author=request.form['author'], rating=request.form['rating'])
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template("add.html")

@app.route("/edit/<int:book_id>", methods=["GET", "POST"])
def edit_rating(book_id):
    needed_book = db.get_or_404(Books, book_id)
    if request.method == "POST":
        needed_book.rating = float(request.form['new-rating'])
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", book=needed_book)


@app.route("/delete")
def delete():
    book_id = request.args.get('book_id') #Getting hold of the arguments sent from the html files (in url_for)
                                            # without needing to add them to the route and the function as an input
    book_to_delete = db.get_or_404(Books, book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)