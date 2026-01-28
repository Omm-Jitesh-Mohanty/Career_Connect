# ai_engine/core/data_loader.py
import pandas as pd
import os
import random
from datetime import datetime

class DataLoader:
    """Professional data loader for multiple datasets"""
    
    def __init__(self):
        self.jobs = []
        self.students = []
        self.load_all_data()
    
    def load_all_data(self):
        """Load data from all available datasets"""
        print("📊 Loading career data from multiple sources...")
        
        # Load job data
        self.load_linkedin_jobs()
        self.load_career_recommendation_data()
        self.load_job_description_data()
        
        # Load student data
        self.load_student_performance_data()
        self.load_student_information_data()
        self.load_edu_data()
        
        # Add professional templates if needed
        if len(self.jobs) < 15:
            self.add_professional_templates()
        
        print(f"✅ Loaded {len(self.jobs)} jobs and {len(self.students)} student profiles")
    
    def load_linkedin_jobs(self):
        """Load LinkedIn job postings dataset"""
        try:
            paths = [
                'datasets/postings.csv',
                'datasets/job Datasset.csv',
                'datasets/postings.csv',
                'postings.csv'
            ]
            
            for path in paths:
                if os.path.exists(path):
                    df = pd.read_csv(path, low_memory=False, nrows=100)
                    print(f"   📁 Loading LinkedIn jobs from: {path}")
                    
                    for idx, row in df.iterrows():
                        if len(self.jobs) >= 80:
                            break
                            
                        title = str(row.get('title', '')).strip()
                        if not title or title.lower() == 'nan':
                            continue
                            
                        job = {
                            'id': f"linkedin_{idx}",
                            'title': title,
                            'company': str(row.get('company', row.get('company_name', 'Tech Company'))).strip(),
                            'location': str(row.get('location', 'Remote')).strip(),
                            'category': self.categorize_job(title),
                            'required_skills': self.extract_skills_linkedin(row),
                            'experience_level': self.get_experience_level(title),
                            'salary_range': self.estimate_realistic_salary(title),
                            'job_type': str(row.get('formatted_work_type', 'Full-time')),
                            'description': self.get_job_description(row, title),
                            'growth_potential': random.choice(['High', 'Very High', 'Medium']),
                            'is_real_data': True,
                            'data_source': 'LinkedIn',
                            'posted_date': datetime.now().strftime("%Y-%m-%d")
                        }
                        self.jobs.append(job)
                    
                    print(f"   ✅ Added {len([j for j in self.jobs if j['data_source'] == 'LinkedIn'])} LinkedIn jobs")
                    break
                    
        except Exception as e:
            print(f"   ❌ LinkedIn data loading failed: {e}")
    
    def load_career_recommendation_data(self):
        """Load career recommendation dataset"""
        try:
            paths = [
                'datasets/AI-based Career Recommendation.csv',
                'datasets/career_recommender.csv',
                'AI-based Career Recommendation.csv'
            ]
            
            for path in paths:
                if os.path.exists(path):
                    df = pd.read_csv(path, low_memory=False, nrows=50)
                    print(f"   📁 Loading career data from: {path}")
                    
                    for idx, row in df.iterrows():
                        title = str(row.get('Job Role', row.get('job_title', ''))).strip()
                        if not title:
                            continue
                            
                        job = {
                            'id': f"career_{idx}",
                            'title': title,
                            'company': 'Various Companies',
                            'location': 'Multiple Locations',
                            'category': self.categorize_job(title),
                            'required_skills': self.extract_skills_career(row),
                            'experience_level': 'Fresher',
                            'salary_range': self.estimate_realistic_salary(title),
                            'job_type': 'Full-time',
                            'description': f"Career opportunity for {title}",
                            'growth_potential': 'High',
                            'is_real_data': True,
                            'data_source': 'Career Dataset'
                        }
                        self.jobs.append(job)
                    
                    break
                    
        except Exception as e:
            print(f"   ❌ Career data loading failed: {e}")
    
    def load_job_description_data(self):
        """Load job description dataset"""
        try:
            paths = [
                'datasets/jobs/job_skills.csv',
                'datasets/jobs/salaries.csv',
                'job_skills.csv'
            ]
            
            for path in paths:
                if os.path.exists(path):
                    df = pd.read_csv(path, low_memory=False, nrows=50)
                    print(f"   📁 Loading job descriptions from: {path}")
                    
                    for idx, row in df.iterrows():
                        title = str(row.get('job_title', row.get('position', ''))).strip()
                        if not title:
                            continue
                            
                        job = {
                            'id': f"desc_{idx}",
                            'title': title,
                            'company': str(row.get('company', 'Leading Company')).strip(),
                            'location': 'Various Locations',
                            'category': self.categorize_job(title),
                            'required_skills': self.extract_skills_from_description(row),
                            'experience_level': self.get_experience_level(title),
                            'salary_range': self.estimate_realistic_salary(title),
                            'job_type': 'Full-time',
                            'description': str(row.get('job_description', f"Position for {title}")),
                            'growth_potential': random.choice(['High', 'Medium']),
                            'is_real_data': True,
                            'data_source': 'Job Description Dataset'
                        }
                        self.jobs.append(job)
                    
                    break
                    
        except Exception as e:
            print(f"   ❌ Job description loading failed: {e}")
    
    def load_student_performance_data(self):
        """Load student performance data"""
        try:
            paths = [
                'datasets/StudentsPerformance.csv',
                'datasets/student_performance.csv',
                'StudentsPerformance.csv'
            ]
            
            for path in paths:
                if os.path.exists(path):
                    df = pd.read_csv(path, nrows=50)
                    print(f"   📁 Loading student performance from: {path}")
                    
                    for idx, row in df.iterrows():
                        student = {
                            'id': f"perf_{idx}",
                            'math_score': row.get('math score', random.randint(60, 95)),
                            'reading_score': row.get('reading score', random.randint(60, 95)),
                            'writing_score': row.get('writing score', random.randint(60, 95)),
                            'gender': row.get('gender', 'Unknown'),
                            'race_ethnicity': row.get('race/ethnicity', 'Unknown'),
                            'parental_education': row.get('parental level of education', 'Unknown')
                        }
                        self.students.append(student)
                    
                    break
                    
        except Exception as e:
            print(f"   ❌ Student performance loading failed: {e}")
    
    def load_student_information_data(self):
        """Load student information dataset"""
        try:
            paths = [
                'datasets/students.csv',
                'datasets/StudentsPerformance.csv',
                'students.csv'
            ]
            
            for path in paths:
                if os.path.exists(path):
                    df = pd.read_csv(path, nrows=50)
                    print(f"   📁 Loading student info from: {path}")
                    # This dataset can be used for pattern analysis
                    break
                    
        except Exception as e:
            print(f"   ❌ Student info loading failed: {e}")
    
    def load_edu_data(self):
        """Load educational data"""
        try:
            paths = [
                'datasets/xAPI-Edu-Data.csv',
                'datasets/StudentsPerformance.csv',
                'xAPI-Edu-Data.csv'
            ]
            
            for path in paths:
                if os.path.exists(path):
                    df = pd.read_csv(path, nrows=50)
                    print(f"   📁 Loading educational data from: {path}")
                    # Used for educational pattern analysis
                    break
                    
        except Exception as e:
            print(f"   ❌ Educational data loading failed: {e}")
    
    def add_professional_templates(self):
        """Add professional job templates"""
        templates = [
            # Software Engineering
            {
                'title': 'Software Development Engineer',
                'category': 'Software Engineering',
                'skills': 'Python, Java, Data Structures, Algorithms, OOP, SQL, Git',
                'companies': ['Microsoft', 'Google', 'Amazon', 'Tech Solutions', 'Innovate Labs'],
                'locations': ['Bangalore', 'Hyderabad', 'Pune', 'Remote'],
                'salary': '8-15 LPA',
                'type': 'Full-time'
            },
            {
                'title': 'Frontend Developer Intern',
                'category': 'Web Development', 
                'skills': 'JavaScript, HTML, CSS, React, Bootstrap, Responsive Design',
                'companies': ['Web Services', 'Digital Solutions', 'Startup Labs'],
                'locations': ['Remote', 'Bhubaneswar', 'Chennai'],
                'salary': '20-35k/month',
                'type': 'Internship'
            },
            # Data Science
            {
                'title': 'Data Science Intern',
                'category': 'Data Science',
                'skills': 'Python, Machine Learning, Statistics, SQL, Data Analysis, Pandas',
                'companies': ['AI Research Labs', 'Data Analytics Inc', 'ML Solutions'],
                'locations': ['Bangalore', 'Remote', 'Hyderabad'],
                'salary': '25-40k/month', 
                'type': 'Internship'
            },
            {
                'title': 'Machine Learning Engineer',
                'category': 'Artificial Intelligence',
                'skills': 'Python, Deep Learning, TensorFlow, Neural Networks, ML Algorithms',
                'companies': ['AI Innovations', 'Neural Labs', 'Tech Giants'],
                'locations': ['Bangalore', 'Gurgaon', 'Remote'],
                'salary': '12-20 LPA',
                'type': 'Full-time'
            },
            # Cloud & DevOps
            {
                'title': 'Cloud Computing Intern',
                'category': 'Cloud Computing', 
                'skills': 'AWS, Python, Linux, Docker, Cloud Services, Networking',
                'companies': ['Cloud Systems', 'AWS Partners', 'CloudTech'],
                'locations': ['Pune', 'Bangalore', 'Remote'],
                'salary': '22-38k/month',
                'type': 'Internship'
            },
            {
                'title': 'DevOps Engineer',
                'category': 'DevOps',
                'skills': 'AWS, Docker, Kubernetes, Jenkins, Linux, CI/CD, Python',
                'companies': ['Tech Solutions', 'IT Services', 'Product Companies'],
                'locations': ['Bangalore', 'Pune', 'Hyderabad'],
                'salary': '10-18 LPA',
                'type': 'Full-time'
            },
            # Mobile Development
            {
                'title': 'Android Developer',
                'category': 'Mobile Development',
                'skills': 'Java, Kotlin, Android SDK, REST APIs, Firebase, Git',
                'companies': ['Mobile First', 'App Developers', 'Startups'],
                'locations': ['Bangalore', 'Remote', 'Delhi'],
                'salary': '6-12 LPA',
                'type': 'Full-time'
            },
            # Testing
            {
                'title': 'QA Automation Engineer',
                'category': 'Software Testing',
                'skills': 'Selenium, Java, TestNG, Automation, Manual Testing, SQL',
                'companies': ['Testing Solutions', 'IT Services', 'Product Companies'],
                'locations': ['Pune', 'Chennai', 'Bangalore'],
                'salary': '5-9 LPA',
                'type': 'Full-time'
            }
        ]
        
        for i, template in enumerate(templates):
            job = {
                'id': f"template_{i}",
                'title': template['title'],
                'company': random.choice(template['companies']),
                'location': random.choice(template['locations']),
                'category': template['category'],
                'required_skills': template['skills'],
                'experience_level': 'Intern' if 'Intern' in template['title'] else 'Fresher',
                'salary_range': template['salary'],
                'job_type': template['type'],
                'description': f"Excellent opportunity for {template['title']} role with growth potential",
                'growth_potential': random.choice(['High', 'Very High']),
                'is_real_data': False,
                'data_source': 'Professional Templates'
            }
            self.jobs.append(job)
    
    def categorize_job(self, title):
        """Categorize job based on title"""
        title_lower = title.lower()
        
        categories = {
            'Data Science': ['data scientist', 'data analyst', 'machine learning', 'ai', 'artificial intelligence'],
            'Software Engineering': ['software', 'developer', 'engineer', 'programmer', 'sde'],
            'Web Development': ['web', 'frontend', 'backend', 'fullstack', 'react', 'javascript'],
            'Mobile Development': ['android', 'ios', 'mobile', 'flutter'],
            'Cloud Computing': ['cloud', 'aws', 'azure', 'devops'],
            'Software Testing': ['testing', 'qa', 'quality assurance', 'automation'],
            'Business Analytics': ['business analyst', 'data analytics', 'analytics'],
            'Database': ['database', 'sql', 'dba', 'data engineer']
        }
        
        for category, keywords in categories.items():
            if any(keyword in title_lower for keyword in keywords):
                return category
        
        return 'Technology'
    
    def extract_skills_linkedin(self, row):
        """Extract skills from LinkedIn data"""
        skills = []
        title = str(row.get('title', '')).lower()
        
        # Extract from title
        if any(word in title for word in ['python', 'data']):
            skills.extend(['Python', 'Data Analysis'])
        if any(word in title for word in ['java']):
            skills.extend(['Java', 'OOP'])
        if any(word in title for word in ['javascript', 'web']):
            skills.extend(['JavaScript', 'HTML', 'CSS'])
        if any(word in title for word in ['machine learning', 'ml']):
            skills.extend(['Machine Learning', 'Statistics'])
        if any(word in title for word in ['cloud', 'aws']):
            skills.extend(['AWS', 'Cloud Computing'])
        
        # Add soft skills
        skills.extend(['Communication', 'Problem Solving', 'Teamwork'])
        return ', '.join(skills[:8])
    
    def extract_skills_career(self, row):
        """Extract skills from career dataset"""
        skills = []
        
        # Extract from various columns
        for col in row.index:
            if 'skill' in col.lower() or 'technology' in col.lower():
                value = str(row[col])
                if value and value.lower() not in ['nan', 'none']:
                    skills.extend([s.strip() for s in value.split(',')[:3]])
        
        if not skills:
            skills = ['Python', 'Communication', 'Problem Solving']
        
        return ', '.join(skills[:6])
    
    def extract_skills_from_description(self, row):
        """Extract skills from job description"""
        description = str(row.get('job_description', '')).lower()
        skills = []
        
        tech_skills = ['python', 'java', 'javascript', 'sql', 'html', 'css', 'react', 
                      'machine learning', 'aws', 'docker', 'kubernetes', 'git']
        
        for skill in tech_skills:
            if skill in description:
                skills.append(skill.title())
        
        if len(skills) < 3:
            skills.extend(['Communication', 'Problem Solving'])
        
        return ', '.join(skills[:6])
    
    def get_experience_level(self, title):
        """Determine experience level from title"""
        title_lower = title.lower()
        if any(word in title_lower for word in ['intern', 'trainee', 'fresher']):
            return 'Intern'
        elif any(word in title_lower for word in ['senior', 'lead', 'principal', 'manager']):
            return 'Experienced'
        else:
            return 'Fresher'
    
    def estimate_realistic_salary(self, title):
        """Estimate realistic salary based on role"""
        title_lower = title.lower()
        
        salary_ranges = {
            'intern': f"{random.randint(15, 40)}k/month",
            'data scientist': f"{random.randint(8, 15)} LPA",
            'machine learning': f"{random.randint(9, 16)} LPA", 
            'software engineer': f"{random.randint(6, 12)} LPA",
            'web developer': f"{random.randint(5, 10)} LPA",
            'cloud engineer': f"{random.randint(8, 14)} LPA",
            'android developer': f"{random.randint(6, 11)} LPA",
            'qa engineer': f"{random.randint(5, 9)} LPA"
        }
        
        for role, salary in salary_ranges.items():
            if role in title_lower:
                return salary
        
        return f"{random.randint(4, 8)} LPA"
    
    def get_job_description(self, row, title):
        """Generate job description from row data"""
        description = str(row.get('description', row.get('job_description', '')))
        if not description or description.lower() == 'nan':
            return f"Exciting opportunity for {title} role with growth potential and learning opportunities."
        
        return description[:200] + "..." if len(description) > 200 else description
    
    def get_all_jobs(self):
        """Return all loaded jobs"""
        return self.jobs
    
    def get_student_data(self):
        """Return student data for analysis"""
        return self.students