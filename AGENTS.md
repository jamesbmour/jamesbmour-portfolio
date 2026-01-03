# Repository Guidelines

## Project Structure & Module Organization
- Frontend lives in `src/` (Vite + React + TypeScript). Components are grouped in kebab-case folders under `src/components/`; shared types sit in `src/interfaces/`; configuration and copy come from `gitprofile.config.ts`, `src/constants/`, and `src/data/`.
- Styling is primarily Tailwind/DaisyUI with supporting utilities in `src/styles/` and `variables.css` in component folders.
- Static assets are in `public/`; the production bundle is emitted to `dist/` by Vite.
- A lightweight Python helper lives in `backend/main.py` alongside resumes; keep backend changes isolated from the frontend unless explicitly integrated.

## Build, Test, and Development Commands
- `pnpm install` — install dependencies (pnpm is preferred because lockfiles are provided).
- `pnpm dev` — run the Vite dev server for local iteration.
- `pnpm build` — type-check with `tsc` and produce the optimized client build.
- `pnpm preview` — serve the built assets locally to validate the production bundle.
- `pnpm lint` / `pnpm lint:fix` — run ESLint (with TypeScript and React Hooks rules) optionally autofixing.
- `pnpm prettier` / `pnpm prettier:fix` — check or format code/docs/styles per the shared Prettier config.

## Coding Style & Naming Conventions
- Use functional React components written in TypeScript; export components in PascalCase and prefer hooks (`useX`) for shared behavior.
- Keep file and folder names kebab-case; collocate component-specific assets and styles with the component.
- Favor Tailwind utility classes over inline styles; extend theme tokens in `tailwind.config.js` when needed.
- Let Prettier handle whitespace/quoting and ESLint enforce imports, hooks rules, and unused code removal.

## Testing Guidelines
- There is no dedicated automated test suite yet; rely on `pnpm build` for type safety and `pnpm lint` for static analysis before opening a PR.
- If you add tests, co-locate them next to the feature (`*.test.tsx`) and keep them fast and deterministic; prefer React Testing Library patterns and `chai` assertions when applicable.
- Manually verify UI changes in `pnpm dev` and `pnpm preview`, especially components reading from `gitprofile.config.ts` or external APIs.

## Commit & Pull Request Guidelines
- Write concise, imperative commit messages (e.g., "Update Chatbot button size"); group related changes logically.
- For PRs, include a short summary, linked issue/reference, and before/after screenshots for UI updates. Note any config or environment variable requirements (`VITE_*` values in `.env.local`).
- Confirm `pnpm lint` and `pnpm build` succeed before requesting review; call out known limitations or manual steps for reviewers.

## Security & Configuration Tips
- Do not commit secrets; place API keys and host URLs in `.env.local` and reference them via `VITE_*` variables. Add new secrets to `.gitignore` if needed.
- Be mindful of analytics/chat integrations (`@vercel/analytics`, Flowise/OpenAI hosts); mock or guard them in local development when unavailable.
- Keep resume assets and other binaries out of the client bundle unless explicitly required.
