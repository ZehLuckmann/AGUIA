#coding:utf-8
from aguia import db
import time

class Company(db.Model):
    __tablename__ = "company"

    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    email = db.Column(db.String)
    category = db.Column(db.String)

    def __init__(self, name = "", city = "", state = "", email = "", category= "", id = -1):
        if id != -1:
            self.load(id)
        else:
            self.name   = name
            self.city = city
            self.state = state
            self.email  = email
            self.category = category

    def save(self):
        db.session.add(self)
        db.session.commit()

    def load(self, id):
        company = User.query.filter_by(_id=id).first()
        if company:
            self._id = company._id
            self.name = company.name
            self.city = company.city
            self.state = company.state
            self.email  = company.email
            self.category = company.category

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class User(db.Model):
    __tablename__ = "user"

    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    email = db.Column(db.String)

    def __init__(self, username="", password="", email="", id = -1):
        if id != -1:
            self.load(id)
        else:
            self.username = username
            self.password = password
            self.email = email

    def save(self):
        if self.username and self.password and self.email:
            db.session.add(self)
            db.session.commit()

    def login(self):
        user = User.query.filter_by(username = self.username, password = self.password).first()
        if user:
            self._id = user._id
            self.email = user.email
            return True
        return False

    def load(self, id):
        user = User.query.filter_by(_id=id).first()
        if user:
            self._id = user._id
            self.username = user.username
            self.password = user.password
            self.email = user.email

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Bidding(db.Model):

    __tablename__ = "bidding"

    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    summary = db.Column(db.String)
    link_notice = db.Column(db.String)

    def __init__(self, title ="", summary="", link_notice="", id =-1):
        if id != -1:
            self.load(id)
        else:
            self.title = title
            self.summary = summary
            self.link_notice = link_notice

    def save(self):
        db.session.add(self)
        db.session.commit()

    def load(self, id):
        bidding = User.query.filter_by(_id=id).first()
        if bidding:
            self._id = bidding._id
            self.title = bidding.title
            self.summary = bidding.summary
            self.link_notice = bidding.link_notice

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Email(db.Model):

    __tablename__ = "email"

    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender = db.Column(db.String)
    subject = db.Column(db.String)
    text = db.Column(db.String)
    id_bidding = db.Column(db.Integer)

    def __init__(self, bidding = None, user = None, id=-1):
        if id != -1:
            self.load(id)
        else:
            self.sender = user.email
            self.id_bidding = bidding._id
            self.write_email(bidding)

    def write_email(self, bidding):
        self.subject = bidding.title
        self.text = "Senhor(a) Empresário(a),\n\n"
        self.text = self.text + "No Cumprimento do nosso objetivo institucional, informamos a V.Sa. a publicação do edital, pela Prefeitura Municipal de São José:\n\n"
        self.text = self.text + "Título:{0}\n\n".format(bidding.title)
        self.text = self.text + "Objeto:{0}\n\n".format(bidding.summary)
        self.text = self.text + "Para mais informações acesse o link: {0}\n\n".format(bidding.link_notice)
        self.text = self.text + "Desde já agradecemos a atenção, renovando votos de elevada estima e consideração\n"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def load(self, id):
        email = User.query.filter_by(_id=id).first()
        if email:
            self._id = email._id
            self.sender = email.sender
            self.subject = email.subject
            self.text = email.text
            self.id_bidding = email.id_bidding

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class EmailHistory(db.Model):

    __tablename__ = "email_history"

    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_email = db.Column(db.Integer)
    id_company = db.Column(db.Integer)
    date = db.Column(db.String)
    time = db.Column(db.String)

    def __init__(self, id_email = "", id_company = "", id = -1):
        if id != -1:
            self.load(id)
        else:
            self.id_email = id_email
            self.id_company = id_company
            self.date = time.strftime("%d/%m/%Y")
            self.time = time.strftime("%H:%M:%S")

    def save(self):
        db.session.add(self)
        db.session.commit()

    def load(self, id):
        email_history = EmailHistory.query.filter_by(_id=id).first()
        if email_history:
            self._id = email_history._id
            self.title = email_history.id_email
            self.summary = email_history.id_company
            self.link_notice = email_history.date
            self.time = email_history.time

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Category(db.Model):

    __tablename__ = "category"

    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)

    def __init__(self, name="", id=-1):
        if id != -1:
            self.load(id)
        else:
            self.name = name;

    def save(self):
        db.session.add(self)
        db.session.commit()

    def load(self, id):
        category = Category.query.filter_by(_id=id).first()
        if category:
            self._id = category._id
            self.name = category.name

    def delete(self):
        db.session.delete(self)
        db.session.commit()
