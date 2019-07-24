import psycopg2


def get_record(context, query):
    connection = None
    try:
        connection = connect(context)
        cursor = connection.cursor()
        cursor.execute(query)
        record = cursor.fetchall()
        return record
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)
    finally:
        if connection:
            cursor.close()


def connect(context):
    connection = psycopg2.connect(user=context.postgres_user,
                                  password=context.postgres_pass,
                                  host=context.postgres_host,
                                  port=context.postgres_port,
                                  database=context.postgres_db)

    print(connection.get_dsn_parameters(), "\n")
    return connection
