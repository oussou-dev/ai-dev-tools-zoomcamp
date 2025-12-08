import React from 'react';
import CodeMirror from '@uiw/react-codemirror';
import { javascript } from '@codemirror/lang-javascript';
import { python } from '@codemirror/lang-python';
import { java } from '@codemirror/lang-java';
import { cpp } from '@codemirror/lang-cpp';
import { StreamLanguage } from '@codemirror/language';
import { ruby } from '@codemirror/legacy-modes/mode/ruby';
import { vscodeDark } from '@uiw/codemirror-theme-vscode';

const CodeEditor = ({ language, code, onChange }) => {
    const getLanguageExtension = (lang) => {
        switch (lang) {
            case 'javascript':
                return javascript();
            case 'python':
                return python();
            case 'java':
                return java();
            case 'cpp':
                return cpp();
            case 'ruby':
                return StreamLanguage.define(ruby);
            default:
                return python();
        }
    };

    return (
        <div className="code-editor-container" style={{ height: '100%', fontSize: '14px' }}>
            <CodeMirror
                value={code}
                height="100%"
                theme={vscodeDark}
                extensions={[getLanguageExtension(language)]}
                onChange={(value) => onChange(value)}
            />
        </div>
    );
};

export default CodeEditor;
