
import pandas as pd
import os

# Define paths
base_dir = os.path.dirname(__file__)
career_path = os.path.join(base_dir, 'career_data.csv')
opp_path = os.path.join(base_dir, 'opportunities.csv')

# --- Expanded Career Data ---
# A rich dataset covering diverse fields: Tech, Arts, Science, Commerce, Vocational, etc.
careers = [
    # Tech & AI
    {"career": "Data Scientist", "interest": "Science, Logic", "skill": "Mathematics, Coding, Python"},
    {"career": "Software Engineer", "interest": "Technology, Building", "skill": "Coding, Problem Solving"},
    {"career": "AI Researcher", "interest": "AI, Research", "skill": "Machine Learning, Mathematics"},
    {"career": "Cybersecurity Analyst", "interest": "Security, Technology", "skill": "Networking, Scripting"},
    {"career": "Web Developer", "interest": "Design, Technology", "skill": "HTML, CSS, JavaScript"},
    {"career": "Cloud Architect", "interest": "Infrastructure, Tech", "skill": "AWS, Azure, Networking"},
    {"career": "Game Developer", "interest": "Gaming, Creativity", "skill": "C++, Unity, Design"},
    {"career": "UX/UI Designer", "interest": "Art, Psychology", "skill": "Design Tools, Empathy"},
    {"career": "Blockchain Developer", "interest": "Crypto, Finance", "skill": "Solidity, Cryptography"},
    {"career": "Robotics Engineer", "interest": "Machines, Hardware", "skill": "C++, Mechanics, Electronics"},

    # Science & Healthcare
    {"career": "Doctor (Physician)", "interest": "Helping People, Health", "skill": "Biology, Empathy"},
    {"career": "Nurse", "interest": "Care, Health", "skill": "Patient Care, Biology"},
    {"career": "Agricultural Scientist", "interest": "Nature, Farming", "skill": "Biology, chemistry"},
    {"career": "Biomedical Engineer", "interest": "Health, Engineering", "skill": "Biology, Mechanics"},
    {"career": "Environmental Scientist", "interest": "Nature, Climate", "skill": "Research, Ecology"},
    {"career": "Pharmacist", "interest": "Chemistry, Health", "skill": "Chemistry, Attention to Detail"},
    {"career": "Psychologist", "interest": "Mind, People", "skill": "Listening, Analysis"},
    {"career": "Veterinarian", "interest": "Animals, Medicine", "skill": "Animal Care, Biology"},
    {"career": "Astronomer", "interest": "Space, Physics", "skill": "Math, Physics, Research"},
    
    # Arts & Humanities
    {"career": "Journalist", "interest": "Storytelling, News", "skill": "Writing, Research"},
    {"career": "Author", "interest": "Stories, Books", "skill": "Creative Writing"},
    {"career": "Graphic Designer", "interest": "Art, Visuals", "skill": "Photoshop, Creativity"},
    {"career": "Musician", "interest": "Music, Performance", "skill": "Instruments, Composition"},
    {"career": "Digital Marketer", "interest": "Social Media, Trends", "skill": "SEO, Content Creation"},
    {"career": "Film Director", "interest": "Movies, Storytelling", "skill": "Leadership, Vision"},
    {"career": "Fashion Designer", "interest": "Style, Clothes", "skill": "Sewing, Sketching"},
    {"career": "Translator", "interest": "Languages, Culture", "skill": "Fluency, Writing"},
    
    # Commerce & Business
    {"career": "Accountant", "interest": "Money, Numbers", "skill": "Math, Excel"},
    {"career": "Economist", "interest": "Markets, Society", "skill": "Analysis, Math"},
    {"career": "Investment Banker", "interest": "Finance, Money", "skill": "Financial Modeling, Analysis"},
    {"career": "Human Resources Manager", "interest": "People, Management", "skill": "Communication, Organization"},
    {"career": "Product Manager", "interest": "Strategy, Tech", "skill": "Leadership, Planning"},
    {"career": "Entrepreneur", "interest": "Business, Innovation", "skill": "Risk Taking, Management"},
    {"career": "Real Estate Agent", "interest": "Property, Sales", "skill": "Negotiation, Communication"},
    
    # Vocational & Trades
    {"career": "Electrician", "interest": "Fixing things, Tech", "skill": "Wiring, Safety"},
    {"career": "Carpenter", "interest": "Wood, Building", "skill": "Woodworking, Math"},
    {"career": "Chef", "interest": "Food, Cooking", "skill": "Culinary Arts, Creativity"},
    {"career": "Pilot", "interest": "Flying, Travel", "skill": "Navigation, Focus"},
    {"career": "Police Officer", "interest": "Justice, Safety", "skill": "Fitness, Law"},
    
    # Education
    {"career": "Teacher", "interest": "Helping Kids, Learning", "skill": "Communication, Patience"},
    {"career": "Professor", "interest": "Research, Academia", "skill": "Teaching, Expertise"},
    {"career": "Education Counselor", "interest": "Guidance, Students", "skill": "Listening, Planning"},
]

