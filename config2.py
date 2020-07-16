from hello import db, Role, User

db.create_all()

roles = [ 'Admin', 'Operator', 'Moderator', 'Pleb' ]

for role in roles:
    print (role)


#admin_role = Role(name='Admin')
#mod_role = Role(name='Moderator')
#user_role = Role(name='User')
#user_john = User(username='peter', role=admin_role)
#user_susan = User(username='maja', role=user_role)
#user_tony = User(username='tony', role=user_role)
#db.session.add(Role(name='foobar'))
#db.session.add(admin_role)
#db.session.add(mod_role)
#db.session.add(user_role)
#db.session.add(user_john)
#db.session.add(user_susan)
#db.session.add(user_tony)
#db.session.commit()
