from peewee import *

bloop = 'gautsi'
bleep = 'gautsi'
dloop = '173.255.208.109'
dleep = 'groups_on_twitter'

mysql_db = MySQLDatabase(user= bloop, password= bleep, host = dloop, database = dleep, port=3306)


class BaseModel(Model):
    class Meta:
        database = mysql_db


class Users(BaseModel):
	user_id = BigIntegerField(primary_key=True)
	num_follows = BigIntegerField(null=True)
	num_friends = BigIntegerField(null=True)
	rank = IntegerField(null=True, default = 0)
	screen_name = CharField(max_length=80, null=True)
	group = CharField(max_length=80, null=True)

	class Meta:
	    db_table = 'users'


class Arrows(BaseModel):
	follow = ForeignKeyField(db_column='follow_id', null=True, rel_model=Users, related_name = 'out_arrows')
	lead = ForeignKeyField(db_column='lead_id', null=True, rel_model=Users, related_name = 'in_arrows')
	group = CharField(max_length=80, null=True)

	class Meta:
	    db_table = 'arrows'

class Bads(BaseModel):
	user_id = BigIntegerField(primary_key=True)
	group = CharField(max_length=80, null=True)





def add_group_to_db(fs, group_name, debug = False):

	#insert the users
	for user_list in fs:
		for user in user_list:

			#get the desired data from the dictionary
			un = user['screen_name']
			idn = user['id']
			fon = user['followers_count']
			frn = user['friends_count'] 

			#check to see if idn is in Users
			result = Users.select().where(Users.user_id == idn)

			#if result's count is 0, then idn is not in users
			if result.count() == 0:
			
				#insert into Users
				if debug:
					print 'inserting ' + un + ' into '+search+'s'

				Users.insert(user_id = idn, num_follows = fon, num_friends = frn, screen_name = un, group = group_name).execute()



#adds arrows to the database
#input: idnumber of source user, a list of target users, and the group_name
#adds arrow (idnumber, i) to Arrows for i in friendlist if i is in the grou_name group of Users
def add_arrows_to_db(idnumber, friendlist, group_name):

	#go through the friend list
	for i in friendlist:

		#if i is in Users and in the right group:
		if Users.select().where(Users.group == group_name, Users.user_id == i).count() > 0:
			
			#insert (idn, i) into Arrows
			Arrows.insert(follow = idnumber, lead = i, group = group_name).execute()


