# All the libraries and packages List 
import imp
from itertools import product
from operator import methodcaller
from re import A
import re
import sqlite3
import email
from email.policy import default
from enum import unique
from tkinter.messagebox import RETRY
from turtle import title
from unicodedata import name
from urllib import response
from xml.dom import ValidationErr
from flask import Flask ,render_template , session , request , redirect , url_for , flash,current_app,make_response,Response
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from wtforms import Form, StringField, PasswordField, validators ,IntegerField ,TextAreaField,DecimalField,SubmitField,ValidationError
from flask_wtf.file import FileAllowed ,FileField ,FileRequired
from flask_uploads import IMAGES , UploadSet , configure_uploads
import os
import secrets
from flask_msearch import Search
from flask_wtf import FlaskForm
from flask_login import LoginManager ,login_required,current_user,logout_user,login_user,UserMixin
from flask_migrate import Migrate
import json
import pdfkit
from fpdf import FPDF
import stripe

publishable_key ='pk_test_51KQrSsSFRNzrRUwbw33NDQUtt79tVmmaAh23qIJSmNaRZo2HB0nJT4LSfiXTH1I7sDUIgG4PHrKv1UMLvLRFunq6003zbsZOUF'
stripe.api_key ='sk_test_51KQrSsSFRNzrRUwbmIECwjGtz8bsVnGB0l3Jm985QNgtu15zwXaQ7sna0klJhJ2k2cX7lwtM1xntrMBxqRkrAVJE00XQEuiLOY'

# Appliction Config
basedir = os.path.abspath(os.path.dirname(__file__))
app= Flask(__name__ , template_folder='templates',static_folder='static')
app.secret_key='lkjhasfd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ourdairy.db'
app.config['SECRET_key']='lkjhasfd'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir,'static/images')
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

db = SQLAlchemy(app)
bcrypt=Bcrypt(app)

search=Search()
search.init_app(app)
# MSEARCH_INDEX_NAME =  os.path.join(app.root_path,'msearch')
# MSEARCH_PRIMARY_KEY = 'id'
# MSEARCH_ENABLE = True

migrate=Migrate(app,db)


login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='LoginCustomer'
login_manager.needs_refresh_message_category='danger'
login_manager.login_message=u'please login first'





# Define all the class 
class User(db.Model):#define for Database Model 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    profile = db.Column(db.String(180), unique=False, nullable=False,default='profile.jpg')
    def __repr__(self):
        return '<User %r>' % self.username

db.create_all()



class Brand(db.Model):# Brand Database Model 
    id=db.Column(db.Integer, primary_key=True,autoincrement=True)
    name=db.Column(db.String(30), nullable=False,unique=True)
    def __repr__(self):
        return '<Brand %r>' % self.name

class Category(db.Model):# Category Database Model 
    id=db.Column(db.Integer, primary_key=True,autoincrement=True)
    name=db.Column(db.String(30), nullable=False,unique=True)
    def __repr__(self):
        return '<Category %r>' % self.name

db.create_all()




from datetime import datetime
class Addproducts(db.Model):#Addproducts Database Model 
    __seachbale__ = ['name','description']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10 , 2),nullable=False)
    discount=db.Column(db.Integer ,default=0)
    stock=db.Column(db.Integer , nullable=False)
    description = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)

    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'),nullable=False)
    brand = db.relationship('Brand',backref=db.backref('brands', lazy=True))

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=False)
    category = db.relationship('Category',backref=db.backref('categories', lazy=True))

    image_1=db.Column(db.String(150),nullable=False,default='image.jpg')
    def __repr__(self):
        return '<Addproducts %r>' % self.name
db.create_all()

@login_manager.user_loader
def user_loader(user_loader):
    return RegisterCustomer.query.get(user_loader)

class RegisterCustomer(db.Model, UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),unique=False)
    username=db.Column(db.String(50),unique=True)
    email=db.Column(db.String(50),unique=True)
    name=db.Column(db.String(50),unique=False)
    Password=db.Column(db.String(200),unique=False)
    country=db.Column(db.String(50),unique=False)
    state=db.Column(db.String(50),unique=False)
    city=db.Column(db.String(50),unique=False)
    contact=db.Column(db.String(50),unique=False)
    address=db.Column(db.String(200),unique=False)
    zipcode=db.Column(db.String(50),unique=False)
    profile=db.Column(db.String(200),unique=False,default='profile.jpg')
    date_created=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    
    def __repr__(self):
        return'<RegisterCustomer %r>' % self.name


