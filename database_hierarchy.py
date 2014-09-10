import psycopg2

class db_sto_grad_descent:

	def __init__(self, dbname = "comedians_on_twitter", username = "gautam", users = "comedians", arrows = "arrows"):

		#save the names of the tables
		self.users = users
		self.arrows = arrows
		
		#connect to the database
		self.conn = psycopg2.connect("dbname={} user={}".format(dbname, username))
		self.cur = self.conn.cursor()


		#make the rank column
		self.cur.execute("alter table {} add column rank int default 0;".format(users))


		#commit the changes
		self.conn.commit()



		#get the number of users
		self.cur.execute("select count(*) from {};".format(users))

		result = self.cur.fetchone()
	
		self.num_users = int(result[0])


		#get the number of arrows
		self.cur.execute("select count(*) from {};".format(arrows))

		result = self.cur.fetchone()
	
		self.num_arrows = int(result[0])


		#which user to descend on next (modulo the number of users, plus 1)
		self.user_number = 0

		self.passes = 0


		#the list of hierarchy scores after each iteration of the descent algorithm
		self.hierarchy_list = [0]

		#commit the changes
		self.conn.commit()



	#one iteration of the descent algorithm
	def descend(self):

		#get the id and rank of the user to descend on
		self.cur.execute("select id, rank from {} where my_id = {}".format(self.users, (self.user_number % self.num_users) + 1))

		result = self.cur.fetchone()

		idnumber, rank = int(result[0]), int(result[1])


		#count the relevant in and out neighbors:
		#out neighbors with rank <= rank + 1
		self.cur.execute("select count(*) from {} as u, {} as a where a.follow_id = {} and u.id = a.lead_id and u.rank <= {} + 1".format(self.users, self.arrows, idnumber, rank))

		result = self.cur.fetchone()

		small_out = int(result[0])


		#out neighbors with rank <= rank
		self.cur.execute("select count(*) from {} as u, {} as a where a.follow_id = {} and u.id = a.lead_id and u.rank <= {}".format(self.users, self.arrows, idnumber, rank))

		result = self.cur.fetchone()

		smaller_out = int(result[0])


		#in neighbors with rank >= rank - 1
		self.cur.execute("select count(*) from {} as u, {} as a where a.lead_id = {} and u.id = a.follow_id and u.rank >= {} - 1".format(self.users, self.arrows, idnumber, rank))

		result = self.cur.fetchone()

		large_in = int(result[0])


		#in neighbors with rank >= rank
		self.cur.execute("select count(*) from {} as u, {} as a where a.lead_id = {} and u.id = a.follow_id and u.rank >= {}".format(self.users, self.arrows, idnumber, rank))

		result = self.cur.fetchone()

		larger_in = int(result[0])


        #pressure_down is the decrease in agony if the rank of this vertex is decreased by 1
		pressure_down = smaller_out - large_in

        #pressure_up is the decrease in agony if the rank of this vertex is increased by 1
		pressure_up = larger_in - small_out



		#if there is nonnegative pressure down greater than the pressure up, go down
		if pressure_down > pressure_up and pressure_down >= 0:

			#decrease the rank of this user
			self.cur.execute("update {} set rank = {} where id = {}".format(self.users, rank - 1, idnumber))


			#add the new hierarchy score to the list
			self.hierarchy_list += [self.hierarchy_list[-1] + pressure_down/float(self.num_arrows)]


		#else if there is nonnegative pressure up greater than the pressure up, go up    
		elif pressure_up > pressure_down and pressure_up >= 0:

			#increase the rank of this user
			self.cur.execute("update {} set rank = {} where id = {}".format(self.users, rank + 1, idnumber))

			#add the new hierarchy score to the list
			self.hierarchy_list += [self.hierarchy_list[-1] + pressure_up/float(self.num_arrows)]


		#otherwise, changing the rank doesn't help and add the current hierarchy score to the list        
		else:
			self.hierarchy_list += [self.hierarchy_list[-1]]

		#update the user number
		self.user_number += 1

		#update passes number
		if self.user_number > self.num_users:
			
			self.passes += 1
			
			print "passed! " + str(self.passes)

			self.user_number = 0
			
				

		#commit the changes
		self.conn.commit()

	#descend until a full pass through the users doesn't change the hierarchy
	def descent(self):
	
		stop = False

		while not stop:

			self.descend()

			if self.passes > 0 and self.hierarchy_list[-1] == self.hierarchy_list[-self.num_users]:
				stop = True



	#close the connection
	def close(self):
		self.cur.close()
		self.conn.close()

