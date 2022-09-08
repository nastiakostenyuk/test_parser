from models import create_db
from parser import parse

if __name__ == '__main__':
    create_db()
    pages = int(input("Enter the number of pages"))
    parse(pages)

