export enum Role {
  MASTER = 'master',
  STUDENT = 'student',
}

export interface User {
  uniqueId: string;
  role: Role;
}

export interface SyllabusTopic {
  id: string;
  title: string;
}

export interface Question {
  id: string;
  questionText: string;
  options: string[];
  correctAnswerIndex: number;
}

export interface TestResult {
  id: string;
  studentId: string;
  topicId: string;
  topicTitle: string;
  score: number; // Percentage
  submittedAt: Date;
}
