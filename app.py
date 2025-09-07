import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional
from enhanced_backend import EnhancedDatabaseManager

# Initialize enhanced database
@st.cache_resource
def get_database():
    return EnhancedDatabaseManager()

def apply_custom_css():
    """Apply custom CSS with black background and white elements"""
    st.markdown("""
    <style>
    /* Import Inter font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* Global styles - Black theme */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
        color: white;
    }
    
    /* Main content area */
    .main .block-container {
        background: transparent;
        color: white;
    }
    
    /* Header styles */
    .main-header {
        background: linear-gradient(135deg, #333333 0%, #1a1a1a 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(255, 255, 255, 0.1);
        border: 1px solid #333333;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        color: white;
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin: 0.5rem 0 0 0;
        color: #cccccc;
    }
    
    /* Card styles - Dark cards with white text */
    .card {
        background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%);
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(255, 255, 255, 0.05);
        border: 1px solid #333333;
        margin-bottom: 1.5rem;
        color: white;
    }
    
    /* Sidebar styles - Black sidebar */
    .css-1d391kg {
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
    }
    
    .sidebar-title {
        color: white;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    /* Button styles - White buttons with BLACK text */
    .stButton > button {
        background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
        color: #000000 !important;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 255, 255, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 255, 255, 0.3);
        background: linear-gradient(135deg, #f0f0f0 0%, #e0e0e0 100%);
        color: #000000 !important;
    }
    
    .stButton > button:focus {
        background: linear-gradient(135deg, #e0e0e0 0%, #d0d0d0 100%);
        box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.3);
        color: #000000 !important;
    }
    
    .stButton > button:active {
        color: #000000 !important;
    }
    
    /* Input field styles */
    .stTextInput > div > div > input {
        background-color: #2a2a2a;
        color: white;
        border: 1px solid #444444;
        border-radius: 8px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #ffffff;
        box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.2);
    }
    
    .stSelectbox > div > div > select {
        background-color: #2a2a2a;
        color: white;
        border: 1px solid #444444;
    }
    
    /* Radio button styles */
    .stRadio > div {
        background-color: transparent;
    }
    
    .stRadio label {
        color: white;
    }
    
    /* Form styles */
    .stForm {
        background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%);
        border: 1px solid #333333;
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* Success/Error styles */
    .success-box {
        background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
        color: #000000;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border: 1px solid #cccccc;
    }
    
    .error-box {
        background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
        color: #000000;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border: 1px solid #cccccc;
    }
    
    /* Progress indicators */
    .progress-card {
        background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%);
        border: 2px solid #ffffff;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        margin: 1rem 0;
        color: white;
    }
    
    .progress-number {
        font-size: 2.5rem;
        font-weight: 800;
        color: #ffffff;
    }
    
    /* Login form styles */
    .login-container {
        max-width: 400px;
        margin: 2rem auto;
        background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(255, 255, 255, 0.1);
        border: 1px solid #333333;
        color: white;
    }
    
    /* Table styles */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(255, 255, 255, 0.1);
        background: #2a2a2a;
    }
    
    .dataframe table {
        background: #2a2a2a;
        color: white;
    }
    
    .dataframe th {
        background: #1a1a1a;
        color: white;
        border-bottom: 1px solid #444444;
    }
    
    .dataframe td {
        background: #2a2a2a;
        color: white;
        border-bottom: 1px solid #333333;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Role badge styles */
    .role-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .role-master {
        background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
        color: #000000;
        border: 1px solid #cccccc;
    }
    
    .role-student {
        background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
        color: #000000;
        border: 1px solid #cccccc;
    }
    
    /* Quiz styles */
    .question-card {
        background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(255, 255, 255, 0.05);
        border-left: 4px solid #ffffff;
        color: white;
    }
    
    .question-number {
        color: #ffffff;
        font-weight: 700;
        font-size: 1.1rem;
    }
    
    /* Streamlit specific overrides */
    .stApp > div {
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
    }
    
    /* Sidebar content styling */
    .css-1d391kg .css-1v0mbdj {
        color: white;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background: #2a2a2a;
        border-radius: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #1a1a1a;
        color: white;
        border-radius: 8px;
        margin: 2px;
    }
    
    .stTabs [aria-selected="true"] {
        background: white;
        color: black;
    }
    
    /* Metrics styling */
    .metric-container {
        background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #333333;
    }
    
    /* Chart background */
    .js-plotly-plot {
        background: transparent !important;
    }
    
    /* Text color overrides */
    .stMarkdown {
        color: white;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: white;
    }
    
    p {
        color: #cccccc;
    }
    
    /* Alert styles */
    .stAlert > div {
        background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%);
        color: white;
        border: 1px solid #333333;
    }
    
    .stSuccess > div {
        background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
        color: #000000;
        border: 1px solid #cccccc;
    }
    
    .stError > div {
        background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
        color: #000000;
        border: 1px solid #cccccc;
    }
    
    .stWarning > div {
        background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
        color: #000000;
        border: 1px solid #cccccc;
    }
    
    .stInfo > div {
        background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
        color: #000000;
        border: 1px solid #cccccc;
    }
    </style>
    """, unsafe_allow_html=True)

