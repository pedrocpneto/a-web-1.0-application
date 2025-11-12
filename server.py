from flask import Flask, redirect, request, render_template

app = Flask(__name__)


class Contact:
    _db = []
    _id_counter = 0

    def __init__(self):
        self._id = None
        self._first = None
        self._last = None
        self._email = None

    @property
    def id(self):
        return self._id

    @property
    def first(self):
        return self._first

    @first.setter
    def first(self, value):
        self._first = value

    @property
    def last(self):
        return self._last

    @last.setter
    def last(self, value):
        self._last = value

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        self._phone = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @staticmethod
    def all():
        return Contact._db

    @staticmethod
    def search(search):
        return filter(
            lambda c: search in " ".join([c.first, c.last, c.phone, c.email]),
            Contact._db,
        )

    @staticmethod
    def add(contact):
        Contact._id_counter += 1
        contact._id = Contact._id_counter
        Contact._db.append(contact)


c1 = Contact()
c1.first = "Paul"
c1.last = "James"
c1.phone = "+55 11 99999 9999"
c1.email = "paul.james43@gmail.com"
Contact.add(c1)


@app.route("/")
def index():
    return redirect("/contacts")


@app.route("/contacts")
def contacts():
    search = request.args.get("q")
    if search is not None:
        contacts_set = Contact.search(search)
    else:
        contacts_set = Contact.all()
    return render_template("index.html", contacts=contacts_set)


@app.route("/contacts/new", methods=["GET"])
def contacts_new_get():
    return render_template("new.html", contact=Contact())
