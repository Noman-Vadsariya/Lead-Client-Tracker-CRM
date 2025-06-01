# Django CRM System

A full-featured Lead & Client Tracker CRM built with Django, featuring PostgreSQL integration, REST API support, and Docker deployment.

## Features

- User Authentication with Role-based Access Control
- Lead & Client Management
- Follow-up Date Tracking & Reminders
- Status Pipeline Progression
- Client Notes Timeline
- Custom Tags/Labels
- CSV Import/Export Functionality
- REST API Support
- Docker & PostgreSQL Integration

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- PostgreSQL (if running locally)

## Quick Start with Docker

1. Clone the repository:

```bash
git clone <repository-url>
cd crm-django
```

2. Build and start the containers:

```bash
docker-compose up --build
```

3. Run migrations:

```bash
docker-compose exec web python manage.py migrate
```

4. Create a superuser:

```bash
docker-compose exec web python manage.py createsuperuser
```

The application will be available at http://localhost:8000

## Local Development Setup

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:

```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run migrations:

```bash
python manage.py migrate
```

5. Start the development server:

```bash
python manage.py runserver
```

## Project Structure

```
crm_project/
├── crm/                 # Main CRM application
│   ├── models/         # Database models
│   ├── views/          # View logic
│   ├── admin/          # Admin interface customization
│   └── api/            # REST API endpoints
├── templates/          # HTML templates
├── static/            # Static files
└── manage.py          # Django management script
```

## API Documentation

The REST API is available at `/api/` and includes endpoints for:

- User authentication
- Lead management
- Client management
- Notes and follow-ups
- Tags and labels

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
