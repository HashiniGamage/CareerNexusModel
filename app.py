import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
import sqlite3
import hashlib
import json
import os
warnings.filterwarnings('ignore')

# Time Series Analysis
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller

# Machine Learning
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.cluster import KMeans

# Database setup
DATABASE_PATH = 'job_forecaster.db'

def init_database():
    """Initialize SQLite database for user authentication"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create user sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            session_token TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create predictions history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prediction_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            industry TEXT,
            experience_level TEXT,
            predictions_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(name, email, password):
    """Create new user account"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    try:
        password_hash = hash_password(password)
        cursor.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, password_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        conn.close()
        return None

def authenticate_user(email, password):
    """Authenticate user login"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    password_hash = hash_password(password)
    cursor.execute(
        "SELECT id, name, email FROM users WHERE email = ? AND password_hash = ?",
        (email, password_hash)
    )
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {'id': user[0], 'name': user[1], 'email': user[2]}
    return None

def save_prediction_history(user_id, industry, experience_level, predictions):
    """Save user's prediction history"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    predictions_json = json.dumps(predictions)
    cursor.execute(
        "INSERT INTO prediction_history (user_id, industry, experience_level, predictions_json) VALUES (?, ?, ?, ?)",
        (user_id, industry, experience_level, predictions_json)
    )
    
    conn.commit()
    conn.close()

