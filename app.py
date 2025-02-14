import os
from dotenv import load_dotenv
from application_name import create_app

load_dotenv()
app = create_app()

@app.route('/')
def index():
    return 'Ok, it works!'

if __name__ == '__main__':
    # If you are developing locally:
    app.run(debug=os.environ.get('FLASK_DEBUG', False))
