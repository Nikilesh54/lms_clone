import { Announcement, Assignment, Course, User } from '../types';

export const mockUser: User = {
  id: '1',
  name: 'John Doe',
  email: 'john@example.com',
  role: 'student',
  avatar: 'https://images.unsplash.com/photo-1633332755192-727a05c4013d?w=150&h=150&fit=crop',
};

export const mockCourses: Course[] = [
  {
    id: '1',
    title: 'Introduction to React Development',
    description: 'Learn the fundamentals of React and modern web development',
    instructor: 'Sarah Johnson',
    thumbnail: 'https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=800&h=400&fit=crop',
    progress: 65,
    totalModules: 12,
    completedModules: 8,
    category: 'Web Development',
  },
  {
    id: '2',
    title: 'Data Science Fundamentals',
    description: 'Master the basics of data analysis and visualization',
    instructor: 'Michael Chen',
    thumbnail: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=400&fit=crop',
    progress: 30,
    totalModules: 10,
    completedModules: 3,
    category: 'Data Science',
  },
  // Add more mock courses as needed
];

export const mockAnnouncements: Announcement[] = [
  {
    id: '1',
    title: 'New Course Materials Available',
    content: 'Check out the latest updates in Module 5',
    date: '2024-03-10',
    courseId: '1',
  },
  {
    id: '2',
    title: 'Upcoming Live Session',
    content: 'Join us for a Q&A session this Friday',
    date: '2024-03-15',
    courseId: '2',
  },
];

export const mockAssignments: Assignment[] = [
  {
    id: '1',
    title: 'React Components Project',
    dueDate: '2024-03-20',
    courseId: '1',
    status: 'pending',
  },
  {
    id: '2',
    title: 'Data Visualization Exercise',
    dueDate: '2024-03-25',
    courseId: '2',
    status: 'submitted',
  },
];