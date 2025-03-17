import { Link } from 'react-router-dom';
import { Course } from '../../types';
import { cn } from '../../lib/utils';

interface CourseCardProps {
  course: Course;
  className?: string;
}

const CourseCard = ({ course, className }: CourseCardProps) => {
  return (
    <Link to={`/courses/${course.id}`}>
      <div
        className={cn(
          'bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden transition-transform hover:scale-[1.02]',
          className
        )}
      >
        <img
          src={course.thumbnail}
          alt={course.title}
          className="w-full h-48 object-cover"
        />
        <div className="p-4">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">{course.title}</h3>
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">{course.instructor}</p>
          <div className="mt-4">
            <div className="flex justify-between text-sm text-gray-500 dark:text-gray-400">
              <span>Progress</span>
              <span>{course.progress}%</span>
            </div>
            <div className="mt-1 h-2 bg-gray-200 dark:bg-gray-700 rounded-full">
              <div
                className="h-full bg-[#3A86FF] rounded-full"
                style={{ width: `${course.progress}%` }}
              />
            </div>
          </div>
          <div className="mt-4 flex justify-between items-center">
            <span className="text-sm text-gray-500 dark:text-gray-400">
              {course.completedModules}/{course.totalModules} modules
            </span>
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-100">
              {course.category}
            </span>
          </div>
        </div>
      </div>
    </Link>
  );
};

export default CourseCard;