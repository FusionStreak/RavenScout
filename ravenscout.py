from app import app, db
from app.models import Files, infiniteRechargeParsedData

@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'File':Files, 'infiniteRecharge':infiniteRechargeParsedData}