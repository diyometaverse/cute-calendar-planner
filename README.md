# 🌸 Cute Calendar Planner

A delightful and intuitive planner application built with Django, designed to help manage your schedule, files, and tasks with a cute aesthetic touch.

## ✨ Features

### 📅 Calendar Management
- Interactive calendar view
- List view for events
- Event categorization by priority
- Client association for events
- Easy event creation, editing, and deletion

### 📁 File Management
- Upload and organize files
- Preview images directly in the app
- Support for multiple file types (Images, PDF, Word, Excel)
- File categorization and description
- Date tracking for files

### 🎨 User Interface
- Clean and modern design
- Cute pastel color scheme
- Responsive layout for all devices
- Smooth animations and transitions
- Intuitive navigation

### 🔐 Authentication
- Google OAuth2 integration (feat:kobe-nicodemus)
- Secure user authentication
- Role-based access control

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation

1. Clone the repository
```bash
git clone https://github.com/diyometaverse/cute-calendar-planner.git
cd cute-calendar-planner
```

2. Create and activate virtual environment
```bash
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
Create a `.env` file in the project root:
```plaintext
DB_NAME=postgres
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
GOOGLE_SERVICE_ACCOUNT_BASE64=
GOOGLE_DRIVE_FOLDER_ID=
SUPABASE_URL=
SUPABASE_KEY=
SUPABASE_BUCKET=
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=
```

5. Run migrations
```bash
python manage.py migrate
```

6. Create superuser (admin)
```bash
python manage.py createsuperuser
```

7. Run development server
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## 🛠️ Tech Stack

- **Backend**: Django
- **Frontend**: TailwindCSS, JavaScript
- **Database**: Supabase PostgreSQL (development) / PostgreSQL (production)
- **Authentication**: Django Social Auth
- **Icons**: Lucide
- **File Storage**: Supabase Storage

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Django](https://www.djangoproject.com/)
- [TailwindCSS](https://tailwindcss.com/)
- [Lucide Icons](https://lucide.dev/)
- All contributors who helped with this project

## 👥 Contact

Your Name - [@diyometaverse](https://github.com/diyometaverse)

Project Link: [https://github.com/diyometaverse/cute-calendar-planner](https://github.com/diyometaverse/cute-calendar-planner)
