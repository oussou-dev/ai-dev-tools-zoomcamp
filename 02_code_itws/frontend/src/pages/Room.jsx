import React, { useState, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';
import debounce from 'lodash.debounce';
import CodeEditor from '../components/CodeEditor';
import ControlBar from '../components/ControlBar';
import OutputPanel from '../components/OutputPanel';
import { CODE_SNIPPETS } from '../constants';
import { usePyodide } from '../hooks/usePyodide';

const Room = () => {
    const { roomId } = useParams();
    const [language, setLanguage] = useState('python');
    const [code, setCode] = useState(CODE_SNIPPETS['python']);
    const [output, setOutput] = useState('');
    const { runPython, isLoading } = usePyodide();
    const [socket, setSocket] = useState(null);
    const isRemoteUpdate = useRef(false);

    // Create a ref to hold the debounced function so it persists across renders
    const debouncedSend = useRef(
        debounce((socket, code) => {
            if (socket && socket.readyState === WebSocket.OPEN) {
                socket.send(JSON.stringify({
                    type: 'code_update',
                    code: code
                }));
            }
        }, 300) // 300ms delay
    ).current;

    useEffect(() => {
        const ws = new WebSocket(`ws://localhost:8003/ws/room/${roomId}/`);

        ws.onopen = () => {
            console.log('Connected to WebSocket');
        };

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === 'code_update') {
                isRemoteUpdate.current = true;
                setCode(data.code);
            }
        };

        ws.onclose = () => {
            console.log('Disconnected from WebSocket');
        };

        setSocket(ws);

        return () => {
            ws.close();
        };
    }, [roomId]);

    const handleCodeChange = (newCode) => {
        setCode(newCode);
        // Only send if this is a local change, not a remote update
        if (!isRemoteUpdate.current) {
            debouncedSend(socket, newCode);
        } else {
            isRemoteUpdate.current = false;
        }
    };

    const handleLanguageChange = (newLanguage) => {
        setLanguage(newLanguage);
        const newCode = CODE_SNIPPETS[newLanguage] || '';
        setCode(newCode);

        if (socket && socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify({
                type: 'code_update',
                code: newCode
            }));
        }
    };

    const handleRun = async () => {
        if (language !== 'python') {
            setOutput('Error: Only Python execution is supported in the browser for now.');
            return;
        }

        if (isLoading) {
            setOutput('Loading Python runtime... Please wait.');
            return;
        }

        setOutput(`Running ${language} code...`);
        const result = await runPython(code);
        setOutput(result);
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
                    isLoading={isLoading}
                />
            </div>
            <div className="room-content">
                <div className="editor-panel">
                    <CodeEditor
                        language={language}
                        code={code}
                        onChange={handleCodeChange}
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
