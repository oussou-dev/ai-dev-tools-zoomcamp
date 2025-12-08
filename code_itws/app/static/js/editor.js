// Copied editor bootstrap for Reflex app static folder
const editorEl = document.getElementById("editor");

const editor = CodeMirror(editorEl, {
  value: "# Welcome to CodeITWS\nprint(\"Hello world from Reflex\")\n",
  mode: "python",
  lineNumbers: true,
  matchBrackets: true,
  indentUnit: 4,
  theme: "default",
});

editor.setSize("100%", "100%");

const languageSelect = document.getElementById("language");
if (languageSelect) {
  languageSelect.addEventListener("change", (e) => {
    const lang = e.target.value;
    if (lang === "python") editor.setOption("mode", "python");
    else if (lang === "javascript") editor.setOption("mode", "javascript");
    else if (lang === "java") editor.setOption("mode", "text/x-java");
    else if (lang === "c") editor.setOption("mode", "text/x-csrc");
    else if (lang === "cpp") editor.setOption("mode", "text/x-c++src");
    const preview = document.getElementById("lang-preview");
    if (preview) preview.textContent = languageSelect.selectedOptions[0].text;
  });
}

document.getElementById("create-link")?.addEventListener("click", () => {
  const room = document.getElementById("room")?.value || `r-${Date.now().toString(36)}`;
  const url = `${location.origin}${location.pathname}?room=${room}`;
  document.getElementById("share-link").value = url;
});

document.getElementById("copy-link")?.addEventListener("click", async () => {
  const v = document.getElementById("share-link").value;
  if (!v) return;
  await navigator.clipboard.writeText(v);
  alert("Link copied to clipboard");
});

document.getElementById("run-code")?.addEventListener("click", async () => {
  const lang = document.getElementById("language")?.value || "python";
  const code = editor.getValue();
  const outputEl = document.getElementById("output");
  if (outputEl) outputEl.textContent = "Running...\n";
  try {
    if (lang === "javascript") {
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

document.getElementById("undo")?.addEventListener("click", () => editor.undo());
document.getElementById("redo")?.addEventListener("click", () => editor.redo());

function setConnected(connected) {
  const statusEl = document.getElementById("status-label");
  if (!statusEl) return;
  statusEl.textContent = connected ? "Real-time: connected" : "Real-time: disconnected";
  statusEl.className = connected ? "text-emerald-600 text-sm" : "text-amber-600 text-sm";
}
setConnected(false);
