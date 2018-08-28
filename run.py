import os

from api.App.views import app

os.environ['app_env'] = 'Prod'
if __name__ == '__main__':
    app.run(debug=True)
