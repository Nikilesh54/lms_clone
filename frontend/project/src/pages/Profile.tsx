import { useState, FormEvent } from 'react';
import { mockUser } from '../lib/mockData';

const Profile = () => {
  const [userData, setUserData] = useState({
    name: mockUser.name,
    email: mockUser.email,
  });

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    // Store in localStorage for persistence
    localStorage.setItem('userData', JSON.stringify(userData));
    alert('Profile updated successfully!');
  };

  return (
    <div className="space-y-8">
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center space-x-4">
          <img
            src={mockUser.avatar}
            alt={userData.name}
            className="h-20 w-20 rounded-full"
          />
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{userData.name}</h1>
            <p className="text-gray-500">{userData.email}</p>
            <span className="mt-1 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
              {mockUser.role}
            </span>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Account Settings
        </h2>
        <form className="space-y-4" onSubmit={handleSubmit}>
          <div>
            <label
              htmlFor="name"
              className="block text-sm font-medium text-gray-700"
            >
              Name
            </label>
            <input
              type="text"
              id="name"
              value={userData.name}
              onChange={(e) => setUserData({ ...userData, name: e.target.value })}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-[#3A86FF] focus:ring focus:ring-[#3A86FF] focus:ring-opacity-50"
            />
          </div>
          <div>
            <label
              htmlFor="email"
              className="block text-sm font-medium text-gray-700"
            >
              Email
            </label>
            <input
              type="email"
              id="email"
              value={userData.email}
              onChange={(e) => setUserData({ ...userData, email: e.target.value })}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-[#3A86FF] focus:ring focus:ring-[#3A86FF] focus:ring-opacity-50"
            />
          </div>
          <button
            type="submit"
            className="w-full sm:w-auto px-4 py-2 bg-[#3A86FF] text-white rounded-md hover:bg-[#2563EB] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#3A86FF]"
          >
            Save Changes
          </button>
        </form>
      </div>
    </div>
  );
};

export default Profile;