from app import app
from app.data import db_session


def main():
    db_session.global_init("app/db/blogs.db")
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()

