import MySQLdb

db = MySQLdb.connect("localhost","root","P@ssw0rd")

checkschema = db.cursor()

#Create images shema
checkschema.execute("DROP SCHEMA IF EXISTS images")
checkschema.execute("CREATE SCHEMA images")

dbi= MySQLdb.connect("localhost","root","P@ssw0rd","images")

with dbi:

    cursor = dbi.cursor()

    # Create iImages table to save imported images (for later comparisons)
    cursor.execute("DROP TABLE IF EXISTS cImages")
    cursor.execute("""CREATE TABLE cImages (
        ID INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
        IMG LONGTEXT,
        IMGDESC LONGTEXT,
        IMGX INT(11),
        IMGY INT(11),
        IMGC TINYINT(1),
        F1 LONGTEXT,
        F2 LONGTEXT,
        F3 LONGTEXT,
        F4 LONGTEXT,
        F5 LONGTEXT,
        F6 LONGTEXT,
        F7 LONGTEXT,
        F8 LONGTEXT,
        F9 LONGTEXT )""")

    # Create cImages table to save compared images (for historical reasons)
    cursor.execute("DROP TABLE IF EXISTS iImages")
    cursor.execute("""CREATE TABLE iImages (
        ID INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
        IMG LONGTEXT,
        IMGDESC LONGTEXT,
        IMGX INT(11),
        IMGY INT(11),
        IMGC TINYINT(1),
        F1 LONGTEXT,
        F2 LONGTEXT,
        F3 LONGTEXT,
        F4 LONGTEXT,
        F5 LONGTEXT,
        F6 LONGTEXT,
        F7 LONGTEXT,
        F8 LONGTEXT,
        F9 LONGTEXT )""")
