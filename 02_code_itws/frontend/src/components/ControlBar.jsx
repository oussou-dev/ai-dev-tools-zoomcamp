import React from 'react';

const ControlBar = ({ language, setLanguage, onRun, onShare }) => {
    const languages = ['python', 'javascript', 'java', 'cpp'];

    return (
        <div className="control-bar">
            <div className="control-group">
                <select
                    value={language}
                    onChange={(e) => setLanguage(e.target.value)}
                    className="language-select"
                >
                    {languages.map(lang => (
                        <option key={lang} value={lang}>{lang.toUpperCase()}</option>
                    ))}
                </select>
                <button onClick={onRun} className="run-btn">Run Code</button>
            </div>
            <div className="control-group">
                <button onClick={onShare} className="share-btn">Share Link</button>
            </div>
        </div>
    );
};

export default ControlBar;
