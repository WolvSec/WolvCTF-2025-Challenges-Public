import sqlite3
snacks = [
    {
        'name': 'wctf{the_v01d_hungers_4_m0r3_paper_plates_8626946984}',
        'image': 'uploads/flag.png',
        'count': 1,
    },
    {
        'name': 'dominos',
        'image': 'uploads/dominos1.png',
        'count': 20,
    },
    {
        'name': 'littlecaesars',
        'image': 'uploads/lc1.png',
        'count': 4,
    },
    {
        'name': 'pizzahut',
        'image': 'uploads/ph1.png',
        'count': 1,
    },
]


con = sqlite3.connect('void.db')
cur = con.cursor()
cur.execute("CREATE TABLE snacks(name, image, count)")

for snack in snacks:
    cur.execute(f"INSERT INTO snacks (name, image, count) VALUES(?,?,?)",[snack['name'], snack['image'], snack['count']])

con.commit()