import React from 'react';
import { useTheme } from '../context/ThemeContext';
import { Sun, Moon, Play, Share2 } from 'lucide-react';

const ControlBar = ({ language, setLanguage, onRun, onShare, isLoading }) => {
    const { theme, toggleTheme } = useTheme();

    return (
        <div className="control-bar">
            <div className="control-group">
                <select
                    value={language}
                    onChange={(e) => setLanguage(e.target.value)}
                    className="language-select"
                >
                    <option value="python">Python</option>
                    <option value="javascript">JavaScript</option>
                </select>
                <button
                    className="run-btn"
                    onClick={onRun}
                    disabled={isLoading}
                    style={{ opacity: isLoading ? 0.7 : 1, cursor: isLoading ? 'not-allowed' : 'pointer' }}
                >
                    <Play size={16} />
                    {isLoading ? 'Running...' : 'Run'}
                </button>
            </div>
            <div className="control-group">
                <button onClick={onShare} className="share-btn">
                    <Share2 size={16} />
                    Share
                </button>
                <button onClick={toggleTheme} className="theme-toggle-btn" title="Toggle Theme">
                    {theme === 'dark' ? <Sun size={20} /> : <Moon size={20} />}
                </button>
            </div>
        </div>
    );
};

export default ControlBar;
