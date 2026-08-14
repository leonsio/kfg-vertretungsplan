class KfgVertretungsplanCard extends HTMLElement {
  setConfig(config) {
    this.config = config || {};
    this.sensor = this.config.sensor || "sensor.vertretungsplan";
    this.storageKey = this.config.storage_key || "kfg-vertretungsplan-selected-classes";
    this.selected = this._loadSelection();
    this.render();
  }

  set hass(value) {
    this._hass = value;
    if (this.config) this.render();
  }

  get hass() { return this._hass; }
  getCardSize() { return 8; }

  _loadSelection() {
    try {
      const value = window.localStorage.getItem(this.storageKey);
      return value ? JSON.parse(value) : [];
    } catch (_error) { return []; }
  }

  _saveSelection() {
    try { window.localStorage.setItem(this.storageKey, JSON.stringify(this.selected)); } catch (_error) {}
  }

  toggleClass(cls, selected) {
    this.selected = selected
      ? [...new Set([...this.selected, cls])].sort(this._classSort)
      : this.selected.filter((item) => item !== cls);
    this._saveSelection();
    this.render();
  }

  clearSelection() {
    this.selected = [];
    this._saveSelection();
    this.render();
  }

  _entryClasses(value) {
    return String(value || "")
      .replace(/[()]/g, "")
      .split(",")
      .map((item) => item.trim())
      .filter(Boolean);
  }

  _classSort(a, b) {
    const am = String(a).match(/^(\d+)(.*)$/);
    const bm = String(b).match(/^(\d+)(.*)$/);
    if (am && bm && Number(am[1]) !== Number(bm[1])) return Number(am[1]) - Number(bm[1]);
    return String(a).localeCompare(String(b), "de", { numeric: true });
  }

  _isTodayOrFuture(displayDate, isoToday) {
    const match = String(displayDate || "").match(/^(\d{1,2})\.(\d{1,2})\.?$/);
    if (!match || !isoToday) return true;
    const today = new Date(`${isoToday}T00:00:00`);
    let year = today.getFullYear();
    const month = Number(match[2]) - 1;
    if (today.getMonth() === 11 && month === 0) year += 1;
    return new Date(year, month, Number(match[1])) >= today;
  }

  _buildViewData(data) {
    const weeks = Array.isArray(data.weeks) ? data.weeks : [];
    const days = [];
    const classSet = new Set();
    const today = String(data.today || "");

    for (const week of weeks) {
      for (const day of week.days || []) {
        // The sensor contains weeks[], not a top-level days[] array.
        // Start at today and continue through the end of the next week.
        if (week.week === data.current_week && !this._isTodayOrFuture(day.date, today)) continue;

        const entries = (day.entries || []).map((entry) => {
          const entryClasses = this._entryClasses(entry.klasse);
          entryClasses.forEach((cls) => classSet.add(cls));
          return { ...entry, _classes: entryClasses };
        });
        days.push({ ...day, entries });
      }
    }

    return {
      classes: [...classSet].sort(this._classSort),
      days,
    };
  }

  render() {
    if (!this._hass || !this.config) return;

    const state = this._hass.states[this.sensor];
    const data = state?.attributes || {};
    const view = this._buildViewData(data);
    const classes = view.classes;
    const available = new Set(classes);
    this.selected = this.selected.filter((item) => available.has(item));
    const selected = this.selected;
    const esc = (value) => String(value ?? "").replace(/[&<>"']/g, (c) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
    })[c]);

    let html = `<ha-card><div class="header"><div class="name">Vertretungsplan</div><div class="meta">KW ${esc(data.current_week ?? "")}${data.next_week_available ? " + nächste Woche" : ""}</div></div><div class="toolbar"><span>Klassen</span><button type="button" data-clear>Alle Klassen</button></div><div class="classes">${classes.map((c) => `<label class="chip ${selected.includes(c) ? "selected" : ""}"><input type="checkbox" data-class="${esc(c)}" ${selected.includes(c) ? "checked" : ""}><span>${esc(c)}</span></label>`).join("")}</div><div class="content">`;

    let renderedDays = 0;
    for (const day of view.days) {
      const entries = (day.entries || []).filter((entry) => !selected.length || (entry._classes || []).some((cls) => selected.includes(cls)));
      if (!entries.length && !(day.news || []).length) continue;
      renderedDays += 1;
      html += `<section><h3>${esc(day.weekday)}, ${esc(day.date)}</h3>`;
      for (const news of day.news || []) html += `<div class="news">ℹ️ ${esc(Array.isArray(news) ? news.join(" — ") : news)}</div>`;
      for (const entry of entries) {
        const art = (entry.art || "").toLowerCase();
        const cssClass = art === "entf" ? "entfall" : art === "taus" ? "tausch" : art === "paus" ? "pause" : "vertretung";
        html += `<div class="entry ${cssClass}"><b>${esc(entry.klasse || "—")} · ${esc(entry.stunde)}</b><span>${esc(entry.fach || entry.fach_original || "")}</span><span>${esc(entry.lehrer_original || "")} → ${esc(entry.vertreter || entry.lehrer_nach || "")}</span><span>${esc(entry.raum || "")}</span><strong>${esc(entry.art || "")}</strong>${entry.text ? `<small>${esc(entry.text)}</small>` : ""}</div>`;
      }
      html += `</section>`;
    }

    if (!renderedDays) html += `<div class="empty">Keine Vertretungen im angezeigten Zeitraum.</div>`;
    html += `</div></ha-card>`;

    this.innerHTML = `<style>ha-card{padding:16px}.header{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:12px}.name{font-size:1.3em;font-weight:600}.meta{opacity:.7}.toolbar{display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;font-weight:600}.toolbar button{background:none;border:0;color:var(--primary-color);cursor:pointer;font:inherit}.classes{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:14px}.chip{border:1px solid var(--divider-color);border-radius:16px;padding:5px 10px;cursor:pointer}.chip.selected{background:var(--primary-color);color:var(--text-primary-color)}.chip input{display:none}section{margin:14px 0}h3{margin:8px 0}.news{padding:8px 10px;border-radius:8px;background:var(--secondary-background-color);margin:5px 0}.entry{display:grid;grid-template-columns:auto 1fr 1fr auto auto;gap:8px;align-items:center;padding:8px 10px;border-left:4px solid var(--primary-color);margin:5px 0;border-radius:5px;background:var(--secondary-background-color)}.entry.entfall{border-left-color:var(--error-color)}.entry.tausch{border-left-color:var(--warning-color)}.entry.pause{border-left-color:var(--info-color)}.entry small{grid-column:1/-1;opacity:.8}.empty{padding:16px 0;opacity:.7}@media(max-width:700px){.entry{grid-template-columns:1fr 1fr}.entry span:nth-child(3){grid-column:1/-1}}</style>${html}`;

    this.querySelectorAll("input[data-class]").forEach((element) => element.addEventListener("change", (event) => this.toggleClass(event.target.dataset.class, event.target.checked)));
    this.querySelector("button[data-clear]")?.addEventListener("click", () => this.clearSelection());
  }
}

if (!customElements.get("kfg-vertretungsplan-card")) customElements.define("kfg-vertretungsplan-card", KfgVertretungsplanCard);
if (!customElements.get("vertretungsplan-card")) customElements.define("vertretungsplan-card", KfgVertretungsplanCard);
window.customCards = window.customCards || [];
window.customCards.push({ type: "kfg-vertretungsplan-card", name: "KFG Vertretungsplan", description: "Vertretungsplan mit Mehrfachauswahl von Klassen" });
window.customCards.push({ type: "vertretungsplan-card", name: "KFG Vertretungsplan (Legacy-Name)", description: "Vertretungsplan mit Mehrfachauswahl von Klassen" });
