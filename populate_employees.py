import random
from faker import Faker
from app import app
from repositories.database import db
from models.employee import Employee
from datetime import datetime
fake = Faker('ro_RO')

def generate_fake_cnp():

    prefix = random.choice(['1', '2'])
    year = random.randint(70, 99)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    random_part = random.randint(100000, 999999)
    return int(f"{prefix}{year:02d}{month:02d}{day:02d}{random_part}")

def populate_employees(n=50):
    with app.app_context():
        for _ in range(n):
            employee = Employee(
                name=fake.first_name(),
                surname=fake.last_name(),
                salary_for_current_month=random.randint(3000, 10000),
                number_of_vacation_days_taken=random.randint(0, 5),
                additional_bonuses=random.choice([None, random.randint(200, 1500)]),
                cnp=generate_fake_cnp(),
                current_month=datetime.now().month,
                current_year=datetime.now().year
            )
            db.session.add(employee)
        db.session.commit()
        print(f"{n} employees added successfully.")

if __name__ == "__main__":
    populate_employees()
