from abc import ABC, abstractmethod

# Violate Dependency Inversion Principle
class MySQLDatabase:
    def connect(self):
        print("Connecting to MySQL Database")

class UserService:
    def __init__(self):
        self.db = MySQLDatabase()

user_service = UserService()

# Don't violate Dependency Inversion Principle
class Database(ABC):
    @abstractmethod
    def connect(self):
        pass

class MySQLDatabase(Database):
    def connect(self):
        print("Connecting to MySQL Database")

class PostgreSQLDatabase(Database):
    def connect(self):
        print("Connecting to PostgreSQL Database")

class UserService:
    def __init__(self, db: Database):
        self.db = db

db = MySQLDatabase()
user_service = UserService(db)

"""
Trong ví dụ vi phạm, UserService phụ thuộc trực tiếp vào MySQLDatabase,
nên khi cần thay đổi cơ sở dữ liệu, UserService phải sửa đổi code.

Bằng cách sử dụng Dependency Injection, 
UserService không cần biết chi tiết về cơ sở dữ liệu mà nó sử dụng.
"""