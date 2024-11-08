import os
import psycopg2
from psycopg2 import pool,extras
from urllib.parse import urlparse, parse_qs
from spider.src.utils.common import DATABASE_URL


class PgHelper:
    def __init__(self):
        
        
        # 解析 DATABASE_URL
        parsed_url = urlparse(DATABASE_URL)
        
        # 更安全地提取连接信息
        dbname = parsed_url.path[1:]  # 移除开头的 '/'
        username = parsed_url.username
        password = parsed_url.password
        hostname = parsed_url.hostname
        port = parsed_url.port or 5432  # 如果没有指定端口，默认使用 5432

        self.connection_pool = psycopg2.pool.SimpleConnectionPool(
            1, 20,
            host=hostname,
            port=port,
            dbname=dbname,
            user=username,
            password=password
        )

    def execute_query(self, query, params=None):
        connection = self.connection_pool.getconn()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                connection.commit()
                if cursor.description:
                    return cursor.fetchall()
        except (Exception, psycopg2.Error) as error:
            print(f"Error executing query: {error}")
        finally:
            self.connection_pool.putconn(connection)

    def execute_batch_insert(self, query, params_list):
        connection = self.connection_pool.getconn()
        try:
            with connection.cursor() as cursor:
                psycopg2.extras.execute_batch(cursor, query, params_list)
                connection.commit()
        except (Exception, psycopg2.Error) as error:
            print(f"Error executing batch query: {error}")
        finally:
            self.connection_pool.putconn(connection)

    def insert(self, table, data):
        columns = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        return self.execute_query(query, tuple(data.values()))

    def select(self, table, columns="*", condition=None):
        query = f"SELECT {columns} FROM {table}"
        if condition:
            query += f" WHERE {condition}"
        return self.execute_query(query)

    def update(self, table, data, condition):
        set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {condition}"
        return self.execute_query(query, tuple(data.values()))

    def delete(self, table, condition):
        query = f"DELETE FROM {table} WHERE {condition}"
        return self.execute_query(query)

    def close(self):
        if self.connection_pool:
            self.connection_pool.closeall()

if __name__ == "__main__":
    db = PgHelper()

    # 现在你可以使用 db 对象来执行数据库操作
    results = db.select('room_v2', columns='id, room_id')
    for row in results:
        print(row)

    # 完成后记得关闭连接
    db.close()
