import { ComponentPreview, Previews } from '@react-buddy/ide-toolbox';
import { PaletteTree } from './palette';
import { SanitizedBlog } from '../interfaces/sanitized-config.tsx';
import AvatarCard from '../components/avatar-card';
import { Profile } from '../interfaces/profile.tsx';

interface ComponentPreviewsProps {
  blog: SanitizedBlog;
  avatarRing: boolean;
  loading: boolean;
  profile: Profile | null;
}

const ComponentPreviews = ({
                             avatarRing,
  loading,
  profile,
}: ComponentPreviewsProps) => {
  return (
    <Previews palette={<PaletteTree />}>
      <ComponentPreview path="/AvatarCard">
        <AvatarCard
          avatarRing={avatarRing}
          loading={loading}
          profile={profile}
        />
      </ComponentPreview>
    </Previews>
  );
};

export default ComponentPreviews;