db.create_all()

class JsonEcodedDict(db.TypeDecorator):
    impl=db.Text

    def process_bind_param(self , value ,dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)

    def process_result_value(self,value,dialect):
        if value is None:
            return '{}'
        else:
            return json.loads(value)

class Order_list(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    invoice=db.Column(db.String(20),unique=True,nullable=False)
    status=db.Column(db.String(20),default='Panding',nullable=False)
    customer_id=db.Column(db.Integer,unique=False,nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
    orders=db.Column(JsonEcodedDict)

    def __repr__(self):
        return '<Order %r>' % self.invoice

db.create_all()

class Contactus(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30),unique=False)
    email=db.Column(db.String(50),unique=False)
    Message=db.Column(db.String(200),unique=False)
db.create_all()









# All Forms define here
class RegistrationForm(Form):#define for registration system 
    name = StringField('Name', [validators.Length(min=3, max=25)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35),validators.Email()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')



class LoginForm(Form):# Define login System Form
    email = StringField('Email Address', [validators.Length(min=6, max=35),validators.Email()])
    password = PasswordField('New Password', [validators.DataRequired()]) 



class Addproduct(Form):#Addproducts Form
    name=StringField('Name',[validators.DataRequired()])
    price=DecimalField('Price',[validators.DataRequired()])
    discount=IntegerField('Discount',default=0)
    stock=IntegerField('Stock',[validators.DataRequired()])
    discription = TextAreaField('Discription',[validators.DataRequired()])

    image_1=FileField ('Image', validators=[FileAllowed(['jpg','png','gif','jpeng'])])

class CustomerRegister(FlaskForm):#Customer Registertion Form 
    name=StringField('Name:')
    username=StringField('Username:',[validators.DataRequired()])
    email=StringField('Email:',[validators.Email(),validators.DataRequired()])
    password=PasswordField('Password:',[validators.DataRequired(),validators.EqualTo('confirm',message='Both Password must match !!')])
    confirm=PasswordField('Repet Password:',[validators.DataRequired()])
    countey=StringField('Countey:',[validators.DataRequired()])
    state=StringField('State:',[validators.DataRequired()])
    city=StringField('City:',[validators.DataRequired()])
    contact=StringField('Contact:',[validators.DataRequired()])
    address=StringField('Address:',[validators.DataRequired()])
    zipcode=StringField('Zipcode:',[validators.DataRequired()])

    profile=FileField('Profile',validators=[FileAllowed(['jpg','pnj','jpeg','gif'],'Image only Please')])

    submit = SubmitField('Regiser')
    def validate_username(self, username):
        if RegisterCustomer.query.filter_by(username=username.data).first():
            raise ValidationError("This username is already in use!")
            
    def validate_email(self,email):
        if RegisterCustomer.query.filter_by(email=email.data).first():
            raise ValidationError('Email already in use.')

class CustomerLogin(FlaskForm):
    email=StringField('Email:',[validators.Email(),validators.DataRequired()])
    password=PasswordField('Password:',[validators.DataRequired()])

class ContactUs(Form):#d
    name = StringField('Name', [validators.Length(min=3, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35),validators.Email()])
    Message=StringField('Suggestion:',[validators.DataRequired()])
    


    















# Define Routes for web.
@app.route('/payment',methods=['POST'])
@login_required
def payment():
    invoice=request.form.get('invoice')
    amount=request.form.get('amount')

    orders=Order_list.query.filter_by(customer_id=current_user.id,invoice=invoice).order_by(Order_list.id.desc()).first()
    Order_list.status = 'PAID'
    db.session.commit()
    flash("✌️  !! Thank You for Shopping With US !!  ✌️")
    return redirect(url_for('home'))


@app.route ('/')#Home Page
def home():
    page=request.args.get('page',1,type=int)
    products=Addproducts.query.filter(Addproducts.stock > 0).paginate(page=page,per_page=6)
    brands=Brand.query.join(Addproducts,(Brand.id==Addproducts.brand_id)).all()
    categories=Category.query.join(Addproducts,(Category.id==Addproducts.category_id)).all()
    return render_template("index.html",title="Home Page",products=products,brands=brands,categories=categories)


@app.route('/search_for')
def search_for():
    word=request.args.get('q')
    products = Addproducts.query.msearch(word, fields=['name','description'] , limit=6)
    print('no')
    print('search for=',word)
    print('no')
    brands=Brand.query.join(Addproducts,(Brand.id==Addproducts.brand_id)).all()
    categories=Category.query.join(Addproducts,(Category.id==Addproducts.category_id)).all()
    return render_template ('search.html',products=products,brands=brands,categories=categories)

@app.route('/product/<int:id>')
def single_page(id):
    product=Addproducts.query.get_or_404(id)
    brands=Brand.query.join(Addproducts,(Brand.id==Addproducts.brand_id)).all()
    categories=Category.query.join(Addproducts,(Category.id==Addproducts.category_id)).all()
    return render_template('single_page.html',product=product,brands=brands,categories=categories)

@app.route('/brand/<int:id>')
def get_brand(id):
    page=request.args.get('page',1,type=int)
    get_b = Brand.query.filter_by(id=id).first_or_404()
    brand=Addproducts.query.filter_by(brand=get_b).paginate(page=page,per_page=6)
    brands=Brand.query.join(Addproducts,(Brand.id==Addproducts.brand_id)).all()
    categories=Category.query.join(Addproducts,(Category.id==Addproducts.category_id)).all()
    return render_template("index.html",title="Home Page",brand=brand,brands=brands,categories=categories,get_b=get_b)

@app.route('/category/<int:id>')
def get_cat(id):
    page=request.args.get('page',1,type=int)
    get_cat=Category.query.filter_by(id=id).first_or_404()
    get_cat_prod = Addproducts.query.filter_by(category=get_cat).paginate(page=page,per_page=6)
    brands=Brand.query.join(Addproducts,(Brand.id==Addproducts.brand_id)).all()
    categories=Category.query.join(Addproducts,(Category.id==Addproducts.category_id)).all()
    return render_template("index.html",title="Home Page",get_cat_prod=get_cat_prod,categories=categories,brands=brands,get_cat=get_cat)

@app.route ('/admin')# Admin Page
def admin():
    if 'email' not in session:
        flash("Please Login First " , "danger")
        return redirect(url_for('login'))

    products=Addproducts.query.all()
    return render_template("admin.html",title="Admin",products=products)

@app.route('/order_list',methods=['GET','POST'])
def order():
    if 'email' not in session:
        flash("Please Login First " , "danger")
        return redirect(url_for('login'))
    userList = Order_list.query\
         .join(RegisterCustomer,RegisterCustomer.id== Order_list.customer_id)\
         .add_columns(Order_list.invoice,Order_list.date_created,Order_list.status,Order_list.id, RegisterCustomer.name)

    return render_template('orderlist.html',order=userList)

@app.route('/view/<int:id>')
def view(id):
    if 'email' not in session:
        flash("please Login first","danger")
        return redirect(url_for('login'))
    grandTOtal=0
    subTotal=0 
    order_li=Order_list.query.get_or_404(id)
    for _key, product in order_li.orders.items():
                discount=(product['discount']/100 * float(product['price']))
                subTotal += float(product['price'])*int(product['quantity'])
                subTotal -= discount
                grandTOtal=subTotal
    return render_template('vieworder.html',order_li=order_li,grandTOtal=grandTOtal,subTotal=subTotal)

  
    




@app.route('/customerinfo')
def customer():
    if 'email' not in session:
        flash("Please Login First " , "danger")
        return redirect(url_for('login'))
    customer=RegisterCustomer.query.order_by(RegisterCustomer.id.asc()).all()
    return render_template('customer.html', customer=customer)














@app.route('/register', methods=['GET', 'POST'])#define registertions system
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_pass = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data,username=form.username.data,email=form.email.data,
                    password=hash_pass)
        db.session.add(user)
        db.session.commit()
        flash(f'{form.username.data}Thanks you for registering','success')
        return redirect(url_for('login'))
    else:
        return render_template('register.html', title="register page", form=form) 

@app.route('/login',methods=['GET','POST'])#Login system 
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            session['email']=form.email.data
            flash(f'welcome {form.email.data} you Loged in','success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash('Worng Password or Email Check and try again','danger')

    return render_template('login.html',title="login",form=form)

@app.route('/logout',methods=['GET','POST'])
def logout():
    session.pop('email')
    return redirect(url_for('login'))

    


@app.route('/addbrand',methods=['GET','POST'])#Addbrands 
def addbrand():
    if 'email' not in session:
        flash("Please Login First " , "danger")
        return redirect(url_for('login'))
    if request.method =="POST":
        getbrand=request.form.get('brand')
        brand=Brand(name=getbrand)
        db.session.add(brand)
        flash(f'the Brand {getbrand} add sucessfully','success')
        db.session.commit()
        return redirect(url_for("addbrand"))
    return render_template('add_categories.html',brandSadd='brandSadd',title='Add Brand')




@app.route('/cat')
def cat():
    if 'email' not in session:
        flash("pleas login first ","danger")
        return redirect(url_for('login'))
    brands=Brand.query.order_by(Brand.id.desc()).all()
    return render_template("cat.html",title="Categoty",brands=brands)

@app.route('/updatebrand/<int:id>',methods=['GET','POST'])
def update(id):
    if 'email' not in session:
        flash("please Login first","danger")
        return redirect(url_for('login')) 
    updatebrand=Brand.query.get_or_404(id)
    brand=request.form.get('brand')
    if request.method == "POST":
        updatebrand.name=brand
        flash(f'Category has been update','success')
        db.session.commit()
        return redirect(url_for('cat'))
    return render_template("update.html",title='Update Cat',updatebrand=updatebrand)



@app.route('/deletecat/<int:id>',methods=['GET','POST'])
def deletecat(id):
    if 'email' not in session :
         flash(f'Please login First', 'success')
         return redirect(url_for('login'))
    brand=Brand.query.get_or_404(id)
    try:
       db.session.delete(brand)
       db.session.commit()
       flash(f'Brand  {brand.name} Delete','success')
       
    except:
        flash(f'Brand  is Not Delete Please First Delete Product are available in Brand.','warning')
        return redirect(url_for('admin'))
    
    return redirect(url_for('cat'))
    
    
    

    


    


    
    


@app.route('/addcat',methods=['GET','POST'])
def addcat():
    if 'email' not in session:
        flash("Please Login First " , "danger")
        return redirect(url_for('login'))
    if request.method =="POST":
        getcat=request.form.get('Category')
        cat=Category(name=getcat)
        db.session.add(cat)
        flash(f'the Categories {getcat} add sucessfully','success')
        db.session.commit()
        return redirect(url_for("addcat"))
    return render_template('add_categories.html')
@app.route('/subcat')
def subcat():
    if 'email' not in session:
        flash("pleas login first ","danger")
        return redirect(url_for('login'))
    categories=Category.query.order_by(Category.id.desc()).all()
    return render_template("cat.html",title="Subategoty",categories=categories)

@app.route('/updatesubcat/<int:id>',methods=['GET','POST'])
def updatesub(id):
    if 'email' not in session:
        flash("please Login first","danger")
        return redirect(url_for('login')) 
    updatesubcat=Category.query.get_or_404(id)
    categories=request.form.get('Category')
    if request.method == 'POST':
        updatesubcat.name=categories
        flash(f'Subcategories has been Update' ,'success')
        db.session.commit()
        return redirect(url_for('subcat'))
    return render_template("update.html",title='Update Cat',updatesubcat=updatesubcat)

@app.route('/deletesubcat/<int:id>',methods=['GET','POST'])
def deletesubcat(id):
    if 'email' not in session :
         flash(f'Please login First', 'success')
         return redirect(url_for('login'))
    cat=Category.query.get_or_404(id)
    try:
       db.session.delete(cat)
       db.session.commit()
       flash(f'Brand  {cat.name} Delete','success')
       
    except:
        flash(f'Categories  is Not Delete Please First Delete Product are available in Categories.','warning')
        return redirect(url_for('admin'))
    
    return redirect(url_for('subcat'))



@app.route('/Addproduct',methods=['GET','POST'])#Add products 
def addproduct():
    if 'email' not in session:
        flash("Please Login First " , "danger")
        return redirect(url_for('login'))
    brands=Brand.query.all()
    categories=Category.query.all()
    form=Addproduct(request.form)
    if request.method == "POST":
        name=form.name.data
        price=form.price.data
        discount=form.discount.data
        stock=form.stock.data
        description=form.discription.data
        brand=request.form.get('brand')
        category=request.form.get('category')
        image_1=photos.save(request.files.get('image_1'),name=secrets.token_hex(10)+".")
        addpro=Addproducts(name=name,price=price,discount=discount,stock=stock,description=description,brand_id=brand,category_id=category,image_1=image_1)
    
        db.session.add(addpro)
        db.session.commit()
        flash(f"the product {name} has added " , "success")
        return redirect(url_for("addproduct"))

    return render_template('addproduct.html',title='Add Product',form=form , brands=brands, categories=categories)

@app.route('/updateproduct/<int:id>',methods=['GET','POST'])
def updateproduct(id):
    if 'email' not in session:
        flash(f'Please login first','success')
        return redirect(url_for('login'))
    brands=Brand.query.all()
    categories=Category.query.all()
    brand=request.form.get('brand')
    category=request.form.get('category')
    product=Addproducts.query.get_or_404(id)
    form=Addproduct(request.form)
    if request.method == "POST":
        product.name=form.name.data
        product.price=form.price.data
        product.discount=form.discount.data
        product.brand_id=brand
        product.category_id=category
        product.stock=form.stock.data
        product.description=form.discription.data

        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path,"static/images/" +product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'),name=secrets.token_hex(10)+".")
            except:
                product.image_1=photos.save(request.files.get('image_1'),name=secrets.token_hex(10)+".")

        db.session.commit()
        flash(f'your Product has been update','success')
        return redirect(url_for('admin'))
    form.name.data=product.name
    form.price.data=product.price
    form.discount.data=product.discount
    form.stock.data=product.stock
    form.discription.data=product.description

    return render_template('updpro.html',title="Update Product",form=form,brands=brands,categories=categories,product=product)
@app.route('/deleteprodyuct/<int:id>',methods=['GET','POST'])
def deletepro(id):
    if 'email' not in session:
        flash(f'pleas login first','success')
        return redirect(url_for('login'))
    product=Addproducts.query.get_or_404(id)
    if request.method =="POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
        except Exception as e:
            print(e)
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for('admin'))
    flash(f'Can not delete the product','danger')

    return redirect(url_for('admin'))


def MagerDicts(dict1,dict2):# Merge Items for Cart to add items in cart 
    if isinstance(dict1, list) and isinstance(dict2,list):
        return dict1  + dict2
    if isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))

