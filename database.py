import sqlite3

conn=sqlite3.connect('insurance.db')

query="""
create table project
(age integer , region varchar(5), Children integer , Health integer , sex integer , smoker integer , bmi integer , prediction varchar(10))"""

query_to_fetch= """
select * from project
"""
## to create table
cur=conn.cursor()
# cur= conn.cursor()  # cursor sql
# cur.execute(query)

cur.execute(query_to_fetch)  ## cursor is a temporary memory
for record in cur.fetchall():
    print(record)

cur.close()
conn.close()

