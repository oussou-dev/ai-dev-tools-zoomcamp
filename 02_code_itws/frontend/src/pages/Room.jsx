import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import CodeEditor from '../components/CodeEditor';
import ControlBar from '../components/ControlBar';
import OutputPanel from '../components/OutputPanel';
import { CODE_SNIPPETS } from '../constants';

const Room = () => {
    const { roomId } = useParams();
    const [language, setLanguage] = useState('python');
    const [code, setCode] = useState(CODE_SNIPPETS['python']);
    const [output, setOutput] = useState('');

    const handleLanguageChange = (newLanguage) => {
        setLanguage(newLanguage);
        setCode(CODE_SNIPPETS[newLanguage] || '');
    };

    const handleRun = async () => {
        setOutput(`Running ${language} code...`);
        try {
            const response = await fetch('http://localhost:8003/api/execute/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ code, language }),
            });

            const data = await response.json();
            if (response.ok) {
                setOutput(data.output);
            } else {
                setOutput(`Error: ${data.output}`);
            }
        } catch (error) {
            setOutput(`Error: Failed to connect to server.\n${error.message}`);
        }
    };

    const handleShare = () => {
        navigator.clipboard.writeText(window.location.href);
        alert('Link copied to clipboard!');
    };

    return (
        <div className="room-container">
            <div className="room-header">
                <h2>Interview Room: {roomId}</h2>
                <ControlBar
                    language={language}
                    setLanguage={handleLanguageChange}
                    onRun={handleRun}
                    onShare={handleShare}
                />
            </div>
            <div className="room-content">
                <div className="editor-panel">
                    <CodeEditor
                        language={language}
                        code={code}
                        onChange={setCode}
                    />
                </div>
                <div className="output-panel-wrapper">
                    <OutputPanel output={output} />
                </div>
            </div>
        </div>
    );
};

export default Room;