#cart here user can add items in cart without login user can login to order 
@app.route('/addcart',methods=['GET','POST'])
def AddCart():
    try:
        product_id=request.form.get('product_id')
        quantity=request.form.get('quantity')
        product=Addproducts.query.filter_by(id=product_id).first()

        if product_id and quantity and product and request.method=='POST':
            DictItems={product_id:{'name':product.name,'price':product.price,'discount':product.discount,'quantity':quantity,'image':product.image_1}}
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    for key, item in session['Shoppingcart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            item['quantity'] += 1
                        return redirect(url_for('getcart'))
                else:
                    session['Shoppingcart']=MagerDicts(session['Shoppingcart'],DictItems)
                    return redirect(url_for('getcart'))
            else:
                session['Shoppingcart']=DictItems
                return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(url_for('getcart'))

@app.route('/cart')
def getcart():
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <=0:
        return redirect(url_for('home'))
    subtotal=0
    grandtotal=0
    brands=Brand.query.join(Addproducts,(Brand.id==Addproducts.brand_id)).all()
    categories=Category.query.join(Addproducts,(Category.id==Addproducts.category_id)).all()

    for key, product in session['Shoppingcart'].items():
        discount=(product['discount']/100)*float(product['price'])
        subtotal+=float(product['price'])*int(product['quantity'])
        subtotal-=discount
        grandtotal=float(subtotal)
        

    return render_template('cart.html',title='Check Cart',grandtotal=grandtotal,brands=brands,categories=categories)

@app.route('/updatecart/<int:code>',methods=['GET','POST'])
def updatecart(code):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <=0:
        return redirect(url_for('home'))
    if request.method=='POST':
        quantity=request.form.get('quantity')
        try:
            session.modified =True
            for key ,item in session['Shoppingcart'].items():
                if int(key) == code:
                    item['quantity']= quantity
                    flash('Item updated successfull' 'success')
                    return redirect(url_for('getcart'))
        except Exception as e:
            print(e)
            return redirect(url_for('getcart'))

@app.route('/deletitem/<int:id>',methods=['GET','POST'])
def deleteitem(id):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <=0:
        return redirect(url_for('home'))
    try :
        session.modified =True
        for key ,item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key,None)
                return redirect(url_for('getcart'))
                
        
    except Exception as e:
        print(e)
        return redirect(url_for('getcart'))

