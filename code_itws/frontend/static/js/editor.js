// Minimal editor bootstrap for prototype using CodeMirror 5
const editorEl = document.getElementById("editor");

const editor = CodeMirror(editorEl, {
  value: "# Welcome to CodeITWS\nprint(\"Hello world\")\n",
  mode: "python",
  lineNumbers: true,
  matchBrackets: true,
  indentUnit: 4,
  theme: "default",
});

// Resize CodeMirror to fill parent
editor.setSize("100%", "100%");

// Language switching
const languageSelect = document.getElementById("language");
languageSelect.addEventListener("change", (e) => {
  const lang = e.target.value;
  if (lang === "python") editor.setOption("mode", "python");
  else if (lang === "javascript") editor.setOption("mode", "javascript");
  else if (lang === "java") editor.setOption("mode", "text/x-java");
  else if (lang === "c") editor.setOption("mode", "text/x-csrc");
  else if (lang === "cpp") editor.setOption("mode", "text/x-c++src");
  document.getElementById("lang-preview").textContent = languageSelect.selectedOptions[0].text;
});

// Create/share link
document.getElementById("create-link").addEventListener("click", () => {
  const room = document.getElementById("room").value || `r-${Date.now().toString(36)}`;
  const url = `${location.origin}${location.pathname}?room=${room}`;
  document.getElementById("share-link").value = url;
});

document.getElementById("copy-link").addEventListener("click", async () => {
  const v = document.getElementById("share-link").value;
  if (!v) return;
  await navigator.clipboard.writeText(v);
  alert("Link copied to clipboard");
});

// Run code safely in browser (sandboxed for JS; for Python we'll use Skulpt if available)
document.getElementById("run-code").addEventListener("click", async () => {
  const lang = languageSelect.value;
  const code = editor.getValue();
  const outputEl = document.getElementById("output");
  outputEl.textContent = "Running...\n";
  try {
    if (lang === "javascript") {
      // Run JS in an isolated iframe
      const iframe = document.createElement("iframe");
      iframe.style.display = "none";
      document.body.appendChild(iframe);
      const win = iframe.contentWindow;
      try {
        const result = win.eval(code);
        outputEl.textContent += String(result);
      } catch (err) {
        outputEl.textContent += String(err);
      }
      document.body.removeChild(iframe);
    } else if (lang === "python") {
      // Try to use Skulpt if available
      if (window.Sk) {
        outputEl.textContent = "";
        Sk.configure({ output: (x) => (outputEl.textContent += x) });
        const promise = Sk.misceval.asyncToPromise(() => Sk.importMainWithBody("__main__", false, code, true));
        await promise;
      } else {
        outputEl.textContent += "Python runtime not available in browser. (Skulpt not loaded)";
      }
    } else {
      outputEl.textContent += "Execution for this language is not yet available in the browser.";
    }
  } catch (err) {
    outputEl.textContent += `\nError: ${err}`;
  }
});

// Simple undo/redo
document.getElementById("undo").addEventListener("click", () => editor.undo());
document.getElementById("redo").addEventListener("click", () => editor.redo());

// Placeholder for real-time: connect to backend WS (to be implemented in Reflex stage)
const statusEl = document.getElementById("status");
function setConnected(connected) {
  statusEl.textContent = connected ? "Real-time: connected" : "Real-time: disconnected";
  statusEl.className = connected ? "text-emerald-600 text-sm" : "text-amber-600 text-sm";
}
setConnected(false);
