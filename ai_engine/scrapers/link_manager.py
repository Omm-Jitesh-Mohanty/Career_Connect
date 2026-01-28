# ai_engine/scrapers/link_manager.py - ENHANCED VERSION
from .internship_scraper import InternshipScraper
from .course_scraper import CourseScraper

class LinkManager:
    """ENHANCED manager for REAL branch-specific links"""
    
    def __init__(self):
        self.internship_scraper = InternshipScraper()
        self.course_scraper = CourseScraper()
    
    def get_opportunity_links(self, job_title, skills, category, branch, limit=6):
        """Get REAL internship/job links with branch-specific optimization"""
        print(f"🔗 Getting BRANCH-SPECIFIC links for {job_title} (Branch: {branch})...")
        
        all_links = []
        
        # Get internship links based on skills and branch
        internships = self.internship_scraper.get_internships_by_skills(skills, branch, limit=limit)
        
        for internship in internships:
            # Format details based on available information
            details_parts = []
            if internship.get('stipend'):
                details_parts.append(internship['stipend'])
            elif internship.get('salary'):
                details_parts.append(internship['salary'])
            else:
                details_parts.append('Competitive')
            
            details_parts.append(internship['location'])
            details_parts.append(internship.get('duration', 'Flexible'))
            
            all_links.append({
                'type': 'internship',
                'platform': internship['platform'],
                'title': internship['title'],
                'url': internship['url'],
                'company': internship['company'],
                'details': ' • '.join(details_parts),
                'relevance_score': internship.get('relevance_score', 75)
            })
        
        # Sort by relevance
        all_links.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        return all_links[:limit]
    
    def get_course_links(self, missing_skills, category, branch, limit=6):
        """Get REAL course links for skill development with branch context"""
        print(f"🔗 Getting BRANCH-SPECIFIC course links for {missing_skills} (Branch: {branch})...")
        
        all_courses = []
        
        # Get course links from multiple platforms with branch context
        courses = self.course_scraper.get_courses_by_missing_skills(missing_skills, branch, limit=limit)
        
        for course in courses:
            price_info = "Free" if course.get('free', False) else "Paid"
            rating = course.get('rating', 4.5)
            level = course.get('level', 'All Levels')
            
            all_courses.append({
                'type': 'course',
                'platform': course['platform'],
                'title': course['title'],
                'url': course['url'],
                'provider': course.get('provider', course['platform']),
                'details': f"{course.get('duration', 'Self-paced')} • {level} • {price_info} • ⭐{rating}",
                'relevance_score': course.get('relevance_score', 75)
            })
        
        # Sort by relevance
        all_courses.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        return all_courses[:limit]
    
    def get_comprehensive_development_plan(self, student_profile, job_recommendations, courses_limit=4, internships_limit=4):
        """Get comprehensive development plan with branch-specific resources"""
        development_plan = {}
        
        for job in job_recommendations:
            job_title = job['title']
            missing_skills = job.get('missing_skills', [])
            
            if missing_skills:
                missing_skills_str = ", ".join(missing_skills)
                
                development_plan[job_title] = {
                    'missing_skills': missing_skills,
                    'courses': self.get_course_links(
                        missing_skills_str, 
                        job['category'], 
                        student_profile.branch,
                        limit=courses_limit
                    ),
                    'internships': self.get_opportunity_links(
                        job_title,
                        missing_skills_str,
                        job['category'],
                        student_profile.branch,
                        limit=internships_limit
                    ),
                    'readiness_boost': f"+{min(len(missing_skills) * 8, 40)}% after completion",
                    'timeline': '4-12 weeks based on skill complexity'
                }
            else:
                # Provide general career development resources
                development_plan[job_title] = {
                    'missing_skills': [],
                    'courses': self.get_course_links(
                        "Career Development, Interview Skills, Professional Growth",
                        job['category'],
                        student_profile.branch,
                        limit=courses_limit
                    ),
                    'internships': self.get_opportunity_links(
                        job_title,
                        "Entry Level, Fresher Opportunities",
                        job['category'],
                        student_profile.branch,
                        limit=internships_limit
                    ),
                    'readiness_boost': "+15% professional readiness",
                    'timeline': '2-8 weeks for career preparation'
                }
        
        return development_plan