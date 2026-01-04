import { useCallback, useEffect, useState } from 'react';
import axios, { AxiosError } from 'axios';
import { formatDistance } from 'date-fns';
import {
  CustomError,
  GENERIC_ERROR,
  INVALID_CONFIG_ERROR,
  INVALID_GITHUB_USERNAME_ERROR,
  setTooManyRequestError,
} from '../constants/errors';
import { HelmetProvider } from 'react-helmet-async';
import '../assets/index.css';
import { getInitialTheme, getSanitizedConfig, setupHotjar } from '../utils';
import { SanitizedConfig } from '../interfaces/sanitized-config';
import ErrorPage from './error-page';
import HeadTagEditor from './head-tag-editor';
import { DEFAULT_THEMES } from '../constants/default-themes';
import ThemeChanger from './theme-changer';
import { BG_COLOR } from '../constants';
import AvatarCard from './avatar-card';
import { Profile } from '../interfaces/profile';
import DetailsCard from './details-card';
import SkillCard from './skill-card';
import ExperienceCard from './experience-card';
import EducationCard from './education-card';
// import CertificationCard from './certification-card';
import { GithubProject } from '../interfaces/github-project';
import GithubProjectCard from './github-project-card';
import ExternalProjectCard from './external-project-card';
import BlogCard from './blog-card';
import Footer from './footer';
// import { createChat } from 'https://cdn.jsdelivr.net/npm/@n8n/chat/dist/chat.bundle.es.js';
// import { createChat } from '@n8n/chat';
// import '@n8n/chat/style.css';
import LatestYoutube from './latest-youtube';

// import '../styles/chat.css'; // Import the chat CSS
import './variables.css';

// import Chatbot from './chatbot';
// import Header from './header'; // Adjust the path as necessary
// import ResumeViewer from './ResumeViewer/ResumeViewer'; // Adjust the path as necessary
// import '@n8n/chat/style.css';
// import { createChat } from '@n8n/chat';

/**
 * Renders the GitProfile component.
 *
 * @param {Object} config - the configuration object
 * @return {JSX.Element} the rendered GitProfile component
 */
