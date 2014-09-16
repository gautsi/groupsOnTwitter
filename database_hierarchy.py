import pymysql

bl = 'gautsi'
bw = 'gautsi'
dl = '173.255.208.109'
dw = 'groups_on_twitter'

mysql_db = MySQLDatabase(user=bl, password=bw, host=dl, database=dw, port=3306)


class db_sto_grad_descent:

    def __init__(self, group='writer'):

        #save the group name
        self.group = group

        #connect to the database
        self.cur = mysql_db.cursor()

        #set the rank to 0
        self.cur.execute("update users as u set u.rank = 0 where "
                         "u.group = '{}'".format(self.group))

        #get the number of users
        self.cur.execute("select count(*) from users as u "
                         "where u.group = '{}';".format(self.group))

        result = self.cur.fetchone()

        self.num_users = int(result[0])

        #get the number of arrows
        self.cur.execute("select count(*) from arrows as a "
                         "where a.group = '{}';".format(self.group))

        result = self.cur.fetchone()

        self.num_arrows = int(result[0])

        #which user to descend on next
        self.cur.execute("select min(u.user_id) from users as u "
                         "where u.group = '{}';".format(self.group))

        result = self.cur.fetchone()

        self.first_id = int(result[0])

        self.user_id = self.first_id

        #number of passes
        self.passes = 0

        #the list of hierarchy scores after each iteration
        #of the descent algorithm
        self.hierarchy_list = [0]

        #commit the changes
        mysql_db.commit()

    #one iteration of the descent algorithm
    def descend(self):

        #get the rank of the user to descend on
        self.cur.execute("select u.rank from users as u "
                         "where u.user_id = {} "
                         "and u.group = '{}'".format(self.user_id, self.group))

        result = self.cur.fetchone()

        rank = int(result[0])

        #count the relevant in and out neighbors:
        #out neighbors with rank <= rank + 1
        self.cur.execute("select count(*) from users as u, arrows as a "
                         "where a.follow_id = {} and u.user_id = a.lead_id "
                         "and u.rank <= {} + 1 "
                         "and u.group = '{}'".format(self.user_id,
                                                     rank, self.group))

        result = self.cur.fetchone()

        small_out = int(result[0])

        #out neighbors with rank <= rank
        self.cur.execute("select count(*) from users as u, arrows as a "
                         "where a.follow_id = {} and u.user_id = a.lead_id "
                         "and u.rank <= {} "
                         "and u.group = '{}'".format(self.user_id,
                                                     rank, self.group))

        result = self.cur.fetchone()

        smaller_out = int(result[0])

        #in neighbors with rank >= rank - 1
        self.cur.execute("select count(*) from users as u, arrows as a "
                         "where a.lead_id = {} and u.user_id = a.follow_id "
                         "and u.rank >= {} - 1 "
                         "and u.group = '{}'".format(self.user_id,
                                                     rank, self.group))

        result = self.cur.fetchone()

        large_in = int(result[0])

        #in neighbors with rank >= rank
        self.cur.execute("select count(*) from users as u, arrows as a "
                         "where a.lead_id = {} and u.user_id = a.follow_id "
                         "and u.rank >= {} "
                         "and u.group = '{}'".format(self.user_id,
                                                     rank, self.group))

        result = self.cur.fetchone()

        larger_in = int(result[0])

        #pressure_down is the decrease in agony
        #if the rank of this vertex is decreased by 1
        pressure_down = smaller_out - large_in

        #pressure_up is the decrease in agony
        #if the rank of this vertex is increased by 1
        pressure_up = larger_in - small_out

        #if there is nonnegative pressure down greater
        #than the pressure up, go down
        if pressure_down > pressure_up and pressure_down >= 0:

            #decrease the rank of this user
            self.cur.execute("update users as u set u.rank = {} "
                             "where u.user_id = {}".format(rank - 1,
                                                           self.user_id))

            #add the new hierarchy score to the list
            hier_change = pressure_down/float(self.num_arrows)
            self.hierarchy_list += [self.hierarchy_list[-1] + hier_change]

        #else if there is nonnegative pressure up greater
        #than the pressure up, go up
        elif pressure_up > pressure_down and pressure_up >= 0:

            #increase the rank of this user
            self.cur.execute("update users as u set u.rank = {} "
                             "where u.user_id = {}".format(rank + 1,
                                                           self.user_id))

            #add the new hierarchy score to the list
            hier_change = pressure_up/float(self.num_arrows)
            self.hierarchy_list += [self.hierarchy_list[-1] + hier_change]

        #otherwise, changing the rank doesn't help and add the current
        #hierarchy score to the list
        else:
            self.hierarchy_list += [self.hierarchy_list[-1]]

        #update the user id
        self.cur.execute("select min(u.user_id) from users as u "
                         "where u.user_id > {} "
                         "and u.group = '{}';".format(self.user_id,
                                                      self.group))

        result = self.cur.fetchone()

        #if at the end
        if result[0] is None:

            #update passes number
            self.passes += 1

            print "passed! " + str(self.passes)

            self.user_id = self.first_id

        else:
            self.user_id = int(result[0])

        #commit the changes
        mysql_db.commit()

    #descend until a full pass through the users doesn't
    #change the hierarchy
    def descent(self):

        stop = False

        while not stop:

            self.descend()

            if self.passes > 0:
                prev_pass_hier = self.hierarchy_list[-self.num_users]
            if self.hierarchy_list[-1] == prev_pass_hier:
                stop = True

    #close the connection
    def close(self):
        self.cur.close()
        mysql_db.close()
