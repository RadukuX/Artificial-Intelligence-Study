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
