import twittersearch as ts
from twython import Twython



twy = Twython(APP_KEY, APP_SECRET)	

#getting the group from twitter
def get_group_from_twitter(group_name = "comedian", debug = False):

	fs = []

	for i in xrange(50):
		if debug:
			print 'getting page' + str(i+1)
		fs.append(ts.fetchsamples(i + 1, search = group_name))

	fs = [i[0] for i in fs]

	return fs


#finding arrows from twitter
#returns the list of user_ids of out neighbors of idnumber from the cursor page, and the next cursor
def FindArrows(idnumber = None, cursor = -1):

	#get the friends list
	data_dict = twy.get_friends_ids(user_id = idnumber, cursor = cursor)
	frl = data_dict['ids']

	return frl, data_dict['next_cursor']
	


