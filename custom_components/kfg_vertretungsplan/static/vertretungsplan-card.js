const CARD_NAME = 'kfg-vertretungsplan-card';

const TEACHERS = {
  BÄR: 'F. Bär', BRL: 'H. Barthel', BAR: 'B. Bartos', BAZ: 'P. Bartz', BEK: 'A. Beek', BNR: 'A. Berner', BLR: 'J. Biehler', BIN: 'K. Bingemer', BTH: 'N. Birth', BLT: 'M. Blatt', BLO: 'P. Blodt', BRM: 'S. Brinkmann', 'BRÜ': 'S. Brüning', BRK: 'C. Brunk', 'BÜ': 'T. Bühl', BU: 'F. Burghardt', CHL: 'J. Chlup', CLS: 'M. Clérisse', DF: 'M. Diefenbach', DLG: 'L. Dilges', DRD: 'S. Dorfard', DRG: 'S. Düring', ECK: 'O. Ecker', EDF: 'E. Edelhoff', EGR: 'M. Egerer', EIN: 'D. Einberger', EIS: 'N. Eis', ERM: 'S. Erdmann', FZL: 'F. Fevzioglu', FSR: 'S. Fischer', FLS: 'F. Flesch', FRA: 'J. Frankfurth', FDR: 'W. Friedrich', GTN: 'F. Gärtner', GAL: 'S. Gallet', GLS: 'M. Glaessel', GRF: 'F. Graf', GR: 'H. Greis', GTR: 'S. Guter', HMS: 'J. Hamschmidt', HCH: 'F. Hechler', HEI: 'L. Heikaus', HK: 'J. Henkel', HC: 'J. Henrici', HBT: 'A. Herbst', HER: 'S. Herrmann', HEU: 'G. Heupel', HIG: 'M. Hieger', HLR: 'S. Himmelreich', HIN: 'I. Hintz', HOL: 'A. Holstein', HTE: 'C. Holte', 'HÜS': 'J. Hüsing', JOH: 'K. Johannson', 'JÖ': 'K. Jörgens', JTG: 'A. Jütting', KTH: 'F. Kanthak', KE: 'S. Kettner', KDA: 'K. Kholodova', KN: 'J. König', KRT: 'N. Krätke', KRN: 'M. Kroning', LMB: 'M. Lembach', LEN: 'K. Lenz', LBN: 'M. Loeben', LUD: 'S. Ludwig', MAA: 'K. Maar', MLN: 'M. Malinotschka', MTI: 'L. Martini', MCL: 'I. Michel', MIK: 'M. Mik', MLR: 'R. Möller-Wälde', MK: 'M. Müller-Kammerinke', MU: 'N. Muschalla', NHS: 'A.-K. Nienhaus', NF: 'S. Nolof', NLT: 'U. Nolting', PAL: 'M. Palchik', PWL: 'I. Pawlowski', PTG: 'M. Petsching', PHI: 'B. Philippsen', POL: 'P. Pollner', RAB: 'M. Rabel', RBL: 'Rabel', RBN: 'M. Rabinovych', RNT: 'L. Ranft', REI: 'K. Reichert', REU: 'M.T. Reuter', RIC: 'M. Richter', RIE: 'R. Ries', RSE: 'M. Rose', RLF: 'A. Rottluff', 'RÜF': 'S. Rüffert', SFL: 'N. Salus-Flohr', SRF: 'M. Scharf', SHF: 'D. Scheffler', SH: 'C. Scheidhauer', SLD: 'C. Schlaud', SLI: 'A. Schlicht', SMI: 'C. Schmitt', SLZ: 'M. Scholz', SHO: 'F. Schossau', SRB: 'A. Schreiber', SST: 'J. Schuster', SC: 'K. Scior', SPI: 'B. Spielmann', TAC: 'C. Tacke', TG: 'Z. Twardowska-Gehrke', UNC: 'R. Unckell', VCR: 'V. Vaccaro', VLT: 'A. Veltjens', VTT: 'H. Vitt', WGN: 'M. Wagner', WA: 'C. Wagner', WHL: 'A. Wahl', WBR: 'H. Weber', WE: 'U. Welker', WEN: 'S. Wenig', WES: 'B. Wenzel-Stelzig', WPL: 'C. Westphal', WIE: 'T. Wiens', WF: 'O. Wolf', WLK: 'S. Wolk', WND: 'A. Wunderer', ZNN: 'A. Zinn', ZSI: 'A. Zsilinszky', BMN: 'S. Baumann', FRY: 'V. Frey', HST: 'M.J. Hastrich', LBU: 'F. Lebeau', MND: 'F. Meinders', SWZ: 'E. Schweitzer', STC: 'L. Stachel', STN: 'M. Suton', TRV: 'L. Trovato', WLS: 'M. Walsh', WLL: 'B. Will'
};

