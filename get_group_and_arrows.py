from twitter_tools import *
from database_tools import *


group_name = "tech"

path = "/home/gautam/Dropbox/programming_projects/twitter2/groups/peewee/"

#Has the group already been inserted into users?

if Users.select().where(Users.group == group_name).count() == 0:

	#If not,
	#Step -1: get group users from twitter

	fs = get_group_from_twitter(group_name = group_name)

	#Step 0: insert group into database
	
	add_group_to_db(fs = fs, group_name = group_name)

else:
	
	#If yes,
	#Step 1: get the current user/cursor
	
	#If no arrows have been inserted:
	if Arrows.select().where(Arrows.group == group_name).count() == 0:

		#Make a file will store the current user id and cursor
		write_number_file = open(path + group_name+'_write_num', 'w')

		first_id = Users.select(fn.Min(Users.user_id)).where(Users.group == group_name).scalar()

		write_number_file.write(str(first_id) + ' -1')
		write_number_file.close()

	#get the current id and cursor from the write number file
	write_number_file = open(path + group_name+'_write_num', 'r')
	write_id, cursor_number = [int(i) for i in write_number_file.readline().split()]

	write_number_file.close()

	#get the arrow list and next cursor from twitter if you can, and add them to the database
	try:
		arrow_list, next_cursor = FindArrows(idnumber = write_id, cursor = cursor_number)
		add_arrows_to_db(idnumber = write_id, friendlist = arrow_list, group_name = group_name)

	#if you can't, print the error, put write_id into Bads, set cursor to 0
	except Exception, err:
		print Exception, err
		Bads.insert(user_id = write_id, group = group_name)
		next_cursor = 0

	#update the write number file
	write_number_file = open(path + group_name+'_write_num', 'w')
	
	if next_cursor == 0:
		#move on to the next user
		next_id = Users.select(fn.Min(Users.user_id)).where(Users.group == group_name, Users.user_id > write_id).scalar()

		write_number_file.write(str(next_id) + ' -1')
	else:
		write_number_file.write(str(write_id) + ' ' + str(next_cursor))
	write_number_file.close()

	



