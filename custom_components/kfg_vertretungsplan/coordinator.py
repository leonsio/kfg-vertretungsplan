from __future__ import annotations

from datetime import date, datetime, timedelta
import logging
import re
from typing import Any

from aiohttp import ClientError
from bs4 import BeautifulSoup
from bs4.dammit import UnicodeDammit
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
WEEKDAYS = {"Montag": 1, "Dienstag": 2, "Mittwoch": 3, "Donnerstag": 4, "Freitag": 5, "Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5}
KOLLEGIUM_URL = "https://www.kaiserin-friedrich.de/schule/kollegium/"
KOLLEGIUM_UPDATE_INTERVAL = timedelta(hours=24)


class KFGCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Fetch and parse the school-wide Untis substitution plan."""

    def __init__(self, hass, base_url: str, scan_interval: int) -> None:
        self.base_url = base_url.rstrip("/")
        self._colleagues: dict[str, str] = {}
        self._colleagues_updated: datetime | None = None
        super().__init__(hass, logger=_LOGGER, name=DOMAIN, update_interval=timedelta(seconds=scan_interval))

    async def _async_update_data(self) -> dict[str, Any]:
        today = date.today()
        current_week = today.isocalendar().week
        next_week = (today + timedelta(days=7)).isocalendar().week
        weeks = [parsed for week in (current_week, next_week) if (parsed := await self._fetch_week(week)) is not None]
        if not weeks:
            raise UpdateFailed("Kein Vertretungsplan konnte geladen werden.")

        if self._colleagues_updated is None or datetime.now().astimezone() - self._colleagues_updated >= KOLLEGIUM_UPDATE_INTERVAL:
            await self._update_colleagues()

        days = []
        for week_data in weeks:
            for day in week_data["days"]:
                iso_date = self._date_for_weekday(today, week_data["week"], day["weekday_number"])
                if iso_date is None or iso_date < today:
                    continue
                item = dict(day)
                item.update(iso_date=iso_date.isoformat(), week=week_data["week"], week_type=week_data.get("week_type", ""))
                days.append(item)
        days.sort(key=lambda item: item["iso_date"])
        classes = sorted({entry["klasse"].strip() for day in days for entry in day["entries"] if entry.get("klasse", "").strip()})
        _LOGGER.debug("Parsed KFG plan: weeks=%s days=%s entries=%s classes=%s", [w["week"] for w in weeks], len(days), sum(len(d["entries"]) for d in days), classes)
        return {
            "generated": datetime.now().astimezone().isoformat(),
            "today": today.isoformat(),
            "current_week": current_week,
            "next_week": next_week,
            "next_week_available": any(w["week"] == next_week for w in weeks),
            "classes": classes,
            "days": days,
            "weeks": weeks,
            "colleagues": self._colleagues,
            "colleagues_updated": self._colleagues_updated.isoformat() if self._colleagues_updated else None,
        }

    async def _update_colleagues(self) -> None:
        """Refresh the abbreviation -> teacher-name mapping once per day."""
        session = async_get_clientsession(self.hass)
        try:
            async with session.get(KOLLEGIUM_URL, timeout=20, headers={"User-Agent": "HomeAssistant-KFG-Vertretungsplan/1.0"}) as response:
                if response.status != 200:
                    _LOGGER.warning("KFG Kollegium returned HTTP %s", response.status)
                    return
                raw_body = await response.read()
        except (ClientError, TimeoutError) as err:
            _LOGGER.warning("Unable to fetch KFG Kollegium: %s", err)
            return

        body = self._decode_html(raw_body)
        soup = BeautifulSoup(body, "html.parser")
        colleagues: dict[str, str] = {}
        for table in soup.find_all("table"):
            for row in table.find_all("tr"):
                cells = row.find_all(["td", "th"])
                if len(cells) < 2:
                    continue
                abbreviation = cells[0].get_text(" ", strip=True).upper()
                name = cells[1].get_text(" ", strip=True)
                if re.fullmatch(r"[A-ZÄÖÜẞ]{1,4}", abbreviation) and name and name.lower() not in {"lehrer und lehrerinnen", "lehrer", "lehrerin"}:
                    colleagues[abbreviation] = name

        if not colleagues:
            _LOGGER.warning("KFG Kollegium page contained no teacher mappings")
            return

        self._colleagues = dict(sorted(colleagues.items()))
        self._colleagues_updated = datetime.now().astimezone()
        _LOGGER.info("Updated KFG Kollegium: %d teacher mappings", len(self._colleagues))

    @staticmethod
    def _date_for_weekday(today: date, week: int, weekday: int) -> date | None:
        for year in (today.year - 1, today.year, today.year + 1):
            try:
                candidate = date.fromisocalendar(year, week, weekday)
            except ValueError:
                continue
            if abs((candidate - today).days) <= 370:
                return candidate
        return None

    async def _fetch_week(self, week: int) -> dict[str, Any] | None:
        url = f"{self.base_url}/{week}/w/w00000.htm"
        session = async_get_clientsession(self.hass)
        try:
            async with session.get(url, timeout=20, headers={"User-Agent": "HomeAssistant-KFG-Vertretungsplan/1.0"}) as response:
                if response.status != 200:
                    _LOGGER.debug("Untis week %s returned HTTP %s", week, response.status)
                    return None
                raw_body = await response.read()
        except (ClientError, TimeoutError) as err:
            _LOGGER.warning("Unable to fetch %s: %s", url, err)
            return None

        body = self._decode_html(raw_body)
        soup = BeautifulSoup(body, "html.parser")
        title = soup.title.get_text(" ", strip=True) if soup.title else ""
        if "Untis" not in title:
            _LOGGER.warning("%s does not look like an Untis page", url)
            return None
        week_match = re.search(r"Woche\s+([AB])", soup.get_text(" ", strip=True), re.IGNORECASE)
        anchors = soup.select('a[name="1"], a[name="2"], a[name="3"], a[name="4"], a[name="5"]')
        days = []
        for anchor in anchors:
            number = int(anchor.get("name"))
            header_text = self._day_header_text(anchor)
            match = re.search(r"(\d{1,2}\.\d{1,2}\.)\s*([A-Za-zÄÖÜäöüß]+)", header_text)
            weekday = match.group(2) if match else ""
            weekday_number = WEEKDAYS.get(weekday, number)
            table = anchor.find_next("table", class_="subst")
            entries = []
            status = None
            if table:
                for row in table.find_all("tr"):
                    cells = row.find_all(["td", "th"])
                    values = [cell.get_text(" ", strip=True) for cell in cells]
                    if not values:
                        continue
                    if len(values) == 1:
                        status = values[0]
                    elif len(values) >= 11 and values[0].strip().lower() not in {"klasse(n)", "klasse"}:
                        entries.append(self._entry(cells[:11]))
            news = self._extract_news(anchor)
            _LOGGER.debug("Untis week %s day %s %s: entries=%d news=%d status=%s", week, number, match.group(1) if match else "?", len(entries), len(news), status)
            days.append({"weekday_number": weekday_number, "weekday": weekday, "date": match.group(1) if match else "", "news": news, "entries": entries, "status": status})
        return {"week": week, "week_type": f"Woche {week_match.group(1).upper()}" if week_match else "", "title": title, "url": url, "days": days}

    @staticmethod
    def _decode_html(raw_body: bytes) -> str:
        """Decode Untis HTML, including legacy German encodings used by the school site."""
        dammit = UnicodeDammit(raw_body, is_html=True)
        if dammit.unicode_markup:
            return dammit.unicode_markup

        for encoding in ("cp1252", "iso-8859-1", "utf-8"):
            try:
                return raw_body.decode(encoding)
            except UnicodeDecodeError:
                continue
        return raw_body.decode("utf-8", errors="replace")

    @staticmethod
    def _day_header_text(anchor) -> str:
        parent = anchor.parent
        if parent:
            text = parent.get_text(" ", strip=True)
            if re.search(r"\d{1,2}\.\d{1,2}\.\s*[A-Za-zÄÖÜäöüß]+", text):
                return text
        parts = []
        node = anchor
        for _ in range(12):
            node = node.next_sibling
            if node is None:
                break
            text = node.get_text(" ", strip=True) if hasattr(node, "get_text") else str(node).strip()
            if text:
                parts.append(text)
            if re.search(r"\d{1,2}\.\d{1,2}\.\s*[A-Za-zÄÖÜäöüß]+", " ".join(parts)):
                break
        return " ".join(parts)

    @staticmethod
    def _extract_news(anchor) -> list[list[str]]:
        """Extract news only from the current day section."""
        next_anchor = anchor.find_next("a", attrs={"name": re.compile(r"^[1-5]$")})
        heading = None

        for node in anchor.find_all_next():
            if next_anchor is not None and node is next_anchor:
                break
            if not getattr(node, "name", None):
                continue
            text = node.get_text(" ", strip=True)
            if re.fullmatch(r"Nachrichten\s+(?:zum\s+)?Tag", text, re.IGNORECASE):
                heading = node
                break

        if heading is None:
            return []

        table = heading.find_parent("table")
        if table is None or "subst" in table.get("class", []):
            return []

        rows: list[list[str]] = []
        for row in table.find_all("tr"):
            cells = [cell.get_text(" ", strip=True) for cell in row.find_all(["td", "th"])]
            cells = [cell for cell in cells if cell]
            if not cells:
                continue
            if len(cells) == 1 and re.fullmatch(r"Nachrichten\s+(?:zum\s+)?Tag", cells[0], re.IGNORECASE):
                continue
            if cells[0].strip().lower() in {"klasse(n)", "klasse"}:
                return []
            rows.append(cells)

        return rows

    @staticmethod
    def _entry(cells) -> dict[str, Any]:
        values = [cell.get_text(" ", strip=True) for cell in cells]
        strike = {}
        for index, key in ((3, "vertreter"), (4, "fach"), (5, "fach_original"), (7, "lehrer_original"), (8, "lehrer_nach"), (9, "art")):
            struck = [node.get_text(" ", strip=True) for node in cells[index].find_all("strike")]
            if struck:
                strike[key] = " ".join(struck)
        return {"klasse": values[0], "datum": values[1], "stunde": values[2], "vertreter": values[3], "fach": values[4], "fach_original": values[5], "raum": values[6], "lehrer_original": values[7], "lehrer_nach": values[8], "art": values[9], "text": values[10], "strike": strike}
