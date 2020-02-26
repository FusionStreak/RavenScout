import os
from app import create_app, create_db, create_migrate


if os.path.exists('.flaskenv'):
    print('Importing environment from .env file')
    for line in open('.flaskenv'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

app = create_app('default')
db = create_db(app)
migrate = create_migrate(app, db)

from app.models import Files, infiniteRechargeParsedData
from app import routes, models

@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'File':Files, 'infiniteRecharge':infiniteRechargeParsedData}