const GitProfile = ({ config }: { config: Config }) => {
  const [sanitizedConfig] = useState<SanitizedConfig | Record<string, never>>(
    getSanitizedConfig(config),
  );
  // createChat({
  //   webhookUrl:
  //     'https://n8n.jdb7.us/webhook/f1c26d49-a173-45d6-a871-5b017074f7c1/chat',

  //   initialMessages: [
  //     'Hi there! 👋 My name is James. What would you like to know about me?',
  //     'E.g. What work have you done with LLMs.',
  //   ],
  //   i18n: {
  //     en: {
  //       title: 'Hi Chat! 👋',
  //       subtitle: 'Chat with me resume, Experiences, and projects.',
  //       footer: '',
  //       getStarted: 'New Conversation',
  //       inputPlaceholder: 'Type your question..',
  //       closeButtonTooltip: 'Close Chat', // Required property
  //     },
  //   },
  // });

  const [theme, setTheme] = useState<string>(DEFAULT_THEMES[0]);
  const [error, setError] = useState<CustomError | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [profile, setProfile] = useState<Profile | null>(null);
  const [githubProjects, setGithubProjects] = useState<GithubProject[]>([]);

  const getGithubProjects = useCallback(
    async (publicRepoCount: number): Promise<GithubProject[]> => {
      if (sanitizedConfig.projects.github.mode === 'automatic') {
        if (publicRepoCount === 0) {
          return [];
        }

        const excludeRepo =
          sanitizedConfig.projects.github.automatic.exclude.projects
            .map((project) => `+-repo:${project}`)
            .join('');

        const query = `user:${
          sanitizedConfig.github.username
        }+fork:${!sanitizedConfig.projects.github.automatic.exclude
          .forks}${excludeRepo}`;
        const url = `https://api.github.com/search/repositories?q=${query}&sort=${sanitizedConfig.projects.github.automatic.sortBy}&per_page=${sanitizedConfig.projects.github.automatic.limit}&type=Repositories`;

        const repoResponse = await axios.get(url, {
          headers: { 'Content-Type': 'application/vnd.github.v3+json' },
        });
        const repoData = repoResponse.data;

        return repoData.items;
      } else {
        if (sanitizedConfig.projects.github.manual.projects.length === 0) {
          return [];
        }
        const repos = sanitizedConfig.projects.github.manual.projects
          .map((project) => `+repo:${project}`)
          .join('');

        const url = `https://api.github.com/search/repositories?q=${repos}&type=Repositories`;

        const repoResponse = await axios.get(url, {
          headers: { 'Content-Type': 'application/vnd.github.v3+json' },
        });
        const repoData = repoResponse.data;

        return repoData.items;
      }
    },
    [
      sanitizedConfig.github.username,
      sanitizedConfig.projects.github.mode,
      sanitizedConfig.projects.github.manual.projects,
      sanitizedConfig.projects.github.automatic.sortBy,
      sanitizedConfig.projects.github.automatic.limit,
      sanitizedConfig.projects.github.automatic.exclude.forks,
      sanitizedConfig.projects.github.automatic.exclude.projects,
    ],
  );

  const loadData = useCallback(async () => {
    try {
      setLoading(true);

      const response = await axios.get(
        `https://api.github.com/users/${sanitizedConfig.github.username}`,
      );
      const data = response.data;

      setProfile({
        avatar: data.avatar_url,
        name: data.name || ' ',
        bio: data.bio || '',
        location: data.location || '',
        company: data.company || '',
      });

      if (!sanitizedConfig.projects.github.display) {
        return;
      }

      setGithubProjects(await getGithubProjects(data.public_repos));
    } catch (error) {
      handleError(error as AxiosError | Error);
    } finally {
      setLoading(false);
    }
  }, [
    sanitizedConfig.github.username,
    sanitizedConfig.projects.github.display,
    getGithubProjects,
  ]);

  useEffect(() => {
    if (Object.keys(sanitizedConfig).length === 0) {
      setError(INVALID_CONFIG_ERROR);
    } else {
      setError(null);
      setTheme(getInitialTheme(sanitizedConfig.themeConfig));
      setupHotjar(sanitizedConfig.hotjar);
      loadData().then((r) => r);
    }
  }, [sanitizedConfig, loadData]);

  useEffect(() => {
    theme && document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  const handleError = (error: AxiosError | Error): void => {
    console.error('Error:', error);

    if (error instanceof AxiosError) {
      try {
        const reset = formatDistance(
          new Date(error.response?.headers?.['x-ratelimit-reset'] * 1000),
          new Date(),
          { addSuffix: true },
        );

        if (typeof error.response?.status === 'number') {
          switch (error.response.status) {
            case 403:
              setError(setTooManyRequestError(reset));
              break;
            case 404:
              setError(INVALID_GITHUB_USERNAME_ERROR);
              break;
            default:
              setError(GENERIC_ERROR);
              break;
          }
        } else {
          setError(GENERIC_ERROR);
        }
      } catch (innerError) {
        setError(GENERIC_ERROR);
      }
    } else {
      setError(GENERIC_ERROR);
    }
  };

  return (
    <HelmetProvider>
      <div className="h-screen fade-in">
        {/* <link
          href="https://cdn.jsdelivr.net/npm/@n8n/chat/dist/style.css"
          rel="stylesheet"
        /> */}
        ;{/* add style sheet css  */}
        <script>{/* Add any necessary scripts or styles here */}</script>
        {/*<Header*/}
        {/*  onSelectTab={function (): void {*/}
        {/*    throw new Error('Function not implemented.');*/}
        {/*  }}*/}
        {/*/>{' '}*/}
        {/* Add the Header component here */}
        {error ? (
          <ErrorPage
            status={error.status}
            title={error.title}
            subTitle={error.subTitle}
          />
        ) : (
          <>
            <HeadTagEditor
              googleAnalyticsId={sanitizedConfig.googleAnalytics.id}
              appliedTheme={theme}
            />
            <div className={`p-4 lg:p-10 min-h-full ${BG_COLOR}`}>
              <div className="grid grid-cols-1 gap-4 lg:grid-cols-4 rounded-box">
                <div className="col-span-1">
                  <div className="grid grid-cols-1 gap-4">
                    {/* <div className="card-body">
                      <h3 className="text-2xl font-bold text-center">
                        This website is still under development
                      </h3>
                    </div> */}
                    {!sanitizedConfig.themeConfig.disableSwitch && (
                      <ThemeChanger
                        theme={theme}
                        setTheme={setTheme}
                        loading={loading}
                        themeConfig={sanitizedConfig.themeConfig}
                      />
                    )}
                    <AvatarCard
                      profile={profile}
                      loading={loading}
                      avatarRing={sanitizedConfig.themeConfig.displayAvatarRing}
                      resumeFileUrl={sanitizedConfig.resume.fileUrl}
                    />
                    <DetailsCard
                      profile={profile}
                      loading={loading}
                      github={sanitizedConfig.github}
                      social={sanitizedConfig.social}
                    />
                    {sanitizedConfig.educations.length !== 0 && (
                      <EducationCard
                        loading={loading}
                        educations={sanitizedConfig.educations}
                      />
                    )}

                    {sanitizedConfig.experiences.length !== 0 && (
                      <ExperienceCard
                        loading={loading}
                        experiences={sanitizedConfig.experiences}
                      />
                    )}
                    {sanitizedConfig.skills.length !== 0 && (
                      <SkillCard
                        loading={loading}
                        skills={sanitizedConfig.skills}
                      />
                    )}

                    {/* {sanitizedConfig.certifications.length !== 0 && (
                      <CertificationCard
                        loading={loading}
                        certifications={sanitizedConfig.certifications}
                      />
                    )} */}
                  </div>
                </div>
                <div className="col-span-1 lg:col-span-3">
                  <div className="grid grid-cols-1 gap-6">
                    {/* add expericance card */}
                    {sanitizedConfig.social.youtube && (
                      <LatestYoutube channelId="UCg5Reo1UiJHniv9KFGkRIPg" />
                    )}
                    {sanitizedConfig.blog.display && (
                      <BlogCard
                        loading={loading}
                        googleAnalyticsId={sanitizedConfig.googleAnalytics.id}
                        blog={sanitizedConfig.blog}
                      />
                    )}
                    {sanitizedConfig.projects.github.display && (
                      <GithubProjectCard
                        header={sanitizedConfig.projects.github.header}
                        limit={sanitizedConfig.projects.github.automatic.limit}
                        githubProjects={githubProjects}
                        loading={loading}
                        username={sanitizedConfig.github.username}
                        googleAnalyticsId={sanitizedConfig.googleAnalytics.id}
                      />
                    )}

                    {sanitizedConfig.projects.external.projects.length !==
                      0 && (
                      <ExternalProjectCard
                        loading={loading}
                        header={sanitizedConfig.projects.external.header}
                        externalProjects={
                          sanitizedConfig.projects.external.projects
                        }
                        googleAnalyticId={sanitizedConfig.googleAnalytics.id}
                      />
                    )}
                    {/* <ResumeViewer /> */}
                  </div>
                </div>
              </div>
            </div>
            {sanitizedConfig.footer && (
              <footer
                className={`p-4 footer ${BG_COLOR} text-base-content footer-center`}
              >
                <div className="shadow card compact bg-base-100">
                  <Footer content={sanitizedConfig.footer} loading={loading} />
                </div>
              </footer>
            )}
            {/* <StreamlitApp /> */}
          </>
        )}
      </div>
    </HelmetProvider>
  );
};

export default GitProfile;
