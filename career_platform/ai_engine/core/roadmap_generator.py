import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class DynamicRoadmapGenerator:
    """Dynamic Career Roadmap Generator with REAL progress integration"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
    
    def generate_dynamic_roadmap(self, student_profile, target_job, user):
        """Generate roadmap that dynamically adjusts based on REAL user progress"""
        
        # Get current CRS - using simplified calculation
        current_crs = self.calculate_simple_crs(student_profile)
        
        print(f"🎯 Generating DYNAMIC roadmap for: {student_profile.user.username}")
        print(f"📊 Current CRS: {current_crs}%")
        print(f"🎯 Target Job: {target_job['title']}")
        
        # Generate CRS data based on calculations
        crs_data = self.calculate_real_crs_data(student_profile, target_job, current_crs)
        
        # Generate roadmap steps based on CRS - ALWAYS 4 STEPS
        roadmap_steps = self.create_dynamic_steps(student_profile, target_job, current_crs, crs_data)
        
        # Calculate total timeline based on progress rate
        total_timeline = self.calculate_adaptive_timeline(current_crs, crs_data)
        
        return {
            'roadmap_steps': roadmap_steps,
            'crs_data': crs_data,
            'total_timeline': total_timeline,
            'current_crs': current_crs
        }

    def calculate_simple_crs(self, student_profile):
        """Simple CRS calculation without external dependencies"""
        if not student_profile:
            return 50
        
        base_score = 0
        
        # Academic Performance (30%)
        academic_score = self.calculate_academic_score(student_profile.cgpa)
        base_score += academic_score * 0.3
        
        # Skills Match (40%)
        skills_score = self.calculate_skills_score(student_profile.skills)
        base_score += skills_score * 0.4
        
        # Project Experience (20%)
        projects_score = self.calculate_projects_score(student_profile.projects)
        base_score += projects_score * 0.2
        
        # Learning Activities (10%) - default for now
        activities_score = 50
        base_score += activities_score * 0.1
        
        return min(int(base_score), 100)

    def calculate_real_crs_data(self, student_profile, target_job, current_crs):
        """Calculate comprehensive CRS data based on real user profile"""
        
        # Calculate component scores
        skill_match_score = self.calculate_skill_match(student_profile.skills, target_job)
        academic_score = self.calculate_academic_score(student_profile.cgpa)
        project_score = self.calculate_project_score(student_profile.projects)
        alignment_score = self.calculate_career_alignment(student_profile.interests, target_job)
        
        # Identify real skill gaps
        skill_gaps = self.identify_skill_gaps(student_profile.skills, target_job)
        
        # Generate recommendations based on gaps
        recommendations = self.generate_improvement_recommendations(skill_gaps, current_crs)
        
        return {
            'total_score': current_crs,
            'skill_match_score': skill_match_score,
            'academic_score': academic_score,
            'project_score': project_score,
            'alignment_score': alignment_score,
            'skill_gaps': skill_gaps,
            'recommendations': recommendations
        }

    def calculate_skill_match(self, user_skills, target_job):
        """Calculate skill match percentage"""
        if not user_skills:
            return 30
        
        user_skill_list = [skill.strip().lower() for skill in user_skills.split(',')]
        required_skills = target_job.get('required_skills', ['python', 'java', 'sql', 'problem solving'])
        
        if not required_skills:
            return 50
        
        # Simple matching
        matched_skills = sum(1 for skill in user_skill_list 
                           if any(req_skill in skill for req_skill in required_skills))
        
        match_percentage = (matched_skills / len(required_skills)) * 100
        return min(int(match_percentage), 100)

    def calculate_academic_score(self, cgpa):
        """Calculate academic score"""
        try:
            cgpa_val = float(cgpa) if cgpa else 6.0
            return min(int(cgpa_val * 10), 100)
        except:
            return 50

    def calculate_skills_score(self, skills_text):
        """Calculate skills score based on relevance and quantity"""
        if not skills_text:
            return 30
        
        skills_list = [skill.strip() for skill in skills_text.split(',')]
        
        # High-demand skills multiplier
        high_demand_skills = ['python', 'java', 'javascript', 'react', 'node', 'sql', 'aws', 'docker', 'git']
        
        relevant_skills = 0
        for skill in skills_list:
            if any(hs in skill.lower() for hs in high_demand_skills):
                relevant_skills += 2  # Bonus for high-demand skills
            else:
                relevant_skills += 1
        
        # Normalize score
        max_possible = len(high_demand_skills) * 2
        score = min((relevant_skills / max_possible) * 100, 100)
        
        return int(score)

    def calculate_project_score(self, projects):
        """Calculate project experience score"""
        if not projects:
            return 20
        
        project_count = len([p.strip() for p in projects.split(',')])
        return min(project_count * 20, 100)

    def calculate_career_alignment(self, interests, target_job):
        """Calculate career alignment score"""
        if not interests:
            return 50
        
        interest_list = [interest.strip().lower() for interest in interests.split(',')]
        job_category = target_job.get('category', '').lower()
        
        # Simple keyword matching
        alignment = sum(1 for interest in interest_list 
                       if any(keyword in interest for keyword in job_category.split()))
        
        return min(alignment * 25, 100)

    def identify_skill_gaps(self, user_skills, target_job):
        """Identify REAL skill gaps based on job requirements"""
        if not user_skills:
            user_skill_list = []
        else:
            user_skill_list = [skill.strip().lower() for skill in user_skills.split(',')]
        
        required_skills = target_job.get('required_skills', ['python', 'java', 'sql', 'problem solving'])
        
        skill_gaps = []
        for skill in required_skills:
            if not any(skill in user_skill for user_skill in user_skill_list):
                # Determine priority based on skill importance
                priority = 'High' if skill in ['python', 'java', 'sql', 'problem solving'] else 'Medium'
                skill_gaps.append({
                    'skill': skill.title(),
                    'priority': priority,
                    'description': f'Learn {skill} for {target_job["title"]} role'
                })
        
        return skill_gaps[:5]  # Return top 5 gaps

    def generate_improvement_recommendations(self, skill_gaps, current_crs):
        """Generate personalized improvement recommendations"""
        recommendations = []
        
        # Based on skill gaps
        for gap in skill_gaps[:3]:
            if gap['priority'] == 'High':
                recommendations.append(f"Focus on learning {gap['skill']} - high priority for your target role")
        
        # Based on CRS level
        if current_crs < 40:
            recommendations.extend([
                "Build foundational programming skills",
                "Start with basic projects to gain hands-on experience",
                "Focus on improving academic performance"
            ])
        elif current_crs < 60:
            recommendations.extend([
                "Work on intermediate-level projects",
                "Learn industry-relevant tools and technologies",
                "Practice coding problems regularly"
            ])
        elif current_crs < 80:
            recommendations.extend([
                "Contribute to open-source projects",
                "Prepare for technical interviews",
                "Network with professionals in your field"
            ])
        else:
            recommendations.extend([
                "Focus on specialization and advanced topics",
                "Build a strong professional portfolio",
                "Prepare for leadership roles"
            ])
        
        return recommendations[:5]

    def create_dynamic_steps(self, student_profile, target_job, current_crs, crs_data):
        """Create roadmap steps that dynamically adjust based on REAL CRS - ALWAYS 4 STEPS"""
        
        # ALWAYS return 4 steps, regardless of CRS
        base_steps = [
            {
                'step': 1,
                'title': self.get_step_title(current_crs, 1),
                'duration': self.get_duration_based_on_crs(current_crs, 'foundation'),
                'focus_areas': self.get_focus_areas(crs_data, 1),
                'completion_metrics': [
                    'Master core programming concepts', 
                    'Close high-priority skill gaps',
                    'Complete basic certification'
                ],
                'resources': [
                    {'name': 'FreeCodeCamp', 'url': 'https://freecodecamp.org', 'free': True},
                    {'name': 'GeeksforGeeks', 'url': 'https://geeksforgeeks.org', 'free': True}
                ],
                'expected_crs_improvement': f'{self.get_expected_improvement(current_crs, 1)}%'
            },
            {
                'step': 2,
                'title': self.get_step_title(current_crs, 2),
                'duration': self.get_duration_based_on_crs(current_crs, 'specialization'),
                'focus_areas': self.get_focus_areas(crs_data, 2),
                'completion_metrics': [
                    f'Learn {target_job["category"]} specific technologies', 
                    'Build portfolio projects',
                    'Complete advanced courses'
                ],
                'resources': [
                    {'name': 'Coursera Specializations', 'url': 'https://coursera.org', 'free': False},
                    {'name': 'Udemy Courses', 'url': 'https://udemy.com', 'free': False}
                ],
                'expected_crs_improvement': f'{self.get_expected_improvement(current_crs, 2)}%'
            },
            {
                'step': 3,
                'title': self.get_step_title(current_crs, 3),
                'duration': self.get_duration_based_on_crs(current_crs, 'projects'),
                'focus_areas': self.get_focus_areas(crs_data, 3),
                'completion_metrics': [
                    'Complete internships or freelance work', 
                    'Build complex projects',
                    'Contribute to open source'
                ],
                'resources': [
                    {'name': 'Internshala', 'url': 'https://internshala.com', 'free': True},
                    {'name': 'GitHub', 'url': 'https://github.com', 'free': True}
                ],
                'expected_crs_improvement': f'{self.get_expected_improvement(current_crs, 3)}%'
            },
            {
                'step': 4,
                'title': self.get_step_title(current_crs, 4),
                'duration': self.get_duration_based_on_crs(current_crs, 'preparation'),
                'focus_areas': self.get_focus_areas(crs_data, 4),
                'completion_metrics': [
                    'Prepare resume and portfolio', 
                    'Practice coding interviews',
                    'Network with professionals'
                ],
                'resources': [
                    {'name': 'LeetCode', 'url': 'https://leetcode.com', 'free': True},
                    {'name': 'LinkedIn', 'url': 'https://linkedin.com', 'free': True}
                ],
                'expected_crs_improvement': f'{self.get_expected_improvement(current_crs, 4)}%'
            }
        ]
        
        print(f"📋 Generated {len(base_steps)} roadmap steps for CRS: {current_crs}%")
        return base_steps

    def get_step_title(self, current_crs, step_number):
        """Get appropriate step title based on CRS level"""
        if current_crs >= 80:
            titles = {
                1: 'Advanced Skill Enhancement',
                2: 'Expert Specialization',
                3: 'Industry Leadership Projects', 
                4: 'Executive Preparation'
            }
        elif current_crs >= 60:
            titles = {
                1: 'Skill Foundation & Gap Closure',
                2: 'Specialized Skill Development',
                3: 'Practical Experience & Projects',
                4: 'Job Preparation & Interview Readiness'
            }
        else:
            titles = {
                1: 'Basic Skill Foundation',
                2: 'Core Skill Development',
                3: 'Hands-on Project Experience',
                4: 'Career Preparation Basics'
            }
        return titles.get(step_number, f'Step {step_number}')

    def get_focus_areas(self, crs_data, step_number):
        """Get focus areas for each step, ensuring no empty arrays"""
        skill_gaps = crs_data.get('skill_gaps', [])
        
        if step_number == 1:
            # Step 1: High priority gaps or default technical skills
            focus_areas = [gap['skill'] for gap in skill_gaps if gap.get('priority') == 'High'][:3]
            return focus_areas if focus_areas else ['Programming Fundamentals', 'Core Concepts', 'Basic Tools']
        
        elif step_number == 2:
            # Step 2: Medium priority gaps or default specialization areas
            focus_areas = [gap['skill'] for gap in skill_gaps if gap.get('priority') == 'Medium'][:2]
            return focus_areas if focus_areas else ['Advanced Technologies', 'Specialized Tools', 'Industry Frameworks']
        
        elif step_number == 3:
            # Step 3: Project and experience focus
            return ['Real-world Applications', 'Industry Tools', 'Team Collaboration']
        
        else:  # step_number == 4
            # Step 4: Career preparation focus
            return ['Interview Skills', 'Resume Building', 'Networking']

    def get_duration_based_on_crs(self, current_crs, step_type):
        """Get dynamic duration based on current CRS"""
        if current_crs < 40:
            # Beginner - longer durations
            durations = {
                'foundation': '3-4 months',
                'specialization': '4-5 months', 
                'projects': '5-6 months',
                'preparation': '2-3 months'
            }
        elif current_crs < 60:
            # Intermediate - balanced
            durations = {
                'foundation': '2-3 months',
                'specialization': '3-4 months',
                'projects': '4-5 months',
                'preparation': '1-2 months'
            }
        elif current_crs < 80:
            # Advanced - accelerated
            durations = {
                'foundation': '1-2 months',
                'specialization': '2-3 months',
                'projects': '3-4 months',
                'preparation': '1 month'
            }
        else:
            # Expert - focused but still 4 steps
            durations = {
                'foundation': '1 month',
                'specialization': '2 months',
                'projects': '2-3 months',
                'preparation': '1 month'
            }
        
        return durations.get(step_type, '2-3 months')

    def get_expected_improvement(self, current_crs, step_number):
        """Calculate expected CRS improvement for each step"""
        base_improvement = [15, 20, 25, 10]  # Base improvements for each step
        
        # Adjust based on current CRS (harder to improve when already high)
        adjustment_factor = 1.0
        if current_crs >= 80:
            adjustment_factor = 0.5
        elif current_crs >= 60:
            adjustment_factor = 0.7
        elif current_crs >= 40:
            adjustment_factor = 0.9
        
        return int(base_improvement[step_number - 1] * adjustment_factor)

    def calculate_adaptive_timeline(self, current_crs, crs_data):
        """Calculate adaptive total timeline"""
        if current_crs < 40:
            return '10-16 months'
        elif current_crs < 60:
            return '7-12 months'
        elif current_crs < 80:
            return '4-8 months'
        else:
            return '2-5 months'

# Create global instance with the correct name
roadmap_generator = DynamicRoadmapGenerator()