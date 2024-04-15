// header.tsx
import React from 'react';

interface HeaderTabsProps {
  onSelectTab: (tab: string) => void;
}

/**
 * HeaderTabs component for displaying navigation tabs
 */
const Header: React.FC<HeaderTabsProps> = ({ onSelectTab }) => {
  return (
    <div className="bg-base-100 shadow-lg p-4 flex justify-center space-x-4">
      <button className="tab tab-bordered tab-active" onClick={() => onSelectTab('home')}>Home</button>
      <button className="tab tab-bordered" onClick={() => onSelectTab('projects')}>Projects</button>
      <button className="tab tab-bordered" onClick={() => onSelectTab('contact')}>Contact</button>
    </div>
  );
};

export default Header;
