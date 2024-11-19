// gitprofile.config.ts

const CONFIG = {
  github: {
    username: 'jamesbmour', // Your GitHub org/user name. (This is the only required config)
  },
  /**
   * If you are deploying to https://<USERNAME>.github.io/, for example your repository is at https://github.com/arifszn/arifszn.github.io, set base to '/'.
   * If you are deploying to https://<USERNAME>.github.io/<REPO_NAME>/,
   * for example your repository is at https://github.com/arifszn/portfolio, then set base to '/portfolio/'.
   */
  base: '/',
  projects: {
    github: {
      display: true, // Display GitHub projects?
      header: 'Projects',
      mode: 'automatic', // Mode can be: 'automatic' or 'manual'
      automatic: {
        sortBy: 'updated', // Sort projects by 'stars' or 'updated'
        limit: 4, // How many projects to display.
        exclude: {
          forks: false, // Forked projects will not be displayed if set to true.
          projects: [
            'jamesbmour/FlutterChatAppTutorial',
            'jamesbmour/langchain-tutorials',
            'jamesbmour/cheatsheets',
            'jamesbmour/James-Personal-Portfolio',
          ], // These projects will not be displayed. example: ['arifszn/my-project1', 'arifszn/my-project2']
        },
      },
      manual: {
        // Properties for manually specifying projects
        projects: ['jamesbmour/finrl', 'jamesbmour/blog_tutorials'], // List of repository names to display. example: ['arifszn/my-project1', 'arifszn/my-project2']
      },
    },
    external: {
      header: 'My Projects',
      // To hide the `External Projects` section, keep it empty.
      projects: [
        {
          title: 'Multi-Agent Coordination in Overcooked: A RL Approach',
          description:
            'This paper addresses the Overcooked environment, a multi-agent challenge inspired by the game, where two AI chefs collaborate to efficiently deliver soups. By utilizing reward shaping and innovative strategies, the study demonstrates how teamwork and adaptive algorithms can tackle complex, dynamic tasks, providing insights into optimizing AI collaboration in time-sensitive scenarios.',
          imageUrl: 'public/overcooked.jpg',
          link: 'https://drive.google.com/file/d/1xzq6-yHNT9PSKmzCwEVLC3c_x7n-WGQv/view?usp=sharing',
        },
        {
          title: 'Document Intelligence',
          description:
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed euismod, nunc ut.',
          imageUrl:
            'https://img.freepik.com/free-vector/illustration-gallery-icon_53876-27002.jpg',
          link: 'https://example.com',
        },
      ],
    },
  },
  seo: {
    title: 'James Brendamour Portfolio',
    description: "Freelance Consultant @ Bmours | Master's in Computer Science",
    imageURL: 'https://avatars.githubusercontent.com/u/22489672?v=4',
  },
  social: {
    linkedin: 'jamesbmour',
    // mastodon: '',
    youtube: 'justcodeit77', // example: 'pewdiepie'
    // dribbble: '',
    // behance: '',
    medium: '@jamesbrendamour7',
    dev: 'jamesbmour',
    // stackoverflow: '', // example: '1/jeff-atwood'
    website: 'jamesbmour.com',
    phone: '513-543-8687',
    email: 'James@bmours.com',
  },
  resume: {
    fileUrl:
      'https://drive.google.com/file/d/1-6aOoQLVlatLv3w_70qHEPEh16TUCBWR/view?usp=sharing', // Empty fileUrl will hide the `Download Resume` button.
  },
  skills: [
    'Python',
    'Streamlit',
    'Dash',
    'NLP',
    'LLMs',
    'OpenAI API',
    'LangChain',
    'LangGraph',
    'LLama Index',
    'LangSmith',
    'Fine-Tuning',
    'RL',
    'Data Science',
    'LLM',
    'Scikit-learn',
    'Spacy',
    'Redis',
    'Docker',
    'AWS',
    'Azure',
    'GCP',
    'Machine Learning',
    'Deep Learning',
    'PyTorch',
    'TensorFlow',
    'Keras',
    'Flask',
    'FastAPI',
    'JavaScript',
    'React.js',
    'Node.js',
    'Nest.js',
    'MySQL',
    'PostgresSQL',
    'Git',
    'Docker',
    'CSS',
    'Tailwind',
    'Tableau',
    'Power BI',
    'Java',
  ],
  experiences: [
    {
      company: 'EY',
      position: 'AI & Automation Technology Consultant',
      from: 'Sep 2018',
      to: 'Aug 2022',
      companyLink: 'https://www.ey.com/en_us',
    },
    {
      company: 'Freelance Consultant',
      position: 'Data Science & Machine Leaning Consultant',
      from: 'Aug 2022',
      to: 'Present',
      companyLink: '',
    },
    {
      company: 'Siemens  R&D',
      position: 'Intern in Data Science & Machine Learning',
      from: 'July 2019',
      to: 'August 2021',
      companyLink: 'https://www.siemens.com/global/en.html',
    },
  ],
  certifications: [
    {
      name: 'Lorem ipsum',
      body: 'Lorem ipsum dolor sit amet',
      year: 'March 2022',
      link: 'https://example.com',
    },
  ],
  educations: [
    {
      institution: 'Ohio State University',
      degree: 'Bachelors of Science in Integrated Systems Engineering',
      minor: 'Minor in Business',
      from: '2013',
      to: '2018',
    },
    {
      institution: 'Georgia Institute of Technology',
      degree: 'Masters of Science in Computer Science (Machine Learning)',
      from: '2021',
      to: '2024',
    },
  ],
  // Display articles from your medium or dev account. (Optional)
  blog: {
    source: 'dev', // medium | dev
    username: 'jamesbmour', // to hide blog section, keep it empty
    limit: 4, // How many articles to display. Max is 10.
  },
  googleAnalytics: {
    id: '', // GA3 tracking id/GA4 tag id UA-XXXXXXXXX-X | G-XXXXXXXXXX
  },
  // Track visitor interaction and behavior. https://www.hotjar.com
  hotjar: {
    id: '5129603',
    snippetVersion: 6,
  },
  themeConfig: {
    defaultTheme: 'business',

    // Hides the switch in the navbar
    // Useful if you want to support a single color mode
    disableSwitch: false,

    // Should use the prefers-color-scheme media-query,
    // using user system preferences, instead of the hardcoded defaultTheme
    respectPrefersColorScheme: false,

    // Display the ring in Profile picture
    displayAvatarRing: true,

    // Available themes. To remove any theme, exclude from here.
    // themes: [
    //   'dark',
    //   'light',
    //   'cupcake',
    //   'bumblebee',
    //   'emerald',
    //   'corporate',
    //   'synthwave',
    //   'retro',
    //   'cyberpunk',
    //   'valentine',
    //   'halloween',
    //   'garden',
    //   'forest',
    //   'aqua',
    //   'lofi',
    //   'pastel',
    //   'fantasy',
    //   'wireframe',
    //   'black',
    //   'luxury',
    //   'dracula',
    //   'cmyk',
    //   'autumn',
    //   'business',
    //   'acid',
    //   'lemonade',
    //   'night',
    //   'coffee',
    //   'winter',
    //   'dim',
    //   'nord',
    //   'sunset',
    //   'procyon',
    // ],
    themes: [
      'dark',
      'forest',
      'black',
      'luxury',
      'dracula',
      'business',
      'night',
      'dim',
      'nord',
      'sunset',
      'procyon',
    ],
    // Custom theme, applied to `procyon` theme
    customTheme: {
      primary: '#fc055b',
      secondary: '#219aaf',
      accent: '#e8d03a',
      neutral: '#2A2730',
      'base-100': '#E3E3ED',
      '--rounded-box': '3rem',
      '--rounded-btn': '3rem',
    },
  },

  // // Optional Footer. Supports plain text or HTML.
  // footer: `Made b James Brendamour
  //     class="text-primary" href="https://github.com/jamesbmour/jamesbrendamour.me"
  //     target="_blank"
  //     rel="noreferrer"
  //   >GitProfile</>`,

  // enablePWA: true,
};

export default CONFIG;
