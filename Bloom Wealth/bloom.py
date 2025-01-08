from bloom import create_app, db
from bloom.models import User, Portfolio  # Import all your models

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Portfolio': Portfolio}

if __name__ == '__main__':
    app.run(debug=True)