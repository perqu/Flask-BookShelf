from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, fields, marshal_with
import GoogleAPI

app = Flask(__name__)
app.secret_key = "615479af3de3482bdb6ed6c5f8f15457"
api = Api(app)

# SQLAlchemy Database Configuration With MySQL
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql://DBUSER:PASSWORD@pperenc.atthost24.pl/DBNAME"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# Creating model table for our Book database
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    authors = db.Column(db.String(100))
    published_date = db.Column(db.String(10))
    ISBN10 = db.Column(db.String(10))
    ISBN13 = db.Column(db.String(13))
    page_count = db.Column(db.Integer)
    preview_link = db.Column(db.String(100))
    language = db.Column(db.String(3))

    def __init__(
        self,
        title,
        authors,
        published_date,
        ISBN10,
        ISBN13,
        page_count,
        preview_link,
        language,
    ):

        self.title = title
        self.authors = authors
        self.published_date = published_date
        self.ISBN10 = ISBN10
        self.ISBN13 = ISBN13
        self.page_count = page_count
        self.preview_link = preview_link
        self.language = language

    def __repr__(self):
        return f"""Book(title: {self.title}, authors: {self.authors}, published_date: {self.published_date}, ISBN10: {self.ISBN10}, ISBN13: {self.ISBN13}, page_count: {self.page_count}, preview_link: {self.preview_link}, language: {self.language})"""


# Creating resource fields to serialize data
resource_fields = {
    "id": fields.Integer,
    "title": fields.String,
    "authors": fields.String,
    "published_date": fields.String,
    "ISBN10": fields.String,
    "ISBN13": fields.String,
    "page_count": fields.Integer,
    "preview_link": fields.String,
    "language": fields.String,
}

# Creating restapi to response with filtered data from DB
class restapi(Resource):
    @marshal_with(resource_fields)
    def get(self):
        phrase = request.args.get("phrase")
        results_by_title = Book.query.filter(
            Book.title.ilike(f"%{phrase}%")).all()
        results_by_authors = Book.query.filter(
            Book.authors.ilike(f"%{phrase}%")).all()
        results_by_language = Book.query.filter(
            Book.language.ilike(f"%{phrase}%")
        ).all()

        results = list(
            set(results_by_title + results_by_authors + results_by_language))

        return results

# Routes Below


api.add_resource(restapi, "/restapi")


@app.route("/")
def Index():
    all_data = Book.query.all()
    return render_template("index.html", books=all_data)


@app.route("/google", methods=["GET"])
def google():
    search = 'default'
    try:
        search = request.args.get("search")
        all_data = GoogleAPI.GetBookData(search)
        return render_template("import.html", books=all_data, search=search)
    except:
        all_data = None
        return render_template("import.html", books=all_data, search=search)


@app.route("/insert", methods=["POST"])
def insert():

    if request.method == "POST":

        title = request.form["title"]
        authors = request.form["authors"]
        published_date = request.form["published_date"]
        ISBN10 = request.form["ISBN10"]
        ISBN13 = request.form["ISBN13"]
        page_count = request.form["page_count"]
        preview_link = request.form["preview_link"]
        language = request.form["language"]

        my_data = Book(
            title,
            authors,
            published_date,
            ISBN10,
            ISBN13,
            page_count,
            preview_link,
            language,
        )
        db.session.add(my_data)
        db.session.commit()

        flash("Book Inserted Successfully")

        return redirect(url_for("Index"))


@app.route("/update", methods=["GET", "POST"])
def update():

    if request.method == "POST":
        my_data = Book.query.get(request.form.get("id"))

        my_data.title = request.form["title"]
        my_data.authors = request.form["authors"]
        my_data.published_date = request.form["published_date"]
        my_data.ISBN10 = request.form["ISBN10"]
        my_data.ISBN13 = request.form["ISBN13"]
        my_data.page_count = request.form["page_count"]
        my_data.preview_link = request.form["preview_link"]
        my_data.language = request.form["language"]

        db.session.commit()
        flash("Book Updated Successfully")

        return redirect(url_for("Index"))


@app.route("/delete/<id>/", methods=["GET", "POST"])
def delete(id):
    my_data = Book.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Book Deleted Successfully")

    return redirect(url_for("Index"))


@app.route("/import/", methods=["GET", "POST"])
def import_from_google():
    search = request.args.get("search")

    title = request.args.get("title")
    authors = request.args.get("authors")
    published_date = request.args.get("published_date")
    ISBN10 = request.args.get("ISBN10")
    ISBN13 = request.args.get("ISBN13")
    page_count = request.args.get("page_count")
    preview_link = request.args.get("preview_link")
    language = request.args.get("language")

    my_data = Book(
        title,
        authors,
        published_date,
        ISBN10,
        ISBN13,
        page_count,
        preview_link,
        language,
    )
    db.session.add(my_data)
    db.session.commit()

    flash("Book Inserted Successfully")

    return redirect(url_for("google", search=search))


if __name__ == "__main__":
    app.run(debug=True)
