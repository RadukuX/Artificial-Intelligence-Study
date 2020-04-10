from flaskai.repository.db_connection import DbConnection


class TeamRepository:

    def get_info(self, team_id):   
        conn = DbConnection().create_connection(DbConnection.database)
        sql = ''' SELECT * FROM extra_data WHERE team_id=? LIMIT 10; '''
        with conn:
            cursor = conn.cursor()
            result = {}
            cursor.execute(sql, [team_id])
            counter = 0
            for i, row in enumerate(cursor):
                year = row[1]
                investment = row[2]
                age = row[3]
                wins = row[4]
                draws = row[5]
                defeats = row[6]
                place = row[7]
                info = [year, investment, age, wins, draws, defeats, place]
                season = 'season' + str(counter)
                result[season] = info
                counter = counter + 1
            cursor.close()
            return result

    def get_team_name(self, team_id):
        conn = DbConnection().create_connection(DbConnection.database)
        sql = ''' SELECT name FROM team WHERE id=? '''
        with conn:
            cursor = conn.cursor()
            cursor.execute(sql, [team_id])
            name = cursor.fetchall()
            cursor.close()
            return name[0][0]
    
    def get_team_live(self, team_name, team_id):
        conn = DbConnection().create_connection(DbConnection.database)
        sql = ''' SELECT DISTINCT opponent FROM results WHERE opponent LIKE ? AND team_id=? LIMIT 1'''.format(team_name)
        with conn:
            cursor = conn.cursor()
            cursor.execute(sql, [ '%' + team_name + '%', team_id])
            nr_of_opponents = cursor.fetchall()
            cursor.close()
            return nr_of_opponents

    def get_team_b(self, my_team):
        conn = DbConnection().create_connection(DbConnection.database)
        sql = ''' SELECT DISTINCT name FROM team WHERE name LIKE ? LIMIT 1'''
        with conn:
            cursor = conn.cursor()
            cursor.execute(sql, ['%' + my_team + '%'])
            my_team = cursor.fetchall()
            cursor.close()
            print(my_team)
            return my_team