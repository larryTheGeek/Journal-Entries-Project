from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):  # one to many relationship between User - Entry
    """User class - a user has many entries"""

    __tablename__ = "users"

    # Users log into the app through a username and password. The can provide an
    # email to request their password if it's forgotten

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)

    username = db.Column(db.String(100),
                         nullable=False,
                         unique=True)

    password = db.Column(db.String(100),
                         nullable=False)

    email = db.Column(db.String(100))

    entries = db.relationship('Entry', backref='users', lazy='dynamic')  # lazy means you can find out how many entries per user

    def __repr__(self):
        """Human readable when printed"""

        return "<User_id is <%s>, username is <%s>" % (self.user_id, self.username)

    @classmethod
    def get_by_username(cls, username):
        """Get the number of entries for the username"""

        return User.query.filter_by(username=username).count()

    # def get_token(self, expiration=100):
    #     s = Serializer(current_app.config['SECRET_KEY'], expiration)
    #     return s.dumps({'user': self.id}).decode('utf-8')

    # @staticmethod
    # def verify_token(token):
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     try:
    #         data = s.loads(token)
    #     except:
    #         return None
    #     id = data.get('user')
    #     if id:
    #         return User.query.get(id)
    #     return None


class Entry(db.Model):  # many to many relationship with tags, many to one with Users
    """A user can have multiple entries"""

    __tablename__ = "entries"

    entry_id = db.Column(db.Integer, 
                         autoincrement=True, 
                         primary_key=True)
    
    entry_date = db.Column(db.DateTime, 
                           nullable=True)  # this can be queried later
    
    entry_title = db.Column(db.String(50))
    
    entry_body = db.Column(db.String(1000), 
                           nullable=False)
    
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.user_id'), 
                        nullable=True)

    user = db.relationship('User', backref='users')

    # def __repr__(self):
    #     """Human readable when printed"""
    #     return "<Entry id is <%s> with Datetime <%s> for username <%s>\
    #     " % (self.entry_id, self.entry_date)

class Tag(db.Model):  # many to many relationship between Tags and Entries
    """Journal entries can have multiple tags"""

    __tablename__ = "tags"

    tag_1 = db.Column(db.String(25), 
                      default='contemplative', 
                      primary_key=True)
    
    # Structuring this correctly? The entry can have up to five tags
    tag_2 = db.Column(db.String(25), 
                      nullable=True)
    
    tag_3 = db.Column(db.String(25), 
                      nullable=True)
    
    tag_4 = db.Column(db.String(25), 
                      nullable=True)
    
    tag_5 = db.Column(db.String(25), 
                      nullable=True)
    
    tag_6 = db.Column(db.String(25), 
                      nullable=True)

    @classmethod
    def get_by_tag_type(cls, tag):
        """Get all the entries matching that tag"""

        return cls.query.filter_by(tag=tag).all()


# Association Table
class EntryTag(db.Model):
    """Association table for the many to many relationship between entries and tags"""

    __tablename__ = "entry_tags"

    entrytag_id = db.Column(db.Integer, 
                            primary_key=True, 
                            autoincrement=True)

    entry_id = db.Column(db.Integer, 
                         db.ForeignKey('entries.entry_id'), 
                         nullable=False)

    tag_1 = db.Column(db.String(50), 
                      db.ForeignKey('tags.tag_1'), 
                      nullable=False)

    entry = db.relationship('Entry', backref='entries')

    tag = db.relationship('Tag', backref='tags')


def connect_to_db(app, db_uri="postgresql:///entry"):
    """Connects to the database"""

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = app
    db.init_app(app)

if __name__ == "__main__":

    from server import app
    connect_to_db(app, "postgresql:///entry")

    print "Connected to DB"

# Example data for tests

def example_data():

    """Create some sample data for test.py"""

    # Clear data 
    User.query.delete()
    Entry.query.delete()
    Tag.query.delete()
    EntryTag.query.delete()

    exuser1 = User(1, 'fluffykitty', 'password123', 'youknowit@aol.com')

    exentry1 = Entry(1, '2016-11-11 12:01AM', 'Update on my day', 'It was a good day and I felt like I could take on the world', 1)

    extag1 = Tag('happy')

    exentrytag = EntryTag(1, 1, 'happy')

    db.session.add_all()
    db.session.commit()
