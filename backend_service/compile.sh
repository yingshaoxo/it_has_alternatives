cd backend_service
pyinstaller main.py --noconfirm --onefile --add-data "./vue:vue" --hidden-import fastapi --hidden-import uvicorn --hidden-import pymongo --hidden-import auto_everything --name main.run 
