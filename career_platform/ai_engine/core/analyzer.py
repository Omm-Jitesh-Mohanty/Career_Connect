# ai_engine/core/analyzer.py
import random

class SkillAnalyzer:
    """Advanced skill gap analyzer with market insights"""
    
    def __init__(self, data_loader):
        self.data_loader = data_loader
        self.jobs = data_loader.get_all_jobs()
    
    def analyze_skill_gaps(self, student_profile, career_recommendations=None):
        """Analyze specific technical skill gaps based on actual profile and job market"""
        try:
            student_skills = getattr(student_profile, 'skills', '').lower()
            student_branch = getattr(student_profile, 'branch', '').lower()
            
            # Parse student skills properly
            student_skill_list = [s.strip() for s in student_skills.split(',') if s.strip()]
            
            # If career recommendations are provided, use them to find missing skills
            if career_recommendations:
                gaps = self.analyze_gaps_from_recommendations(student_profile, career_recommendations, student_skill_list)
                if gaps:
                    return gaps[:4]  # Return top 4 gaps from recommendations
            
            # Fallback to general technical skill analysis
            return self.analyze_technical_skill_gaps(student_profile, student_skill_list, student_branch)
            
        except Exception as e:
            print(f"⚠️ Skill gap analysis error: {e}")
            return self.get_fallback_skill_gaps()
    
    def analyze_skill_gaps_with_careers(self, student_profile, career_recommendations):
        """Enhanced skill gap analysis using career recommendations - FIXED METHOD"""
        try:
            print(f"🔍 Analyzing gaps from {len(career_recommendations)} career recommendations")
            
            if not career_recommendations:
                return self.analyze_skill_gaps(student_profile)
            
            student_skills = getattr(student_profile, 'skills', '').lower()
            student_skill_list = [s.strip() for s in student_skills.split(',') if s.strip()]
            print(f"📝 Student skills: {student_skill_list}")
            
            # Extract required skills from career recommendations
            required_skills = set()
            skill_frequency = {}
            
            for job in career_recommendations:
                # Get skills from required_skills field
                if 'required_skills' in job:
                    skills_text = job['required_skills'].lower()
                    job_skills = [s.strip() for s in skills_text.split(',') if s.strip()]
                    required_skills.update(job_skills)
                    for skill in job_skills:
                        skill_frequency[skill] = skill_frequency.get(skill, 0) + 1
                
                # Get skills from missing_skills (these are what you need)
                if 'missing_skills' in job:
                    missing_skills = [s.lower().strip() for s in job['missing_skills']]
                    required_skills.update(missing_skills)
                    for skill in missing_skills:
                        skill_frequency[skill] = skill_frequency.get(skill, 0) + 1
            
            print(f"📊 Required skills from jobs: {list(required_skills)}")
            
            # Analyze which required skills are missing
            gaps = []
            for skill in required_skills:
                skill_missing = True
                for student_skill in student_skill_list:
                    if (skill in student_skill.lower() or 
                        student_skill.lower() in skill or 
                        self.is_skill_similar(skill, student_skill)):
                        skill_missing = False
                        break
                
                if skill_missing and len(skill) > 2:  # Avoid very short strings
                    skill_demand_count = skill_frequency.get(skill, 1)
                    
                    priority_score = min(100, skill_demand_count * 25)
                    priority = 'Critical' if priority_score > 80 else 'High' if priority_score > 60 else 'Medium'
                    
                    gap_info = {
                        'skill': skill.title(),
                        'market_demand': f"Required in {skill_demand_count} of your recommended jobs",
                        'priority': priority,
                        'priority_score': priority_score,
                        'learning_path': self.get_structured_learning_path(skill, student_profile.branch),
                        'duration': self.estimate_learning_duration(skill),
                        'resources': self.get_learning_resources(skill),
                        'projects': self.get_project_ideas(skill),
                        'reason': f"Essential for {skill_demand_count} recommended career paths"
                    }
                    gaps.append(gap_info)
                    print(f"🎯 Found gap: {skill} (priority: {priority})")
            
            # Sort by priority and return
            gaps.sort(key=lambda x: x['priority_score'], reverse=True)
            print(f"✅ Final gaps found: {len(gaps)}")
            return gaps[:5]  # Return top 5 gaps
            
        except Exception as e:
            print(f"⚠️ Enhanced skill gap analysis error: {e}")
            return self.analyze_skill_gaps(student_profile)
    
    def analyze_technical_skill_gaps(self, student_profile, student_skill_list, student_branch):
        """Analyze general technical skill gaps"""
        try:
            # Analyze real skill demand from job market
            skill_demand = self.analyze_market_demand()
            
            gaps = []
            technical_skills_priority = {
                'python': 95, 'java': 85, 'javascript': 80, 'sql': 90, 'machine learning': 75,
                'react': 70, 'aws': 80, 'docker': 65, 'data structures': 85, 'algorithms': 85,
                'html': 60, 'css': 60, 'node.js': 65, 'mongodb': 60, 'rest api': 70,
                'c++': 70, 'c#': 65, 'php': 55, 'angular': 60, 'vue': 55,
                'typescript': 65, 'express': 60, 'spring': 70, 'hibernate': 60,
                'kubernetes': 60, 'azure': 65, 'gcp': 60, 'firebase': 55
            }
            
            # Check for missing high-demand technical skills
            for skill, base_demand in technical_skills_priority.items():
                # Check if student doesn't have this skill
                skill_missing = True
                for student_skill in student_skill_list:
                    if skill in student_skill.lower() or student_skill.lower() in skill:
                        skill_missing = False
                        break
                
                if skill_missing:
                    # Calculate actual demand percentage
                    actual_demand = skill_demand.get(skill, 0)
                    demand_percentage = (actual_demand / len(self.jobs)) * 100 if self.jobs else base_demand
                    
                    # Adjust priority based on branch
                    priority_score = self.calculate_technical_priority(skill, student_branch, demand_percentage)
                    
                    gaps.append({
                        'skill': skill.title(),
                        'market_demand': f"{max(demand_percentage, base_demand):.1f}% of tech jobs require {skill.title()}",
                        'priority': 'Critical' if priority_score > 80 else 'High' if priority_score > 60 else 'Medium',
                        'priority_score': priority_score,
                        'learning_path': self.get_structured_learning_path(skill, student_branch),
                        'duration': self.estimate_learning_duration(skill),
                        'resources': self.get_learning_resources(skill),
                        'projects': self.get_project_ideas(skill),
                        'reason': self.get_technical_gap_reason(skill, student_branch)
                    })
            
            # Sort by priority and return top gaps
            gaps.sort(key=lambda x: x['priority_score'], reverse=True)
            return gaps[:4]  # Return top 4 technical gaps
            
        except Exception as e:
            print(f"⚠️ Technical skill gap analysis error: {e}")
            return self.get_fallback_skill_gaps()
    
    def analyze_gaps_from_recommendations(self, student_profile, career_recommendations, student_skill_list):
        """Analyze skill gaps based on career recommendations"""
        try:
            gaps = []
            skill_frequency = {}
            
            # Count how often each missing skill appears in recommendations
            for job in career_recommendations:
                if 'missing_skills' in job:
                    for skill in job['missing_skills']:
                        skill_lower = skill.lower().strip()
                        skill_frequency[skill_lower] = skill_frequency.get(skill_lower, 0) + 1
            
            # Create gap entries for frequently missing skills
            for skill, frequency in skill_frequency.items():
                if frequency >= 1:  # Skills missing in at least one recommendation
                    # Verify student actually doesn't have this skill
                    skill_missing = True
                    for student_skill in student_skill_list:
                        if (skill in student_skill.lower() or 
                            student_skill.lower() in skill or 
                            self.is_skill_similar(skill, student_skill)):
                            skill_missing = False
                            break
                    
                    if skill_missing and len(skill) > 2:
                        priority_score = min(100, frequency * 25)
                        priority = 'Critical' if priority_score > 80 else 'High' if priority_score > 60 else 'Medium'
                        
                        gaps.append({
                            'skill': skill.title(),
                            'market_demand': f"Required in {frequency} of your recommended jobs",
                            'priority': priority,
                            'priority_score': priority_score,
                            'learning_path': self.get_structured_learning_path(skill, student_profile.branch),
                            'duration': self.estimate_learning_duration(skill),
                            'resources': self.get_learning_resources(skill),
                            'projects': self.get_project_ideas(skill),
                            'reason': f"Essential for {frequency} recommended career paths"
                        })
            
            return gaps
            
        except Exception as e:
            print(f"⚠️ Recommendation-based gap analysis error: {e}")
            return []
    
    def is_skill_similar(self, skill1, skill2):
        """Check if two skills are similar"""
        skill1 = skill1.lower()
        skill2 = skill2.lower()
        
        # Common skill variations
        variations = {
            'python': ['python programming', 'python3', 'python development'],
            'javascript': ['js', 'javascript programming'],
            'html': ['html5', 'html/css'],
            'css': ['css3', 'html/css'],
            'react': ['reactjs', 'react.js'],
            'node': ['nodejs', 'node.js'],
            'sql': ['database', 'mysql', 'postgresql'],
            'machine learning': ['ml', 'ai'],
            'data structures': ['ds', 'algorithms'],
        }
        
        for base_skill, aliases in variations.items():
            if skill1 in [base_skill] + aliases and skill2 in [base_skill] + aliases:
                return True
        
        return False
    
    def calculate_technical_priority(self, skill, branch, demand_percentage):
        """Calculate priority for technical skills"""
        base_score = demand_percentage
        
        # Branch-specific bonuses
        branch_bonuses = {
            'computer': {
                'python': 20, 'java': 15, 'data structures': 20, 'algorithms': 20, 
                'machine learning': 15, 'sql': 15, 'aws': 10, 'docker': 10
            },
            'electrical': {
                'python': 15, 'embedded': 20, 'iot': 20, 'arduino': 15, 'c++': 15
            },
            'mechanical': {
                'python': 10, 'cad': 20, 'solidworks': 20, 'matlab': 15, 'ansys': 15
            },
            'civil': {
                'autocad': 20, 'revit': 20, 'project management': 15, 'estimation': 10
            }
        }
        
        for branch_key, bonuses in branch_bonuses.items():
            if branch_key in branch:
                base_score += bonuses.get(skill, 0)
                break
        
        return min(base_score, 100)
    
    def analyze_market_demand(self):
        """Analyze current market demand for skills"""
        skill_demand = {}
        
        for job in self.jobs:
            skills = [s.strip().lower() for s in job['required_skills'].split(',')]
            for skill in skills:
                if skill.strip() and len(skill) > 2:
                    skill_demand[skill] = skill_demand.get(skill, 0) + 1
        
        return skill_demand
    
    def get_technical_gap_reason(self, skill, branch):
        """Get specific reason for technical skill gap"""
        reasons = {
            'python': 'Essential for software development, data science, and automation across all domains',
            'java': 'Critical for enterprise applications, Android development, and large-scale systems',
            'javascript': 'Fundamental for web development, frontend frameworks, and full-stack development',
            'sql': 'Required for database management, data analysis, and backend development roles',
            'machine learning': 'High-growth field with excellent career opportunities and high salaries',
            'react': 'Most popular frontend framework with massive industry adoption',
            'aws': 'Cloud computing skills are essential for modern application deployment',
            'data structures': 'Core computer science concept crucial for technical interviews',
            'algorithms': 'Fundamental for problem-solving in coding interviews and real-world applications',
            'docker': 'Containerization skills are in high demand for DevOps roles',
            'node.js': 'Essential for JavaScript backend development and full-stack roles',
            'mongodb': 'Popular NoSQL database skills needed for modern web applications'
        }
        return reasons.get(skill, f'High demand technical skill in {branch} engineering field')
    
    def get_fallback_skill_gaps(self):
        """Fallback with relevant technical skills"""
        return [
            {
                'skill': 'Python Programming',
                'market_demand': '85% of software jobs require Python',
                'priority': 'Critical',
                'learning_path': [
                    'Python Basics & Syntax (2 weeks)',
                    'Data Structures & Algorithms (4 weeks)',
                    'Projects & Practice (4 weeks)'
                ],
                'duration': '10 weeks',
                'resources': [
                    {'name': 'Python for Everybody', 'platform': 'Coursera', 'free': True, 'url': 'https://www.coursera.org/specializations/python'},
                    {'name': 'Automate the Boring Stuff', 'platform': 'Online Book', 'free': True, 'url': 'https://automatetheboringstuff.com/'}
                ],
                'projects': [
                    'Build a web scraper',
                    'Create a data analysis dashboard',
                    'Develop a simple web application'
                ],
                'reason': 'Most demanded programming language across all tech domains'
            },
            {
                'skill': 'SQL & Databases',
                'market_demand': '75% of data-related roles require SQL',
                'priority': 'High',
                'learning_path': [
                    'SQL Fundamentals (2 weeks)',
                    'Database Design (2 weeks)',
                    'Advanced Queries (2 weeks)'
                ],
                'duration': '6 weeks',
                'resources': [
                    {'name': 'SQL for Data Science', 'platform': 'Coursera', 'free': True, 'url': 'https://www.coursera.org/learn/sql-for-data-science'},
                    {'name': 'SQL Practice Exercises', 'platform': 'HackerRank', 'free': True, 'url': 'https://www.hackerrank.com/domains/sql'}
                ],
                'projects': [
                    'Design a student database',
                    'Analyze sales data with SQL',
                    'Build a reporting system'
                ],
                'reason': 'Essential for database management and data analysis roles'
            }
        ]
    
    def get_structured_learning_path(self, skill, branch):
        """Get structured learning path for a skill"""
        paths = {
            'python': [
                'Python Basics & Syntax (1-2 weeks)',
                'Data Structures & Algorithms (3-4 weeks)',
                'Object-Oriented Programming (2 weeks)',
                'Projects & Practice (3-4 weeks)'
            ],
            'java': [
                'Java Fundamentals (2-3 weeks)',
                'Object-Oriented Programming (2-3 weeks)',
                'Spring Framework (3-4 weeks)',
                'Build REST APIs (2 weeks)'
            ],
            'machine learning': [
                'Python for Data Science (2 weeks)',
                'Statistics & Mathematics (3 weeks)',
                'ML Algorithms & Models (4 weeks)',
                'Real-world Projects (4 weeks)'
            ],
            'web development': [
                'HTML, CSS, JavaScript (3 weeks)',
                'React.js Framework (3 weeks)',
                'Backend with Node.js (3 weeks)',
                'Full-stack Project (3 weeks)'
            ],
            'aws': [
                'Cloud Concepts (1 week)',
                'AWS Core Services (3 weeks)',
                'Hands-on Labs (2 weeks)',
                'Project Deployment (2 weeks)'
            ],
            'data analysis': [
                'Python Pandas (2 weeks)',
                'Data Visualization (2 weeks)',
                'SQL for Analysis (2 weeks)',
                'Analytics Projects (3 weeks)'
            ],
            'sql': [
                'Database Fundamentals (1 week)',
                'SQL Queries (2 weeks)',
                'Advanced SQL (2 weeks)',
                'Database Design (1 week)'
            ],
            'react': [
                'JavaScript ES6+ (2 weeks)',
                'React Fundamentals (2 weeks)',
                'State Management (2 weeks)',
                'Projects (2 weeks)'
            ]
        }
        
        default_path = [
            'Fundamentals (2-3 weeks)',
            'Intermediate Concepts (3 weeks)',
            'Advanced Topics (3 weeks)',
            'Practical Projects (4 weeks)'
        ]
        
        return paths.get(skill.lower(), default_path)
    
    def estimate_learning_duration(self, skill):
        """Estimate learning duration based on skill complexity"""
        durations = {
            'python': '8-10 weeks',
            'java': '10-12 weeks', 
            'machine learning': '12-16 weeks',
            'web development': '10-12 weeks',
            'aws': '6-8 weeks',
            'data analysis': '8-10 weeks',
            'react': '6-8 weeks',
            'sql': '4-6 weeks',
            'javascript': '6-8 weeks',
            'html': '2-4 weeks',
            'css': '2-4 weeks',
            'docker': '4-6 weeks'
        }
        
        return durations.get(skill.lower(), '8-12 weeks')
    
    def get_learning_resources(self, skill):
        """Get curated learning resources"""
        resources = {
            'python': [
                {'name': 'Python for Everybody', 'platform': 'Coursera', 'free': True, 'url': 'https://www.coursera.org/specializations/python'},
                {'name': 'Automate the Boring Stuff', 'platform': 'Online Book', 'free': True, 'url': 'https://automatetheboringstuff.com/'},
                {'name': 'Python Official Documentation', 'platform': 'Python.org', 'free': True, 'url': 'https://docs.python.org/3/'}
            ],
            'java': [
                {'name': 'Java Programming & Software Engineering', 'platform': 'Coursera', 'free': True, 'url': 'https://www.coursera.org/specializations/java-programming'},
                {'name': 'Spring Framework Guide', 'platform': 'Spring.io', 'free': True, 'url': 'https://spring.io/guides'},
                {'name': 'Java Practice Exercises', 'platform': 'HackerRank', 'free': True, 'url': 'https://www.hackerrank.com/domains/java'}
            ],
            'machine learning': [
                {'name': 'Machine Learning Specialization', 'platform': 'Coursera', 'free': True, 'url': 'https://www.coursera.org/specializations/machine-learning-introduction'},
                {'name': 'Fast.ai Practical Deep Learning', 'platform': 'Fast.ai', 'free': True, 'url': 'https://course.fast.ai/'},
                {'name': 'Kaggle Micro-courses', 'platform': 'Kaggle', 'free': True, 'url': 'https://www.kaggle.com/learn'}
            ],
            'web development': [
                {'name': 'The Odin Project', 'platform': 'Odin Project', 'free': True, 'url': 'https://www.theodinproject.com/'},
                {'name': 'Full Stack Open', 'platform': 'University of Helsinki', 'free': True, 'url': 'https://fullstackopen.com/en/'},
                {'name': 'FreeCodeCamp', 'platform': 'FreeCodeCamp', 'free': True, 'url': 'https://www.freecodecamp.org/'}
            ],
            'sql': [
                {'name': 'SQL for Data Science', 'platform': 'Coursera', 'free': True, 'url': 'https://www.coursera.org/learn/sql-for-data-science'},
                {'name': 'SQL Bolt', 'platform': 'SQL Bolt', 'free': True, 'url': 'https://sqlbolt.com/'},
                {'name': 'W3Schools SQL', 'platform': 'W3Schools', 'free': True, 'url': 'https://www.w3schools.com/sql/'}
            ],
            'react': [
                {'name': 'React Official Tutorial', 'platform': 'React.js', 'free': True, 'url': 'https://reactjs.org/tutorial/tutorial.html'},
                {'name': 'Full Stack Open', 'platform': 'University of Helsinki', 'free': True, 'url': 'https://fullstackopen.com/en/'},
                {'name': 'React Practice Projects', 'platform': 'FreeCodeCamp', 'free': True, 'url': 'https://www.freecodecamp.org/learn/front-end-development-libraries/'}
            ]
        }
        
        default_resources = [
            {'name': 'Online Course', 'platform': 'Coursera/edX', 'free': True, 'url': 'https://www.coursera.org/'},
            {'name': 'Official Documentation', 'platform': 'Official', 'free': True, 'url': '#'},
            {'name': 'Practice Platform', 'platform': 'HackerRank/LeetCode', 'free': True, 'url': 'https://www.hackerrank.com/'}
        ]
        
        return resources.get(skill.lower(), default_resources)
    
    def get_project_ideas(self, skill):
        """Get practical project ideas for skill development"""
        projects = {
            'python': [
                'Build a personal budget tracker',
                'Create a web scraper for job postings',
                'Develop a simple chatbot',
                'Build a data analysis dashboard'
            ],
            'java': [
                'Create a student management system',
                'Build a REST API for a library system',
                'Develop a simple e-commerce application',
                'Create a multiplayer game'
            ],
            'machine learning': [
                'Predict house prices using regression',
                'Build a spam email classifier',
                'Create a movie recommendation system',
                'Develop an image recognition model'
            ],
            'web development': [
                'Build a portfolio website',
                'Create a task management app',
                'Develop a weather application',
                'Build a social media clone'
            ],
            'data analysis': [
                'Analyze COVID-19 dataset trends',
                'Create sales performance dashboard',
                'Analyze student performance patterns',
                'Build customer segmentation model'
            ],
            'sql': [
                'Design and implement a library database',
                'Create complex queries for business analytics',
                'Build a reporting system with multiple tables',
                'Optimize database performance'
            ],
            'react': [
                'Build a todo list application',
                'Create a weather app with API integration',
                'Develop a portfolio website with React',
                'Build a chat application interface'
            ]
        }
        
        return projects.get(skill.lower(), [
            'Build a simple application',
            'Create a portfolio project',
            'Solve real-world problems',
            'Contribute to open source'
        ])
    
    def get_ml_concepts_used(self):
        """Explain ML concepts used in the system"""
        return {
            'content_based_filtering': {
                'concept': 'Content-Based Filtering with TF-IDF',
                'purpose': 'Match student skills and profile with job requirements using text similarity',
                'algorithms': 'TF-IDF Vectorization + Cosine Similarity + K-means Clustering',
                'implementation': 'Converts skills, job titles, and descriptions to numerical vectors for similarity calculation',
                'advantage': 'Direct skill-based matching using real job market data'
            },
            'rule_based_matching': {
                'concept': 'Multi-factor Rule-Based Matching',
                'purpose': 'Recommend jobs based on academic profile, branch relevance, and skill overlap',
                'algorithms': 'CGPA scoring + Branch analysis + Skill matching + Experience level matching',
                'implementation': 'Comprehensive scoring system considering multiple student attributes',
                'advantage': 'Considers academic performance, branch specialization, and practical skills'
            },
            'diversity_sampling': {
                'concept': 'Diversity-aware Recommendation Sampling',
                'purpose': 'Ensure recommendations cover multiple job categories and companies',
                'algorithms': 'Category-based sampling + Company diversity + Cluster sampling',
                'implementation': 'Balances relevance with exploration across different career paths',
                'advantage': 'Provides diverse career options rather than similar repetitive suggestions'
            },
            'skill_gap_analysis': {
                'concept': 'Market-Driven Skill Gap Analysis',
                'purpose': 'Identify high-demand skills missing from student profile with branch relevance',
                'algorithms': 'Frequency analysis + Demand calculation + Branch relevance scoring',
                'implementation': 'Analyzes job market to find most requested skills with personalized priority',
                'advantage': 'Data-driven skill development guidance aligned with market needs'
            }
        }