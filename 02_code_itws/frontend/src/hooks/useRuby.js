import { useState, useEffect, useRef } from 'react';

export const useRuby = () => {
    const [isRubyLoading, setIsRubyLoading] = useState(true);
    const rubyVM = useRef(null);

    useEffect(() => {
        const loadRuby = async () => {
            try {
                // Check if already loaded
                if (rubyVM.current) {
                    setIsRubyLoading(false);
                    return;
                }

                console.log("Loading Ruby WASM...");

                // Load the script if not present
                if (!window["ruby-wasm-wasi"]) {
                    const script = document.createElement('script');
                    script.src = "https://cdn.jsdelivr.net/npm/@ruby/3.3-wasm-wasi@2.6.2/dist/browser.script.iife.js";
                    document.body.appendChild(script);
                    await new Promise(resolve => script.onload = resolve);
                }

                const { DefaultRubyVM } = window["ruby-wasm-wasi"];

                // Fetch the WASM binary
                const response = await fetch("https://cdn.jsdelivr.net/npm/@ruby/3.3-wasm-wasi@2.6.2/dist/ruby+stdlib.wasm");
                const buffer = await response.arrayBuffer();
                const module = await WebAssembly.compile(buffer);
                const { vm } = await DefaultRubyVM(module);

                rubyVM.current = vm;
                setIsRubyLoading(false);
                console.log("Ruby VM loaded successfully");
            } catch (err) {
                console.error("Failed to load Ruby VM", err);
                setIsRubyLoading(false);
            }
        };

        loadRuby();
    }, []);

    const runRuby = async (code) => {
        // Wait for VM if it's still loading
        if (!rubyVM.current) {
            if (isRubyLoading) {
                // Simple polling wait
                let attempts = 0;
                while (!rubyVM.current && attempts < 50) {
                    await new Promise(r => setTimeout(r, 100));
                    attempts++;
                }
            }
        }

        if (!rubyVM.current) return "Error: Ruby VM failed to load or timed out.";

        try {
            // Wrap code to capture stdout
            const wrappedCode = `
                require 'stringio'
                original_stdout = $stdout
                $stdout = StringIO.new
                begin
                    ${code}
                rescue => e
                    puts "Error: #{e.message}"
                end
                result = $stdout.string
                $stdout = original_stdout
                result
            `;
            const result = rubyVM.current.eval(wrappedCode);
            return result.toString();
        } catch (err) {
            return `Runtime Error: ${err.message}`;
        }
    };

    return { runRuby, isRubyLoading };
};
