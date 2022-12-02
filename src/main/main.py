from api import app
from db import db_session

if __name__ == '__main__':
    app.run(debug=False, port=6000, host='127.0.0.1')
    db_session.close()
