# AI Rules for MeetMind

## Tech Stack
- React 19 with Vite for fast development
- TypeScript for type safety
- React Router v7 for client-side routing
- Tailwind CSS for utility-first styling
- shadcn/ui component library built on Radix UI and Tailwind
- Lucide React for consistent icons
- Docker for containerization (frontend and backend)
- Python/FastAPI backend (inferred from main.py)
- PostgreSQL for data storage (implied)
- Celery for background tasks (mentioned in ADR)
- MinIO for object storage (mentioned)
- OpenRouter API for audio transcription and LLM

## Library Usage Rules
- **Styling**: Use Tailwind CSS classes exclusively; do not write custom CSS or use CSS-in-JS libraries.
- **UI Components**: Prefer shadcn/ui components; if a component is missing, create a new component extending shadcn/ui primitives.
- **Icons**: Use lucide-react icons; import only needed icons to keep bundle small.
- **State Management**: Use React's built-in hooks (useState, useEffect, useContext) for local and moderate global state; avoid adding external state libraries unless complexity demands it (then consider Zustand or Jotai).
- **Data Fetching**: Use React Query (tanstack/query) for server state; if not installed, install it; otherwise use fetch/axios with useEffect.
- **Forms**: Use React Hook Form for form handling with validation; integrate with Yup or Zod for schema validation.
- **Notifications**: Use react-hot-toast for toast messages (if needed).
- **Routing**: Use React Router v7; define routes in src/App.tsx; lazy-load pages with React.lazy and Suspense.
- **Utilities**: Keep utility functions in src/utils; avoid large utility libraries like lodash unless specific functions needed.
- **Testing**: Not configured yet; when adding tests, use Vitest and React Testing Library.
- **Code Splitting**: Use dynamic imports for lazy loading routes and heavy components.
- **Error Handling**: Use error boundaries for UI errors; do not suppress errors with empty catch blocks.
- **Environment Variables**: Prefix client-side variables with VITE_; keep secrets in backend .env only.
- **File Organization**: 
  - Pages: src/pages/
  - Components: src/components/
  - Hooks: src/hooks/
  - Utils: src/utils/
  - Types: src/types/
  - Assets: src/assets/
- **Backend**: 
  - Use FastAPI for API endpoints.
  - Use Pydantic models for request/response validation.
  - Use SQLAlchemy ORM with Alembic for migrations.
  - Use Celery for background tasks with Redis broker.
  - Use MinIO client (minio) for object storage.
  - Use OpenRouter Python client or direct HTTP calls for AI services.
  - Keep API keys and secrets in backend .env, never commit.