# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a personal portfolio website based on GitProfile, built with React, TypeScript, Vite, and Tailwind CSS. It dynamically fetches GitHub profile data and displays projects, skills, experience, education, and blog posts. The site includes an integrated chatbot powered by Flowise for interactive resume exploration.

## Core Architecture

### Configuration System
- **`gitprofile.config.ts`**: Central configuration file controlling all portfolio content (profile info, projects, skills, experience, education, blog, theme, analytics)
- Configuration is injected globally via Vite's `define` feature as `CONFIG` constant (see `vite.config.ts`)
- Type definitions in `global.d.ts` provide strong typing for the config object

### Component Structure
- **`src/components/gitprofile.tsx`**: Main application component that orchestrates all other components
  - Fetches GitHub profile data via GitHub API
  - Manages theme state and error handling
  - Renders card-based layout (avatar, details, skills, experience, education, projects, blog)
  - Integrates chatbot component
- **Card Components**: Each section is a separate card component (AvatarCard, DetailsCard, SkillCard, etc.)
- **Layout**: Uses Tailwind CSS with DaisyUI for theming (4-column grid on desktop, single column on mobile)

### Data Flow
1. On mount, `gitprofile.tsx` fetches GitHub user data from `https://api.github.com/users/{username}`
2. For projects, it queries GitHub's search API based on config settings (automatic or manual mode)
3. Blog articles fetched from dev.to or Medium API based on `blog.source` config
4. All data managed via React hooks (useState, useEffect, useCallback)

### Chatbot Integration
- Uses `flowise-embed-react` package for chatbot UI
- Configured in `src/components/chatbot/index.tsx`
- Connects to external Flowise instance at `https://fw.jb7.me`
- Backend (currently unused): FastAPI-based chat service in `backend/main.py` with LangChain integration for RAG over resume PDF

### Theme System
- DaisyUI themes configured in `gitprofile.config.ts` under `themeConfig`
- Theme switcher component allows runtime theme changes
- Custom theme colors can be defined in `customTheme` config
- Theme persisted to localStorage and applied via `data-theme` attribute

## Common Development Commands

### Development
```bash
npm run dev          # Start Vite dev server (default: http://localhost:5173)
npm run build        # TypeScript compile + Vite production build
npm run preview      # Preview production build locally
```

### Code Quality
```bash
npm run lint         # Run ESLint on .ts/.tsx files
npm run lint:fix     # Auto-fix ESLint issues
npm run prettier     # Check code formatting
npm run prettier:fix # Auto-format code
```

### Backend (Optional)
```bash
cd backend
python main.py       # Start FastAPI server on port 8000
```

## Key Files and Directories

- **`gitprofile.config.ts`**: Edit this to update portfolio content (skills, projects, experience, social links, etc.)
- **`src/components/`**: All React components organized by feature
- **`src/interfaces/`**: TypeScript interface definitions for data models
- **`src/utils/index.tsx`**: Utility functions (config sanitization, theme helpers, Hotjar setup)
- **`src/constants/`**: Error messages, theme definitions, and other constants
- **`vite.config.ts`**: Vite configuration with React, MDX, PWA, and HTML injection plugins
- **`global.d.ts`**: Global type definitions for Config interface

## Important Technical Details

### GitHub API Integration
- Uses unauthenticated GitHub API (rate limit: 60 requests/hour)
- Rate limit errors (403) handled with user-friendly error page showing reset time
- Projects can be filtered by stars/updated date, excluded by name, and forks can be hidden

### Type Safety
- Strict TypeScript configuration (`tsconfig.json` with strict mode enabled)
- `Config` interface in `global.d.ts` defines entire configuration schema
- Sanitized config type in `src/interfaces/sanitized-config.tsx` for runtime validation

### Build and Deployment
- GitHub Actions workflow at `.github/workflows/nextjs.yml` (note: outdated, uses Next.js steps but project uses Vite)
- Production build outputs to `dist/` directory
- PWA support via `vite-plugin-pwa` (configured but disabled by default in config)

### Styling Approach
- Tailwind CSS for utility-first styling
- DaisyUI components for pre-built UI elements
- Custom CSS in `src/assets/index.css` and `src/components/variables.css`
- Responsive design with mobile-first approach

## Configuration Notes

When modifying portfolio content:
1. Edit `gitprofile.config.ts` - this is the single source of truth
2. No need to touch component code unless adding new features
3. GitHub projects can be automatic (fetched by criteria) or manual (specific repos)
4. Blog integration supports dev.to or Medium
5. Theme customization through `themeConfig.themes` array and `customTheme` object

## Development Workflow

1. Make changes to config or components
2. Run `npm run lint` and `npm run prettier` to ensure code quality
3. Test in dev server with `npm run dev`
4. Build for production with `npm run build`
5. Verify production build with `npm run preview`