@app.route('/clearcart',methods=['GET','POST'])
def clearcart():
    try:
        session.pop('Shoppingcart',None)
        return redirect (url_for('home'))
    except Exception as e:
        print(e)



#Customer Registration
@app.route('/customer/register',methods=['GET','POST'])
def custtomer_register():
    form=CustomerRegister()
    if form.validate_on_submit():
        hash_password=bcrypt.generate_password_hash(form.password.data)
        register=RegisterCustomer(name=form.name.data,username=form.username.data,email=form.email.data,Password=hash_password,country=form.countey.data,
                                state=form.state.data,city=form.city.data,contact=form.contact.data,address=form.address.data,zipcode=form.zipcode.data)
        db.session.add(register)
        flash(f'{form.name.data} Thank you for register ','success')
        db.session.commit()
        return redirect(url_for('LoginCustomer'))
    return render_template('c_register.html',form=form,title="Customer Register")

@app.route('/customer/login',methods=['GET','POST'])
def LoginCustomer():
    form=CustomerLogin()
    if form.validate_on_submit():
        user=RegisterCustomer.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.Password,form.password.data):
            login_user(user)
            flash('You are login now' ,'success')
            next=request.args.get('next')
            return redirect(next or url_for('home'))
        flash('Incorrect Email or password','danger')
        return redirect(url_for('LoginCustomer'))
    return render_template('c_login.html',title='User Login',form=form)

