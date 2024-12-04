"""This page creates the database table"""

from app import db
from app import UserMixin


class Borrowed(db.Model): # This establishes the association table with the extra data columns needed
    __tablename__ = "borrowed_table"
    memberID = db.Column(db.Integer,db.ForeignKey("member_table.id"), primary_key=True)
    gearID = db.Column(db.Integer,db.ForeignKey("gear_table.id"), primary_key=True)
    qtyBorrowed = db.Column(db.Integer)
    dateBorrowed = db.Column(db.Date)
    gear = db.relationship("Gear", back_populates="members")
    member = db.relationship("Member", back_populates="gears")


class Member(db.Model,UserMixin): # Member to Borrowed is a one to many relationship
    __tablename__ = "member_table"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(500))
    password = db.Column(db.String(500))
    admin = db.Column(db.Boolean)
    gears = db.relationship('Borrowed', back_populates='member')


class Gear(db.Model): # Gear to Borrowed is a one to many relationship
    __tablename__ = "gear_table"
    id = db.Column(db.Integer, primary_key=True)
    qtyTotal = db.Column(db.Integer)
    qtyAvailable = db.Column(db.Integer)
    members = db.relationship("Borrowed",back_populates="gear")
    typeID = db.Column(db.Integer, db.ForeignKey('type.id'))
    sizeID = db.Column(db.Integer, db.ForeignKey('size.id'))


    def __repr__(self):
        return f"{self.id},{self.qtyTotal},{self.qtyAvailable},{self.typeID},{self.sizeID}"

  
class Size(db.Model): # Size to Gear is a one to many relationship
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String(50))
    gears = db.relationship('Gear',backref='size', lazy=True)

    
class Type(db.Model): # Type to Gear is a one to many relationship
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    gears = db.relationship('Gear',backref='type', lazy=True)