// ResumeViewer.tsx
import React, { useState } from 'react';
import { MDXProvider } from '@mdx-js/react';
import ResumeContent from './resume.mdx'; // Adjust the path as necessary

const ResumeViewer: React.FC = () => {
  const [showResume, setShowResume] = useState(false);

  const handleToggleResume = () => {
    setShowResume((prevState) => !prevState);
  };

  return (
    <div>
      <button onClick={handleToggleResume}>
        {showResume ? 'Hide Resume' : 'Show Resume'}
      </button>
      {showResume && (
        <div className="resume-content">
          <MDXProvider>
            <ResumeContent />
          </MDXProvider>
        </div>
      )}
    </div>
  );
};

export default ResumeViewer;
