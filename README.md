# Modern CRM System

A powerful, user-friendly Customer Relationship Management (CRM) system built with Django and Bootstrap 5. This CRM helps you manage leads, clients, and follow-ups efficiently.

![Dashboard View](gallery/dashboard.png)
_Dashboard with key metrics and follow-ups_

## 🌟 Key Features

### 📊 Dashboard

- Real-time lead pipeline statistics
- Today's follow-ups at a glance
- Recent activity tracking
- Quick action buttons

### 👥 Lead Management

- Comprehensive lead tracking
- Status-based pipeline view
- Advanced filtering and search
- Bulk import/export functionality
- Follow-up scheduling

### 🤝 Client Management

- Client profile management
- Interaction history
- Document attachments
- Custom fields support

### 📅 Follow-up System

- Calendar integration
- Email notifications
- Status tracking
- Priority management

### 📱 Modern UI

- Responsive design
- Dark/Light mode
- Intuitive navigation
- Mobile-friendly interface

![Leads View](gallery/leads.png)
_Lead management interface with filtering and actions_

## 🚀 Quick Start

1. Clone the repository:

```bash
git clone https://github.com/yourusername/crm-django.git
cd crm-django
```

2. Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up the database:

```bash
python manage.py migrate
```

5. Create a superuser:

```bash
python manage.py createsuperuser
```

6. Run the development server:

```bash
python manage.py runserver
```

7. Access the application:

- Main interface: http://localhost:8000
- Admin interface: http://localhost:8000/admin

## 🛠️ Technology Stack

- **Backend**: Django 4.2
- **Frontend**: Bootstrap 5
- **Database**: PostgreSQL
- **Authentication**: Django Authentication
- **API**: Django REST Framework
- **Documentation**: Swagger/OpenAPI

## 📋 Features in Detail

### Lead Management

- Create and track leads through the sales pipeline
- Assign leads to team members
- Track lead status and history
- Import/export lead data
- Advanced search and filtering

### Client Management

- Store client information securely
- Track client interactions
- Manage client documents
- Custom client fields
- Client activity timeline

### Follow-up System

- Schedule and track follow-ups
- Email notifications
- Calendar integration
- Follow-up templates
- Status tracking

### Reporting

- Lead pipeline analytics
- Team performance metrics
- Custom report generation
- Export reports in multiple formats

## 🔒 Security Features

- Role-based access control
- Secure password management
- Session management
- API authentication
- Data encryption

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support, email support@example.com or create an issue in the repository.

---

Built with ❤️ using Django and Bootstrap
