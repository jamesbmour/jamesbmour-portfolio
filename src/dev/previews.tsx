import { ComponentPreview, Previews } from '@react-buddy/ide-toolbox';
import { PaletteTree } from './palette';
import BlogCard from '../components/blog-card';
import { SanitizedBlog } from '../interfaces/sanitized-config.tsx';

interface ComponentPreviewsProps {
  blog: SanitizedBlog;
}

const ComponentPreviews = ({ blog }: ComponentPreviewsProps) => {
  return (
    <Previews palette={<PaletteTree />}>
      <ComponentPreview path="/BlogCard">
        <BlogCard blog={blog} loading />
      </ComponentPreview>
    </Previews>
  );
};

export default ComponentPreviews;