# --- Expanded Opportunities Data ---
opportunities = [
    # Scholarships
    {"Type": "Scholarship", "Name": "UWC Global Scholarship", "Field": "AI, General", "Target Group": "Rural Students", "Country": "Global", "URL": "https://www.uwc.org", "Description": "Fully funded high school education for underrepresented students"},
    {"Type": "Scholarship", "Name": "Gates Cambridge Scholarship", "Field": "All", "Target Group": "International Students", "Country": "UK", "URL": "https://www.gatescambridge.org", "Description": "Full-cost scholarships for outstanding applicants from countries outside the UK to pursue a full-time postgraduate degree"},
    {"Type": "Scholarship", "Name": "Chevening Scholarships", "Field": "Leadership", "Target Group": "Emerging Leaders", "Country": "UK", "URL": "https://www.chevening.org", "Description": "Fully funded scholarships to undertake any master's course at any UK university"},
    {"Type": "Scholarship", "Name": "Fulbright Foreign Student Program", "Field": "All", "Target Group": "International Students", "Country": "USA", "URL": "https://foreign.fulbrightonline.org", "Description": "Brings citizens of other countries to the United States for Master’s degree or Ph.D. study"},
    {"Type": "Scholarship", "Name": "Erasmus+ Master Loans", "Field": "All", "Target Group": "EU/Non-EU Students", "Country": "Europe", "URL": "https://ec.europa.eu/programmes/erasmus-plus", "Description": "EU funded scholarships for various master programs across Europe"},
    {"Type": "Scholarship", "Name": "DAAD Undergraduate Scholarships", "Field": "Engineering", "Target Group": "Developing countries", "Country": "Germany", "URL": "https://daad.de", "Description": "Bachelor-level scholarships in STEM fields"},
    {"Type": "Scholarship", "Name": "Rotary Peace Fellowships", "Field": "Peace, Conflict Resolution", "Target Group": "Leaders", "Country": "Global", "URL": "https://www.rotary.org", "Description": "Fully funded academic fellowships for master's degrees/certificates"},
    
    # Internships & Platforms
    {"Type": "Internship", "Name": "UNICEF AI Internship", "Field": "Machine Learning", "Target Group": "Low-income students", "Country": "Global", "URL": "https://www.unicef.org", "Description": "Remote AI internship focused on social good"},
    {"Type": "Platform", "Name": "Google AI for Youth", "Field": "AI", "Target Group": "Youth", "Country": "Based in India", "URL": "https://ai.google", "Description": "Free AI training programs for students in rural areas"},
    {"Type": "Platform", "Name": "Khan Academy", "Field": "All", "Target Group": "K-12 Students", "Country": "Global", "URL": "https://www.khanacademy.org", "Description": "Free world-class education for anyone, anywhere"},
    {"Type": "Platform", "Name": "Coursera for Refugees", "Field": "Various", "Target Group": "Refugees", "Country": "Global", "URL": "https://www.coursera.org/refugees", "Description": "Free access to Coursera catalog for refugees"},
    {"Type": "Internship", "Name": "CERN Technical Student Programme", "Field": "Physics, Engineering", "Target Group": "Undergraduates", "Country": "Switzerland", "URL": "https://careers.cern/students", "Description": "Practical training period for students in applied physics, engineering or computing"},
]

def generate_csvs():
    df_career = pd.DataFrame(careers)
    df_opp = pd.DataFrame(opportunities)
    
    df_career.to_csv(career_path, index=False)
    print(f"Generated {career_path} with {len(df_career)} careers.")
    
    df_opp.to_csv(opp_path, index=False)
    print(f"Generated {opp_path} with {len(df_opp)} opportunities.")

if __name__ == "__main__":
    generate_csvs()
