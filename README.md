# RhythmFusion Music Recommendation System

[中文文档](README_zh.md)

## Description
RhythmFusion is a modern music recommendation system built with Django and Vue.js. It provides personalized music recommendations, playlist management, and a seamless user experience through its intuitive interface.

## Features

### Frontend
- User authentication (login/register)
- Personalized playlist management
- Music player with playback controls
- Song recommendation system
- Responsive design for all devices
- Real-time playlist updates
- Interactive song operations (add to playlist, get recommendations)

### Backend
- RESTful API architecture
- User authentication and authorization
- Music database management
- Playlist CRUD operations
- Hybrid recommendation algorithm
- CSV batch import for music data
- Secure file handling for user avatars

## Tech Stack

### Frontend
- Vue 3.5.13 with Composition API
- TypeScript
- Vite 6.2.1
- Pinia for state management
- Axios for HTTP requests
- SCSS for styling

### Backend
- Django 5.0.2
- Django REST framework
- SQLite (configurable to other databases)
- Django authentication system
- Custom recommendation algorithms

## Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup
1. Clone the repository
```bash
git clone https://github.com/SOV710/RhythmFusion.git
cd RhythmFusion/backend
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run database migrations
```bash
python manage.py migrate
```

5. Create superuser (optional)
```bash
python manage.py createsuperuser
```

### Frontend Setup
1. Navigate to frontend directory
```bash
cd ../frontend
```

2. Install dependencies
```bash
npm install
```

## Usage

### Start Backend Server
```bash
cd backend
python manage.py runserver
```
The backend API will be available at `http://127.0.0.1:8000`

### Start Frontend Development Server
```bash
cd frontend
npm run dev
```
The frontend application will be available at `http://localhost:5173`

## Project Structure

### Backend Structure
```
backend/
├── user/           # User management app
├── music/          # Music management app
├── playlist/       # Playlist management app
├── recommendation/ # Recommendation system
├── api/           # API integration layer
└── media/         # Media files storage
```

### Frontend Structure
```
frontend/
├── src/
│   ├── assets/     # Static assets
│   ├── components/ # Vue components
│   ├── stores/     # Pinia state management
│   └── axios.ts    # Axios configuration
├── public/         # Public resources
└── configuration files
```

## Contribution Guidelines

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Standards
- Follow the existing code style
- Write clear commit messages
- Add appropriate documentation
- Include tests for new features
- Ensure all tests pass before submitting PR

## License
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Django team for the excellent web framework
- Vue.js team for the progressive JavaScript framework
- All contributors who have helped shape this project 
