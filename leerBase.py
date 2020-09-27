import sqlite3
conn = sqlite3.connect('example.db')
c = conn.cursor()
c.execute("SELECT * FROM pass")
response = c.fetchall()
print("{:^35}{:^35}".format("Email", "Contraña"))
for e, p in response:
    print("{:^35}  {:^35}".format(e, p))
