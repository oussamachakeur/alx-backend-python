#!/usr/bin/python3

seed = __import__('seed')

# Step 1: Connect to MySQL server (no specific DB yet)
connection = seed.connect_db()
if connection:
    seed.create_database(connection)
    connection.close()
    print("connection successful")

    # Step 2: Connect to the ALX_prodev database
    connection = seed.connect_to_prodev()

    if connection:
        # Step 3: Create the user_data table
        seed.create_table(connection)

        # Step 4: Insert data from CSV
        seed.insert_data(connection, 'user_data.csv')

        # Step 5: Print some data to verify
        cursor = connection.cursor()

        # Check if database exists (should already be true)
        cursor.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'ALX_prodev';")
        result = cursor.fetchone()
        if result:
            print("Database ALX_prodev is present")

        # Fetch and print first 5 rows
        cursor.execute("SELECT * FROM user_data LIMIT 5;")
        rows = cursor.fetchall()
        print(rows)

        cursor.close()
