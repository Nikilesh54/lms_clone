import { useParams } from 'react-router-dom';
import { mockCourses } from '../lib/mockData';

const CourseDetails = () => {
  const { id } = useParams();
  const course = mockCourses.find((c) => c.id === id);

  if (!course) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold text-gray-900">Course not found</h2>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <img
          src={course.thumbnail}
          alt={course.title}
          className="w-full h-64 object-cover"
        />
        <div className="p-6">
          <h1 className="text-2xl font-bold text-gray-900">{course.title}</h1>
          <p className="mt-2 text-gray-600">{course.description}</p>
          <div className="mt-4 flex items-center">
            <span className="text-sm text-gray-500">Instructor:</span>
            <span className="ml-2 font-medium">{course.instructor}</span>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Course Progress
        </h2>
        <div className="space-y-4">
          <div className="flex justify-between text-sm text-gray-500">
            <span>Overall Progress</span>
            <span>{course.progress}%</span>
          </div>
          <div className="h-2 bg-gray-200 rounded-full">
            <div
              className="h-full bg-[#3A86FF] rounded-full"
              style={{ width: `${course.progress}%` }}
            />
          </div>
          <div className="mt-2 text-sm text-gray-500">
            {course.completedModules} of {course.totalModules} modules completed
          </div>
        </div>
      </div>
    </div>
  );
};

export default CourseDetails;