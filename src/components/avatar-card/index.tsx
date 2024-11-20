import { FALLBACK_IMAGE } from '../../constants';
import { Profile } from '../../interfaces/profile';
import { skeleton } from '../../utils';
import LazyImage from '../lazy-image';
import { useState } from 'react';
import ContactModal from './contact-modal';

// import ResumeContent from '../resume/resume.mdx';

interface AvatarCardProps {
  profile: Profile | null;
  loading: boolean;
  avatarRing: boolean;
  resumeFileUrl?: string;
}

/**
 * Renders an AvatarCard component.
 * @param profile - The profile object.
 * @param loading - A boolean indicating if the profile is loading.
 * @param avatarRing - A boolean indicating if the avatar should have a ring.
 * @param resumeFileUrl - The URL of the resume file.
 * @returns JSX element representing the AvatarCard.
 */
const AvatarCard: React.FC<AvatarCardProps> = ({
  profile,
  loading,
  avatarRing,
  resumeFileUrl,
}): JSX.Element => {
  const [isContactModalOpen, setIsContactModalOpen] = useState(false);

  return (
    <div className="shadow-lg card compact bg-base-100">
      <div className="grid py-8 place-items-center">
        {loading || !profile ? (
          <div className="avatar opacity-90">
            <div className="w-32 h-32 mb-8 rounded-full">
              {skeleton({
                widthCls: 'w-full',
                heightCls: 'h-full',
                shape: '',
              })}
            </div>
          </div>
        ) : (
          <div className="avatar opacity-90">
            <div
              className={`mb-8 rounded-full w-32 h-32 ${
                avatarRing
                  ? 'ring ring-primary ring-offset-base-100 ring-offset-2'
                  : ''
              }`}
            >
              {
                <LazyImage
                  src={profile.avatar ? profile.avatar : FALLBACK_IMAGE}
                  alt={profile.name}
                  placeholder={skeleton({
                    widthCls: 'w-full',
                    heightCls: 'h-full',
                    shape: '',
                  })}
                />
              }
            </div>
          </div>
        )}
        <div className="px-8 mx-auto text-center">
          <h5 className="text-2xl font-bold">
            {loading || !profile ? (
              skeleton({ widthCls: 'w-48', heightCls: 'h-8' })
            ) : (
              <span className="text-base-content opacity-70">
                {profile.name}
              </span>
            )}
          </h5>
          <div className="mt-3 font-mono text-base-content text-opacity-60">
            {loading || !profile
              ? skeleton({ widthCls: 'w-48', heightCls: 'h-5' })
              : profile.bio}
          </div>
        </div>
        <div className="flex gap-2 mt-6">
          {resumeFileUrl && (
            <a
              href={resumeFileUrl}
              target="_blank"
              className="text-xs opacity-50 btn btn-outline btn-sm"
              download
              rel="noreferrer"
            >
              Download Resume
            </a>
          )}
          {/* Add Contact Button */}
          <button
            className="text-xs opacity-50 btn btn-outline btn-sm"
            onClick={() => setIsContactModalOpen(true)}
          >
            Contact
          </button>
        </div>
      </div>
      {profile && (
        <ContactModal
          isOpen={isContactModalOpen}
          onClose={() => setIsContactModalOpen(false)}
          profile={profile}
        />
      )}
    </div>
  );
};

export default AvatarCard;
