# 🎓 Enhanced WIDA Syllabus Tracker

A comprehensive **Streamlit-based** WIDA test preparation platform with advanced student analytics, detailed profile management, and cloud storage integration.

![Version](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/python-3.11+-green)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red)

## ✨ Features Overview

### 🔐 **Enhanced Authentication System**
- **Detailed Student Registration**: First name, last name, date of birth, unique ID
- **Role-based Access Control**: Student and Master (KRURA) permissions
- **Secure Password Protection**: Optional bcrypt-hashed passwords
- **Automatic Profile Creation**: Analytics profiles generated on registration

### 👨‍🎓 **Student Experience**
- **Personal Dashboard**: Categorized WIDA topics by skill domain
- **Comprehensive Analytics**: Read-only performance overview with charts
- **Progress Tracking**: Visual indicators of test completion and scores
- **Interactive Learning**: 20+ WIDA topics across Reading, Listening, Speaking, Writing
- **Performance Insights**: Strengths identification and improvement areas

### 👨‍💼 **Master (KRURA) Management**
- **Student Profile Management**: Edit analytics for any student
- **Learning Goals Setting**: Customize objectives for each student
- **Achievement Tracking**: Record milestones and accomplishments
- **Study Planning**: Set schedules and motivation levels
- **Priority Management**: Mark students needing extra attention
- **Comprehensive Oversight**: View all student data and progress

### 📊 **Advanced Analytics**
- **Visual Performance Charts**: Category breakdown and trend analysis
- **Automated Calculations**: Real-time analytics generation
- **GitHub Cloud Storage**: Automatic backup of test results
- **Historical Tracking**: Performance trends over time
- **Data-Driven Insights**: Strength and weakness identification

## � Quick Start

### Prerequisites
- Python 3.11 or higher
- Git (for cloning)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Unigalactix/MR.COACH.git
cd MR.COACH
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run app.py
```

4. **Access the app**
Open your browser to `http://localhost:8501`

## 🎯 Usage Guide

### **For Students**
1. **Register**: Click "Register" and fill in your complete profile
2. **Login**: Use your unique ID to access your dashboard
3. **Take Tests**: Browse topics by category and complete assessments
4. **View Analytics**: Check your personal performance dashboard

### **For Master (KRURA)**
1. **Login**: Use ID `KRURA` to access master features
2. **Manage Students**: Navigate to "Student Analytics" 
3. **Edit Profiles**: Select students to customize their analytics
4. **Track Progress**: Monitor all student performance and goals

## 📁 Project Structure

```
MR.COACH/
├── app.py                    # Main Streamlit application
├── enhanced_backend.py       # Advanced database with analytics
├── backend.py               # Original database (legacy)
├── requirements.txt         # Python dependencies
├── ENHANCED_FEATURES.md     # Detailed feature documentation
├── README.md               # This file
└── .streamlit/             # Streamlit configuration
```

## 🛠 Technical Details

### **Technology Stack**
- **Frontend**: Streamlit with custom CSS theming
- **Backend**: SQLite database with advanced analytics
- **Authentication**: bcrypt password hashing
- **Visualization**: Plotly charts with dark theme
- **Cloud Storage**: GitHub API integration
- **Languages**: Python 3.11+

### **Database Schema**
- **Users**: Extended profiles with analytics data
- **Topics**: Comprehensive WIDA content library
- **Questions**: Detailed assessments with explanations
- **Results**: Test outcomes with GitHub sync status

### **Key Dependencies**
- `streamlit>=1.28.0` - Web application framework
- `plotly>=5.15.0` - Interactive data visualization
- `bcrypt>=4.0.0` - Secure password hashing
- `pandas>=1.5.0` - Data manipulation
- `requests>=2.28.0` - GitHub API integration

## 🔧 Configuration

### **GitHub Cloud Storage (Optional)**
Create `.streamlit/secrets.toml`:
```toml
[github]
token = "your_github_token_here"
repo_owner = "your_username"
repo_name = "wida-results"
```

### **Demo Accounts**
- **Master**: Login ID `KRURA`
- **Student**: Login ID `student1` (or register new)

## 🎨 Features Showcase

### **Enhanced Registration**
- Complete profile collection
- Automatic analytics setup
- Professional validation
- Terms acceptance

