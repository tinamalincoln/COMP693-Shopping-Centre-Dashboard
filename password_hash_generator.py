from werkzeug.security import generate_password_hash
print(generate_password_hash("admin1Pass", method="pbkdf2:sha256", salt_length=16))
print(generate_password_hash("editor1Pass", method="pbkdf2:sha256", salt_length=16))
