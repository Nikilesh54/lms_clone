import { useState, useRef, useEffect } from 'react';
import { 
  Play, Pause, Volume2, VolumeX, Maximize, 
  PictureInPicture, Settings, Bookmark
} from 'lucide-react';
import { VideoBookmark } from '../../types';

interface VideoPlayerProps {
  src: string;
  courseId: string;
  moduleId: string;
  onBookmark?: (bookmark: VideoBookmark) => void;
  onTimeUpdate?: (time: number) => void;
  initialPosition?: number;
}

const VideoPlayer = ({ 
  src, 
  courseId, 
  moduleId, 
  onBookmark, 
  onTimeUpdate,
  initialPosition = 0 
}: VideoPlayerProps) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [volume, setVolume] = useState(1);
  const [isMuted, setIsMuted] = useState(false);
  const [playbackRate, setPlaybackRate] = useState(1);

  useEffect(() => {
    if (videoRef.current && initialPosition) {
      videoRef.current.currentTime = initialPosition;
    }
  }, [initialPosition]);

  const togglePlay = () => {
    if (videoRef.current) {
      if (isPlaying) {
        videoRef.current.pause();
      } else {
        videoRef.current.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  const handleTimeUpdate = () => {
    if (videoRef.current) {
      setCurrentTime(videoRef.current.currentTime);
      onTimeUpdate?.(videoRef.current.currentTime);
    }
  };

  const handleLoadedMetadata = () => {
    if (videoRef.current) {
      setDuration(videoRef.current.duration);
    }
  };

  const toggleMute = () => {
    if (videoRef.current) {
      videoRef.current.muted = !isMuted;
      setIsMuted(!isMuted);
    }
  };

  const handleVolumeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newVolume = parseFloat(e.target.value);
    if (videoRef.current) {
      videoRef.current.volume = newVolume;
      setVolume(newVolume);
    }
  };

  const handleSpeedChange = (speed: number) => {
    if (videoRef.current) {
      videoRef.current.playbackRate = speed;
      setPlaybackRate(speed);
    }
  };

  const togglePiP = async () => {
    try {
      if (document.pictureInPictureElement) {
        await document.exitPictureInPicture();
      } else if (videoRef.current) {
        await videoRef.current.requestPictureInPicture();
      }
    } catch (error) {
      console.error('PiP failed:', error);
    }
  };

  const handleBookmark = () => {
    if (videoRef.current && onBookmark) {
      const bookmark: VideoBookmark = {
        id: Date.now().toString(),
        timestamp: videoRef.current.currentTime,
        label: `Bookmark at ${new Date().toISOString()}`,
        courseId,
        moduleId
      };
      onBookmark(bookmark);
    }
  };

  const formatTime = (time: number) => {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  return (
    <div className="relative bg-black rounded-lg overflow-hidden">
      <video
        ref={videoRef}
        src={src}
        className="w-full"
        onTimeUpdate={handleTimeUpdate}
        onLoadedMetadata={handleLoadedMetadata}
      />
      
      <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-4">
        <div className="flex items-center space-x-4">
          <button onClick={togglePlay} className="text-white">
            {isPlaying ? <Pause className="h-6 w-6" /> : <Play className="h-6 w-6" />}
          </button>

          <div className="flex-1">
            <input
              type="range"
              min={0}
              max={duration}
              value={currentTime}
              onChange={(e) => {
                if (videoRef.current) {
                  videoRef.current.currentTime = Number(e.target.value);
                }
              }}
              className="w-full"
            />
            <div className="flex justify-between text-white text-sm mt-1">
              <span>{formatTime(currentTime)}</span>
              <span>{formatTime(duration)}</span>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            <button onClick={toggleMute} className="text-white">
              {isMuted ? <VolumeX className="h-6 w-6" /> : <Volume2 className="h-6 w-6" />}
            </button>

            <div className="relative group">
              <button className="text-white" onClick={() => {}}>
                <Settings className="h-6 w-6" />
              </button>
              <div className="absolute bottom-full right-0 mb-2 hidden group-hover:block bg-black/90 rounded-lg p-2">
                <div className="text-white text-sm">
                  <p className="mb-2">Playback Speed</p>
                  {[0.5, 1, 1.25, 1.5, 2].map((speed) => (
                    <button
                      key={speed}
                      onClick={() => handleSpeedChange(speed)}
                      className={`block w-full text-left px-3 py-1 rounded hover:bg-white/10 ${
                        playbackRate === speed ? 'bg-white/20' : ''
                      }`}
                    >
                      {speed}x
                    </button>
                  ))}
                </div>
              </div>
            </div>

            <button onClick={handleBookmark} className="text-white">
              <Bookmark className="h-6 w-6" />
            </button>

            <button onClick={togglePiP} className="text-white">
              <PictureInPicture className="h-6 w-6" />
            </button>

            <button
              onClick={() => videoRef.current?.requestFullscreen()}
              className="text-white"
            >
              <Maximize className="h-6 w-6" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VideoPlayer;