@app.route('/customer/logout')
def customer_logout():
    logout_user()
    return redirect(url_for('LoginCustomer'))

def updatecart():#delete Unwanted Details From Cart 
    for _key ,product in session['Shoppingcart'].items():
        session.modified=True
        del product['image']
        return updatecart

@app.route('/getorder')
@login_required
def getorder():
    if current_user.is_authenticated:
        customer_id=current_user.id
        invoice=secrets.token_hex(5)
        
        try:
            order=Order_list(invoice=invoice,customer_id=customer_id,orders=session['Shoppingcart'])
            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart')
            flash('Your order has been sent successfull ','success')
            return redirect(url_for('place_order',invoice=invoice))
        except Exception as e:
            print(e)
            flash('some thing want wrong to get order','danger')
            return redirect(url_for('getcart'))

@app.route('/PlaceOrder/<invoice>')
@login_required
def place_order(invoice):
    if current_user.is_authenticated:
        grandTOtal=0
        subTotal=0
        customer_id=current_user.id
        customert=RegisterCustomer.query.filter_by(id=customer_id).first()
        orders=Order_list.query.filter_by(customer_id=customer_id).first()
        for _key, product in orders.orders.items():
            discount=(product['discount']/100 * float(product['price']))
            subTotal += float(product['price'])*int(product['quantity'])
            subTotal -= discount
            grandTOtal=subTotal
    else:
        return redirect (url_for('LoginCustomer'))
    return render_template('Order.html',invoice=invoice,grandTOtal=grandTOtal,customert=customert,orders=orders)


