import { useState, useEffect, useRef } from 'react';

export const usePyodide = () => {
    const [pyodide, setPyodide] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [output, setOutput] = useState('');

    useEffect(() => {
        const loadPyodide = async () => {
            try {
                // Check if pyodide is already loaded globally
                if (window.loadPyodide) {
                    const pyodideInstance = await window.loadPyodide({
                        indexURL: "https://cdn.jsdelivr.net/pyodide/v0.25.0/full/"
                    });
                    setPyodide(pyodideInstance);
                    setIsLoading(false);
                    return;
                }

                // Load script dynamically
                const script = document.createElement('script');
                script.src = "https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js";
                script.async = true;
                script.onload = async () => {
                    try {
                        const pyodideInstance = await window.loadPyodide({
                            indexURL: "https://cdn.jsdelivr.net/pyodide/v0.25.0/full/"
                        });
                        setPyodide(pyodideInstance);
                        setIsLoading(false);
                    } catch (err) {
                        console.error("Failed to initialize Pyodide:", err);
                        setIsLoading(false);
                    }
                };
                document.body.appendChild(script);
            } catch (error) {
                console.error("Error loading Pyodide script:", error);
                setIsLoading(false);
            }
        };

        loadPyodide();
    }, []);

    const runPython = async (code) => {
        if (!pyodide) return "Pyodide is loading...";

        try {
            // Redirect stdout to capture print statements
            pyodide.setStdout({ batched: (msg) => setOutput((prev) => prev + msg + "\n") });
            // Clear previous output? Maybe let the caller handle clearing.
            // For now, let's reset output before run if we want fresh output, 
            // but usually we want to append or just show the result of this run.
            // Let's return the result and also manage a state for stdout.

            // Actually, a better pattern for this hook might be to just return the run function 
            // and let it return the output string, including stdout.

            // Reset stdout capture
            let capturedOutput = "";
            pyodide.setStdout({ batched: (msg) => { capturedOutput += msg + "\n"; } });

            await pyodide.runPythonAsync(code);
            return capturedOutput;
        } catch (error) {
            return `Error: ${error.message}`;
        }
    };

    return { runPython, isLoading };
};
