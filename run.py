# run.py

import os
from rounds import app

if __name__ == '__main__':
    if app.config['DEBUG']:
        app.run(debug=True)
    else:
        port = int(os.environ.get('PORT', 5000)) 
        app.run(host='0.0.0.0', port=port, debug=False)

#app.run(debug=True)