@app.route('/demo')
def demo():
    return render_template('demo.html')


@app.route('/get_pdf/<invoice>',methods=['GET','POST'])
@login_required
def get_pdf(invoice):
    if current_user.is_authenticated:
        grandTOtal=0
        subTotal=0
        customer_id=current_user.id
        if request.method == "POST":
            
            customert=RegisterCustomer.query.filter_by(id=customer_id).first()
            orders=Order_list.query.filter_by(customer_id=customer_id, invoice=invoice).order_by(Order_list.id.desc())\
                .join(RegisterCustomer,RegisterCustomer.id== Order_list.customer_id)\
                .add_columns(Order_list.invoice,Order_list.date_created,Order_list.status,Order_list.id, Order_list.orders,RegisterCustomer.address,RegisterCustomer.city,RegisterCustomer.state,RegisterCustomer.country,RegisterCustomer.contact,RegisterCustomer.zipcode).first()
            for _key, product in orders.orders.items():
                discount=(product['discount']/100 * float(product['price']))
                subTotal += float(product['price'])*int(product['quantity'])
                subTotal -= discount
                grandTOtal=subTotal
           
            rendered = render_template('PDF.html',invoice=invoice,grandTOtal=grandTOtal,customert=customert,orders=orders)
            pdf = pdfkit.from_string(rendered, False)
            response = make_response(pdf)
            response.headers['content-Type'] ='application/pdf'
            response.headers['content-Disposition'] ='inline:filename='+invoice+'.pdf'
            return response
        return request(url_for('getorder'))

