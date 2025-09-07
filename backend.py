import streamlit as st
import sqlite3
import bcrypt
import uuid
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import pandas as pd

class DatabaseManager:
    """Handles all database operations for the WIDA application"""
    
    def __init__(self, db_path: str = "wida_app.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                unique_id TEXT PRIMARY KEY,
                role TEXT NOT NULL CHECK (role IN ('master', 'student')),
                password_hash TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Syllabus topics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS topics (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
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
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES users (unique_id),
                FOREIGN KEY (topic_id) REFERENCES topics (id)
            )
        ''')
        
        # Insert default users if they don't exist
        default_users = [
            ('KRURA', 'master'),
            ('student1', 'student'),
            ('student2', 'student')
        ]
        
        for user_id, role in default_users:
            cursor.execute('INSERT OR IGNORE INTO users (unique_id, role) VALUES (?, ?)', (user_id, role))
        
        # Insert default topics if they don't exist
        default_topics = [
            ('topic-1', 'Reading Comprehension'),
            ('topic-2', 'Listening Skills'),
            ('topic-3', 'Writing and Grammar')
        ]
        
        for topic_id, title in default_topics:
            cursor.execute('INSERT OR IGNORE INTO topics (id, title) VALUES (?, ?)', (topic_id, title))
        
        # Insert default questions if they don't exist
        default_questions = [
            # Reading Comprehension questions
            ('q1-1', 'topic-1', 'What is the main idea of a passage?', 
             'The primary point the author is making', 'A minor detail', 'The author\'s name', 'The publisher', 0),
            ('q1-2', 'topic-1', 'An inference is:', 
             'Something stated directly', 'A conclusion based on evidence', 'A summary of the plot', 'A character\'s name', 1),
            
            # Listening Skills questions
            ('q2-1', 'topic-2', 'Active listening involves:', 
             'Hearing the words', 'Waiting for your turn to speak', 'Focusing fully on the speaker', 'Ignoring non-verbal cues', 2),
            
            # Writing and Grammar questions
            ('q3-1', 'topic-3', 'Which of the following is a complete sentence?', 
             'Running in the park.', 'She runs.', 'Because it was raining.', 'And then went home.', 1),
            ('q3-2', 'topic-3', 'What does a noun refer to?', 
             'An action', 'A person, place, or thing', 'A descriptive word', 'A connecting word', 1)
        ]
        
        for question_data in default_questions:
            cursor.execute('''
                INSERT OR IGNORE INTO questions 
                (id, topic_id, question_text, option_a, option_b, option_c, option_d, correct_answer) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
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
            # For backward compatibility, if no password is set, allow login without password
            if user[2] is None or password is None:
                return {'unique_id': user[0], 'role': user[1]}
            # If password is set, verify it
            elif bcrypt.checkpw(password.encode('utf-8'), user[2]):
                return {'unique_id': user[0], 'role': user[1]}
        
        return None
    
    def register_user(self, unique_id: str, password: str = None) -> bool:
        """Register a new user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            password_hash = None
            if password:
                password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            cursor.execute('INSERT INTO users (unique_id, role, password_hash) VALUES (?, ?, ?)', 
                          (unique_id, 'student', password_hash))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            conn.close()
            return False
    
    def get_all_users(self) -> List[Dict]:
        """Get all users"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT unique_id, role FROM users ORDER BY role, unique_id')
        users = cursor.fetchall()
        
        conn.close()
        return [{'unique_id': user[0], 'role': user[1]} for user in users]
    
    def remove_user(self, unique_id: str) -> bool:
        """Remove a user (except master users)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if user is master
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
        """Get all syllabus topics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, title FROM topics ORDER BY created_at')
        topics = cursor.fetchall()
        
        conn.close()
        return [{'id': topic[0], 'title': topic[1]} for topic in topics]
    
    def add_topic(self, title: str) -> bool:
        """Add a new topic"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        topic_id = f"topic-{uuid.uuid4().hex[:8]}"
        cursor.execute('INSERT INTO topics (id, title) VALUES (?, ?)', (topic_id, title))
        conn.commit()
        conn.close()
        return True
    
    def get_questions_for_topic(self, topic_id: str) -> List[Dict]:
        """Get all questions for a specific topic"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, question_text, option_a, option_b, option_c, option_d, correct_answer 
            FROM questions WHERE topic_id = ?
        ''', (topic_id,))
        questions = cursor.fetchall()
        
        conn.close()
        return [{
            'id': q[0],
            'question_text': q[1],
            'options': [q[2], q[3], q[4], q[5]],
            'correct_answer': q[6]
        } for q in questions]
    
    def submit_test_result(self, student_id: str, topic_id: str, topic_title: str, score: int) -> str:
        """Submit test result and return result ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        result_id = f"result-{uuid.uuid4().hex[:8]}"
        cursor.execute('''
            INSERT INTO test_results (id, student_id, topic_id, topic_title, score) 
            VALUES (?, ?, ?, ?, ?)
        ''', (result_id, student_id, topic_id, topic_title, score))
        
        conn.commit()
        conn.close()
        return result_id
    
    def get_student_results(self, student_id: str) -> List[Dict]:
        """Get all test results for a student"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, topic_id, topic_title, score, submitted_at 
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
            'submitted_at': r[4]
        } for r in results]
    
    def get_all_results(self) -> List[Dict]:
        """Get all test results"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, student_id, topic_id, topic_title, score, submitted_at 
            FROM test_results 
            ORDER BY submitted_at DESC
        ''', )
        results = cursor.fetchall()
        
        conn.close()
        return [{
            'id': r[0],
            'student_id': r[1],
            'topic_id': r[2],
            'topic_title': r[3],
            'score': r[4],
            'submitted_at': r[5]
        } for r in results]
    
    def get_result_by_id(self, result_id: str) -> Optional[Dict]:
        """Get a specific test result by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, student_id, topic_id, topic_title, score, submitted_at 
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
                'submitted_at': result[5]
            }
        return None
