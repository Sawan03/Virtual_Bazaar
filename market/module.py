from market import db1
from market import bcrypt
from market import login_manager
from flask_login import UserMixin

class User(db1.Model,UserMixin):
    id = db1.Column(db1.Integer(),primary_key = True)
    username = db1.Column(db1.String(30),nullable=False,unique = True)
    email_address = db1.Column(db1.String(50),nullable = False,unique =True)
    password_hash = db1.Column(db1.String(60),nullable = False)
    budget = db1.Column(db1.Integer(),nullable = False,default = 100000)
    item = db1.relationship ('Item',backref='owned_user',lazy = True)
    
    ## 1,000 after three 0 we add a comma that comma come from this prettier function
    @property
    def prettier_budget(self):
        if len(str(self.budget))>=4:
               return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]} ₹'
        else:
            return f'{self.budget} ₹'
    @property
    def password(self):
        return self.password
    
 
    @password.setter
    def password(self,plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    
    #@login_manager.user_loader        
    def check_password_correction(self,attemped_password):
        return bcrypt.check_password_hash(self.password_hash,attemped_password)
    def can_buy(self,item_obj):
        return self.budget>= item_obj.price
    
    def canSell(self,item_obj):
        return item_obj in self.item

class Item(db1.Model,UserMixin):
    
    id = db1.Column(db1.Integer(),primary_key = True)
    name = db1.Column(db1.String(length=30),nullable = False, unique = True)
    price = db1.Column(db1.Integer(),nullable = False)
    barcode =  db1.Column(db1.String(length=15),nullable = False, unique = True)
    description =  db1.Column(db1.String(length=1024),nullable = False, unique = True)
    owner = db1.Column(db1.Integer(),db1.ForeignKey('user.id'))
    
    def __init__(self,name,price,barcode,description):
        self.name = name
        self.price = price
        self.barcode = barcode
        self.description= description
        
    def _repr_(self)->str:
       return f'Item{self.name}'
     

    def buy(self,user):
        self.owner = user.id
        user.budget -= self.price
        db1.session.commit()

    def sell(self,user):
        self.owner = None 
        user.budget += self.price
        db1.session.commit()
