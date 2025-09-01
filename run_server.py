import os
import subprocess
import sys

os.chdir('library_project')

print("Starting Library Management System...")
print("Server will be available at: http://127.0.0.1:8000")
print("Admin panel at: http://127.0.0.1:8000/admin/")
print("Admin credentials: admin / admin123")
print("\nPress Ctrl+C to stop the server\n")

try:
    subprocess.run([sys.executable, 'manage.py', 'runserver', '127.0.0.1:8000'])
except KeyboardInterrupt:
    print("\nServer stopped.")