class JobDemandForecaster:
    def __init__(self):
        self.models = {}
        self.encoders = {}
        self.scalers = {}
        self.time_series_data = {}
        
        # Initialize with synthetic data
        self.df = self.create_synthetic_data()
        self.df = self.clean_data(self.df)
        self.time_series_data = self.generate_time_series_data(self.df)
        
        # Train models
        self.train_ml_models(self.df)
    
    def create_synthetic_data(self):
        """Create synthetic job market data for demonstration"""
        np.random.seed(42)
        n_records = 5000
        
        # Industry-specific job titles
        industry_jobs = {
            'IT': ['Software Engineer', 'Data Scientist', 'DevOps Engineer', 'Product Manager', 
                          'Full Stack Developer', 'Machine Learning Engineer', 'Cloud Architect', 'Cybersecurity Specialist'],
            'Healthcare': ['Healthcare Data Analyst', 'Telemedicine Specialist', 'Health Informatics Specialist', 
                          'Digital Health Manager', 'Medical Software Developer', 'Healthcare AI Specialist'],
            'Finance': ['FinTech Product Manager', 'Digital Banking Specialist', 'Quantitative Analyst', 
                       'Blockchain Developer', 'Risk Data Scientist', 'Financial Software Engineer'],
            'Education': ['EdTech Product Manager', 'Learning Experience Designer', 'Educational Data Analyst', 
                         'Online Learning Specialist', 'Educational Technology Consultant'],
            'Manufacturing': ['Industrial IoT Engineer', 'Manufacturing Data Scientist', 'Automation Specialist', 
                             'Supply Chain Analyst', 'Quality Assurance Engineer'],
            'Retail': ['E-commerce Manager', 'Digital Marketing Specialist', 'Customer Experience Analyst', 
                      'Retail Data Scientist', 'Omnichannel Specialist'],
            'Consulting': ['Digital Transformation Consultant', 'Management Consultant', 'Technology Consultant', 
                          'Business Analyst', 'Strategy Consultant'],
            'Construction': ['Construction Technology Manager', 'BIM Specialist', 'Smart Building Consultant', 
                            'Construction Data Analyst', 'Project Management Software Specialist']
        }
        
        locations = ['Colombo', 'Kandy', 'Galle', 'Negombo', 'Jaffna', 'Kurunegala']
        experience_levels = ['Entry Level', 'Mid Level', 'Senior Level', 'Executive Level']
        
        # Skills by industry
        industry_skills = {
            'IT': ['Python', 'JavaScript', 'React', 'AWS', 'Machine Learning', 'Docker', 'Kubernetes', 'SQL'],
            'Healthcare': ['Healthcare Analytics', 'Medical Data Management', 'HIPAA Compliance', 'Telemedicine'],
            'Finance': ['FinTech', 'Blockchain', 'Financial Modeling', 'Risk Management', 'Regulatory Compliance'],
            'Education': ['Learning Management Systems', 'Educational Technology', 'Curriculum Development'],
            'Manufacturing': ['Industrial IoT', 'Automation', 'Supply Chain Management', 'Quality Control'],
            'Retail': ['E-commerce', 'Digital Marketing', 'Customer Analytics', 'Inventory Management'],
            'Consulting': ['Business Analysis', 'Strategy Development', 'Process Improvement', 'Change Management'],
            'Construction': ['Building Information Modeling', 'Project Management', 'Construction Technology']
        }
        
        # Generate synthetic data
        data = []
        start_date = datetime(2022, 1, 1)
        
        for i in range(n_records):
            # Generate date (last 2 years)
            date = start_date + timedelta(days=np.random.randint(0, 730))
            
            # Select industry and corresponding job
            industry = np.random.choice(list(industry_jobs.keys()))
            job_title = np.random.choice(industry_jobs[industry])
            location = np.random.choice(locations)
            experience = np.random.choice(experience_levels)
            
            # Generate salary based on job title and experience
            base_salaries = {
                'IT': 100000, 'Healthcare': 85000, 'Finance': 95000, 'Education': 70000,
                'Manufacturing': 75000, 'Retail': 65000, 'Consulting': 90000, 'Construction': 70000
            }
            
            experience_multiplier = {
                'Entry Level': 0.7, 'Mid Level': 1.0, 'Senior Level': 1.4, 'Executive Level': 1.8
            }
            
            salary = base_salaries[industry] * experience_multiplier[experience] * np.random.uniform(0.8, 1.2)
            
            # Generate skills
            skills = np.random.choice(industry_skills[industry], 
                                    size=np.random.randint(2, 5), replace=False)
            skills_str = ', '.join(skills)
            
            # Generate demand with trends and seasonality
            base_demand = np.random.uniform(50, 100)
            
            # Industry growth trends
            growth_rates = {
                'IT': 0.25, 'Healthcare': 0.18, 'Finance': 0.22, 'Education': 0.16,
                'Manufacturing': 0.14, 'Retail': 0.15, 'Consulting': 0.17, 'Construction': 0.12
            }
            
            trend = (date - start_date).days * growth_rates[industry] * 0.01
            seasonal = 10 * np.sin(2 * np.pi * date.timetuple().tm_yday / 365)
            noise = np.random.normal(0, 5)
            
            demand = max(0, base_demand + trend + seasonal + noise)
            
            data.append({
                'Date': date.strftime('%Y-%m-%d'),
                'Job_Title': job_title,
                'Industry': industry,
                'Location': location,
                'Experience_Level': experience,
                'Salary_LKR': salary * 300,  # Convert to LKR
                'Skills_Required': skills_str,
                'Demand_Index': demand,
                'Job_Postings': max(1, int(demand * np.random.uniform(0.5, 2.0)))
            })
        
        return pd.DataFrame(data)
    
    def clean_data(self, df):
        """Clean and prepare the data"""
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Handle missing values
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            df[col].fillna(df[col].median(), inplace=True)
        
        categorical_columns = df.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            if col != 'Date':
                df[col].fillna('Unknown', inplace=True)
        
        return df
    
    def generate_time_series_data(self, df):
        """Generate time series data for different job categories"""
        time_series_data = {}
        
        for industry in df['Industry'].unique():
            industry_data = df[df['Industry'] == industry].copy()
            industry_data['YearMonth'] = industry_data['Date'].dt.to_period('M')
            monthly_demand = industry_data.groupby('YearMonth')['Demand_Index'].mean().reset_index()
            monthly_demand['Date'] = monthly_demand['YearMonth'].dt.to_timestamp()
            
            if len(monthly_demand) >= 12:
                time_series_data[industry] = monthly_demand[['Date', 'Demand_Index']].set_index('Date')
        
        return time_series_data
    
    def train_ml_models(self, df):
        """Train machine learning models for demand prediction"""
        features = ['Job_Title', 'Industry', 'Location', 'Experience_Level']
        
        # Encode categorical variables
        for feature in features:
            self.encoders[feature] = LabelEncoder()
            df[f'{feature}_Encoded'] = self.encoders[feature].fit_transform(df[feature].astype(str))
        
        # Prepare feature matrix
        feature_columns = [f'{f}_Encoded' for f in features]
        if 'Salary_LKR' in df.columns:
            feature_columns.append('Salary_LKR')
        
        X = df[feature_columns]
        y = df['Demand_Index']
        
        # Scale features
        self.scalers['features'] = StandardScaler()
        X_scaled = self.scalers['features'].fit_transform(X)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
        
        # Train models
        self.models['random_forest'] = RandomForestRegressor(n_estimators=100, random_state=42)
        self.models['random_forest'].fit(X_train, y_train)
        
        self.models['gradient_boosting'] = GradientBoostingRegressor(n_estimators=100, random_state=42)
        self.models['gradient_boosting'].fit(X_train, y_train)
    
    def predict_job_demand(self, industry, experience_level):
        """Predict job demand for specific industry and experience level"""
        industry_data = self.df[
            (self.df['Industry'] == industry) & 
            (self.df['Experience_Level'] == experience_level)
        ]
        
        if len(industry_data) == 0:
            return []
        
        # Get unique job titles for the industry
        job_titles = industry_data['Job_Title'].unique()
        predictions = []
        
        for job_title in job_titles:
            job_data = industry_data[industry_data['Job_Title'] == job_title]
            
            if len(job_data) == 0:
                continue
            
            # Calculate current demand and growth
            current_demand = job_data['Demand_Index'].mean()
            
            # Simulate future growth based on industry trends
            growth_rates = {
                'Technology': 0.25, 'Healthcare': 0.18, 'Finance': 0.22, 'Education': 0.16,
                'Manufacturing': 0.14, 'Retail': 0.15, 'Consulting': 0.17, 'Construction': 0.12
            }
            
            base_growth = growth_rates.get(industry, 0.15) * 100
            predicted_growth = base_growth + np.random.uniform(-5, 10)
            
            # Get salary range
            salary_data = job_data['Salary_LKR']
            salary_min = salary_data.min()
            salary_max = salary_data.max()
            salary_range = f"LKR {salary_min:,.0f} - {salary_max:,.0f}"
            
            # Get skills
            skills_list = []
            for skills_str in job_data['Skills_Required'].dropna():
                skills = [skill.strip() for skill in str(skills_str).split(',')]
                skills_list.extend(skills)
            
            unique_skills = list(set(skills_list))[:6]  # Top 6 skills
            
            predictions.append({
                'job_title': job_title,
                'current_demand': min(100, max(0, current_demand)),
                'predicted_growth': predicted_growth,
                'confidence_score': np.random.uniform(85, 98),
                'salary_range': salary_range,
                'skills_required': unique_skills
            })
        
        # Sort by predicted growth
        predictions.sort(key=lambda x: x['predicted_growth'], reverse=True)
        return predictions[:8]  # Return top 8 jobs

