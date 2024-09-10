import { ComponentPreview, Previews } from '@react-buddy/ide-toolbox';
import { PaletteTree } from './palette';
import BlogCard from '../components/blog-card';
import { SanitizedBlog } from '../interfaces/sanitized-config.tsx';
import AvatarCard from '../components/avatar-card';

interface ComponentPreviewsProps {
  blog: SanitizedBlog;
  avatarRing: boolean;
  loading: boolean;
  profile: Profile | null;
}

const ComponentPreviews = ({
  blog,
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
