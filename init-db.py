from hello import db

db.create_all()

admin_role = Role(name='Admin')
from hello import Role, User
user_johnny = User(username='johnny', role=admin_role)
