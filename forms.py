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
