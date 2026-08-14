const CARD_NAME = 'kfg-vertretungsplan-card';

class KfgVertretungsplanCard extends HTMLElement {
  setConfig(config) {
    this.config = config || {};
    this.attachShadow({ mode: 'open' });
  }

  set hass(hass) {
    this._hass = hass;
    if (!this.config || !this.shadowRoot) return;
    this._render();
  }

  getCardSize() {
    return 8;
  }

  _render() {
    const entityId = this.config.sensor || this.config.entity || 'sensor.vertretungsplan';
    const entity = this._hass.states[entityId];
    const attrs = entity?.attributes || {};
    const weeks = Array.isArray(attrs.weeks) ? attrs.weeks : [];

    const allEntries = [];
    for (const week of weeks) {
      for (const day of week.days || []) {
        for (const entry of day.entries || []) {
          allEntries.push({ ...entry, weekday: day.weekday, date: day.date, week: week.week });
        }
      }
    }

    const classes = [...new Set(allEntries
      .flatMap(e => this._splitClasses(e.klasse))
      .filter(Boolean))]
      .sort(this._classSort.bind(this));

    if (!this._selectedClasses) {
      this._selectedClasses = new Set();
    }

    const selected = this._selectedClasses;
    const visibleEntries = selected.size
      ? allEntries.filter(e => this._splitClasses(e.klasse).some(c => selected.has(c)))
      : allEntries;

    const today = new Date();
    const currentDate = new Date(today.getFullYear(), today.getMonth(), today.getDate());
    const days = [];
    for (const week of weeks) {
      for (const day of week.days || []) {
        const parsed = this._parseDate(day.date, today.getFullYear());
        if (!parsed || parsed < currentDate) continue;
        const entries = visibleEntries.filter(e => e.week === week.week && e.date === day.date);
        days.push({ ...day, week: week.week, weekType: week.week_type, entries });
      }
    }

    this.shadowRoot.innerHTML = `
      <style>
        :host { display:block; }
        ha-card { overflow:hidden; }
        .header { padding:18px 20px 12px; }
        .title { font-size:1.35rem; font-weight:600; }
        .subtitle { margin-top:4px; color:var(--secondary-text-color); font-size:.9rem; }
        .section { padding:0 16px 14px; }
        .section-title { font-size:.78rem; text-transform:uppercase; letter-spacing:.08em; color:var(--secondary-text-color); margin:10px 4px 8px; }
        .classes { display:flex; flex-wrap:wrap; gap:7px; }
        button { border:1px solid var(--divider-color); background:var(--card-background-color); color:var(--primary-text-color); border-radius:18px; padding:7px 12px; cursor:pointer; font:inherit; font-size:.88rem; }
        button.selected { background:var(--primary-color); color:var(--text-primary-color); border-color:var(--primary-color); }
        .day { margin:10px 0 16px; border:1px solid var(--divider-color); border-radius:12px; overflow:hidden; }
        .day-header { padding:10px 13px; background:var(--secondary-background-color); display:flex; justify-content:space-between; align-items:center; }
        .day-name { font-weight:600; }
        .day-date { color:var(--secondary-text-color); font-size:.88rem; }
        .week-badge { font-size:.72rem; color:var(--secondary-text-color); margin-left:8px; }
        .table-wrap { overflow-x:auto; }
        table { width:100%; border-collapse:collapse; font-size:.88rem; }
        th { text-align:left; color:var(--secondary-text-color); font-weight:500; font-size:.75rem; padding:8px 10px; border-bottom:1px solid var(--divider-color); white-space:nowrap; }
        td { padding:9px 10px; border-bottom:1px solid var(--divider-color); vertical-align:top; }
        tr:last-child td { border-bottom:0; }
        .klasse { font-weight:600; white-space:nowrap; }
        .lesson { white-space:nowrap; font-weight:600; }
        .art { white-space:nowrap; }
        .muted { color:var(--secondary-text-color); }
        .empty { padding:18px; color:var(--secondary-text-color); text-align:center; }
        @media (max-width: 600px) { th:nth-child(4), td:nth-child(4) { display:none; } th,td { padding:8px 7px; } }
      </style>
      <ha-card>
        <div class="header">
          <div class="title">Vertretungsplan</div>
          <div class="subtitle">KW ${attrs.current_week ?? '–'} + nächste Woche${attrs.next_week_available ? '' : ' · nächste Woche noch nicht verfügbar'}</div>
        </div>
        <div class="section">
          <div class="section-title">Klassen</div>
          <div class="classes">
            <button class="${selected.size === 0 ? 'selected' : ''}" data-all>Alle Klassen</button>
            ${classes.map(c => `<button class="${selected.has(c) ? 'selected' : ''}" data-class="${this._escape(c)}">${this._escape(c)}</button>`).join('')}
          </div>
        </div>
        <div class="section">
          ${days.map(day => this._renderDay(day)).join('') || '<div class="empty">Keine Vertretungen für die ausgewählten Klassen vorhanden.</div>'}
        </div>
      </ha-card>
    `;

    this.shadowRoot.querySelector('[data-all]')?.addEventListener('click', () => {
      this._selectedClasses.clear();
      this._render();
    });
    this.shadowRoot.querySelectorAll('[data-class]').forEach(button => {
      button.addEventListener('click', () => {
        const cls = button.dataset.class;
        if (selected.has(cls)) selected.delete(cls); else selected.add(cls);
        this._render();
      });
    });
  }

