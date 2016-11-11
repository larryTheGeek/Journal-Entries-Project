from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

class User(db.Model): #one to many relationship
    """User class - a user has many entries"""

    __tablename__ = "users"

    # Users log into the app through a username and password. The can provide an
    # email to request their password if it's forgotten 

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)    
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False) #does this need to be hashed? <input type = password>
    email = db.Column(db.String(100), nullable=True) # <input type = email>

    def __repr__(self):
        """Human readable when printed"""

        return "<Username is <%s>, email address is <%s>, and password is \
        shhhhh we don't tell>" % (self.user_id, self.username)

    @classmethod
    def get_by_username(cls, username):
        """Get the number of entries for the username"""

        return User.query.filter_by(username=username).count()

class Tag(db.Model): #one to many
    """Journal entries can have multiple tags"""

    __tablename__ = "tags"

    tag = db.Column(db.String(25), default='contemplative', primary_key=True)
    # Structuring this correctly? The entry can have up to five tags 
    tag_2 = db.Column(db.String(25), nullable=True)
    tag_3 = db.Column(db.String(25), nullable=True)
    tag_4 = db.Column(db.String(25), nullable=True)
    tag_5 = db.Column(db.String(25), nullable=True)
    tag_6 = db.Column(db.String(25), nullable=True)

    
    @classmethod
    def get_by_tag_type(cls, tag):
        """Get all the entries matching that tag"""

        return cls.query.filter_by(tag=tag).all()

class Entry(db.Model): #many to one
    """A user can have multiple entries"""

    __tablename__ = "entries"

    entry_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    entry_date = db.Column(db.DateTime, nullable=False) #this can be queried later 
    entry_body = db.Column(db.String(1000), nullable=False)
    username = db.Column(db.ForeignKey('users.user_id'), nullable=False)
    tag = db.Column(db.ForeignKey('tags.tag'), nullable=False) 
    # a one to many relationship places the fk on the child table referencing the parent

    user = db.relationship('User', backref='users') 
    tag = db.relationship('Tag', backref='tags')

    def __repr__(self):
        """Human readable when printed"""

        return "<Entry id is <%s> with Datetime <%s> for username <%s>\
        " % (self.entry_id, self.entry_date, self.username)



class EntryTag(db.Model):
    """Association table for the many to many relationship between entries and tags"""

    __tablename__ = "entry_tags"

    entrytag_id = db.Column(db.Integer, primary_key=True)
    entry_id = db.Column(db.Integer, db.ForeignKey('entries.entry_id'), nullable=False)
    tag = db.Column(db.String(50), db.ForeignKey('tags.tag'), nullable=False)

    entry = db.relationship('Entry', backref='entries')
    tag = db.relationship('Tag', backref='tags')

def connect_to_db(app, db_uri="postgresql:///entry"):
    """Connects to the database"""

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.app = app
    db.init_app(app)

if __name__ == "__main__":

    from server import app
    connect_to_db(app)

    print "Connected to DB"

