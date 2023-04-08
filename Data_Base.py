import sqlalchemy

from sqlalchemy.orm import sessionmaker
import psycopg2



DSN = 'postgresql://postgres:qwr1d@localhost:5432/postgres'  # адрес базы
engine = sqlalchemy.create_engine(DSN)  # создаем движок

conn = psycopg2.connect(database='postgres', user='postgres', password='qwr1d')

Session = sessionmaker(bind=engine)


def drop_table():
    with conn.cursor() as cur:
        cur.execute('''
                            drop table data_user;

                        '''
                    )
    conn.commit()
    print('удалена таблица data_user')


def create_table():
    with conn.cursor() as cur:


        cur.execute('''
                create table if not exists data_user(
                    id serial primary key,
                    id_user int,
                    foto_url varchar(250) unique

                    );
            '''
                    )
        conn.commit()
        print('создана таблица data_user')


def save_tabel_data_user(data):
    with conn.cursor() as cur:
        cur.execute('''
                              insert into data_user(id_user,foto_url)
                              values(%s,%s); 

                          ''', (data[0], data[4]))
        conn.commit()
        print('данные внесены')




def send_db(id):
    a = str(id)
    with conn.cursor() as cur:
        cur.execute('''
                select id from data_user where id_user = %s;
            ''', (a,))
        a = cur.fetchone()

        return a


