import os
from django.db import models
import psycopg2
from postgres_copy import CopyMapping

host = 'localhost'
port = ''
dbname = 'dbsisred'
username = 'usdbgallery'
password = 'Abcd123#'

with open('D:\\INFORMACION CREG\\Estados.csv','wb+') as destination:
            for chunk in inventory_file.chunks():
                destination.write(chunk)
        print "Inventory Saved."
        reader = csv.reader(open('Estados.csv','rb'))
        count = 0 
        for row in reader:
            if count == 0:
                count=1
                continue
            count = count +1
            try:
                self.cur.execute("""INSERT into  public.sisred_app_estado values(%s,%s)""",(row[0],row[1]))
                print "INSERT into public.sisred_app_estado values('",row[0],"','",row[1])"
            except:
                pass
        print count
        
        self.cur
        self.db_conn.commit()

        print "file uploades"