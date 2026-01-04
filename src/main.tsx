import React from 'react';
import ReactDOM from 'react-dom/client';
import GitProfile from './components/gitprofile.tsx';
import { DevSupport } from '@react-buddy/ide-toolbox';
import { ComponentPreviews, useInitial } from './dev';
import { inject } from '@vercel/analytics';

// Initialize Vercel Web Analytics
inject();

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <DevSupport
      // eslint-disable-next-line @typescript-eslint/ban-ts-comment
      // @ts-expect-error
      ComponentPreviews={ComponentPreviews}
      useInitialHook={useInitial}
    >
      <>
        <GitProfile config={CONFIG} />
      </>
    </DevSupport>
    ;
  </React.StrictMode>,
);
