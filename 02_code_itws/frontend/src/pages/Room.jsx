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

    // Runtimes
    const { runPython, isLoading: isPythonLoading } = usePyodide();

    const [socket, setSocket] = useState(null);
    const socketRef = useRef(null);

    // Create a ref to hold the debounced function so it persists across renders
    const debouncedSend = useRef(
        debounce((code) => {
            const ws = socketRef.current;
            if (ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({
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
                setCode(data.code);
            } else if (data.type === 'language_update') {
                setLanguage(data.language);
            }
        };

        ws.onclose = () => {
            console.log('Disconnected from WebSocket');
        };

        setSocket(ws);
        socketRef.current = ws;

        return () => {
            ws.close();
            socketRef.current = null;
        };
    }, [roomId]);

    const handleCodeChange = (newCode) => {
        setCode(newCode);
        debouncedSend(newCode);
    };

    const handleLanguageChange = (newLanguage) => {
        setLanguage(newLanguage);
        const newCode = CODE_SNIPPETS[newLanguage] || '';
        setCode(newCode);

        if (socket && socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify({
                type: 'language_update',
                language: newLanguage
            }));
            // Also send code update for the new snippet
            socket.send(JSON.stringify({
                type: 'code_update',
                code: newCode
            }));
        }
    };

    const runJavaScript = async (code) => {
        const logs = [];
        const originalLog = console.log;
        const originalError = console.error;

        console.log = (...args) => {
            logs.push(args.map(arg => typeof arg === 'object' ? JSON.stringify(arg) : String(arg)).join(' '));
            originalLog(...args);
        };

        console.error = (...args) => {
            logs.push("Error: " + args.map(arg => typeof arg === 'object' ? JSON.stringify(arg) : String(arg)).join(' '));
            originalError(...args);
        };

        try {
            // Create a safe-ish scope
            const func = new Function('console', `return (async () => { 
                try {
                    ${code}
                } catch(e) {
                    console.error(e.message);
                }
            })()`);

            await func({ log: console.log, error: console.error });
        } catch (error) {
            logs.push(`Execution Error: ${error.message}`);
        } finally {
            console.log = originalLog;
            console.error = originalError;
        }
        return logs.join('\n') || 'No output';
    };

    const handleRun = async () => {
        setOutput(`Running ${language} code...`);

        if (language === 'python') {
            if (isPythonLoading) {
                setOutput('Loading Python runtime... Please wait.');
                return;
            }
            const result = await runPython(code);
            setOutput(result);
        } else if (language === 'javascript') {
            const result = await runJavaScript(code);
            setOutput(result);
        } else {
            setOutput(`Error: Execution for ${language} is not supported yet.`);
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
                    isLoading={isPythonLoading}
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
