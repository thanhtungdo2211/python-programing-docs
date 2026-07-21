# Violate Single Responsibility Principle
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def send_email(self, message):
        print(f"Sending email to {self.email}: {message}")

user = User("Alice", "alice@gmail.com")
user.send_email("Hello!")

# Don't violate Single Responsibility Principle
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class EmailService:
    def send_email(self, user, message):
        print(f"Sending email to {user.email}: {message}")

user = User("Alice", "alice@gmail.com")
service = EmailService().send_email(user, "Hello!")

"""
Trong ví dụ trên, chúng ta có một class User, 
nó chịu trách nhiệm lưu trữ thông tin của một người dùng 
và gửi email cho người dùng đó."""