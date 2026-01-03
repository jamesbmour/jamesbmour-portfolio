import { useEffect, useState } from 'react';
import axios from 'axios';
import { skeleton } from '../../utils';

interface Video {
  id: string;
  title: string;
  thumbnail: string;
  link: string;
  pubDate: string;
  description: string;
}

interface RssItem {
  guid: string;
  title: string;
  link: string;
  pubDate: string;
  description: string;
}

const LatestYoutube = ({ channelId }: { channelId: string }) => {
  const [videos, setVideos] = useState<Video[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    const fetchVideos = async () => {
      try {
        const rssUrl = `https://www.youtube.com/feeds/videos.xml?channel_id=${channelId}`;
        const response = await axios.get(
          `https://api.rss2json.com/v1/api.json?rss_url=${encodeURIComponent(rssUrl)}`
        );

        if (response.data.status === 'ok') {
          const fetchedVideos = response.data.items.slice(0, 6).map((item: RssItem) => {
            // Extract video ID from link or guid if possible
            const videoId = item.guid.split(':')[2];
            return {
              id: videoId,
              title: item.title,
              thumbnail: `https://i.ytimg.com/vi/${videoId}/hqdefault.jpg`,
              link: item.link,
              pubDate: item.pubDate,
              description: item.description,
            };
          });
          setVideos(fetchedVideos);
        } else {
          setError(true);
        }
      } catch (err) {
        console.error('Failed to fetch YouTube videos', err);
        setError(true);
      } finally {
        setLoading(false);
      }
    };

    if (channelId) {
      fetchVideos();
    }
  }, [channelId]);

  if (error || (!loading && videos.length === 0)) return null;

  return (
    <div className="card shadow-lg compact bg-base-100 mb-8">
      <div className="card-body">
        <div className="mx-3 mb-2 flex items-center justify-between">
          <div className="flex items-center">
            <svg
              className="inline-block w-8 h-8 text-primary mr-4"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              fill="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                fillRule="evenodd"
                d="M21.7 8.037a4.26 4.26 0 0 0-3.019-3.02C16.014 4.3 9.774 4.3 9.774 4.3s-6.24 0-8.907.717A4.26 4.26 0 0 0 .847 8.037a40.56 40.56 0 0 0-.847 8.927 40.56 40.56 0 0 0 .847 8.927 4.26 4.26 0 0 0 3.019 3.02c2.667.683 8.907.683 8.907.683s6.24 0 8.907-.717a4.26 4.26 0 0 0 3.019-3.02 40.56 40.56 0 0 0 .847-8.927 40.56 40.56 0 0 0-.847-8.927ZM10 16.964V10L16 13.5l-6 3.464Z"
                clipRule="evenodd"
              />
            </svg>
            <h5 className="card-title text-lg">Latest Videos</h5>
          </div>
          <a
            href={`https://www.youtube.com/channel/${channelId}`}
            target="_blank"
            rel="noreferrer"
            className="text-opacity-60 hover:text-opacity-100 transition-opacity opacity-50 text-base-content text-sm"
          >
            See All
          </a>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {loading
            ? Array.from({ length: 6 }).map((_, index) => (
                <div key={index} className="flex flex-col gap-4">
                  {skeleton({
                    widthCls: 'w-full',
                    heightCls: 'h-40',
                    shape: 'rounded-lg',
                  })}
                  {skeleton({
                    widthCls: 'w-3/4',
                    heightCls: 'h-4',
                    shape: 'rounded-lg',
                  })}
                  {skeleton({
                    widthCls: 'w-1/2',
                    heightCls: 'h-4',
                    shape: 'rounded-lg',
                  })}
                </div>
              ))
            : videos.map((video) => (
                <a
                  key={video.id}
                  href={video.link}
                  target="_blank"
                  rel="noreferrer"
                  className="group flex flex-col gap-2 hover:opacity-80 transition-opacity"
                >
                  <div className="relative aspect-video w-full overflow-hidden rounded-lg bg-base-200 shadow-sm group-hover:shadow-md transition-all">
                    <img
                      src={video.thumbnail}
                      alt={video.title}
                      className="h-full w-full object-cover"
                      loading="lazy"
                    />
                  </div>
                  <h3 className="font-medium text-sm line-clamp-1 leading-snug">
                    {video.title}
                  </h3>
                  <p className="text-xs opacity-60 line-clamp-2">
                    {video.description}
                  </p>
                  <p className="text-xs opacity-40 mt-1">
                    {new Date(video.pubDate).toLocaleDateString(undefined, {
                      year: 'numeric',
                      month: 'short',
                      day: 'numeric',
                    })}
                  </p>
                </a>
              ))}
        </div>
      </div>
    </div>
  );
};

export default LatestYoutube;