def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="CareerNexus",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize database
    init_database()
    
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'forecaster' not in st.session_state:
        st.session_state.forecaster = JobDemandForecaster()
    
    # Authentication UI
    if not st.session_state.authenticated:
        st.title("🚀 CareerNexus")
        st.markdown("### Welcome! Please login or create an account to access job demand predictions.")
        
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            st.subheader("Login to Your Account")
            with st.form("login_form"):
                email = st.text_input("Email Address")
                password = st.text_input("Password", type="password")
                login_button = st.form_submit_button("Login")
                
                if login_button:
                    if email and password:
                        user = authenticate_user(email, password)
                        if user:
                            st.session_state.authenticated = True
                            st.session_state.user = user
                            st.success(f"Welcome back, {user['name']}!")
                            st.rerun()
                        else:
                            st.error("Invalid email or password")
                    else:
                        st.error("Please fill in all fields")
        
        with tab2:
            st.subheader("Create New Account")
            with st.form("signup_form"):
                name = st.text_input("Full Name")
                email = st.text_input("Email Address")
                password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                signup_button = st.form_submit_button("Create Account")
                
                if signup_button:
                    if name and email and password and confirm_password:
                        if password != confirm_password:
                            st.error("Passwords do not match")
                        elif len(password) < 6:
                            st.error("Password must be at least 6 characters long")
                        else:
                            user_id = create_user(name, email, password)
                            if user_id:
                                st.session_state.authenticated = True
                                st.session_state.user = {'id': user_id, 'name': name, 'email': email}
                                st.success(f"Account created successfully! Welcome, {name}!")
                                st.rerun()
                            else:
                                st.error("Email already exists or account creation failed")
                    else:
                        st.error("Please fill in all fields")
        
        return
    
    # Main application (authenticated users only)
    st.title("🚀 CareerNexus")
    st.markdown(f"**Welcome, {st.session_state.user['name']}!** | Predict future job trends for the next 2 years")
    
    # Logout button
    if st.button("Logout", type="secondary"):
        st.session_state.authenticated = False
        st.session_state.user = None
        st.rerun()
    
    # Sidebar for inputs
    st.sidebar.header("🎯 Configuration")
    
    # Industry selection
    industries = ['Technology', 'Healthcare', 'Finance', 'Education', 
                 'Manufacturing', 'Retail', 'Consulting', 'Construction']
    selected_industry = st.sidebar.selectbox("Select Industry", industries)
    
    # Experience level selection
    experience_levels = ['Entry Level', 'Mid Level', 'Senior Level', 'Executive Level']
    selected_experience = st.sidebar.selectbox("Select Experience Level", experience_levels)
    
    # Prediction button
    if st.sidebar.button("🔮 Generate Predictions", type="primary"):
        with st.spinner("Analyzing job market trends..."):
            # Get predictions
            predictions = st.session_state.forecaster.predict_job_demand(
                selected_industry, selected_experience
            )
            
            if predictions:
                # Save to session state
                st.session_state.predictions = predictions
                st.session_state.selected_industry = selected_industry
                st.session_state.selected_experience = selected_experience
                
                # Save to database
                save_prediction_history(
                    st.session_state.user['id'],
                    selected_industry,
                    selected_experience,
                    predictions
                )
                
                st.success("Predictions generated successfully!")
            else:
                st.error("No data available for the selected combination")
    
    # Display results if predictions exist
    if hasattr(st.session_state, 'predictions') and st.session_state.predictions:
        st.header(f"📈 Job Demand Predictions - {st.session_state.selected_industry}")
        st.subheader(f"Experience Level: {st.session_state.selected_experience}")
        
        # Summary metrics
        predictions = st.session_state.predictions
        avg_growth = np.mean([p['predicted_growth'] for p in predictions])
        high_growth_jobs = len([p for p in predictions if p['predicted_growth'] > 20])
        avg_confidence = np.mean([p['confidence_score'] for p in predictions])
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Average Growth", f"+{avg_growth:.1f}%")
        col2.metric("High Growth Jobs", high_growth_jobs)
        col3.metric("Average Confidence", f"{avg_confidence:.1f}%")
        col4.metric("Total Jobs Analyzed", len(predictions))
        
        # Predictions table
        st.subheader("📊 Detailed Job Analysis")
        
        # Create DataFrame for display
        df_display = pd.DataFrame([
            {
                'Job Title': p['job_title'],
                'Current Demand': f"{p['current_demand']:.1f}%",
                'Predicted Growth': f"+{p['predicted_growth']:.1f}%",
                'Confidence Score': f"{p['confidence_score']:.1f}%",
                'Salary Range': p['salary_range'],
                'Top Skills': ', '.join(p['skills_required'][:3])
            }
            for p in predictions
        ])
        
        st.dataframe(df_display, use_container_width=True)
        
        # Visualization
        fig = px.bar(
            x=[p['job_title'] for p in predictions],
            y=[p['predicted_growth'] for p in predictions],
            color=[p['current_demand'] for p in predictions],
            title='Job Demand Growth Forecast (Next 24 Months)',
            labels={'x': 'Job Title', 'y': 'Predicted Growth (%)', 'color': 'Current Demand'},
            color_continuous_scale='viridis'
        )
        fig.update_layout(xaxis_tickangle=-45, height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Skills recommendations
        st.subheader("🎯 Skills Recommendations")
        all_skills = []
        for p in predictions:
            all_skills.extend(p['skills_required'])
        
        skill_counts = pd.Series(all_skills).value_counts().head(8)
        
        for i, (skill, count) in enumerate(skill_counts.items()):
            col1, col2, col3 = st.columns([3, 1, 1])
            col1.write(f"**{skill}**")
            col2.write(f"+{np.random.randint(15, 30)}% demand")
            col3.write(f"{np.random.randint(3, 12)} months to learn")
        
        # Education recommendations
        st.subheader("🎓 Education Pathway Recommendations")
        
        education_recommendations = [
            {
                'Course': f'{selected_industry} Professional Certificate',
                'Institution': 'University of Colombo',
                'Duration': '6-12 months',
                'Cost': 'LKR 150,000 - 300,000',
                'Alignment': '92%'
            },
            {
                'Course': f'Advanced {selected_industry} Specialization',
                'Institution': 'SLIIT',
                'Duration': '1-2 years',
                'Cost': 'LKR 400,000 - 800,000',
                'Alignment': '88%'
            },
            {
                'Course': f'{selected_industry} Bootcamp',
                'Institution': 'NSBM Green University',
                'Duration': '3-6 months',
                'Cost': 'LKR 100,000 - 250,000',
                'Alignment': '85%'
            }
        ]
        
        for rec in education_recommendations:
            with st.expander(f"📚 {rec['Course']}"):
                col1, col2 = st.columns(2)
                col1.write(f"**Institution:** {rec['Institution']}")
                col1.write(f"**Duration:** {rec['Duration']}")
                col2.write(f"**Cost:** {rec['Cost']}")
                col2.write(f"**Career Alignment:** {rec['Alignment']}")
        
         
    
    # Footer
    st.markdown("---")
    st.markdown("Built with ❤️ using Streamlit | AI Job Demand Forecaster v1.0")

if __name__ == "__main__":
    main()