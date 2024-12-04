"""This page implements a lot of functionality through
passing in variable to pages and making database calls"""

#https://www.freecodecamp.org/news/how-to-authenticate-users-in-flask/
#https://flask-login.readthedocs.io/en/latest/#how-it-works
#https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#association-object
#https://testdriven.io/blog/flask-sessions/


# CURRENTLY WORKING ON:
    # https://flask-user.readthedocs.io/en/latest/authorization.html
    # https://stackoverflow.com/questions/61061102/flask-user-login-required-and-roles-required-not-working
    # https://flask-user.readthedocs.io/en/v0.6/roles_required_app.html


from flask import render_template, flash, request, redirect, url_for, session
from app import app, db, admin, login_manager, bcrypt, login_required, login_user, logout_user, current_user
from .models import Gear, Borrowed, Member, Size, Type
from .forms import newGearForm, signupForm, loginForm, changePass, returnGear
from sqlalchemy.orm import joinedload
import datetime
from flask_admin.contrib.sqla import ModelView


@login_manager.user_loader
def load_user(user_id):
    return Member.query.get(int(user_id))

app.app_context().push()
admin.add_view(ModelView(Gear, db.session))
admin.add_view(ModelView(Borrowed, db.session))
admin.add_view(ModelView(Member, db.session))
admin.add_view(ModelView(Size, db.session))
admin.add_view(ModelView(Type, db.session))