@app.route('/download/report/pdf',methods=['POST'])
def report_pdf():
     if current_user.is_authenticated:
        grandTOtal=0
        subTotal=0
        customer_id=current_user.id
        if request.method == "POST":
            add=RegisterCustomer.add
            customert=RegisterCustomer.query.filter_by(id=customer_id).first()
            orders=Order_list.query.filter_by(customer_id=customer_id).order_by(Order_list.id.desc()).first()
            for _key, product in orders.orders.items():
                discount=(product['discount']/100 * float(product['price']))
                subTotal += float(product['price'])*int(product['quantity'])
                subTotal -= discount
                grandTOtal=subTotal
        ren=render_template('pdf.html',grandTOtal=grandTOtal,customert=customert,orders=orders)
        pdf = FPDF(ren)
        response=make_response(pdf.output(dest='S').encode('latin-1'))
        response.headers.set('Content-Disposition', 'attachment', filename='Invoice.pdf')
        response.headers.set('Content-Type', 'application/pdf')
        #return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=employee_report.pdf'})
        return response

@app.route('/cancel/order/<int:id>',methods=['GET','POST'])
@login_required
def cancel_order(id):
    if current_user.is_authenticated:
        order=Order_list.query.get_or_404(id)
        if request.method =="POST":
            db.session.delete(order)
            db.session.commit()
            flash('Order Cencle Successfull','suceess')
            return redirect(url_for('home'))

@app.route('/aboutus')
def aboutus():
    brands=Brand.query.join(Addproducts,(Brand.id==Addproducts.brand_id)).all()
    categories=Category.query.join(Addproducts,(Category.id==Addproducts.category_id)).all()
    return render_template('aboutus.html',title='About Us',brands=brands,categories=categories)

@app.route('/contact_us',methods=['GET','POST'])
def contact_us():
    
    brands=Brand.query.join(Addproducts,(Brand.id==Addproducts.brand_id)).all()
    categories=Category.query.join(Addproducts,(Category.id==Addproducts.category_id)).all()
    form=ContactUs(request.form)
    if request.method == 'POST' and form.validate():
        contact=Contactus(name=form.name.data,email=form.email.data,Message=form.Message.data)
        db.session.add(contact)
        db.session.commit()
        flash("Thank You For Contact Us.")
        return redirect(url_for('home'))

    return render_template('contact_us.html',title='contact us',brands=brands,categories=categories,form=form)


# @app.route('/register', methods=['GET', 'POST'])#define registertions system
# def register():
#     form = RegistrationForm(request.form)
#     if request.method == 'POST' and form.validate():
#         hash_pass = bcrypt.generate_password_hash(form.password.data)
#         user = User(name=form.name.data,username=form.username.data,email=form.email.data,
#                     password=hash_pass)
#         db.session.add(user)
#         db.session.commit()
#         flash(f'{form.username.data}Thanks you for registering','success')
#         return redirect(url_for('login'))
#     else:
#         return render_template('register.html', title="register page", form=form) 
@app.route('/message')
def message():
    if 'email' not in session:
        flash("please Login first","danger")
        return redirect(url_for('login'))
    mes=Contactus.query.order_by(Contactus.id.desc()).all()
    return render_template('message.html',title='Contant Us info',mes=mes)
    



    
if __name__ == "__main__":
    app.run(host="localhost",port="400", debug=True)