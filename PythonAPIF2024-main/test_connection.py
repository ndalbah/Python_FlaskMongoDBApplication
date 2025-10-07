from pymongo import MongoClient
import bcrypt
import app_config as config

# Connect to the database (ensure you have your database setup)
client = MongoClient(config.CONST_MONGO_URL)
collection = client[config.CONST_DATABASE][config.CONST_USER_COLLECTION]

def test_password_verification():
    user_info = {
        "email": "yo@gmail.com",  # Use a test email
        "password": "yo"    # Use the password you set for the user
    }

    # Fetch the user from the database
    user = collection.find_one({'email': user_info["email"]})

    if user:
        hashed_password = user['password']  # No need to encode, already in bytes

        # Check if the password matches
        is_password_correct = bcrypt.checkpw(user_info['password'].encode('utf-8'), hashed_password)

        print(f"Password is correct: {is_password_correct}")  # Should print True if the password is correct
    else:
        print("User not found!")

if __name__ == "__main__":
    test_password_verification()
