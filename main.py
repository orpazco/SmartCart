from api import app
from db import db_session

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    db_session.close()
