export interface User {
  id: string;
  name: string;
  email: string;
  role: 'student' | 'instructor' | 'admin';
  avatar: string;
  lastAccessed?: string[];
}

export interface Course {
  id: string;
  title: string;
  description: string;
  instructor: string;
  thumbnail: string;
  progress: number;
  totalModules: number;
  completedModules: number;
  category: string;
  modules: CourseModule[];
  lastPosition?: number;
}

export interface CourseModule {
  id: string;
  title: string;
  type: 'video' | 'quiz' | 'pdf';
  content: string;
  duration?: number;
  completed: boolean;
}

export interface Announcement {
  id: string;
  title: string;
  content: string;
  date: string;
  courseId: string;
}

export interface Assignment {
  id: string;
  title: string;
  dueDate: string;
  courseId: string;
  status: 'pending' | 'submitted' | 'graded';
}

export interface VideoBookmark {
  id: string;
  timestamp: number;
  label: string;
  courseId: string;
  moduleId: string;
}

export interface Note {
  id: string;
  content: string;
  timestamp: number;
  courseId: string;
  moduleId: string;
}

export interface Quiz {
  id: string;
  title: string;
  timeLimit?: number;
  questions: QuizQuestion[];
}

export interface QuizQuestion {
  id: string;
  type: 'multiple-choice' | 'true-false' | 'matching';
  question: string;
  options: string[];
  correctAnswer: string | string[];
}