const LABELS = { Betr: 'Betreuung', Vertr: 'Vertretung', Entf: 'Entfall', Taus: 'Tausch', Freis: 'Freistunde', Raum: 'Raumänderung', 'Statt-Vertretung': 'Statt-Vertretung', Paus: 'Pausenaufsicht', SES: 'Sonderunterricht', 'Vtr. ohne Lehrer': 'Vertretung ohne Lehrer' };
const SUBJECTS = { E: 'Englisch', E1: 'Englisch', E2: 'Englisch', D: 'Deutsch', M: 'Mathematik', SP: 'Sport', BIO: 'Biologie', CH: 'Chemie', F: 'Französisch', F2: 'Französisch', L: 'Latein', L1: 'Latein', L2: 'Latein', GE: 'Geschichte', PW: 'Politik und Wirtschaft', GR: 'Griechisch', ETH: 'Ethik', REV: 'Evangelische Religion', RKA: 'Katholische Religion', KU: 'Kunst', PH: 'Physik', MUS: 'Musik', Dsp: 'Darstellendes Spiel', 'AG-Theater': 'AG Theater' };

class KfgVertretungsplanCard extends HTMLElement {
  setConfig(config) { this.config = config || {}; this.attachShadow({ mode: 'open' }); }
  set hass(hass) { this._hass = hass; if (!this.config || !this.shadowRoot) return; this._render(); }
  getCardSize() { return 8; }

