from market import app
from flask import render_template,redirect,url_for,flash,request
from market.module import Item ,User
from market.form import RegisterForm , LoginForm , BuyForm , SellForm
from market import db1
from flask_login import login_user,logout_user,login_required,current_user
@app.route("/")
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market', methods = ['GET','POST'])
@login_required
def Market_page():
    buyform = BuyForm()
    selling_form = SellForm()
    if request.method=='POST':
        #this is for but items
        buyed_item =  request.form.get('buyed_item')
        b_item_obj = Item.query.filter_by(name = buyed_item).first()
        if b_item_obj:
           if current_user.can_buy(b_item_obj):
                b_item_obj.buy(current_user)
                flash(f"Congratulations ! you buy {b_item_obj.name} for {b_item_obj.price}",category="success")
           else:
               flash(f"Unfortunately,you don't have enough money to buy {b_item_obj.name}",category="danger")
           return redirect(url_for('Market_page'))
        #this is for sell the items
        sold_item = request.form.get('sold_item')
        s_item_obj = Item.query.filter_by(name= sold_item).first()
        if s_item_obj:
            if current_user.canSell(s_item_obj):
                s_item_obj.sell(current_user)
                flash(f"Congratulations ! you sell {s_item_obj.name} for {s_item_obj.price}",category="success")
            else:
                flash(f"Somthing went wrong!{s_item_obj.name}",category="danger")

    if request.method == "GET":

     items=Item.query.filter_by(owner = None )

     owned_items = Item.query.filter_by(owner =current_user.id )

     return render_template('index.html',items=items,buyform = buyform,owned_items= owned_items,selling_form=selling_form)

@app.route('/register' , methods = ['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username = form.username.data,
                              email_address = form.email_address.data,
                              password = form.password1.data)
        db1.session.add(user_to_create)
        db1.session.commit()
        login_user(user_to_create)
        flash(f" Account created successfully! you are logged in as {user_to_create.username}",category='info')
        return redirect(url_for('Market_page'))
    if form.errors !={}:
      for err_msg in form.errors.values(): 
        flash(f'There was an error with create a user:{err_msg}',category='danger')
    return render_template('register.html',form = form)

@app.route('/Login' , methods = ['GET'])
def login_page():
   form = LoginForm()
   return render_template('login.html',form = form)

   
@app.route('/Login',methods =['POST'])
def submit_page():
    form = LoginForm()
    if form.validate_on_submit():
        # Retrieve the user from the database by their username
        attempted_user = User.query.filter_by(username = form.username.data).first()

        if attempted_user and attempted_user.check_password_correction(form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in, {attempted_user.username}', category="success")
            return redirect(url_for('Market_page'))
        else:
            flash('Username and password do not match. Please try again.', category="danger")
            return redirect(url_for('login_page'))

    # If form validation fails, the user will be redirected back to the login page with error messages displayed.
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()    
    flash("you have been logged out!", category='info')
    return redirect(url_for('home_page')) 


@app.route('/admin')
def admin_page():
    all_data = Item.query.all()
    return render_template('admin.html',items = all_data)

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        barcode = request.form['barcode']
        description = request.form['description']
    my_data = Item(name,price,barcode,description)
    db1.session.add(my_data)
    db1.session.commit()
    flash(f"Item Added successfully!",category='success')
    return redirect(url_for('admin_page'))
 
@app.route('/update',methods = ['POST','GET'])
def update():
    if request.method == 'POST':
        my_data = Item.query.get(request.form.get('id'))
        my_data.name = request.form['name']
        my_data.price = request.form['price']
        my_data.barcode = request.form['barcode']
      #  my_data.description = request.form['description']
        db1.session.commit()
        flash(f"Item updated Successfully!",category='success')
        return redirect(url_for('admin_page'))
        

@app.route('/delete/<id>/', methods = ['POST','GET'])
def delete(id):
    my_data = Item.query.get(id)
    db1.session.delete(my_data)
    db1.session.commit()
    flash(f"Item Deleted Successfully!",category='success')
    return redirect(url_for('admin_page'))

