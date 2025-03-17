import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Clock, PlayCircle } from 'lucide-react';
import { Course } from '../../types';
import { mockCourses } from '../../lib/mockData';

const RecentCourses = () => {
  const [recentCourses, setRecentCourses] = useState<Course[]>([]);

  useEffect(() => {
    setRecentCourses(mockCourses.slice(0, 3));
  }, []);

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
      <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4 flex items-center">
        <Clock className="h-5 w-5 mr-2 text-[#3A86FF]" />
        Continue Learning
      </h2>
      <div className="space-y-4">
        {recentCourses.map((course) => (
          <Link
            key={course.id}
            to={`/courses/${course.id}`}
            className="block group"
          >
            <div className="flex items-center space-x-4 p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
              <div className="relative w-24 h-16 rounded-md overflow-hidden">
                <img
                  src={course.thumbnail}
                  alt={course.title}
                  className="object-cover w-full h-full"
                />
                <div className="absolute inset-0 bg-black/40 group-hover:bg-black/50 transition-colors flex items-center justify-center">
                  <PlayCircle className="h-8 w-8 text-white" />
                </div>
              </div>
              <div className="flex-1">
                <h3 className="font-medium text-gray-900 dark:text-gray-100 group-hover:text-[#3A86FF] transition-colors">
                  {course.title}
                </h3>
                <div className="mt-1">
                  <div className="flex justify-between text-sm text-gray-500 dark:text-gray-400">
                    <span>{course.progress}% complete</span>
                  </div>
                  <div className="mt-1 h-1.5 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-[#3A86FF] rounded-full transition-all duration-300"
                      style={{ width: `${course.progress}%` }}
                    />
                  </div>
                </div>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default RecentCourses;