  _render() {
    const entityId = this.config.sensor || this.config.entity || 'sensor.vertretungsplan';
    const entity = this._hass.states[entityId];
    const attrs = entity?.attributes || {};
    const weeks = Array.isArray(attrs.weeks) ? attrs.weeks : [];
    const allEntries = [];
    for (const week of weeks) for (const day of week.days || []) for (const entry of day.entries || []) allEntries.push({ ...entry, weekday: day.weekday, date: day.date, week: week.week, weekType: week.week_type, news: day.news || [] });

    const classes = [...new Set(allEntries.flatMap(e => this._splitClasses(e.klasse)).filter(Boolean))].sort(this._classSort.bind(this));
    const configuredClasses = Array.isArray(this.config.classes) ? this.config.classes.map(String).map(x => x.trim()).filter(Boolean) : null;
    const fixed = configuredClasses && configuredClasses.length > 0;
    const singleFixedClass = fixed && configuredClasses.length === 1;
    const filterClasses = fixed ? configuredClasses : classes;
    const showClassFilter = !singleFixedClass;

    if (!this._selectedClasses) this._selectedClasses = new Set(fixed ? configuredClasses : []);
    if (fixed) {
      const allowed = new Set(configuredClasses);
      this._selectedClasses = new Set([...this._selectedClasses].filter(c => allowed.has(c)));
      if (!this._selectedClasses.size) this._selectedClasses = new Set(configuredClasses);
    }
    const selected = this._selectedClasses;
    const visibleEntries = selected.size ? allEntries.filter(e => this._splitClasses(e.klasse).some(c => selected.has(c))) : allEntries;

    const today = new Date();
    const currentDate = new Date(today.getFullYear(), today.getMonth(), today.getDate());
    const days = [];
    const seen = new Set();
    for (const week of weeks) for (const day of week.days || []) {
      const parsed = this._parseDate(day.date, today.getFullYear());
      if (!parsed || parsed < currentDate) continue;
      const key = `${week.week}-${day.date}`;
      if (seen.has(key)) continue;
      seen.add(key);
      days.push({ ...day, week: week.week, weekType: week.week_type, entries: visibleEntries.filter(e => e.week === week.week && e.date === day.date) });
    }

    const classBlock = showClassFilter ? `<div class="section"><div class="section-title">Klassen</div>${fixed ? `<div class="fixed">Fest konfiguriert: <strong>${configuredClasses.map(this._escape).join(', ')}</strong></div>` : ''}<div class="classes"><button class="${selected.size === 0 ? 'selected' : ''}" data-all>Alle Klassen</button>${filterClasses.map(c => `<button class="${selected.has(c) ? 'selected' : ''}" data-class="${this._escape(c)}">${this._escape(c)}</button>`).join('')}</div></div>` : '';

    this.shadowRoot.innerHTML = `<style>
      :host{display:block}ha-card{overflow:hidden}.header{padding:18px 20px 12px}.title{font-size:1.4rem;font-weight:600}.subtitle{margin-top:5px;color:var(--secondary-text-color);font-size:.9rem}.section{padding:0 16px 14px}.section-title{font-size:.78rem;text-transform:uppercase;letter-spacing:.08em;color:var(--secondary-text-color);margin:10px 4px 8px}.classes{display:flex;flex-wrap:wrap;gap:7px}button{border:1px solid var(--divider-color);background:var(--card-background-color);color:var(--primary-text-color);border-radius:18px;padding:7px 12px;cursor:pointer;font:inherit;font-size:.88rem}button.selected{background:var(--primary-color);color:var(--text-primary-color);border-color:var(--primary-color)}.fixed{color:var(--secondary-text-color);font-size:.82rem;margin:4px}.day{margin:10px 0 16px;border:1px solid var(--divider-color);border-radius:12px;overflow:hidden}.day-header{padding:11px 13px;background:var(--secondary-background-color);display:flex;align-items:center;gap:10px}.day-heading{display:flex;align-items:center;gap:9px;flex-wrap:wrap}.day-name,.day-date{font-weight:700}.week-type{font-weight:800;margin-left:3px}.week-a{color:var(--primary-color)}.week-b{color:var(--accent-color,var(--primary-color))}.news{margin:10px;padding:10px 12px;border-radius:9px;background:var(--secondary-background-color);border-left:4px solid var(--primary-color)}.news-title{font-weight:700;margin-bottom:4px}.news p{margin:3px 0}.table-wrap{overflow-x:auto}table{width:100%;border-collapse:collapse;font-size:.88rem}th{text-align:left;color:var(--secondary-text-color);font-weight:600;font-size:.75rem;padding:8px 10px;border-bottom:1px solid var(--divider-color);white-space:nowrap}td{padding:9px 10px;border-bottom:1px solid var(--divider-color);vertical-align:top}tr:last-child td{border-bottom:0}tr.art-entfall{background:rgba(244,67,54,.10)}tr.art-vertretung{background:rgba(33,150,243,.08)}tr.art-betreuung{background:rgba(76,175,80,.10)}tr.art-tausch{background:rgba(255,152,0,.11)}tr.art-raumänderung{background:rgba(156,39,176,.09)}.klasse{font-weight:700;white-space:nowrap}.lesson{white-space:nowrap;font-weight:700}.art{white-space:nowrap;font-weight:600}.empty{padding:18px;color:var(--secondary-text-color);text-align:center}@media(max-width:700px){th:nth-child(4),td:nth-child(4){display:none}th,td{padding:8px 7px}}
    </style><ha-card><div class="header"><div class="title">Vertretungsplan</div></div>${classBlock}<div class="section">${days.map(day => this._renderDay(day, singleFixedClass)).join('') || '<div class="empty">Keine Vertretungen für die ausgewählten Klassen vorhanden.</div>'}</div></ha-card>`;

    if (showClassFilter) {
      this.shadowRoot.querySelector('[data-all]')?.addEventListener('click', () => {
        this._selectedClasses = new Set();
        if (fixed) this._selectedClasses = new Set(configuredClasses);
        this._render();
      });
      this.shadowRoot.querySelectorAll('[data-class]').forEach(button => button.addEventListener('click', () => {
        const cls = button.dataset.class;
        if (selected.has(cls)) {
          selected.delete(cls);
          if (fixed && selected.size === 0) selected.add(cls);
        } else {
          selected.add(cls);
        }
        this._render();
      }));
    }
  }

