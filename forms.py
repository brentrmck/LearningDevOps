from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField, DecimalField, TextAreaField
from wtforms.validators import InputRequired, NumberRange

class MerchForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    quantity = IntegerField('Quantity', validators=[InputRequired(), NumberRange(min=0)])
    price = DecimalField('Price', validators=[InputRequired(), NumberRange(min=0)])
    description = TextAreaField('Description', validators=[InputRequired()])
