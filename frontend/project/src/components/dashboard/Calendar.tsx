import { useState } from 'react';
import { format, startOfMonth, endOfMonth, eachDayOfInterval, isSameMonth, isSameDay } from 'date-fns';
import { Calendar as CalendarIcon } from 'lucide-react';
import { mockAssignments } from '../../lib/mockData';

const Calendar = () => {
  const [currentDate, setCurrentDate] = useState(new Date());
  const start = startOfMonth(currentDate);
  const end = endOfMonth(currentDate);
  const days = eachDayOfInterval({ start, end });

  const getEventsForDay = (date: Date) => {
    return mockAssignments.filter(assignment => 
      isSameDay(new Date(assignment.dueDate), date)
    );
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
      <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4 flex items-center">
        <CalendarIcon className="h-5 w-5 mr-2 text-[#3A86FF]" />
        Calendar
      </h2>
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="font-medium text-gray-900 dark:text-gray-100">{format(currentDate, 'MMMM yyyy')}</h3>
          <div className="flex space-x-2">
            <button
              onClick={() => setCurrentDate(new Date(currentDate.setMonth(currentDate.getMonth() - 1)))}
              className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-full text-gray-600 dark:text-gray-400"
            >
              ←
            </button>
            <button
              onClick={() => setCurrentDate(new Date(currentDate.setMonth(currentDate.getMonth() + 1)))}
              className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-full text-gray-600 dark:text-gray-400"
            >
              →
            </button>
          </div>
        </div>
        <div className="grid grid-cols-7 gap-1">
          {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map((day) => (
            <div key={day} className="text-center text-sm font-medium text-gray-500 dark:text-gray-400 py-2">
              {day}
            </div>
          ))}
          {days.map((day) => {
            const events = getEventsForDay(day);
            return (
              <div
                key={day.toString()}
                className={`
                  p-2 text-center text-sm rounded-lg
                  ${isSameMonth(day, currentDate) 
                    ? 'text-gray-900 dark:text-gray-100' 
                    : 'text-gray-400 dark:text-gray-600'}
                  ${events.length > 0 ? 'bg-blue-50 dark:bg-blue-900/20' : ''}
                `}
              >
                <span className="block">{format(day, 'd')}</span>
                {events.length > 0 && (
                  <div className="mt-1 h-1 w-1 bg-[#3A86FF] rounded-full mx-auto" />
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default Calendar;