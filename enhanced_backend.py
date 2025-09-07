import streamlit as st
import sqlite3
import bcrypt
import uuid
import json
import base64
import requests
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import pandas as pd

class GitHubStorage:
    """GitHub-based storage for student data and test results"""
    
    def __init__(self, repo_owner: str, repo_name: str, token: str = None):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.token = token or st.secrets.get("github_token", "")
        self.base_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        } if self.token else {}
    
    def save_test_result(self, result_data: Dict) -> bool:
        """Save test result to GitHub repository"""
        if not self.token:
            return False
            
        try:
            # Create filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_results/{result_data['student_id']}_{timestamp}_{result_data['id']}.json"
            
            # Encode content
            content = base64.b64encode(json.dumps(result_data, default=str).encode()).decode()
            
            # Create file in repository
            data = {
                "message": f"Add test result for {result_data['student_id']}",
                "content": content,
                "branch": "main"
            }
            
            response = requests.put(f"{self.base_url}/contents/{filename}", 
                                  headers=self.headers, json=data)
            return response.status_code in [200, 201]
        except Exception as e:
            st.error(f"GitHub storage error: {e}")
            return False
    
    def save_user_data(self, user_data: Dict) -> bool:
        """Save user registration data to GitHub"""
        if not self.token:
            return False
            
        try:
            filename = f"users/{user_data['unique_id']}.json"
            content = base64.b64encode(json.dumps(user_data, default=str).encode()).decode()
            
            data = {
                "message": f"Add user {user_data['unique_id']}",
                "content": content,
                "branch": "main"
            }
            
            response = requests.put(f"{self.base_url}/contents/{filename}", 
                                  headers=self.headers, json=data)
            return response.status_code in [200, 201]
        except Exception as e:
            st.error(f"GitHub user storage error: {e}")
            return False
    
    def get_all_results(self) -> List[Dict]:
        """Retrieve all test results from GitHub"""
        if not self.token:
            return []
            
        try:
            response = requests.get(f"{self.base_url}/contents/test_results", 
                                  headers=self.headers)
            if response.status_code != 200:
                return []
                
            results = []
            files = response.json()
            
            for file_info in files:
                if file_info['name'].endswith('.json'):
                    file_response = requests.get(file_info['download_url'])
                    if file_response.status_code == 200:
                        results.append(file_response.json())
            
            return results
        except Exception as e:
            st.error(f"GitHub retrieval error: {e}")
            return []

