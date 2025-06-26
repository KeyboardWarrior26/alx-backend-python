#!/usr/bin/python3
seed = __import__('seed')


def stream_user_ages():
    """
    Generator that yields user ages one at a time.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")

    for row in cursor:
        yield row['age']

    connection.close()


def average_user_age():
    """
    Uses the stream_user_ages generator to calculate the average age
    without loading all data into memory.
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    if count == 0:
        print("Average age of users: 0")
    else:
        average = total_age / count
        print(f"Average age of users: {average:.1f}")


if __name__ == "__main__":
    average_user_age()
