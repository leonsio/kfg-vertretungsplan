class KfgVertretungsplanCard extends HTMLElement {
  setConfig(config) {
    this.config = config || {};
    this.sensor = this.config.sensor || "sensor.vertretungsplan";
    this.selectedEntity = this.config.selected_entity || "input_text.vertretungsplan_klassen";
    this.render();
  }
  set hass(value) {
    this._hass = value;
    if (this.config) this.render();
  }
  get hass() { return this._hass; }
  getCardSize() { return 8; }

  async toggleClass(cls, selected) {
    const state = this.hass.states[this.selectedEntity];
    const current = (state?.state || "").split(",").map(x => x.trim()).filter(Boolean);
    const next = selected
      ? [...new Set([...current, cls])].sort()
      : current.filter(x => x !== cls);
    await this.hass.callService("input_text", "set_value", {
      entity_id: this.selectedEntity,
      value: next.join(", ")
    });
  }

  render() {
    if (!this._hass || !this.config) return;
    const s = this._hass.states[this.sensor];
    const data = s?.attributes || {};
    const classes = data.classes || [];
    const selected = (this._hass.states[this.selectedEntity]?.state || "")
      .split(",").map(x => x.trim()).filter(Boolean);
    const days = data.days || [];
    const esc = x => String(x ?? "").replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c]);
    let html = `<ha-card><div class="header"><div class="name">Vertretungsplan</div><div class="meta">KW ${esc(data.current_week ?? "")}${data.next_week_available ? " + nächste Woche" : ""}</div></div><div class="classes">${classes.map(c => `<label class="chip ${selected.includes(c) ? "selected" : ""}"><input type="checkbox" data-class="${esc(c)}" ${selected.includes(c) ? "checked" : ""}><span>${esc(c)}</span></label>`).join("")}</div><div class="content">`;
    for (const day of days) {
      const entries = (day.entries || []).filter(e => !selected.length || selected.includes((e.klasse || "").trim()));
      if (!entries.length && !(day.news || []).length) continue;
      html += `<section><h3>${esc(day.weekday)}, ${esc(day.date)}</h3>`;
      for (const n of (day.news || [])) html += `<div class="news">ℹ️ ${esc(n.join(" — "))}</div>`;
      for (const e of entries) {
        const art = (e.art || "").toLowerCase();
        const cls = art === "entf" ? "entfall" : art === "taus" ? "tausch" : art === "paus" ? "pause" : "vertretung";
        html += `<div class="entry ${cls}"><b>${esc(e.klasse || "—")} · ${esc(e.stunde)}</b><span>${esc(e.fach || e.fach_original || "")}</span><span>${esc(e.lehrer_original || "")} → ${esc(e.vertreter || e.lehrer_nach || "")}</span><span>${esc(e.raum || "")}</span><strong>${esc(e.art || "")}</strong>${e.text ? `<small>${esc(e.text)}</small>` : ""}</div>`;
      }
      html += `</section>`;
    }
    html += `</div></ha-card>`;
    this.innerHTML = `<style>ha-card{padding:16px}.header{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:12px}.name{font-size:1.3em;font-weight:600}.meta{opacity:.7}.classes{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:14px}.chip{border:1px solid var(--divider-color);border-radius:16px;padding:5px 10px;cursor:pointer}.chip.selected{background:var(--primary-color);color:var(--text-primary-color)}.chip input{display:none}section{margin:14px 0}h3{margin:8px 0}.news{padding:8px 10px;border-radius:8px;background:var(--secondary-background-color);margin:5px 0}.entry{display:grid;grid-template-columns:auto 1fr 1fr auto auto;gap:8px;align-items:center;padding:8px 10px;border-left:4px solid var(--primary-color);margin:5px 0;border-radius:5px;background:var(--secondary-background-color)}.entry.entfall{border-left-color:var(--error-color)}.entry.tausch{border-left-color:var(--warning-color)}.entry.pause{border-left-color:var(--info-color)}.entry small{grid-column:1/-1;opacity:.8}@media(max-width:700px){.entry{grid-template-columns:1fr 1fr}.entry span:nth-child(3){grid-column:1/-1}}</style>${html}`;
    this.querySelectorAll("input[data-class]").forEach(el => el.addEventListener("change", ev => this.toggleClass(ev.target.dataset.class, ev.target.checked)));
  }
}
customElements.define("kfg-vertretungsplan-card", KfgVertretungsplanCard);
window.customCards = window.customCards || [];
window.customCards.push({type: "kfg-vertretungsplan-card", name: "KFG Vertretungsplan", description: "Vertretungsplan mit Mehrfachauswahl von Klassen"});
