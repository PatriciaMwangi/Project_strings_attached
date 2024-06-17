import sqlite3

conn = sqlite3.Connection('crotchet.db')
conn.row_factory=sqlite3.Row
cursor=conn.cursor()