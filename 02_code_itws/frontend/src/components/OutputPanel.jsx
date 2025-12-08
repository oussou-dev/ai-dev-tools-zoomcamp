import React from 'react';

const OutputPanel = ({ output }) => {
    return (
        <div className="output-panel">
            <h3>Output</h3>
            <div className="output-content">
                <pre>{output || 'Run code to see output...'}</pre>
            </div>
        </div>
    );
};

export default OutputPanel;
