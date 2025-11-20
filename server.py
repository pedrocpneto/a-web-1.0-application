from flask import Flask, flash, redirect, request, render_template

app = Flask(__name__)
app.secret_key = "pedrocpneto"


class Contact:
    _db = {}
    _id_counter = 0

    def __init__(self):
        self._id = None
        self._first = None
        self._last = None
        self._email = None
        self._errors = None

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

    @property
    def errors(self):
        return self._errors

    @errors.setter
    def errors(self, value):
        self._errors = value

    def save(self):
        if self._id is None:
            Contact._id_counter += 1
            self._id = Contact._id_counter
            Contact._db[str(self._id)] = self
        return True

    def delete(self):
        Contact._db.pop(str(self._id))

    @staticmethod
    def all():
        return Contact._db.values()

    @staticmethod
    def search(search):
        return filter(
            lambda c: search in " ".join([c.first, c.last, c.phone, c.email]),
            Contact._db.values(),
        )

    @staticmethod
    def find(contact_id):
        return Contact._db[contact_id]


c1 = Contact()
c1.first = "Paul"
c1.last = "James"
c1.phone = "+55 11 99999 9999"
c1.email = "paul.james43@gmail.com"
c1.save()


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


@app.route("/contacts/new", methods=["POST"])
def contacts_new():
    c = Contact()
    c.first = request.form["first"]
    c.last = request.form["last"]
    c.phone = request.form["phone"]
    c.email = request.form["email"]
    if c.save():
        flash("Created New Contact!")
        return redirect("/contacts")
    else:
        return render_template("new.html", contact=c)


@app.route("/contacts/<contact_id>")
def contacts_view(contact_id=0):
    contact = Contact.find(contact_id)
    return render_template("show.html", contact=contact)


@app.route("/contacts/<contact_id>/edit", methods=["GET"])
def contacts_edit(contact_id=0):
    contact = Contact.find(contact_id)
    return render_template("edit.html", contact=contact)


@app.route("/contacts/<contact_id>/edit", methods=["POST"])
def contacts_edit_post(contact_id=0):
    contact = Contact.find(contact_id)
    contact.first = request.form["first"]
    contact.last = request.form["last"]
    contact.phone = request.form["phone"]
    contact.email = request.form["email"]
    flash("Updated Contact!")
    return redirect("/contacts/" + str(contact_id))


@app.route("/contacts/<contact_id>/delete", methods=["POST"])
def contacts_delete(contact_id=0):
    contact = Contact.find(contact_id)
    contact.delete()
    flash("Deleted contact!")
    return redirect("/contacts")
