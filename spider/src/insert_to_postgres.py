import psycopg2
import os
import re

# PostgreSQL 连接信息
DB_HOST = "159.138.107.78"
DB_PORT = 5432
DB_NAME = "demo"
DB_USER = "demo"
DB_PASSWORD = "tgscan1024"

# SQL 文件路径
SQL_FILE_PATH = "D:\project\git\\tgscan\\api-server\\src\\main\\resources\\sql\\20241218\\room_v2.sql"



def extract_insert_statements(file_path):
    """
    从SQL文件中逐行解析并提取完整的INSERT语句。
    :param file_path: SQL文件路径
    :return: 提取的INSERT语句列表
    """
    statements = []
    current_statement = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            # 去除行两端的空白字符
            line = line.strip()

            # 如果行以 INSERT INTO 开头，可能是新语句
            if line.startswith("INSERT INTO"):
                if current_statement:  # 如果有未完成的语句，加入列表
                    statements.append(" ".join(current_statement))
                    current_statement = []
                current_statement.append(line)
            else:
                # 否则继续拼接当前语句
                current_statement.append(line)

            # 如果行以 `);` 结尾，说明当前语句完成
            if line.endswith(");"):
                statements.append(" ".join(current_statement))
                current_statement = []

    # 检查是否有剩余未完成的语句
    if current_statement:
        statements.append(" ".join(current_statement))

    return statements


def batch_insert(statements, batch_size=1000):
    """
    批量插入SQL语句到PostgreSQL表中。
    :param statements: 提取的SQL INSERT语句列表
    :param batch_size: 每次批量插入的行数
    """
    try:
        # 连接数据库
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()

        batch = []
        for i, statement in enumerate(statements, start=1):
            # print(statement)
            batch.append(statement)
            if len(batch) == batch_size or i == len(statements):
                cursor.execute("BEGIN;")
                for stmt in batch:
                    cursor.execute(stmt)
                cursor.execute("COMMIT;")
                batch = []  # 清空批量缓存
                print(f"Inserted {i}/{len(statements)} records...")

        print("All data inserted successfully!")

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


if __name__ == "__main__":
    # 提取完整的INSERT语句
    statements = extract_insert_statements(SQL_FILE_PATH)

    if statements:
        print(f"Extracted {len(statements)} INSERT statements.")
        batch_insert(statements)
    else:
        print("No valid INSERT statements found.")

    # batch_insert(["INSERT INTO \"room_v2\" (\"id\", \"room_id\", \"link\", \"name\", \"jhi_desc\", \"member_cnt\", \"msg_cnt\", \"type\", \"status\", \"collected_at\", \"lang\", \"tags\", \"extra\", \"icon\") VALUES (17684, 'ucwchat', 'https://t.me/ucwchat', 'Чат UCW 🇺🇦', '❗️У чаті заборонено: • Обговорення інших чатів про реслінг; • Флуд, спам; • Погрози та образи; • 18+ контент; • Спойлерити шоу (можна після 12 годин з кінця шоу); • Випрошування грошей.', 56, NULL, 'GROUP', 'COLLECTED', '2024-12-14 10:45:24', 'UK', '', '{''popularity'': 6081, ''image'': ''7cbbf1553c73885616b8ebabbf827476b83334aa0910557a7a59e23c3742dab32f773246feaf114de7ba489fcd8433ddde6bd816e36f183ec32b4eb4f68d7f1c.jpg'', ''status_change'': ''down'', ''source'': ''combot''}', 'icon_ucwchat.jpg');"])
