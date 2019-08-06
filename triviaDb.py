import sqlite3
import pandas as pd

class triviaDb:
    def __init__(self):
        self.database = ""
        super(self.__class__, self).__init__()
#        self.create_connection(self.database)

    def create_connection(self, db_file):
        """ create a database connection to the SQLite database
            specified by the db_file
        :param db_file: database file
        :return: Connection object or None
        """
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except ErException as e:
            print(e)
            return e

        return None

    def update_question(self, conn, question):
        """
        update has_been_used of a trivia question
        :param conn:
        :param question rowid:
        """
        sql = ''' UPDATE go_time_trivia
                SET has_been_used = 1
                WHERE rowid = ?'''
        try:
            cur = conn.cursor()
            cur.execute(sql, question)
            conn.commit()
        except Exception as e:
            print(e)

    def reset_question_list(self, conn):
        """
        Reset the has been used toggle for all trivia questions
        :param conn:
        """

        sql = ''' UPDATE go_time_trivia
                SET has_been_used = 0'''
        try:
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
        except Exception as e:
            print(e)

    def test(self):
        database = "/Users/fcorn/tmp/quizShow.db"

        # create a database connection
        conn = create_connection(database)

        reset_question_list(conn)

        # Get random question list
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        questionList =  '''
            SELECT
                g.rowid,
                g.QUESTION,
                g.yellow,
                g.green,
                g.red,
                g.blue,
                g.correct_answer
            FROM
                go_time_trivia AS g
            WHERE
                g.has_been_used = 0
            ORDER BY
                RANDOM() ASC
        '''
        cursor.execute(questionList)

        rows = cursor.fetchall()
        for row in rows:
            # Ask the question

            # Mark the question as used
            update_question(conn, (row[0],))

            # print the question
            print('{0}: {1}, {2}, {3}, {4}, {5}, {6}'.format(
                row['rowid'], row['question'], row['yellow'], row['green'], row['red'], row['blue'], row['correct_answer']))

        # Close database connection
        conn.close()


if __name__ == '__main__':              # if we're running file directly and not importing it
    test()                              # run the main function
