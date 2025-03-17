# Modern Learning Management System (LMS) Frontend

A modern, responsive Learning Management System built with React, TypeScript, and Tailwind CSS.

## Features

### Core Pages
1. **Dashboard**
   - Student/instructor view
   - Course progress tracking
   - Upcoming deadlines
   - Announcements feed

2. **Course Catalog**
   - Filterable course grid
   - Search functionality
   - Category filtering

3. **Course Page**
   - Video player (supports MP4, WebM, MOV, AVI, MKV)
   - PDF materials viewer
   - Interactive quiz interface
   - Progress tracking

4. **User Profile**
   - Account settings
   - Course enrollment history
   - Achievements tracking

5. **Admin Panel**
   - Course management
   - User administration
   - Content moderation

### Technical Features
- Responsive design (mobile, tablet, desktop)
- Modern React patterns with hooks
- TypeScript for type safety
- Tailwind CSS for styling
- React Router for navigation
- Mock data for development

## Getting Started

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

## Project Structure

```
src/
├── components/     # Reusable UI components
├── lib/           # Utilities and helpers
├── pages/         # Main route components
├── types/         # TypeScript definitions
└── main.tsx       # Application entry point
```

## Design System

### Colors
- Primary: #3A86FF
- Background: #FFFFFF
- Text: #333333

### Components
- Modern, clean UI components
- Consistent styling
- Responsive design patterns
- Loading states for data operations

## Development

### Prerequisites
- Node.js 16+
- npm or yarn

### Commands
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Future Improvements
- Backend API integration
- Real-time notifications
- Advanced analytics
- Social learning features
- Gamification elements

## License
MIT