import { CalendarDays, BookOpen, Bell } from 'lucide-react';
import { mockAnnouncements, mockAssignments, mockCourses, mockUser } from '../lib/mockData';
import CourseCard from '../components/dashboard/CourseCard';
import RecentCourses from '../components/dashboard/RecentCourses';
import Calendar from '../components/dashboard/Calendar';
import NotificationCenter from '../components/dashboard/NotificationCenter';

const Dashboard = () => {
  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">
          Welcome back, {mockUser.name}!
        </h1>
        <div className="flex items-center space-x-4">
          <NotificationCenter />
          <img
            src={mockUser.avatar}
            alt={mockUser.name}
            className="h-10 w-10 rounded-full"
          />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <RecentCourses />
          
          <div>
            <h2 className="text-lg font-semibold text-gray-900 mb-4">
              Your Courses
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              {mockCourses.map((course) => (
                <CourseCard key={course.id} course={course} />
              ))}
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <Calendar />

          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <CalendarDays className="h-5 w-5 mr-2 text-[#3A86FF]" />
              Upcoming Deadlines
            </h2>
            <div className="space-y-4">
              {mockAssignments.map((assignment) => (
                <div
                  key={assignment.id}
                  className="flex items-center justify-between"
                >
                  <div>
                    <p className="font-medium text-gray-900">
                      {assignment.title}
                    </p>
                    <p className="text-sm text-gray-500">Due {assignment.dueDate}</p>
                  </div>
                  <span
                    className={`px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      assignment.status === 'pending'
                        ? 'bg-yellow-100 text-yellow-800'
                        : 'bg-green-100 text-green-800'
                    }`}
                  >
                    {assignment.status}
                  </span>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <Bell className="h-5 w-5 mr-2 text-[#3A86FF]" />
              Announcements
            </h2>
            <div className="space-y-4">
              {mockAnnouncements.map((announcement) => (
                <div key={announcement.id} className="border-b pb-4 last:border-0">
                  <p className="font-medium text-gray-900">{announcement.title}</p>
                  <p className="text-sm text-gray-500 mt-1">
                    {announcement.content}
                  </p>
                  <p className="text-xs text-gray-400 mt-2">
                    {announcement.date}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;