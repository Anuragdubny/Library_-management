# Library Management System

A Django-based library management application with modern UI and complete functionality.

## Features

- 📚 Book catalog with cover images
- 👤 User authentication (login/register)
- 📖 Borrow/return books
- 🛒 Shopping cart functionality
- 👨‍💼 Admin interface
- 🎨 Modern UI with Tailwind CSS

## Quick Start

1. **Install Django:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run setup:**
   ```bash
   python setup.py
   ```

3. **Create admin user:**
   ```bash
   python create_admin.py
   ```

4. **Add sample books:**
   ```bash
   python add_books.py
   python update_book_images.py
   ```

5. **Start server:**
   ```bash
   cd library_project
   python manage.py runserver
   ```

6. **Visit:** http://127.0.0.1:8000

## Default Login
- **Admin:** admin / admin123

## Tech Stack
- Django 4.0+
- Tailwind CSS
- SQLite
- HTML5/CSS3/JavaScript

## Project Structure
```
library_project/
├── books/          # Main app
├── templates/      # HTML templates
├── static/         # CSS/JS files
└── manage.py       # Django management
```

## Screenshots
- Modern book catalog with cover images
- User-friendly login/registration
- Shopping cart functionality
- Admin panel for management

## License
MIT License