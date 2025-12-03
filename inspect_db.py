import pymysql
# import psycopg2
import json
from typing import Dict, List, Any

def analyze_mysql_structure(host='localhost', user='root', password='', database=''):
    """Анализ структуры MySQL базы данных"""
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    # cursor = conn.cursor(dictionary=True)

    structure = {
        'database': database,
        'tables': [],
        'relationships': []
    }

    with connection.cursor() as cursor:
        
        # Получаем таблицы
        cursor.execute("""
            SELECT TABLE_NAME, TABLE_ROWS, ENGINE, TABLE_COLLATION
            FROM information_schema.TABLES 
            WHERE TABLE_SCHEMA = %s AND TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_NAME
        """, (database,))
        
        for table in cursor.fetchall():
            table_info = {
                'name': table['TABLE_NAME'],
                'rows': table['TABLE_ROWS'],
                'engine': table['ENGINE'],
                'columns': [],
                'indexes': [],
                'primary_key': []
            }
            
            # Получаем колонки
            cursor.execute("""
                SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, 
                    COLUMN_DEFAULT, COLUMN_KEY, EXTRA, COLUMN_COMMENT
                FROM information_schema.COLUMNS 
                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
                ORDER BY ORDINAL_POSITION
            """, (database, table['name']))
            
            for col in cursor.fetchall():
                column_info = {
                    'name': col['COLUMN_NAME'],
                    'type': col['DATA_TYPE'],
                    'nullable': col['IS_NULLABLE'] == 'YES',
                    'default': col['COLUMN_DEFAULT'],
                    'key': col['COLUMN_KEY'],
                    'extra': col['EXTRA']
                }
                if col['COLUMN_KEY'] == 'PRI':
                    table_info['primary_key'].append(col['COLUMN_NAME'])
                table_info['columns'].append(column_info)
            
            # Получаем внешние ключи
            cursor.execute("""
                SELECT COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
                FROM information_schema.KEY_COLUMN_USAGE
                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s 
                    AND REFERENCED_TABLE_NAME IS NOT NULL
            """, (database, table['name']))
            
            for fk in cursor.fetchall():
                relationship = {
                    'from_table': table['name'],
                    'from_column': fk['COLUMN_NAME'],
                    'to_table': fk['REFERENCED_TABLE_NAME'],
                    'to_column': fk['REFERENCED_COLUMN_NAME']
                }
                structure['relationships'].append(relationship)
            
            structure['tables'].append(table_info)
        
        cursor.close()
        conn.close()
        return structure

def analyze_postgres_structure(host='localhost', user='postgres', password='', database=''):
    """Анализ структуры PostgreSQL базы данных"""
    conn = psycopg2.connect(
        host=host, user=user, password=password, database=database
    )
    cursor = conn.cursor()
    
    structure = {
        'database': database,
        'tables': [],
        'relationships': []
    }
    
    # Получаем таблицы
    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables 
        WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
        ORDER BY table_name
    """)
    
    for (table_name,) in cursor.fetchall():
        table_info = {
            'name': table_name,
            'columns': [],
            'primary_key': [],
            'indexes': []
        }
        
        # Получаем колонки
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, 
                   column_default, is_identity
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = %s
            ORDER BY ordinal_position
        """, (table_name,))
        
        for col in cursor.fetchall():
            column_info = {
                'name': col[0],
                'type': col[1],
                'nullable': col[2] == 'YES',
                'default': col[3],
                'identity': col[4]
            }
            table_info['columns'].append(column_info)
        
        # Получаем первичные ключи
        cursor.execute("""
            SELECT kcu.column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
                ON tc.constraint_name = kcu.constraint_name
            WHERE tc.table_schema = 'public' 
                AND tc.table_name = %s 
                AND tc.constraint_type = 'PRIMARY KEY'
        """, (table_name,))
        
        for (pk_col,) in cursor.fetchall():
            table_info['primary_key'].append(pk_col)
        
        # Получаем внешние ключи
        cursor.execute("""
            SELECT kcu.column_name, ccu.table_name, ccu.column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
                ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage ccu
                ON ccu.constraint_name = tc.constraint_name
            WHERE tc.table_schema = 'public' 
                AND tc.table_name = %s 
                AND tc.constraint_type = 'FOREIGN KEY'
        """, (table_name,))
        
        for fk in cursor.fetchall():
            relationship = {
                'from_table': table_name,
                'from_column': fk[0],
                'to_table': fk[1],
                'to_column': fk[2]
            }
            structure['relationships'].append(relationship)
        
        structure['tables'].append(table_info)
    
    cursor.close()
    conn.close()
    return structure

# Пример использования
if __name__ == "__main__":
    # Для MySQL
    mysql_structure = analyze_mysql_structure(
        host='localhost', user='root', password='HfgFGty217GF', database='vitte'
    )
    
    # # Для PostgreSQL
    # postgres_structure = analyze_postgres_structure(
    #     host='localhost', user='postgres', password='HfgFGty217GF', database='vitte'
    # )
    
    # Сохраняем результаты
    with open('mysql_structure.json', 'w', encoding='utf-8') as f:
        json.dump(mysql_structure, f, indent=2, ensure_ascii=False)
    
    with open('postgres_structure.json', 'w', encoding='utf-8') as f:
        json.dump(postgres_structure, f, indent=2, ensure_ascii=False)
    
    print("Структура базы данных сохранена в JSON файлы")