from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, FloatField, SubmitField
from wtforms.validators import DataRequired

class TransactionForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    details = StringField('Details', validators=[DataRequired()])
    expected_date = DateTimeField('Expected Date', validators=[DataRequired()])
    payday = DateTimeField('Payday', validators=[DataRequired()])
    recurrence = StringField('Recurrence', validators=[DataRequired()])
    expected_value = FloatField('Expected Value', validators=[DataRequired()])
    paid_value = FloatField('Paid Value', validators=[DataRequired()])
    submit = SubmitField('Submit')