  _renderDay(day) {
    const entries = day.entries || [];
    return `
      <div class="day">
        <div class="day-header">
          <div><span class="day-name">${this._escape(day.weekday || '')}</span><span class="week-badge">KW ${day.week}</span></div>
          <div class="day-date">${this._escape(day.date || '')}</div>
        </div>
        ${entries.length ? `<div class="table-wrap"><table>
          <thead><tr><th>Klasse</th><th>Stunde</th><th>Fach</th><th>Lehrer</th><th>Vertretung</th><th>Raum</th><th>Art</th></tr></thead>
          <tbody>${entries.map(e => `
            <tr>
              <td class="klasse">${this._escape(e.klasse || '–')}</td>
              <td class="lesson">${this._escape(e.stunde || '–')}</td>
              <td>${this._escape(e.fach || '–')}</td>
              <td>${this._escape(e.lehrer_original || '–')}</td>
              <td>${this._escape(e.vertreter || '–')}</td>
              <td>${this._escape(e.raum || '–')}</td>
              <td class="art">${this._escape(e.art || '–')}</td>
            </tr>`).join('')}</tbody>
        </table></div>` : `<div class="empty">Keine Vertretungen</div>`}
      </div>`;
  }

  _splitClasses(value) {
    if (!value) return [];
    return String(value).replace(/[()]/g, '').split(',').map(x => x.trim()).filter(Boolean);
  }

  _classSort(a, b) {
    const na = a.match(/^(\d+)/); const nb = b.match(/^(\d+)/);
    if (na && nb && Number(na[1]) !== Number(nb[1])) return Number(na[1]) - Number(nb[1]);
    if (na && !nb) return -1; if (!na && nb) return 1;
    return a.localeCompare(b, 'de', { numeric: true });
  }

  _parseDate(value, year) {
    if (!value) return null;
    const m = String(value).match(/(\d{1,2})\.(\d{1,2})\.?/);
    return m ? new Date(year, Number(m[2]) - 1, Number(m[1])) : null;
  }

  _escape(value) {
    return String(value).replace(/[&<>"']/g, c => ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;' }[c]));
  }
}

if (!customElements.get(CARD_NAME)) customElements.define(CARD_NAME, KfgVertretungsplanCard);
if (!customElements.get('vertretungsplan-card')) customElements.define('vertretungsplan-card', KfgVertretungsplanCard);

window.customCards = window.customCards || [];
if (!window.customCards.some(c => c.type === CARD_NAME)) {
  window.customCards.push({ type: CARD_NAME, name: 'KFG Vertretungsplan', description: 'Vertretungsplan des Kaiserin-Friedrich-Gymnasiums' });
}