### **Student Analytics Dashboard**
- Performance overview cards
- Category-wise score breakdown
- Performance trend visualization
- Strengths and improvement areas

### **Master Management Interface**
- Student selection dropdown
- Editable goals and achievements
- Study notes and scheduling
- Motivation level tracking
- Priority student marking

## 📈 Analytics Features

- **Real-time Calculations**: Automatic performance metrics
- **Visual Charts**: Interactive Plotly graphs
- **Trend Analysis**: Historical performance tracking
- **Category Breakdown**: Subject-wise performance
- **Cloud Backup**: GitHub integration for data persistence

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## � License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For questions or issues:
- Create an issue on GitHub
- Contact the development team
- Check the [ENHANCED_FEATURES.md](ENHANCED_FEATURES.md) for detailed feature documentation

---

**Built with ❤️ using Streamlit and modern Python technologies**
- **Comprehensive Management Hub** with tabbed interface
- **Syllabus Editor** - add and manage topics
- **Student Analytics** - interactive charts and performance data
- **User Management** - add/remove students, view all users
- **Data Visualization** - Plotly charts for score analysis

### 🎨 UI/UX Design
- **Gradient backgrounds** matching original design
- **Card-based layouts** with shadows and rounded corners
- **Responsive design** that works on all screen sizes
- **Custom CSS styling** maintaining original color scheme
- **Interactive elements** with hover effects and transitions

### 🗄️ Backend Database
- **SQLite database** for data persistence
- **User management** with password hashing
- **Test results storage** with timestamps
- **Topic and question management**
- **Data relationships** with foreign keys

## Installation & Setup

1. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   streamlit run app.py
   ```

3. **Access the application:**
   - Open your browser to `http://localhost:8501`

## Demo Accounts

### Master Account
- **Username:** KRURA
- **Role:** Master (Full access to management features)

### Student Accounts
- **Username:** student1
- **Username:** student2
- **Role:** Student (Access to tests and personal results)

## Database Schema

### Users Table
- `unique_id` (PRIMARY KEY)
- `role` (master/student)
- `password_hash` (optional)
- `created_at`

### Topics Table
- `id` (PRIMARY KEY)
- `title`
- `created_at`

### Questions Table
- `id` (PRIMARY KEY)
- `topic_id` (FOREIGN KEY)
- `question_text`
- `option_a`, `option_b`, `option_c`, `option_d`
- `correct_answer` (0-3)

### Test Results Table
- `id` (PRIMARY KEY)
- `student_id` (FOREIGN KEY)
- `topic_id` (FOREIGN KEY)
- `topic_title`
- `score`
- `submitted_at`

## Key Technical Features

### 🔧 Backend (backend.py)
- **DatabaseManager class** for all database operations
- **Password hashing** with bcrypt for security
- **Data validation** and error handling
- **CRUD operations** for all entities
- **Connection management** with proper closing

### 🎨 Frontend (app.py)
- **Streamlit components** with custom CSS styling
- **Session state management** for user persistence
- **Form handling** with validation
- **Data visualization** with Plotly
- **Responsive layout** with columns and containers

### 🎯 Features Maintained from Original
- **Complete UI design** with gradients and modern styling
- **All functionality** including tests, analytics, and management
- **Role-based access** with proper permission checks
- **Data persistence** unlike the original localStorage approach
- **Real-time updates** with Streamlit's reactive model

## File Structure

```
├── app.py              # Main Streamlit application
├── backend.py          # Database management and business logic
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── wida_app.db        # SQLite database (created automatically)
```

## Conversion Highlights

### From React Router to Streamlit Pages
- **Session state routing** replaces React Router
- **Page functions** for each major view
- **Sidebar navigation** for easy access

### From Context API to Database
- **SQLite backend** replaces React Context
- **Persistent data** instead of localStorage
- **Proper data relationships** with foreign keys

### From CSS Classes to Streamlit Styling
- **Custom CSS injection** maintains visual design
- **Streamlit components** with styled containers
- **Responsive grid layouts** using columns

### Enhanced Features
- **Real database** instead of mock data
- **Password security** with hashing
- **Better data persistence** across sessions
- **Interactive charts** with Plotly
- **Improved user experience** with Streamlit's reactive updates

This Streamlit version provides all the functionality of the original React application while adding robust backend support and maintaining the beautiful UI design.