@app.route('/', methods=['GET', 'POST'])
def home():
    adminVal = session.get('adminVal',False)
    return render_template('home.html',isAdmin=adminVal)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    adminVal = session.get('adminVal',False)
    form = changePass()
    if form.validate_on_submit():
        user = Member.query.filter_by(id=session.get('userID')).first()

        if bcrypt.check_password_hash(user.password,form.current.data): #Changes the password only if their current password matches
            user.password = bcrypt.generate_password_hash(form.new.data)
            db.session.commit()
            flash("Password changed")
            referrer= request.referrer
            return redirect(referrer)
        else:
            flash("Invalid password", "danger")

  
    return render_template('profile.html',isAdmin=adminVal, form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        try:
            user = Member.query.filter_by(username=form.user.data).first()
            if bcrypt.check_password_hash(user.password,form.password.data): #checks the password matches the one saved
                login_user(user)
                session['adminVal'] = user.admin
                session['userID'] = user.id
                 # sets the admin value, so new pages are shown if the user is an admin
                return redirect(url_for('home'))
            else:
                flash("Invalid Username or Password!", "danger")

        except:
            flash("Error")
    return render_template('login.html',form=form,isAdmin=False)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = signupForm()
    if form.validate_on_submit():
        #get the data from the form - hash the password - save to DB
        email = form.username.data
        pwd = bcrypt.generate_password_hash(form.password2.data)
        member = Member.query.filter_by(username = form.username.data).first()
        if member: #if the email is already in the database, they cannot create another account
            flash("Account already exists!")
        else:
            if form.password1.data == form.password2.data:
                newuser = Member(username=email, password=pwd) #adds new user details to db
                db.session.add(newuser)
                db.session.commit()
                return redirect(url_for('login'))
            else:
                flash("Passwords do not match")
    return render_template('signup.html',form=form,isAdmin=False)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('adminVal', default=None)
    return redirect(url_for('login'))


@app.route('/create',methods=['GET','POST'])
def newGear():
    adminVal = session.get('adminVal',False)
    form = newGearForm()
    types = Type.query.with_entities(Type.type).all()
    form.gearOptions(types) # sends the gear types to be shown in the drop down options
  
    if form.validate_on_submit():
        sizeVal = form.size.data
        s = Size.query.filter_by(size=sizeVal).first() #if the new gear has an associated size that will be added to the database
        sID = s.id
        if form.type.data == 'Other':
            typeVal = form.other.data
            newType = Type(type=typeVal)
            db.session.add(newType)
            db.session.commit() # allows the admin to add a new type of gear to the db

            t = Type.query.filter_by(type=typeVal).first() 
            tID = t.id
        
            try:
                newGear = Gear(qtyTotal = form.qty.data,qtyAvailable=form.qty.data,typeID=tID,sizeID=sID)
            except:
                newGear = Gear(qtyTotal = form.qty.data,qtyAvailable=form.qty.data,typeID=tID) 
        
            db.session.add(newGear)
            db.session.commit()

        else:
            #there is already this type of data so i need to check if it exists in that size
            typeVal = form.type.data 
            t = Type.query.filter_by(type=typeVal).first() 
            tID = t.id
            gear = Gear.query.filter_by(typeID=tID).first()
            if not sID:
                gear.qtyAvailable += form.qty.data
                gear.qtyTotal += form.qty.data
                db.session.commit()
            else:
                newSize = Size.query.filter_by(id=sID).first()
                if newSize.size == form.size.data:
                    gear.qtyAvailable += form.qty.data
                    gear.qtyTotal += form.qty.data
                    db.session.commit()
                else:
                    newGear = Gear(qtyTotal = form.qty.data,qtyAvailable=form.qty.data,typeID=tID,sizeID=sID)
                    db.session.add(newGear)
                    db.session.commit()
        
        
        flash("Gear list updated")

        referrer= request.referrer
        return redirect(referrer)

    return render_template('create.html',form=form,isAdmin=adminVal)

@app.route('/gear', methods=['GET', 'POST'])
def gear():
    adminVal = session.get('adminVal',False)

    gear = Gear.query.filter(Gear.qtyAvailable !=0).all() #gets all of the gear that is not completely borrowed
    types=[]
    typeIDs = []
    for g in gear:
        typeIDs.append(g.typeID) #this is getting gearIDs
    for id in typeIDs:
        types.append(Gear.query.filter(Gear.typeID==id).first()) #getting all of the correlated types
    
    return render_template('gear.html',isAdmin=adminVal,availableGear=gear,distinctTypes=types)

@app.route('/borrowed/', methods=['GET', 'POST'])
def borrowed():
    adminVal = session.get('adminVal',False)
    items = Borrowed.query.filter(Borrowed.memberID == session.get('userID')).all()
    forms = [] # Creating multiple forms for each item borrowed so can 
               # individually pass in the number available to return
    form = returnGear()
    for item in items:
        form = returnGear()
        form.returnOptions(item.qtyBorrowed)
        forms.append(form)

    gearIDs = []
    types=[]
    typeIDs = []
    for val in items:
        gearIDs.append(val.gearID) #Getting all of the gearIDs that are borrowed
   
    for g in gearIDs: #getting the type IDs from the borrowed gear
        typeIDs.append(Gear.query.filter(Gear.id==int(g)).with_entities(Gear.typeID).first())

    for id in typeIDs: #getting the type vals from their ids
        types.append(Gear.query.filter(Gear.typeID==id[0]).first()) 
    
    if form.validate_on_submit():
        num = form.qty.data
        borrowedItem = Borrowed.query.filter_by(memberID=session.get('userID'), gearID=request.form.get('gearID')).first()
        borrowedItem.qtyBorrowed -= int(num)
        if borrowedItem.qtyBorrowed == 0: #if the user has returned all of that type of gear, the borrowed record is deleted
            db.session.delete(borrowedItem)

        gearRecord = Gear.query.get(request.form.get('gearID'))
        gearRecord.qtyAvailable += int(num) #updates the number of that gear that is now available
        db.session.commit()
        flash("Item returned")

        referrer= request.referrer
        return redirect(referrer)

    return render_template('borrowed.html',isAdmin=adminVal, vals=items, forms=forms, distinctTypes=types)

@app.route('/borrow/<int:gearID>', methods=['GET', 'POST'])
def borrow(gearID):
    adminVal = session.get('adminVal',False)
    item = Gear.query.get(gearID)

    try:
        #this runs if the user has not borrowed that type of gear before, creates a new Borrowed record and adds to db
        newBorrow = Borrowed(memberID=session.get('userID'),gearID=gearID,qtyBorrowed=1,dateBorrowed=datetime.date.today())
        db.session.add(newBorrow)
        item.qtyAvailable -= 1
        db.session.commit()
        flash("New item borrowed")
    except:
        db.session.rollback() #cancels the previous attempted db insertion
        existing = Borrowed.query.filter_by(memberID=session.get('userID'), gearID=gearID).first()
        existing.qtyBorrowed +=1 
        item.qtyAvailable -= 1
        flash("Another item borrowed!")
    
    db.session.commit()
    referrer= request.referrer
    return redirect(referrer)

@app.route('/borrowedGear', methods=['GET', 'POST'])
def borrowedGear():
    adminVal = session.get('adminVal',False)
    items = Borrowed.query.all()

    members=[]
    memberIDs = []
    for val in items:
        if val.memberID not in memberIDs:
            memberIDs.append(val.memberID) #Getting all of the memberIDs that have borrowed something
    
    for u in memberIDs: #getting the type IDs from the borrowed gear
        members.append(Member.query.filter(Member.id==u).first())

    return render_template('borrowedGear.html',isAdmin=adminVal, vals=items, users=members)


@app.route('/allGear', methods=['GET', 'POST'])
def allGear():
    adminVal = session.get('adminVal',False)

    gear = Gear.query.all() 
    types=[]
    typeIDs = []
    #getting all of the types of all of the gear
    for g in gear:
        if g.typeID not in typeIDs:
            typeIDs.append(g.typeID)
    for id in typeIDs:
        types.append(Gear.query.filter(Gear.typeID==id).first())
    
    return render_template('allGear.html',isAdmin=adminVal,allGear=gear, distinctTypes=types)


