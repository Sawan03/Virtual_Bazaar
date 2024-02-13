from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import Length,EqualTo,DataRequired,Email,ValidationError
from market.module import User

class RegisterForm(FlaskForm):
     
      def validate_username(self,username_to_check): #this function check in our form that validate word are there aftter that it wil check username exist in oour form ii it exist then we will check that same mame userare try to register 
         user  = User.query.filter_by(username = username_to_check.data).first()
         if user:
               raise ValidationError('Username already exists ! please try a different username')
      def validate_email_address(self ,email_address_to_check):
            email_address  = User.query.filter_by(email_address = email_address_to_check.data).first()
            if email_address:
                raise ValidationError('Email Address already exists ! please try a diffrent email address')
      
      
      username = StringField(label='User Name', validators=[Length(min=2,max=30),DataRequired()])
      email_address = StringField(label='Email',validators=[Email(),DataRequired()])
      password1 = PasswordField(label='Password',validators=[Length(min =6),DataRequired()])
      password2 = PasswordField(label='Confirm Password',validators=[EqualTo('password1'),DataRequired()])
      submit = SubmitField(label='Create Account')

    
class LoginForm(FlaskForm):
     username = StringField(label='User Name',validators=[DataRequired()]) 
     password = PasswordField(label='Password',validators=[DataRequired()])  
     submit = SubmitField(label='Sign in')  


class BuyForm(FlaskForm):
      submit = SubmitField(label='Buy Item!') 


class SellForm(FlaskForm):
      submit = SubmitField(label='Sell Item!') 
                 