class EnhancedDatabaseManager:
    """Enhanced database manager with GitHub integration and WIDA content"""
    
    def __init__(self, db_path: str = "wida_app.db", use_github: bool = True):
        self.db_path = db_path
        self.use_github = use_github
        self.github_storage = GitHubStorage("Unigalactix", "MR.COACH") if use_github else None
        self.init_database()
    
    def init_database(self):
        """Initialize the database with comprehensive WIDA content"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                unique_id TEXT PRIMARY KEY,
                role TEXT NOT NULL CHECK (role IN ('master', 'student')),
                password_hash TEXT,
                first_name TEXT,
                last_name TEXT,
                date_of_birth DATE,
                github_synced BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                profile_analytics TEXT
            )
        ''')
        
        # Syllabus topics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS topics (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                difficulty_level TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Questions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id TEXT PRIMARY KEY,
                topic_id TEXT NOT NULL,
                question_text TEXT NOT NULL,
                option_a TEXT NOT NULL,
                option_b TEXT NOT NULL,
                option_c TEXT NOT NULL,
                option_d TEXT NOT NULL,
                correct_answer INTEGER NOT NULL CHECK (correct_answer IN (0, 1, 2, 3)),
                explanation TEXT,
                FOREIGN KEY (topic_id) REFERENCES topics (id)
            )
        ''')
        
        # Test results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_results (
                id TEXT PRIMARY KEY,
                student_id TEXT NOT NULL,
                topic_id TEXT NOT NULL,
                topic_title TEXT NOT NULL,
                score INTEGER NOT NULL,
                time_taken INTEGER,
                github_synced BOOLEAN DEFAULT FALSE,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES users (unique_id),
                FOREIGN KEY (topic_id) REFERENCES topics (id)
            )
        ''')
        
        # Insert default users
        default_users = [
            ('KRURA', 'master'),
            ('student1', 'student'),
            ('student2', 'student')
        ]
        
        for user_id, role in default_users:
            cursor.execute('INSERT OR IGNORE INTO users (unique_id, role) VALUES (?, ?)', (user_id, role))
        
        # Insert comprehensive WIDA syllabus topics
        wida_topics = [
            # Reading Domain
            ('reading-1', 'Reading Comprehension Basics', 'Reading', 'Beginner'),
            ('reading-2', 'Academic Vocabulary in Context', 'Reading', 'Intermediate'),
            ('reading-3', 'Text Analysis and Interpretation', 'Reading', 'Advanced'),
            ('reading-4', 'Compare and Contrast Texts', 'Reading', 'Intermediate'),
            ('reading-5', 'Making Inferences from Text', 'Reading', 'Advanced'),
            
            # Listening Domain
            ('listening-1', 'Basic Listening Comprehension', 'Listening', 'Beginner'),
            ('listening-2', 'Academic Discussions', 'Listening', 'Intermediate'),
            ('listening-3', 'Lecture Comprehension', 'Listening', 'Advanced'),
            ('listening-4', 'Following Multi-step Instructions', 'Listening', 'Intermediate'),
            
            # Speaking Domain
            ('speaking-1', 'Basic Oral Communication', 'Speaking', 'Beginner'),
            ('speaking-2', 'Academic Presentations', 'Speaking', 'Intermediate'),
            ('speaking-3', 'Argumentative Speaking', 'Speaking', 'Advanced'),
            ('speaking-4', 'Collaborative Discussions', 'Speaking', 'Intermediate'),
            
            # Writing Domain
            ('writing-1', 'Sentence Structure and Grammar', 'Writing', 'Beginner'),
            ('writing-2', 'Paragraph Development', 'Writing', 'Intermediate'),
            ('writing-3', 'Essay Writing and Organization', 'Writing', 'Advanced'),
            ('writing-4', 'Research and Citation Skills', 'Writing', 'Advanced'),
            ('writing-5', 'Persuasive Writing Techniques', 'Writing', 'Intermediate'),
            
            # Language Functions
            ('function-1', 'Describing and Explaining', 'Language Functions', 'Beginner'),
            ('function-2', 'Comparing and Contrasting', 'Language Functions', 'Intermediate'),
            ('function-3', 'Arguing and Justifying', 'Language Functions', 'Advanced'),
            ('function-4', 'Sequencing and Narrating', 'Language Functions', 'Intermediate')
        ]
        
        for topic_id, title, category, difficulty in wida_topics:
            cursor.execute('''
                INSERT OR IGNORE INTO topics (id, title, category, difficulty_level) 
                VALUES (?, ?, ?, ?)
            ''', (topic_id, title, category, difficulty))
        
        # Insert comprehensive WIDA questions
        wida_questions = [
            # Reading Comprehension Basics
            ('q-read-1-1', 'reading-1', 'What is the main purpose of previewing a text before reading?', 
             'To finish reading faster', 'To understand the text structure and content', 'To find spelling errors', 'To count the pages', 1,
             'Previewing helps readers understand what to expect and activates prior knowledge.'),
            ('q-read-1-2', 'reading-1', 'Which strategy helps identify the main idea of a paragraph?', 
             'Reading only the first word', 'Looking for repeated keywords and concepts', 'Counting sentences', 'Skipping difficult words', 1,
             'Main ideas are often supported by repeated keywords and key concepts throughout the paragraph.'),
            
            # Academic Vocabulary
            ('q-read-2-1', 'reading-2', 'In academic texts, what does "synthesize" mean?', 
             'To break apart', 'To combine information from multiple sources', 'To memorize', 'To translate', 1,
             'Synthesis involves combining information from different sources to create new understanding.'),
            ('q-read-2-2', 'reading-2', 'The word "inference" in academic writing refers to:', 
             'Direct quotes from text', 'Conclusions drawn from evidence', 'Summary statements', 'Title headings', 1,
             'Inferences are logical conclusions based on evidence and reasoning.'),
            
            # Text Analysis
            ('q-read-3-1', 'reading-3', 'When analyzing author\'s purpose, which question is most important?', 
             'How long is the text?', 'Why did the author write this text?', 'When was it published?', 'Who is the publisher?', 1,
             'Understanding author\'s purpose is key to text analysis and critical reading.'),
            
            # Basic Listening
            ('q-listen-1-1', 'listening-1', 'Active listening requires:', 
             'Just hearing words', 'Full attention and engagement', 'Taking notes only', 'Memorizing everything', 1,
             'Active listening involves engaged attention, processing, and response.'),
            ('q-listen-1-2', 'listening-1', 'What helps improve listening comprehension?', 
             'Listening to music', 'Predicting content and asking questions', 'Speaking loudly', 'Reading while listening', 1,
             'Prediction and questioning enhance comprehension by activating prior knowledge.'),
            
            # Academic Discussions
            ('q-listen-2-1', 'listening-2', 'In academic discussions, "discourse markers" help listeners:', 
             'Count speakers', 'Follow the flow of ideas', 'Remember names', 'Take breaks', 1,
             'Discourse markers like "however," "furthermore" signal relationships between ideas.'),
            
            # Basic Grammar
            ('q-write-1-1', 'writing-1', 'A complete sentence must have:', 
             'Many adjectives', 'A subject and predicate', 'Five words minimum', 'Perfect spelling', 1,
             'Complete sentences require both a subject (who/what) and predicate (action/description).'),
            ('q-write-1-2', 'writing-1', 'Which sentence shows correct subject-verb agreement?', 
             'The students is studying', 'The student are studying', 'The students are studying', 'The student were studying', 2,
             'Plural subjects require plural verbs: "students are" not "students is."'),
            
            # Paragraph Development
            ('q-write-2-1', 'writing-2', 'A well-developed paragraph should have:', 
             'Only one sentence', 'A topic sentence and supporting details', 'No punctuation', 'Random ideas', 1,
             'Effective paragraphs start with a topic sentence and include relevant supporting details.'),
            
            # Essay Writing
            ('q-write-3-1', 'writing-3', 'The introduction paragraph should:', 
             'Include the conclusion', 'Present the thesis and hook the reader', 'List all evidence', 'Be the longest paragraph', 1,
             'Introductions present the main argument (thesis) and engage reader interest.'),
            
            # Language Functions - Describing
            ('q-func-1-1', 'function-1', 'When describing a process, which transition words are most helpful?', 
             'However, but, although', 'First, next, then, finally', 'In conclusion, therefore', 'For example, such as', 1,
             'Sequential transitions help readers follow step-by-step processes clearly.'),
            
            # Comparing and Contrasting
            ('q-func-2-1', 'function-2', 'Which phrase signals a contrast?', 
             'In addition', 'On the other hand', 'For instance', 'As a result', 1,
             '"On the other hand" explicitly signals that contrasting information follows.'),
            
            # Speaking - Presentations
            ('q-speak-2-1', 'speaking-2', 'Effective academic presentations should:', 
             'Read directly from notes', 'Include clear organization and visual aids', 'Speak very quickly', 'Avoid eye contact', 1,
             'Good presentations are well-organized, use visual support, and engage the audience.'),
        ]
        
        for question_data in wida_questions:
            cursor.execute('''
                INSERT OR IGNORE INTO questions 
                (id, topic_id, question_text, option_a, option_b, option_c, option_d, correct_answer, explanation) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', question_data)
        
        conn.commit()
        conn.close()
    
    def authenticate_user(self, unique_id: str, password: str = None) -> Optional[Dict]:
        """Authenticate user and return user data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT unique_id, role, password_hash FROM users WHERE unique_id = ?', (unique_id,))
        user = cursor.fetchone()
        
        conn.close()
        
        if user:
            if user[2] is None or password is None:
                return {'unique_id': user[0], 'role': user[1]}
            elif bcrypt.checkpw(password.encode('utf-8'), user[2]):
                return {'unique_id': user[0], 'role': user[1]}
        
        return None
    
    def register_user(self, unique_id: str, password: str = None, first_name: str = None, 
                      last_name: str = None, date_of_birth: str = None) -> bool:
        """Register a new user with detailed profile information and GitHub sync"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            password_hash = None
            if password:
                password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # Create initial analytics profile
            initial_analytics = {
                'total_tests': 0,
                'average_score': 0.0,
                'tests_by_category': {},
                'performance_trend': [],
                'strengths': [],
                'areas_for_improvement': [],
                'study_time_tracking': {},
                'goals': [],
                'achievements': []
            }
            
            cursor.execute('''
                INSERT INTO users (unique_id, role, password_hash, first_name, last_name, 
                                 date_of_birth, github_synced, profile_analytics) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (unique_id, 'student', password_hash, first_name, last_name, 
                  date_of_birth, False, str(initial_analytics)))
            
            # Sync to GitHub if available
            if self.github_storage:
                user_data = {
                    'unique_id': unique_id,
                    'role': 'student',
                    'first_name': first_name,
                    'last_name': last_name,
                    'date_of_birth': date_of_birth,
                    'registered_at': datetime.now().isoformat(),
                    'analytics': initial_analytics
                }
                if self.github_storage.save_user_data(user_data):
                    cursor.execute('UPDATE users SET github_synced = TRUE WHERE unique_id = ?', (unique_id,))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            conn.close()
            return False
    
    def get_user_profile(self, unique_id: str) -> Dict:
        """Get detailed user profile information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT unique_id, role, first_name, last_name, date_of_birth, 
                   profile_analytics, created_at, github_synced 
            FROM users WHERE unique_id = ?
        ''', (unique_id,))
        user = cursor.fetchone()
        
        conn.close()
        
        if user:
            try:
                analytics = eval(user[5]) if user[5] else {}
            except:
                analytics = {}
                
            return {
                'unique_id': user[0],
                'role': user[1],
                'first_name': user[2],
                'last_name': user[3],
                'date_of_birth': user[4],
                'analytics': analytics,
                'created_at': user[6],
                'github_synced': user[7]
            }
        return None
    
    def update_user_analytics(self, unique_id: str, analytics_data: Dict) -> bool:
        """Update user analytics (only for master users editing student profiles)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE users SET profile_analytics = ? WHERE unique_id = ?
            ''', (str(analytics_data), unique_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception:
            conn.close()
            return False
    
    def calculate_student_analytics(self, unique_id: str) -> Dict:
        """Calculate comprehensive analytics for a student"""
        results = self.get_student_results(unique_id)
        
        if not results:
            return {
                'total_tests': 0,
                'average_score': 0.0,
                'tests_by_category': {},
                'performance_trend': [],
                'strengths': [],
                'areas_for_improvement': []
            }
        
        # Calculate analytics
        total_tests = len(results)
        average_score = sum(r['score'] for r in results) / total_tests
        
        # Tests by category
        tests_by_category = {}
        category_scores = {}
        
        for result in results:
            category = result.get('category', 'General')
            if category not in tests_by_category:
                tests_by_category[category] = 0
                category_scores[category] = []
            tests_by_category[category] += 1
            category_scores[category].append(result['score'])
        
        # Performance trend (last 10 tests)
        recent_results = sorted(results, key=lambda x: x['submitted_at'])[-10:]
        performance_trend = [r['score'] for r in recent_results]
        
        # Identify strengths and areas for improvement
        strengths = []
        areas_for_improvement = []
        
        for category, scores in category_scores.items():
            avg_score = sum(scores) / len(scores)
            if avg_score >= 80:
                strengths.append(f"{category} (avg: {avg_score:.1f}%)")
            elif avg_score < 60:
                areas_for_improvement.append(f"{category} (avg: {avg_score:.1f}%)")
        
        return {
            'total_tests': total_tests,
            'average_score': round(average_score, 2),
            'tests_by_category': tests_by_category,
            'performance_trend': performance_trend,
            'strengths': strengths,
            'areas_for_improvement': areas_for_improvement,
            'category_averages': {cat: round(sum(scores)/len(scores), 2) 
                                for cat, scores in category_scores.items()}
        }
    
    def get_all_users(self) -> List[Dict]:
        """Get all users with profile information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT unique_id, role, first_name, last_name, date_of_birth, created_at 
            FROM users ORDER BY role, unique_id
        ''')
        users = cursor.fetchall()
        
        conn.close()
        return [{
            'unique_id': user[0], 
            'role': user[1],
            'first_name': user[2],
            'last_name': user[3],
            'date_of_birth': user[4],
            'created_at': user[5]
        } for user in users]
    
    def remove_user(self, unique_id: str) -> bool:
        """Remove a user (except master users)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT role FROM users WHERE unique_id = ?', (unique_id,))
        user = cursor.fetchone()
        
        if user and user[0] == 'master':
            conn.close()
            return False
        
        cursor.execute('DELETE FROM users WHERE unique_id = ?', (unique_id,))
        conn.commit()
        conn.close()
        return True
    
    def get_topics(self) -> List[Dict]:
        """Get all syllabus topics with categories"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, title, category, difficulty_level 
            FROM topics ORDER BY category, difficulty_level, title
        ''')
        topics = cursor.fetchall()
        
        conn.close()
        return [{
            'id': topic[0], 
            'title': topic[1], 
            'category': topic[2], 
            'difficulty': topic[3]
        } for topic in topics]
    
    def get_topics_by_category(self, category: str) -> List[Dict]:
        """Get topics filtered by category"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, title, category, difficulty_level 
            FROM topics WHERE category = ? ORDER BY difficulty_level, title
        ''', (category,))
        topics = cursor.fetchall()
        
        conn.close()
        return [{
            'id': topic[0], 
            'title': topic[1], 
            'category': topic[2], 
            'difficulty': topic[3]
        } for topic in topics]
    
    def add_topic(self, title: str, category: str = "Custom", difficulty: str = "Intermediate") -> bool:
        """Add a new topic"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        topic_id = f"custom-{uuid.uuid4().hex[:8]}"
        cursor.execute('''
            INSERT INTO topics (id, title, category, difficulty_level) 
            VALUES (?, ?, ?, ?)
        ''', (topic_id, title, category, difficulty))
        conn.commit()
        conn.close()
        return True
    
    def get_questions_for_topic(self, topic_id: str) -> List[Dict]:
        """Get all questions for a specific topic"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, question_text, option_a, option_b, option_c, option_d, correct_answer, explanation
            FROM questions WHERE topic_id = ?
        ''', (topic_id,))
        questions = cursor.fetchall()
        
        conn.close()
        return [{
            'id': q[0],
            'question_text': q[1],
            'options': [q[2], q[3], q[4], q[5]],
            'correct_answer': q[6],
            'explanation': q[7] or "No explanation available."
        } for q in questions]
    
    def submit_test_result(self, student_id: str, topic_id: str, topic_title: str, 
                          score: int, time_taken: int = None) -> str:
        """Submit test result with GitHub sync"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        result_id = f"result-{uuid.uuid4().hex[:8]}"
        cursor.execute('''
            INSERT INTO test_results (id, student_id, topic_id, topic_title, score, time_taken, github_synced) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (result_id, student_id, topic_id, topic_title, score, time_taken, False))
        
        # Sync to GitHub if available
        if self.github_storage:
            result_data = {
                'id': result_id,
                'student_id': student_id,
                'topic_id': topic_id,
                'topic_title': topic_title,
                'score': score,
                'time_taken': time_taken,
                'submitted_at': datetime.now().isoformat()
            }
            if self.github_storage.save_test_result(result_data):
                cursor.execute('UPDATE test_results SET github_synced = TRUE WHERE id = ?', (result_id,))
        
        conn.commit()
        conn.close()
        return result_id
    
    def get_student_results(self, student_id: str) -> List[Dict]:
        """Get all test results for a student"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, topic_id, topic_title, score, time_taken, submitted_at, github_synced
            FROM test_results WHERE student_id = ? 
            ORDER BY submitted_at DESC
        ''', (student_id,))
        results = cursor.fetchall()
        
        conn.close()
        return [{
            'id': r[0],
            'topic_id': r[1],
            'topic_title': r[2],
            'score': r[3],
            'time_taken': r[4],
            'submitted_at': r[5],
            'github_synced': bool(r[6])
        } for r in results]
    
    def get_all_results(self) -> List[Dict]:
        """Get all test results"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, student_id, topic_id, topic_title, score, time_taken, submitted_at, github_synced
            FROM test_results 
            ORDER BY submitted_at DESC
        ''')
        results = cursor.fetchall()
        
        conn.close()
        return [{
            'id': r[0],
            'student_id': r[1],
            'topic_id': r[2],
            'topic_title': r[3],
            'score': r[4],
            'time_taken': r[5],
            'submitted_at': r[6],
            'github_synced': bool(r[7])
        } for r in results]
    
    def get_result_by_id(self, result_id: str) -> Optional[Dict]:
        """Get a specific test result by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, student_id, topic_id, topic_title, score, time_taken, submitted_at, github_synced
            FROM test_results WHERE id = ?
        ''', (result_id,))
        result = cursor.fetchone()
        
        conn.close()
        
        if result:
            return {
                'id': result[0],
                'student_id': result[1],
                'topic_id': result[2],
                'topic_title': result[3],
                'score': result[4],
                'time_taken': result[5],
                'submitted_at': result[6],
                'github_synced': bool(result[7])
            }
        return None
    
    def get_analytics_data(self) -> Dict:
        """Get comprehensive analytics data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get category performance
        cursor.execute('''
            SELECT t.category, AVG(tr.score) as avg_score, COUNT(tr.id) as test_count
            FROM test_results tr
            JOIN topics t ON tr.topic_id = t.id
            GROUP BY t.category
        ''')
        category_stats = cursor.fetchall()
        
        # Get difficulty level performance
        cursor.execute('''
            SELECT t.difficulty_level, AVG(tr.score) as avg_score, COUNT(tr.id) as test_count
            FROM test_results tr
            JOIN topics t ON tr.topic_id = t.id
            GROUP BY t.difficulty_level
        ''')
        difficulty_stats = cursor.fetchall()
        
        # Get student performance summary
        cursor.execute('''
            SELECT student_id, COUNT(id) as total_tests, AVG(score) as avg_score, MAX(score) as best_score
            FROM test_results
            GROUP BY student_id
        ''')
        student_stats = cursor.fetchall()
        
        conn.close()
        
        return {
            'category_performance': [{'category': c[0], 'avg_score': c[1], 'test_count': c[2]} for c in category_stats],
            'difficulty_performance': [{'difficulty': d[0], 'avg_score': d[1], 'test_count': d[2]} for d in difficulty_stats],
            'student_summary': [{'student_id': s[0], 'total_tests': s[1], 'avg_score': s[2], 'best_score': s[3]} for s in student_stats]
        }
