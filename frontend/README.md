# Platform Zarządzania Projektami - Frontend

Modern React-based frontend application for the Project Management Platform, built with TypeScript, Vite, and Tailwind CSS. This application provides a responsive, mobile-first Progressive Web App (PWA) experience.

## 🚀 Tech Stack

- **Framework**: React 18+
- **Language**: TypeScript
- **Build Tool**: Vite 5
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **Data Fetching**: TanStack Query (React Query)
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **PWA**: Vite PWA Plugin with Workbox

## 📋 Prerequisites

- Node.js 18+ or npm
- Backend API running on `http://localhost:8000` (configurable)

## 🛠️ Installation

1. Install dependencies:
```bash
npm install
```

2. Create environment file:
```bash
cp .env.example .env
```

3. Configure environment variables in `.env`:
```env
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=Platform Zarządzania Projektami
```

## 🏃 Running the Application

### Development Mode
Start the development server with hot reload:
```bash
npm run dev
```
The application will be available at `http://localhost:5173`

### Production Build
Build the application for production:
```bash
npm run build
```
The built files will be in the `dist/` directory.

### Preview Production Build
Preview the production build locally:
```bash
npm run preview
```

### Linting
Run ESLint to check code quality:
```bash
npm run lint
```

## 📁 Project Structure

```
frontend/
├── public/              # Static assets
│   ├── manifest.json    # PWA manifest
│   ├── robots.txt       # SEO robots file
│   └── icons/           # App icons
├── src/
│   ├── components/      # React components
│   │   ├── layout/      # Layout components (Header, Sidebar, Footer)
│   │   ├── common/      # Reusable components (Button, Input, Card)
│   │   └── forms/       # Form components
│   ├── pages/           # Page components
│   │   ├── Login/       # Login page
│   │   ├── Dashboard/   # Dashboard page
│   │   └── Tasks/       # Task management pages
│   ├── services/        # API and service layers
│   │   ├── api.ts       # Axios instance with interceptors
│   │   ├── auth.ts      # Authentication service
│   │   └── offline.ts   # PWA offline service
│   ├── store/           # State management
│   │   └── authStore.ts # Authentication store (Zustand)
│   ├── hooks/           # Custom React hooks
│   │   ├── useAuth.ts   # Authentication hook
│   │   └── useMediaQuery.ts # Responsive hook
│   ├── types/           # TypeScript type definitions
│   │   ├── user.ts      # User types
│   │   ├── task.ts      # Task types
│   │   └── api.ts       # API response types
│   ├── utils/           # Utility functions
│   │   ├── constants.ts # App constants
│   │   └── helpers.ts   # Helper functions
│   ├── styles/          # Global styles
│   │   └── index.css    # Tailwind CSS imports
│   ├── App.tsx          # Main app component with routing
│   ├── main.tsx         # Application entry point
│   └── vite-env.d.ts    # Vite TypeScript definitions
├── .env.example         # Environment variables template
├── .eslintrc.cjs        # ESLint configuration
├── index.html           # HTML entry point
├── package.json         # Dependencies and scripts
├── postcss.config.js    # PostCSS configuration
├── tailwind.config.js   # Tailwind CSS configuration
├── tsconfig.json        # TypeScript configuration
├── tsconfig.node.json   # TypeScript config for Node
└── vite.config.ts       # Vite configuration
```

## 🎨 Features

### Authentication
- JWT-based authentication
- Login form with validation
- Protected routes
- Automatic token refresh

### Responsive Design
- Mobile-first approach
- Responsive sidebar (drawer on mobile, fixed on desktop)
- Adaptive layouts for all screen sizes
- Touch-friendly UI elements

### Progressive Web App (PWA)
- Installable on all platforms (Windows, Linux, Android, iOS)
- Offline support with service workers
- App manifest for native-like experience
- Automatic updates

### State Management
- Zustand for global state (authentication)
- React Query for server state and caching
- Local storage for persistence

### UI Components
- Reusable component library
- Tailwind CSS for styling
- Consistent design system
- Loading states and error handling

## 🔌 API Integration

The frontend communicates with the backend API through:
- Base URL: Configured via `VITE_API_URL` environment variable
- Proxy: Development proxy configured in `vite.config.ts` (`/api` → `http://localhost:8000`)
- Authentication: JWT tokens in Authorization headers
- Interceptors: Automatic token injection and error handling

## 🌐 Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## 📱 PWA Installation

Users can install the application:
- **Desktop**: Click the install button in the browser address bar
- **Android**: Use "Add to Home Screen" from browser menu
- **iOS**: Use "Add to Home Screen" from Safari share menu

## 🔒 Security

- HTTPS required for PWA features in production
- JWT token storage in localStorage
- Automatic token cleanup on logout
- CSRF protection through headers

## 🐛 Troubleshooting

### Port already in use
```bash
# Kill the process using port 5173
lsof -ti:5173 | xargs kill -9
```

### Build errors
```bash
# Clear cache and reinstall
rm -rf node_modules dist
npm install
```

### Type errors
```bash
# Ensure TypeScript is properly configured
npm run build
```

## 📚 Additional Resources

- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
- [React Router Documentation](https://reactrouter.com/)
- [TanStack Query Documentation](https://tanstack.com/query/latest)

## 🤝 Contributing

1. Follow the existing code style
2. Use TypeScript for all new files
3. Add proper type definitions
4. Test responsive behavior on multiple devices
5. Ensure PWA features work correctly

## 📝 License

See the main project LICENSE file.
