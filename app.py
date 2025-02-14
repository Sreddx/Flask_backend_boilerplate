import os
from dotenv import load_dotenv
from application_name import create_app

# Load environment variables from .env file
load_dotenv()

# Create the Flask app using your factory
app = create_app()

# Default route
@app.route('/')
def index():
    return 'Ok, it works!'

if __name__ == '__main__':
    # Run the development server; not for production
    app.run(debug=os.environ.get('FLASK_DEBUG', False))
