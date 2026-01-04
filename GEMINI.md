# Project Overview

This is a React-based portfolio website generator. It dynamically creates a personal portfolio using a configuration file (`gitprofile.config.ts`) and data from the GitHub API. The project is built with Vite and utilizes TypeScript, Tailwind CSS, and various other modern web technologies.

The core of the project is the `gitprofile.config.ts` file, where the user can define the content and appearance of their portfolio. This includes personal information, social media links, skills, work experience, education, and projects. The portfolio's theme is also customizable.

## Building and Running

### Development

To run the project in development mode, use the following command:

```bash
npm run dev
```

This will start a local development server, and you can view the portfolio in your browser.

### Building

To build the project for production, use the following command:

```bash
npm run build
```

This will create a `dist` directory with the optimized and minified files ready for deployment.

### Linting and Formatting

The project uses ESLint for linting and Prettier for code formatting. To run the linter, use:

```bash
npm run lint
```

To automatically fix linting issues, use:

```bash
npm run lint:fix
```

To check for formatting issues with Prettier, use:

```bash
npm run prettier
```

To automatically fix formatting issues, use:

```bash
npm run prettier:fix
```

## Development Conventions

The project follows standard React and TypeScript conventions. It enforces a consistent code style using ESLint and Prettier. All portfolio content and configuration are managed through the `gitprofile.config.ts` file. Components are organized in the `src/components` directory, with each component responsible for rendering a specific section of the portfolio.