def show_header(title: str, subtitle: str = ""):
    """Display the main header"""
    st.markdown(f"""
    <div class="main-header">
        <h1>{title}</h1>
        {f'<p>{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)

def show_landing_page():
    """Display the landing page"""
    st.markdown("""
    <div style="text-align: center; padding: 4rem 2rem;">
        <div style="background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%); padding: 3rem; border-radius: 20px; box-shadow: 0 15px 50px rgba(255,255,255,0.1); max-width: 600px; margin: 0 auto; border: 1px solid #333333;">
            <h1 style="font-size: 3rem; font-weight: 800; margin-bottom: 1rem; color: white;">
                Welcome to the <span style="color: #ffffff;">WIDA</span> Syllabus Tracker
            </h1>
            <p style="font-size: 1.2rem; color: #cccccc; margin-bottom: 2rem;">
                Your centralized platform for WIDA screener test preparation. Master your syllabus, track student progress, and achieve success together.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_login_page():
    """Display the login page"""
    db = get_database()
    
    st.markdown("""
    <div class="login-container">
        <h2 style="text-align: center; color: white; margin-bottom: 1rem;">Sign In</h2>
        <p style="text-align: center; color: #cccccc; margin-bottom: 2rem;">Access your WIDA dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        unique_id = st.text_input("Unique ID", placeholder="Your Unique ID")
        password = st.text_input("Password (Optional)", type="password", placeholder="Leave blank for demo users")
        submit = st.form_submit_button("Sign In", use_container_width=True)
        
        if submit:
            if unique_id:
                user = db.authenticate_user(unique_id, password if password else None)
                if user:
                    st.session_state.user = user
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid Unique ID or password")
            else:
                st.error("Please enter your Unique ID")
    
    st.markdown("""
    <div style="text-align: center; margin-top: 2rem; padding: 1rem; background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%); border-radius: 10px; border: 1px solid #333333;">
        <p style="color: white;"><strong>Demo Accounts:</strong></p>
        <p style="color: #cccccc;">Master Login ID: <code style="background: #1a1a1a; padding: 0.2rem 0.5rem; border-radius: 4px; color: white;">KRURA</code></p>
        <p style="color: #cccccc;">Student Login ID: <code style="background: #1a1a1a; padding: 0.2rem 0.5rem; border-radius: 4px; color: white;">student1</code></p>
    </div>
    """, unsafe_allow_html=True)

def show_register_page():
    """Display the enhanced registration page with detailed profile information"""
    db = get_database()
    
    st.markdown("""
    <div class="login-container">
        <h2 style="text-align: center; color: white; margin-bottom: 1rem;">Student Registration</h2>
        <p style="text-align: center; color: #cccccc; margin-bottom: 2rem;">Create your detailed student profile</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("register_form"):
        st.markdown("### Personal Information")
        
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name *", placeholder="Enter your first name")
        with col2:
            last_name = st.text_input("Last Name *", placeholder="Enter your last name")
        
        date_of_birth = st.date_input("Date of Birth *", 
                                     help="This helps us track your learning progress")
        
        st.markdown("### Account Information")
        unique_id = st.text_input("Choose a Unique ID *", 
                                 placeholder="Enter your unique identifier (username)")
        password = st.text_input("Password (Optional)", 
                                type="password", 
                                placeholder="Leave blank for no password",
                                help="Password is optional but recommended for security")
        
        st.markdown("---")
        
        # Terms and conditions
        accept_terms = st.checkbox("I agree to the terms and conditions and privacy policy")
        
        submit = st.form_submit_button("Create Student Profile", use_container_width=True)
        
        if submit:
            if not all([first_name, last_name, unique_id, date_of_birth]):
                st.error("Please fill in all required fields marked with *")
            elif not accept_terms:
                st.error("Please accept the terms and conditions to continue")
            else:
                # Convert date to string format
                dob_str = date_of_birth.strftime('%Y-%m-%d')
                
                if db.register_user(unique_id, password if password else None, 
                                  first_name, last_name, dob_str):
                    st.markdown("""
                    <div class="success-box">
                        <h4 style="color: #000000; margin-bottom: 0.5rem;">🎉 Registration Successful!</h4>
                        <p style="color: #000000; margin: 0;">Welcome to WIDA Test Preparation, {first_name}!</p>
                        <p style="color: #000000; margin: 0.5rem 0 0 0;">Your analytics profile has been created. You can now login to start your learning journey.</p>
                    </div>
                    """.format(first_name=first_name), unsafe_allow_html=True)
                    
                    # Show login button
                    if st.button("Go to Login", use_container_width=True):
                        st.session_state.page = 'login'
                        st.rerun()
                else:
                    st.error("This Unique ID is already taken. Please choose a different one.")
    
    # Back to login link
    st.markdown("---")
    if st.button("← Back to Login", use_container_width=True):
        st.session_state.page = 'login'
        st.rerun()

def show_student_dashboard():
    """Display the student dashboard with enhanced WIDA topics"""
    db = get_database()
    user = st.session_state.user
    
    show_header("Dashboard", f"Welcome back, {user['unique_id']}")
    
    # Get topics and student results
    topics = db.get_topics()
    student_results = db.get_student_results(user['unique_id'])
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3 style="color: white; margin-bottom: 1rem;">📚 WIDA Test Preparation Topics</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if topics:
            # Group topics by category
            categories = {}
            for topic in topics:
                category = topic.get('category', 'General')
                if category not in categories:
                    categories[category] = []
                categories[category].append(topic)
            
            # Create tabs for each category
            category_tabs = st.tabs(list(categories.keys()))
            
            for i, (category, category_topics) in enumerate(categories.items()):
                with category_tabs[i]:
                    st.markdown(f"""
                    <div style="padding: 1rem; background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%); border-radius: 10px; margin: 1rem 0; border: 1px solid #333333;">
                        <h4 style="color: white; margin-bottom: 1rem;">🎯 {category} Skills</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    for topic in category_topics:
                        difficulty_color = {
                            'Beginner': '#4ade80',
                            'Intermediate': '#fbbf24', 
                            'Advanced': '#ef4444'
                        }.get(topic.get('difficulty', 'Intermediate'), '#fbbf24')
                        
                        col_topic, col_difficulty = st.columns([3, 1])
                        
                        with col_topic:
                            if st.button(f"📖 {topic['title']}", key=f"topic_{topic['id']}", use_container_width=True):
                                st.session_state.current_test_topic = topic
                                st.session_state.page = 'test'
                                st.rerun()
                        
                        with col_difficulty:
                            st.markdown(f"""
                            <div style="text-align: center; padding: 0.5rem; background: {difficulty_color}; color: black; border-radius: 6px; font-size: 0.8rem; font-weight: 600;">
                                {topic.get('difficulty', 'Intermediate')}
                            </div>
                            """, unsafe_allow_html=True)
        else:
            st.info("No syllabus topics available yet.")
    
    with col2:
        st.markdown(f"""
        <div class="progress-card">
            <div class="progress-number">{len(student_results)}</div>
            <p style="color: #cccccc; margin: 0;">Tests Completed</p>
            <p style="color: #cccccc; font-size: 0.9rem; margin: 0.5rem 0 0 0;">Keep up the great work!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show GitHub sync status
        if student_results:
            synced_count = sum(1 for r in student_results if r.get('github_synced', False))
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%); border-radius: 10px; margin: 1rem 0; border: 1px solid #333333;">
                <div style="color: white; font-size: 1.2rem; font-weight: 600;">{synced_count}/{len(student_results)}</div>
                <p style="color: #cccccc; margin: 0; font-size: 0.9rem;">Results Backed Up</p>
            </div>
            """, unsafe_allow_html=True)
        
        if student_results:
            st.markdown("""
            <div class="card">
                <h4 style="color: white; margin-bottom: 1rem;">📈 Recent Results</h4>
            </div>
            """, unsafe_allow_html=True)
            
            for result in student_results[:3]:  # Show last 3 results
                score_color = "#ffffff" if result['score'] >= 70 else "#cccccc"
                sync_icon = "☁️" if result.get('github_synced', False) else "💾"
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%); padding: 1rem; margin: 0.5rem 0; border-radius: 8px; border-left: 4px solid {score_color}; border: 1px solid #333333;">
                    <strong style="color: white;">{result['topic_title']}</strong> {sync_icon}<br>
                    <span style="color: {score_color}; font-weight: 600;">{result['score']}%</span>
                    <span style="color: #cccccc; font-size: 0.9rem;"> • {result['submitted_at'][:10]}</span>
                </div>
                """, unsafe_allow_html=True)

def show_student_analytics():
    """Display comprehensive student analytics (read-only for students)"""
    db = get_database()
    user = st.session_state.user
    
    show_header("My Analytics", f"Performance Overview for {user['unique_id']}")
    
    # Get user profile and analytics
    profile = db.get_user_profile(user['unique_id'])
    analytics = db.calculate_student_analytics(user['unique_id'])
    
    if profile:
        # Profile Header
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"""
            <div class="card" style="text-align: center; padding: 2rem;">
                <h3 style="color: white; margin-bottom: 1rem;">👤 Student Profile</h3>
                <h4 style="color: #cccccc;">{profile['first_name']} {profile['last_name']}</h4>
                <p style="color: #cccccc; margin: 0.5rem 0;">ID: {profile['unique_id']}</p>
                <p style="color: #cccccc; margin: 0;">Born: {profile['date_of_birth']}</p>
                <p style="color: #cccccc; margin: 0.5rem 0 0 0;">Member since: {profile['created_at'][:10]}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Analytics Overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="progress-card">
            <div class="progress-number">{analytics['total_tests']}</div>
            <p style="color: #cccccc; margin: 0;">Total Tests</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_color = "#4ade80" if analytics['average_score'] >= 70 else "#fbbf24" if analytics['average_score'] >= 50 else "#ef4444"
        st.markdown(f"""
        <div class="progress-card">
            <div class="progress-number" style="color: {avg_color};">{analytics['average_score']}%</div>
            <p style="color: #cccccc; margin: 0;">Average Score</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="progress-card">
            <div class="progress-number">{len(analytics['strengths'])}</div>
            <p style="color: #cccccc; margin: 0;">Strong Areas</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        improvement_areas = len(analytics['areas_for_improvement'])
        st.markdown(f"""
        <div class="progress-card">
            <div class="progress-number">{improvement_areas}</div>
            <p style="color: #cccccc; margin: 0;">Focus Areas</p>
        </div>
        """, unsafe_allow_html=True)
    
    if analytics['total_tests'] > 0:
        # Performance Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="card">
                <h4 style="color: white; margin-bottom: 1rem;">📊 Category Performance</h4>
            </div>
            """, unsafe_allow_html=True)
            
            if analytics['category_averages']:
                categories = list(analytics['category_averages'].keys())
                scores = list(analytics['category_averages'].values())
                
                fig = go.Figure(data=[
                    go.Bar(x=categories, y=scores, 
                          marker_color=['#4ade80' if s >= 70 else '#fbbf24' if s >= 50 else '#ef4444' for s in scores])
                ])
                fig.update_layout(
                    title="Average Scores by Category",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("""
            <div class="card">
                <h4 style="color: white; margin-bottom: 1rem;">📈 Performance Trend</h4>
            </div>
            """, unsafe_allow_html=True)
            
            if analytics['performance_trend']:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    y=analytics['performance_trend'],
                    x=list(range(1, len(analytics['performance_trend']) + 1)),
                    mode='lines+markers',
                    line=dict(color='#4ade80', width=3),
                    marker=dict(size=8)
                ))
                fig.update_layout(
                    title="Recent Performance Trend",
                    xaxis_title="Test Number",
                    yaxis_title="Score (%)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Strengths and Areas for Improvement
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="card">
                <h4 style="color: white; margin-bottom: 1rem;">💪 Your Strengths</h4>
            </div>
            """, unsafe_allow_html=True)
            
            if analytics['strengths']:
                for strength in analytics['strengths']:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #065f46 0%, #047857 100%); padding: 0.8rem; margin: 0.5rem 0; border-radius: 8px; border-left: 4px solid #4ade80;">
                        <span style="color: white;">✅ {strength}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Complete more tests to identify your strengths!")
        
        with col2:
            st.markdown("""
            <div class="card">
                <h4 style="color: white; margin-bottom: 1rem;">🎯 Focus Areas</h4>
            </div>
            """, unsafe_allow_html=True)
            
            if analytics['areas_for_improvement']:
                for area in analytics['areas_for_improvement']:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #7c2d12 0%, #9a3412 100%); padding: 0.8rem; margin: 0.5rem 0; border-radius: 8px; border-left: 4px solid #fbbf24;">
                        <span style="color: white;">📚 {area}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("Great job! No specific areas need improvement right now.")
    
    else:
        st.markdown("""
        <div class="card" style="text-align: center; padding: 3rem;">
            <h3 style="color: white; margin-bottom: 1rem;">📊 No Analytics Yet</h3>
            <p style="color: #cccccc; margin-bottom: 2rem;">Complete some tests to see your performance analytics!</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Read-only notice
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%); padding: 1rem; margin: 2rem 0; border-radius: 8px; border-left: 4px solid #3b82f6;">
        <p style="color: white; margin: 0;">ℹ️ This analytics page is read-only. Only Master (KRURA) can edit student analytics profiles.</p>
    </div>
    """, unsafe_allow_html=True)