  _renderDay(day, singleFixedClass) {
    const entries = day.entries || [];
    const news = (day.news || []).map(n => this._newsText(n)).map(String).map(n => n.trim()).filter(Boolean);
    const weekClass = String(day.weekType || '').toLowerCase().includes('b') ? 'week-b' : 'week-a';
    const classHeader = singleFixedClass ? '' : '<th>Klasse</th>';
    return `<div class="day"><div class="day-header"><div class="day-heading"><span class="day-name">${this._escape(day.weekday || '')}</span><span class="day-date">${this._escape(day.date || '')}</span><span class="week-type ${weekClass}">${this._escape(day.weekType || '')}</span></div></div>${news.length ? `<div class="news"><div class="news-title">Nachricht des Tages</div>${news.map(n => `<p>${this._escape(n)}</p>`).join('')}</div>` : ''}${entries.length ? `<div class="table-wrap"><table><thead><tr>${classHeader}<th>Stunde</th><th>Fach</th><th>Lehrer</th><th>Vertretung</th><th>Raum</th><th>Art</th></tr></thead><tbody>${entries.map(e => this._renderEntry(e, singleFixedClass)).join('')}</tbody></table></div>` : `<div class="empty">Keine Vertretungen</div>`}</div>`;
  }

  _renderEntry(e, singleFixedClass) {
    const art = this._label(e.art), cls = `art-${art.toLowerCase().replace(/[^a-zäöüß]+/g, '-')}`;
    const classCell = singleFixedClass ? '' : `<td class="klasse">${this._escape(e.klasse || '–')}</td>`;
    return `<tr class="${cls}">${classCell}<td class="lesson">${this._escape(e.stunde || '–')}</td><td>${this._escape(this._subject(e.fach))}</td><td>${this._escape(this._teacher(e.lehrer_original))}</td><td>${this._escape(this._teacher(e.vertreter))}</td><td>${this._escape(e.raum || '–')}</td><td class="art">${this._escape(art)}</td></tr>`;
  }
  _teacher(value){if(!value)return'–';const raw=String(value).trim(),key=raw.toUpperCase();return TEACHERS[key]?`${TEACHERS[key]} (${raw})`:raw}
  _subject(value){if(!value)return'–';const raw=String(value).trim(),key=raw.toUpperCase();return SUBJECTS[key]?`${SUBJECTS[key]} (${raw})`:raw}
  _label(value){if(!value)return'–';const raw=String(value).trim();return LABELS[raw]||raw}
  _newsText(value){
    if(Array.isArray(value)) return value.flat(Infinity).map(v=>this._newsText(v)).filter(Boolean).join(' · ');
    if(typeof value==='string') return value;
    if(value&&typeof value==='object') return value.text||value.news||value.message||value.content||Object.values(value).filter(Boolean).map(v=>this._newsText(v)).join(' · ');
    return String(value??'');
  }
  _splitClasses(value){if(!value)return[];return String(value).replace(/[()]/g,'').split(',').map(x=>x.trim()).filter(Boolean)}
  _classSort(a,b){const na=a.match(/^(\d+)/),nb=b.match(/^(\d+)/);if(na&&nb&&Number(na[1])!==Number(nb[1]))return Number(na[1])-Number(nb[1]);if(na&&!nb)return-1;if(!na&&nb)return 1;return a.localeCompare(b,'de',{numeric:true})}
  _parseDate(value,year){if(!value)return null;const m=String(value).match(/(\d{1,2})\.(\d{1,2})\.?/);return m?new Date(year,Number(m[2])-1,Number(m[1])):null}
  _escape(value){return String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
}

if(!customElements.get(CARD_NAME))customElements.define(CARD_NAME,KfgVertretungsplanCard);
if(!customElements.get('vertretungsplan-card'))customElements.define('vertretungsplan-card',KfgVertretungsplanCard);
