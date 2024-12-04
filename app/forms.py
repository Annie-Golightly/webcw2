"""This page creates the values needed for the forms used"""

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateField, SelectField, IntegerField, PasswordField
from app import models
from wtforms.validators import DataRequired, EqualTo, NumberRange

class newGearForm(FlaskForm):
    """Creates form to add new gear"""
    type = SelectField('Type', validators=[DataRequired()])## get list of choices from database
    other = StringField('Other type')
    size = SelectField('Size', choices=["","xxs","xs","s","m","l","xl","xxl"])
    qty = IntegerField('Quantity added',validators=[DataRequired(),NumberRange(min=1)])

    # Allows the gear type choices to be loaded from the database
    def gearOptions(self,types):
        listOfTypes = [(gear.type)for gear in types]
        listOfTypes.append("Other")
        self.type.choices = listOfTypes


class signupForm(FlaskForm):
    username = StringField('Email',validators=[DataRequired()])
    password1 = PasswordField('Create password',validators=[DataRequired()])
    password2 = PasswordField('Re-enter password',validators=[DataRequired(), EqualTo('password1', message='Passwords do not match')])


class loginForm(FlaskForm):
    user = StringField('Email',validators=[DataRequired()])
    password =PasswordField('Password',validators=[DataRequired()])


class changePass(FlaskForm):
    current = PasswordField('Current password',validators=[DataRequired()])
    new = PasswordField('New password',validators=[DataRequired()])

class returnGear(FlaskForm):
    qty = SelectField('Qty to return', validators=[DataRequired()])

    def returnOptions(self,vals): 
        options = []
        for x in range(1,vals+1):
            options.append(x)
        self.qty.choices = options