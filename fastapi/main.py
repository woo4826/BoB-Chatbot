from sys import argv
import uvicorn
import os 
from config import config




if __name__ == '__main__':

    try:
        if  config["LOG"] == 'DEV':
            uvicorn.run(
                "api:app",
                host='0.0.0.0',
                port=3000,
                workers=1,
                log_level='info',
                reload=True,
            )
        else:
            uvicorn.run(
                "api:app",
                host='0.0.0.0',
                port=8080,
                workers=5,
                log_level='warning',
                reload=False,
            )
    except KeyboardInterrupt:
        print('\nExiting\n')
    except Exception as errormain:
        print('Failed to Start API')
        print('='*100)
        print(str(errormain))
        print('='*100)
        print('Exiting\n')