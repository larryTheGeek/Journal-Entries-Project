# # http://flask.pocoo.org/docs/0.11/patterns/wtforms/
# class RegistrationForm(Form):
#     username = StringField('Username', [validators.Length(min=4, max=25)])
#     email = StringField('Email Address', [validators.Lenght(min=6, max=35)])
#     password = PasswordField('New Password', [
#         validators.DataRequired(),
#         validators.EqualTo('confirm', message='Passwords must match')
#         ])
#     confirm = PasswordField('Repeat Password')
#     accept_tos = BooleanField('I accept the Terms of Service', [validators.DataRequired()])

# https://navaspot.wordpress.com/2014/06/25/how-to-implement-forgot-password-feature-in-flask/

class ExistingUser(object):
    def __init__(self, message="Username or password doesn't exist"):
        self.message = message

    def __call__(self, form, field):
        if not User.query.filter_by(username=field.data).first() or \
        User.query.filter_by(password=field.data).first():
            raise ValidationError(self.message)

reset_rules = [validators.Required(),
               validators.Email(),
               ExistingUser(message='Email address is not available')
               ]

class ResetPassword(Form):
    email = TextField('Email', validators=reset_rules)

class ResetPasswordSubmit(Form):
    password = PasswordField('Password', validators=custom_validators['edit_password'], )
    confirm = PasswordField('Confirm Password')
