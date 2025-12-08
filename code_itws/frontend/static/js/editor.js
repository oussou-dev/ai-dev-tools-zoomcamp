// Initialize CodeMirror from a textarea bound to Reflex State and keep the two in sync.
const textarea = document.getElementById("code-textarea");
let editor;

function initEditorFromTextarea() {
  if (!textarea) return;
  // If CodeMirror isn't attached yet, create it from textarea
  if (!editor) {
    editor = CodeMirror.fromTextArea(textarea, {
      mode: "python",
      lineNumbers: true,
      matchBrackets: true,
      indentUnit: 4,
      theme: "default",
    });
    editor.setSize("100%", "100%");

    // When editor changes, copy to textarea and dispatch input so Reflex picks it up
    editor.on("change", () => {
      const value = editor.getValue();
      if (textarea.value !== value) {
        textarea.value = value;
        textarea.dispatchEvent(new Event("input", { bubbles: true }));
      }
    });
  }
}

// If Reflex updates the textarea value (from server), we should update the editor content
if (textarea) {
  // initialize editor now
  initEditorFromTextarea();

  // observe input events on textarea (these will be dispatched both by user edits and by Reflex updates)
  textarea.addEventListener("input", () => {
    if (!editor) return;
    const taVal = textarea.value;
    if (editor.getValue() !== taVal) {
      // preserve cursor if possible
      const cursor = editor.getCursor();
      editor.setValue(taVal);
      try {
        editor.setCursor(cursor);
      } catch (e) {
        // ignore
      }
    }
  });
}

// Language selector handling
const languageSelect = document.getElementById("language");
if (languageSelect) {
  languageSelect.addEventListener("change", (e) => {
    const lang = e.target.value;
    if (editor) {
      if (lang === "python") editor.setOption("mode", "python");
      else if (lang === "javascript") editor.setOption("mode", "javascript");
      else if (lang === "java") editor.setOption("mode", "text/x-java");
      else if (lang === "c") editor.setOption("mode", "text/x-csrc");
      else if (lang === "cpp") editor.setOption("mode", "text/x-c++src");
    }
    // inform server of language change via hidden input pattern
    const langInput = document.getElementById("language");
    if (langInput) {
      // Reflex can bind select to State via on_change in future; for now the select's change will trigger normal form state
      // (Alternatively, add a hidden input wired to State.set_language)
    }
  });
}

// Create/share link
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

// Run code button (same as before)
document.getElementById("run-code")?.addEventListener("click", async () => {
  const lang = document.getElementById("language")?.value || "python";
  const code = editor ? editor.getValue() : textarea ? textarea.value : "";
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

// Undo/Redo bindings
document.getElementById("undo")?.addEventListener("click", () => editor?.undo());
document.getElementById("redo")?.addEventListener("click", () => editor?.redo());

// Real-time status placeholder
function setConnected(connected) {
  const statusEl = document.getElementById("status");
  if (!statusEl) return;
  statusEl.textContent = connected ? "Real-time: connected" : "Real-time: disconnected";
  statusEl.className = connected ? "text-emerald-600 text-sm" : "text-amber-600 text-sm";
}
setConnected(false);
