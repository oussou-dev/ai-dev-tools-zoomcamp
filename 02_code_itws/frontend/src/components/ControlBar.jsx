import React from 'react';

const ControlBar = ({ language, setLanguage, onRun, onShare, isLoading }) => {
    // const languages = ['python', 'javascript', 'java', 'cpp']; // This line will be removed as options become static

    return (
        <div className="control-bar">
            <div className="control-group">
                <select
                    value={language}
                    onChange={(e) => setLanguage(e.target.value)}
                    className="language-select"
                >
                    {/* {languages.map(lang => (
                        <option key={lang} value={lang}>{lang.toUpperCase()}</option>
                    ))} */}
                    <option value="python">Python</option>
                    <option value="javascript">JavaScript</option>
                </select>
                <button
                    className="run-btn"
                    onClick={onRun}
                    disabled={isLoading}
                    style={{ opacity: isLoading ? 0.7 : 1, cursor: isLoading ? 'not-allowed' : 'pointer' }}
                >
                    {isLoading ? 'Loading...' : 'Run Code'}
                </button>
            </div>
            <div className="control-group">
                <button onClick={onShare} className="share-btn">Share Link</button>
            </div>
        </div>
    );
};

export default ControlBar;
