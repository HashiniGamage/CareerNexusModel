# AI Job Demand Forecasting System

A comprehensive AI-powered system that predicts job demand trends for the next 2 years, provides personalized skills recommendations, and suggests educational pathways.

## Features

### 🔐 User Authentication
- Secure login/signup system with SQLite database
- Password hashing and session management
- User-specific prediction history

### 📊 Job Demand Predictions
- Industry-specific job demand forecasting
- Experience level-based recommendations
- 24-month growth predictions with confidence scores
- Salary range estimates in LKR

### 🎯 Skills Recommendations
- Personalized skill suggestions based on market trends
- Learning time estimates and difficulty levels
- Demand growth projections for each skill

### 🎓 Education Pathways
- Course and certification recommendations
- Local institution partnerships (University of Colombo, SLIIT, NSBM)
- Cost estimates and career alignment scores

### 📈 Advanced Analytics
- Time series analysis using ARIMA models
- Machine learning predictions with Random Forest and Gradient Boosting
- Interactive visualizations with Plotly
- Seasonal decomposition and trend analysis

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone or download the project files**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the database**
   ```bash
   python database_setup.py
   ```

4. **Run the Streamlit application**
   ```bash
   streamlit run app.py
   ```

5. **Access the application**
   - Open your browser and go to `http://localhost:8501`
   - Use the sample credentials or create a new account

## Sample Login Credentials

- **Admin User**: admin@jobforecaster.com / admin123
- **Regular User**: john@example.com / user123

## Supported Industries

1. **Technology** - Software engineering, data science, DevOps
2. **Healthcare** - Digital health, telemedicine, health analytics
3. **Finance** - FinTech, digital banking, blockchain
4. **Education** - EdTech, online learning, educational analytics
5. **Manufacturing** - Industrial IoT, automation, supply chain
6. **Retail** - E-commerce, digital marketing, customer analytics
7. **Consulting** - Digital transformation, business analysis
8. **Construction** - Construction tech, BIM, smart buildings

## Experience Levels

- **Entry Level** (0-2 years)
- **Mid Level** (3-5 years)
- **Senior Level** (6-10 years)
- **Executive Level** (10+ years)

## Database Schema

### Users Table
- User authentication and profile information
- Password hashing with SHA-256
- Account creation and last login tracking

### Prediction History
- Stores all user predictions with timestamps
- JSON format for flexible prediction data storage
- Links predictions to specific users

### User Preferences
- Customizable user settings
- Industry and experience level preferences
- Notification settings

## AI Models

### Time Series Forecasting
- **ARIMA Models** for trend analysis
- **Seasonal Decomposition** for cyclical patterns
- **Stationarity Testing** with Augmented Dickey-Fuller

### Machine Learning
- **Random Forest Regressor** for demand prediction
- **Gradient Boosting** for enhanced accuracy
- **K-Means Clustering** for skill grouping
- **Feature Engineering** with categorical encoding

### Data Processing
- Synthetic data generation for demonstration
- Real-time data cleaning and preprocessing
- Feature scaling and normalization

## File Structure

```
├── app.py                 # Main Streamlit application
├── database_setup.py      # Database initialization script
├── requirements.txt       # Python dependencies
├── README.md             # Documentation
├── job_forecaster.db     # SQLite database (created after setup)
└── static/               # Static assets (if any)
```

## Usage Guide

### 1. Authentication
- Create an account or login with existing credentials
- All predictions require authentication

### 2. Making Predictions
- Select your industry from 8 available options
- Choose your experience level
- Click "Generate Predictions" to get AI-powered forecasts

### 3. Viewing Results
- Review job demand predictions with growth rates
- Explore skills recommendations with learning timelines
- Check education pathway suggestions with costs

### 4. Downloading Data
- Export predictions as CSV files
- Save results for offline analysis

## Customization

### Adding New Industries
1. Update the `industry_jobs` dictionary in `create_synthetic_data()`
2. Add corresponding skills in `industry_skills`
3. Set growth rates in `growth_rates`

### Modifying Predictions
- Adjust the forecasting algorithms in `predict_job_demand()`
- Update salary ranges and skill mappings
- Customize confidence score calculations

### Database Extensions
- Add new tables in `database_setup.py`
- Extend user preferences and feedback systems
- Implement advanced analytics tracking

## Deployment

### Local Development
```bash
streamlit run app.py
```

### Production Deployment
1. **Streamlit Cloud**: Push to GitHub and deploy via Streamlit Cloud
2. **Heroku**: Use Procfile with `web: streamlit run app.py --server.port=$PORT`
3. **Docker**: Create Dockerfile with Python and Streamlit setup

## Security Features

- Password hashing with SHA-256
- SQL injection prevention with parameterized queries
- Session management for user authentication
- Input validation and sanitization

## Performance Optimization

- Efficient database queries with indexing
- Caching of ML model predictions
- Lazy loading of large datasets
- Optimized visualization rendering

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation for common solutions

## Version History

- **v1.0.0** - Initial release with core forecasting features
- **v1.1.0** - Added user authentication and database integration
- **v1.2.0** - Enhanced UI/UX and visualization improvements

---

Built with ❤️ using Streamlit, scikit-learn, and modern web technologies.