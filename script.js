const $ = (id) => document.getElementById(id);
const urlInput = $("backend-url");
let backend = localStorage.getItem("voicetwin_backend") || "http://127.0.0.1:8000";
urlInput.value = backend;
$("reference").addEventListener("change", () => {
  const f = $("reference").files[0];
  $("file-label").textContent = f ? f.name : "Choose a voice sample";
});
$("script").addEventListener("input", () => $("count").textContent = $("script").value.length);
$("speed").addEventListener("input", () => $("speed-label").textContent = Number($("speed").value).toFixed(1) + "×");
$("settings").onclick = () => $("settings-modal").hidden = false;
$("close-modal").onclick = () => $("settings-modal").hidden = true;
$("save-settings").onclick = async () => {
  backend = urlInput.value.trim().replace(/\/+$/, "");
  localStorage.setItem("voicetwin_backend", backend);
  $("settings-modal").hidden = true;
  await checkBackend();
};
function setStatus(message, type = "") {
  $("status").className = "status " + type;
  $("status").lastElementChild.textContent = message;
}
async function checkBackend() {
  $("backend-status").textContent = "Checking…";
  try {
    const r = await fetch(backend + "/api/health");
    if (!r.ok) throw new Error("HTTP " + r.status);
    const d = await r.json();
    $("backend-status").textContent = d.sarvam_configured ? "Connected · Sarvam configured" : "Connected · API key missing";
    if (!d.sarvam_configured) setStatus("Backend connected, but SARVAM_API_KEY is missing.", "error");
    else setStatus("Ready to generate real voice audio.", "ok");
  } catch {
    $("backend-status").textContent = "Not connected";
    setStatus("Start the backend and check the connection URL.", "error");
  }
}
$("generate").onclick = async () => {
  const audio = $("reference").files[0];
  const script = $("script").value.trim();
  if (!audio) return setStatus("Choose a reference audio file first.", "error");
  if (!script) return setStatus("Enter the text you want spoken.", "error");
  const form = new FormData();
  form.append("reference_audio", audio);
  form.append("text", script);
  form.append("language", $("language").value);
  form.append("style", $("style").value);
  form.append("speed", $("speed").value);
  form.append("voice_name", $("voice-name").value || "my-voice");
  const button = $("generate");
  button.disabled = true; button.textContent = "Generating real AI audio…";
  setStatus("Sending voice sample securely to your backend…");
  $("player").hidden = true; $("download").hidden = true;
  try {
    const response = await fetch(backend + "/api/generate/voice", {method:"POST", body:form});
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data.detail || "Request failed (" + response.status + ")");
    const audioUrl = data.audio_url.startsWith("http") ? data.audio_url : backend + data.audio_url;
    $("player").src = audioUrl; $("player").hidden = false;
    $("download").href = audioUrl; $("download").hidden = false;
    setStatus("Voice generated successfully. You can play or download it.", "ok");
  } catch (e) {
    setStatus(e.message || "Generation failed. Check backend logs.", "error");
  } finally {
    button.disabled = false; button.innerHTML = 'Generate cloned voice <span>↗</span>';
  }
};
checkBackend();