def show_master_analytics():
    """Display master analytics page where KRURA can edit student profiles"""
    db = get_database()
    
    show_header("Student Analytics Management", "Edit and monitor all student profiles")
    
    # Get all students
    all_users = db.get_all_users()
    students = [user for user in all_users if user['role'] == 'student']
    
    if not students:
        st.markdown("""
        <div class="card" style="text-align: center; padding: 3rem;">
            <h3 style="color: white; margin-bottom: 1rem;">👥 No Students Registered</h3>
            <p style="color: #cccccc;">Students will appear here once they register.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Student selection
    st.markdown("""
    <div class="card">
        <h3 style="color: white; margin-bottom: 1rem;">👨‍🎓 Select Student to Manage</h3>
    </div>
    """, unsafe_allow_html=True)
    
    selected_student = st.selectbox(
        "Choose a student:",
        options=[f"{s['unique_id']} - {s['first_name']} {s['last_name']}" for s in students],
        format_func=lambda x: x
    )
    
    if selected_student:
        student_id = selected_student.split(' - ')[0]
        student_profile = db.get_user_profile(student_id)
        
        if student_profile:
            # Student Profile Overview
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown(f"""
                <div class="card">
                    <h4 style="color: white; margin-bottom: 1rem;">📋 Profile Information</h4>
                    <p style="color: #cccccc;"><strong>Name:</strong> {student_profile['first_name']} {student_profile['last_name']}</p>
                    <p style="color: #cccccc;"><strong>ID:</strong> {student_profile['unique_id']}</p>
                    <p style="color: #cccccc;"><strong>DOB:</strong> {student_profile['date_of_birth']}</p>
                    <p style="color: #cccccc;"><strong>Joined:</strong> {student_profile['created_at'][:10]}</p>
                    <p style="color: #cccccc;"><strong>Backup Status:</strong> {'☁️ Synced' if student_profile['github_synced'] else '💾 Local'}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Current analytics
                analytics = db.calculate_student_analytics(student_id)
                st.markdown(f"""
                <div class="card">
                    <h4 style="color: white; margin-bottom: 1rem;">📊 Current Statistics</h4>
                    <p style="color: #cccccc;"><strong>Total Tests:</strong> {analytics['total_tests']}</p>
                    <p style="color: #cccccc;"><strong>Average Score:</strong> {analytics['average_score']}%</p>
                    <p style="color: #cccccc;"><strong>Strong Areas:</strong> {len(analytics['strengths'])}</p>
                    <p style="color: #cccccc;"><strong>Focus Areas:</strong> {len(analytics['areas_for_improvement'])}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Editable Analytics Section
            st.markdown("""
            <div class="card">
                <h3 style="color: white; margin-bottom: 1rem;">✏️ Edit Student Analytics Profile</h3>
                <p style="color: #cccccc; margin-bottom: 1rem;">Customize goals, achievements, and notes for this student.</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form(f"edit_analytics_{student_id}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 🎯 Learning Goals")
                    current_goals = student_profile.get('analytics', {}).get('goals', [])
                    goals_text = '\n'.join(current_goals) if current_goals else ""
                    new_goals = st.text_area(
                        "Enter learning goals (one per line):",
                        value=goals_text,
                        height=100,
                        help="Set specific learning objectives for this student"
                    )
                    
                    st.markdown("#### 🏆 Achievements")
                    current_achievements = student_profile.get('analytics', {}).get('achievements', [])
                    achievements_text = '\n'.join(current_achievements) if current_achievements else ""
                    new_achievements = st.text_area(
                        "Enter achievements (one per line):",
                        value=achievements_text,
                        height=100,
                        help="Record notable accomplishments and milestones"
                    )
                
                with col2:
                    st.markdown("#### 📝 Study Notes")
                    current_notes = student_profile.get('analytics', {}).get('study_notes', '')
                    study_notes = st.text_area(
                        "Study notes and observations:",
                        value=current_notes,
                        height=100,
                        help="Add observations about learning style, preferences, etc."
                    )
                    
                    st.markdown("#### ⏰ Study Schedule")
                    current_schedule = student_profile.get('analytics', {}).get('study_schedule', '')
                    study_schedule = st.text_area(
                        "Recommended study schedule:",
                        value=current_schedule,
                        height=100,
                        help="Suggest optimal study times and duration"
                    )
                
                # Motivation level slider
                current_motivation = student_profile.get('analytics', {}).get('motivation_level', 5)
                motivation_level = st.slider(
                    "Current Motivation Level:",
                    min_value=1, max_value=10, 
                    value=current_motivation,
                    help="Rate the student's current motivation level (1-10)"
                )
                
                # Additional settings
                col1, col2 = st.columns(2)
                with col1:
                    send_reminders = st.checkbox(
                        "Send Study Reminders",
                        value=student_profile.get('analytics', {}).get('reminders_enabled', False),
                        help="Enable automated study reminders"
                    )
                
                with col2:
                    priority_student = st.checkbox(
                        "Priority Student",
                        value=student_profile.get('analytics', {}).get('priority_student', False),
                        help="Mark as priority for additional attention"
                    )
                
                if st.form_submit_button("💾 Save Analytics Changes", use_container_width=True):
                    # Prepare updated analytics
                    updated_analytics = student_profile.get('analytics', {})
                    updated_analytics.update({
                        'goals': [goal.strip() for goal in new_goals.split('\n') if goal.strip()],
                        'achievements': [ach.strip() for ach in new_achievements.split('\n') if ach.strip()],
                        'study_notes': study_notes,
                        'study_schedule': study_schedule,
                        'motivation_level': motivation_level,
                        'reminders_enabled': send_reminders,
                        'priority_student': priority_student,
                        'last_updated_by': 'KRURA',
                        'last_updated_at': datetime.now().isoformat()
                    })
                    
                    # Update the analytics
                    if db.update_user_analytics(student_id, updated_analytics):
                        st.success("✅ Analytics profile updated successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to update analytics profile.")
            
            # Display current test results
            student_results = db.get_student_results(student_id)
            if student_results:
                st.markdown("""
                <div class="card">
                    <h4 style="color: white; margin-bottom: 1rem;">📈 Recent Test Results</h4>
                </div>
                """, unsafe_allow_html=True)
                
                for result in student_results[:5]:  # Show last 5 results
                    score_color = "#4ade80" if result['score'] >= 70 else "#fbbf24" if result['score'] >= 50 else "#ef4444"
                    sync_icon = "☁️" if result.get('github_synced', False) else "💾"
                    
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.markdown(f"**{result['topic_title']}** {sync_icon}")
                    with col2:
                        st.markdown(f"<span style='color: {score_color}; font-weight: 600;'>{result['score']}%</span>", unsafe_allow_html=True)
                    with col3:
                        st.markdown(f"<span style='color: #cccccc;'>{result['submitted_at'][:10]}</span>", unsafe_allow_html=True)

def show_master_dashboard():
    """Display the master dashboard"""
    show_header("Dashboard", "Syllabus Management")
    
    st.markdown("""
    <div class="card" style="text-align: center; padding: 3rem;">
        <h3 style="color: white; margin-bottom: 1rem;">🎯 Syllabus & User Management</h3>
        <p style="color: #cccccc; margin-bottom: 2rem;">Manage syllabus content and track all student progress.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔧 Go to Management Dashboard", use_container_width=True):
        st.session_state.page = 'syllabus_management'
        st.rerun()

def show_test_page():
    """Display the test page"""
    if 'current_test_topic' not in st.session_state:
        st.error("No test topic selected")
        return
    
    topic = st.session_state.current_test_topic
    db = get_database()
    
    show_header(f"Test: {topic['title']}", "Answer all questions to complete the test")
    
    questions = db.get_questions_for_topic(topic['id'])
    
    if not questions:
        st.warning("No questions available for this topic yet.")
        return
    
    with st.form("test_form"):
        answers = []
        
        for i, question in enumerate(questions):
            st.markdown(f"""
            <div class="question-card">
                <div class="question-number">Question {i + 1}</div>
                <h4 style="color: #1e293b; margin: 0.5rem 0 1rem 0;">{question['question_text']}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            answer = st.radio(
                f"Select your answer for Question {i + 1}:",
                options=range(len(question['options'])),
                format_func=lambda x: question['options'][x],
                key=f"q_{i}",
                label_visibility="collapsed"
            )
            answers.append(answer)
        
        if st.form_submit_button("Submit Test", use_container_width=True):
            # Calculate score
            correct_answers = sum(1 for i, answer in enumerate(answers) 
                                if answer == questions[i]['correct_answer'])
            score = round((correct_answers / len(questions)) * 100)
            
            # Save result
            result_id = db.submit_test_result(
                st.session_state.user['unique_id'],
                topic['id'],
                topic['title'],
                score
            )
            
            st.session_state.current_result_id = result_id
            st.session_state.page = 'test_result'
            st.rerun()

def show_test_result_page():
    """Display the test result page"""
    if 'current_result_id' not in st.session_state:
        st.error("No test result found")
        return
    
    db = get_database()
    result = db.get_result_by_id(st.session_state.current_result_id)
    
    if not result:
        st.error("Result not found")
        return
    
    show_header("Test Results", f"Your performance on {result['topic_title']}")
    
    # Show score with visual feedback
    score_color = "#ffffff" if result['score'] >= 70 else "#cccccc"
    
    st.markdown(f"""
    <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%); border-radius: 20px; box-shadow: 0 10px 30px rgba(255,255,255,0.1); border: 1px solid #333333;">
        <div style="font-size: 4rem; font-weight: 800; color: {score_color}; margin-bottom: 1rem;">
            {result['score']}%
        </div>
        <h3 style="color: white; margin-bottom: 0.5rem;">{result['topic_title']}</h3>
        <p style="color: #cccccc;">Completed on {result['submitted_at'][:10]}</p>
        
        <div style="margin-top: 2rem; padding: 1rem; background: #1a1a1a; border-radius: 10px; border: 1px solid #333333;">
            <strong style="color: white;">{'🎉 Excellent work!' if result['score'] >= 90 else '👍 Good job!' if result['score'] >= 70 else '📚 Keep studying!'}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("← Back to Dashboard", use_container_width=True):
        st.session_state.page = 'dashboard'
        st.rerun()

def show_syllabus_management_page():
    """Display the syllabus management page"""
    db = get_database()
    
    show_header("Syllabus & User Hub", "Manage syllabus topics, track student analytics, and administer user accounts")
    
    # Tabs for different management sections
    tab1, tab2, tab3 = st.tabs(["📚 Syllabus Editor", "📊 Student Analytics", "👥 User Management"])
    
    with tab1:
        st.markdown("""
        <div class="card">
            <h3 style="color: white; margin-bottom: 1rem;">Add New Topic</h3>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("add_topic_form"):
            new_topic_title = st.text_input("Topic Title", placeholder="Enter new topic title")
            if st.form_submit_button("Add Topic"):
                if new_topic_title.strip():
                    db.add_topic(new_topic_title.strip())
                    st.success(f"Topic '{new_topic_title}' added successfully!")
                    st.rerun()
                else:
                    st.error("Topic title cannot be empty.")
        
        # Show existing topics
        topics = db.get_topics()
        if topics:
            st.markdown("""
            <div class="card">
                <h3 style="color: white; margin-bottom: 1rem;">Existing Topics</h3>
            </div>
            """, unsafe_allow_html=True)
            
            for topic in topics:
                st.markdown(f"<p style='color: #cccccc;'>• {topic['title']}</p>", unsafe_allow_html=True)
        else:
            st.info("No topics created yet.")
    
    with tab2:
        st.markdown("""
        <div class="card">
            <h3 style="color: white; margin-bottom: 1rem;">Student Performance Analytics</h3>
        </div>
        """, unsafe_allow_html=True)
        
        results = db.get_all_results()
        topics = db.get_topics()
        
        if results:
            # Create analytics chart
            df_results = pd.DataFrame(results)
            
            # Average scores by topic
            topic_scores = df_results.groupby('topic_title')['score'].mean().reset_index()
            
            fig = px.bar(
                topic_scores, 
                x='topic_title', 
                y='score',
                title='Average Scores by Topic',
                color='score',
                color_continuous_scale='Viridis'
            )
            fig.update_layout(
                xaxis_title="Topic",
                yaxis_title="Average Score (%)",
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Filter options
            col1, col2, col3 = st.columns(3)
            
            with col1:
                students = df_results['student_id'].unique()
                selected_student = st.selectbox("Filter by Student", ['All Students'] + list(students))
            
            with col2:
                topic_titles = df_results['topic_title'].unique()
                selected_topic = st.selectbox("Filter by Topic", ['All Topics'] + list(topic_titles))
            
            with col3:
                if st.button("Reset Filters"):
                    st.rerun()
            
            # Filter results
            filtered_df = df_results.copy()
            if selected_student != 'All Students':
                filtered_df = filtered_df[filtered_df['student_id'] == selected_student]
            if selected_topic != 'All Topics':
                filtered_df = filtered_df[filtered_df['topic_title'] == selected_topic]
            
            # Display results table
            if not filtered_df.empty:
                # Format the dataframe for display
                display_df = filtered_df[['student_id', 'topic_title', 'score', 'submitted_at']].copy()
                display_df['submitted_at'] = pd.to_datetime(display_df['submitted_at']).dt.strftime('%Y-%m-%d')
                display_df.columns = ['Student ID', 'Topic', 'Score (%)', 'Date']
                
                st.dataframe(display_df, use_container_width=True)
            else:
                st.info("No results match the selected filters.")
        else:
            st.info("No test results available yet.")
    
    with tab3:
        st.markdown("""
        <div class="card">
            <h3 style="color: white; margin-bottom: 1rem;">User Management</h3>
        </div>
        """, unsafe_allow_html=True)
        
        users = db.get_all_users()
        current_user = st.session_state.user
        
        # Filter out current user
        other_users = [u for u in users if u['unique_id'] != current_user['unique_id']]
        
        if other_users:
            for user in other_users:
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    role_class = "role-master" if user['role'] == 'master' else "role-student"
                    st.markdown(f"""
                    <div style="padding: 1rem; background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%); border-radius: 8px; margin: 0.5rem 0; border: 1px solid #333333;">
                        <strong style="color: white;">{user['unique_id']}</strong>
                        <span class="role-badge {role_class}">{user['role']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    if user['role'] != 'master':
                        if st.button(f"Remove", key=f"remove_{user['unique_id']}"):
                            if db.remove_user(user['unique_id']):
                                st.success(f"User {user['unique_id']} removed successfully!")
                                st.rerun()
                            else:
                                st.error("Cannot remove master users.")
        else:
            st.info("No other users found.")

def main():
    """Main application function"""
    st.set_page_config(
        page_title="WIDA Syllabus Tracker",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    apply_custom_css()
    
    # Initialize session state
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'page' not in st.session_state:
        st.session_state.page = 'landing'
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown('<div class="sidebar-title">📚 WIDA Tracker</div>', unsafe_allow_html=True)
        
        if st.session_state.user:
            user = st.session_state.user
            role_color = "#ffffff" if user['role'] == 'master' else "#cccccc"
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%); padding: 1rem; border-radius: 10px; margin-bottom: 1rem; text-align: center; border: 1px solid #333333;">
                <strong style="color: white;">{user['unique_id']}</strong><br>
                <span style="color: {role_color}; font-size: 0.9rem; text-transform: uppercase; font-weight: 600;">{user['role']}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Navigation menu
            if st.button("🏠 Dashboard", use_container_width=True):
                st.session_state.page = 'dashboard'
                st.rerun()
            
            if user['role'] == 'student':
                if st.button("📊 My Analytics", use_container_width=True):
                    st.session_state.page = 'analytics'
                    st.rerun()
            
            if user['role'] == 'master':
                if st.button("⚙️ Management", use_container_width=True):
                    st.session_state.page = 'syllabus_management'
                    st.rerun()
                
                if st.button("👥 Student Analytics", use_container_width=True):
                    st.session_state.page = 'master_analytics'
                    st.rerun()
            
            st.markdown("---")
            
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.user = None
                st.session_state.page = 'landing'
                st.rerun()
        
        else:
            if st.button("🏠 Home", use_container_width=True):
                st.session_state.page = 'landing'
                st.rerun()
            
            if st.button("🔑 Login", use_container_width=True):
                st.session_state.page = 'login'
                st.rerun()
            
            if st.button("📝 Register", use_container_width=True):
                st.session_state.page = 'register'
                st.rerun()
    
    # Main content area
    if st.session_state.page == 'landing':
        show_landing_page()
    elif st.session_state.page == 'login':
        show_login_page()
    elif st.session_state.page == 'register':
        show_register_page()
    elif st.session_state.page == 'dashboard':
        if st.session_state.user:
            if st.session_state.user['role'] == 'master':
                show_master_dashboard()
            else:
                show_student_dashboard()
        else:
            st.session_state.page = 'login'
            st.rerun()
    elif st.session_state.page == 'syllabus_management':
        if st.session_state.user and st.session_state.user['role'] == 'master':
            show_syllabus_management_page()
        else:
            st.session_state.page = 'dashboard'
            st.rerun()
    elif st.session_state.page == 'analytics':
        if st.session_state.user and st.session_state.user['role'] == 'student':
            show_student_analytics()
        else:
            st.session_state.page = 'dashboard'
            st.rerun()
    elif st.session_state.page == 'master_analytics':
        if st.session_state.user and st.session_state.user['role'] == 'master':
            show_master_analytics()
        else:
            st.session_state.page = 'dashboard'
            st.rerun()
    elif st.session_state.page == 'test':
        if st.session_state.user:
            show_test_page()
        else:
            st.session_state.page = 'login'
            st.rerun()
    elif st.session_state.page == 'test_result':
        if st.session_state.user:
            show_test_result_page()
        else:
            st.session_state.page = 'login'
            st.rerun()

if __name__ == "__main__":
    main()
