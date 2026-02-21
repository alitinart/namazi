import math
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
from timezonefinder import TimezoneFinder


# --- Calculation Methods ---
CALCULATION_METHODS = {
    "MWL":       {"fajr": 18.0, "isha": 17.0},   # Muslim World League
    "ISNA":      {"fajr": 15.0, "isha": 15.0},   # Islamic Society of North America
    "Egypt":     {"fajr": 19.5, "isha": 17.5},   # Egyptian General Authority
    "Makkah":    {"fajr": 18.5, "isha": "90"},    # Umm al-Qura (Isha = 90 min after Maghrib)
    "Karachi":   {"fajr": 18.0, "isha": 18.0},   # University of Islamic Sciences, Karachi
    "Tehran":    {"fajr": 17.7, "isha": 14.0},   # Institute of Geophysics, Tehran
    "Jafari":    {"fajr": 16.0, "isha": 14.0},   # Shia Ithna Ashari
}

ASR_METHODS = {
    "Standard": 1,   # Shafi'i, Maliki, Hanbali (shadow = 1x object height)
    "Hanafi":   2,   # Hanafi (shadow = 2x object height)
}


def _julian_date(year, month, day):
    """Calculate Julian Date."""
    if month <= 2:
        year -= 1
        month += 12
    A = math.floor(year / 100)
    B = 2 - A + math.floor(A / 4)
    return math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + B - 1524.5


def _sun_position(jd):
    """Calculate sun declination and equation of time for a given Julian Date."""
    D = jd - 2451545.0  # Days since J2000.0

    # Mean anomaly, mean longitude (degrees)
    g = math.radians((357.529 + 0.98560028 * D) % 360)
    q = (280.459 + 0.98564736 * D) % 360
    L = math.radians((q + 1.915 * math.sin(g) + 0.020 * math.sin(2 * g)) % 360)

    # Obliquity of the ecliptic
    e = math.radians(23.439 - 0.00000036 * D)

    # Right ascension (hours)
    RA = math.degrees(math.atan2(math.cos(e) * math.sin(L), math.cos(L))) / 15
    RA = RA % 24

    # Declination (radians)
    decl = math.asin(math.sin(e) * math.sin(L))

    # Equation of time (hours)
    EqT = (q / 15) - RA

    return decl, EqT


def _hour_angle(target_altitude_deg, latitude_rad, declination_rad):
    """
    Compute the hour angle (degrees) for a body at a given altitude.
    Returns None if the sun never reaches that altitude (circumpolar / polar night).
    """
    cos_t = (
        math.sin(math.radians(target_altitude_deg))
        - math.sin(latitude_rad) * math.sin(declination_rad)
    ) / (math.cos(latitude_rad) * math.cos(declination_rad))

    if cos_t < -1 or cos_t > 1:
        return None
    return math.degrees(math.acos(cos_t))


def _asr_altitude(shadow_factor, latitude_rad, declination_rad):
    """Compute the solar altitude angle (degrees) for Asr prayer."""
    target = math.degrees(
        math.atan(1 / (shadow_factor + math.tan(abs(latitude_rad - declination_rad))))
    )
    return target


def _decimal_hours_to_time(decimal_hours, tz, base_date):
    """Convert decimal hours (UTC) to a timezone-aware datetime."""
    total_seconds = int(round(decimal_hours * 3600))
    dt_utc = datetime(base_date.year, base_date.month, base_date.day,
                      tzinfo=ZoneInfo("UTC")) + timedelta(seconds=total_seconds)
    return dt_utc.astimezone(tz)


def get_prayers(
    latitude,
    longitude,
    prayer_date=None,
    method="MWL",
    asr_method="Standard",
):
    """
    Calculate Islamic prayer times for any location and date.

    Parameters
    ----------
    latitude     : float  – geographic latitude  (negative = south)
    longitude    : float  – geographic longitude (negative = west)
    prayer_date  : date   – target date (defaults to today)
    method       : str    – calculation method key from CALCULATION_METHODS
    asr_method   : str    – "Standard" (Shafi'i/Maliki/Hanbali) or "Hanafi"

    Returns
    -------
    dict with keys: Fajr, Sunrise, Dhuhr, Asr, Maghrib, Isha
    Values are timezone-aware datetime objects.
    """
    if prayer_date is None:
        prayer_date = date.today()
    elif isinstance(prayer_date, str):
        prayer_date = date.fromisoformat(prayer_date)

    if method not in CALCULATION_METHODS:
        raise ValueError(f"Unknown method '{method}'. Choose from: {list(CALCULATION_METHODS)}")

    # --- Timezone detection ---
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lat=latitude, lng=longitude)
    if tz_name is None:
        raise ValueError("Could not determine timezone for this location.")
    tz = ZoneInfo(tz_name)
    dt_local = datetime(prayer_date.year, prayer_date.month, prayer_date.day, tzinfo=tz)
    utc_offset = dt_local.utcoffset().total_seconds() / 3600

    # --- Julian date & sun position ---
    jd = _julian_date(prayer_date.year, prayer_date.month, prayer_date.day)
    decl, EqT = _sun_position(jd)
    lat_rad = math.radians(latitude)

    # --- Solar noon (Dhuhr) in UTC decimal hours ---
    dhuhr_utc = 12 - EqT - (longitude / 15) + (0 if utc_offset == 0 else 0)
    # longitude/15 converts to hours; timezone shift cancels because we stay in UTC
    dhuhr_utc = 12 - EqT - (longitude / 15)

    params = CALCULATION_METHODS[method]
    shadow_factor = ASR_METHODS[asr_method]

    # --- Fajr ---
    fajr_angle = params["fajr"]
    t_fajr = _hour_angle(-fajr_angle, lat_rad, decl)
    fajr_utc = dhuhr_utc - (t_fajr / 15) if t_fajr is not None else None

    # --- Sunrise ---
    t_sunrise = _hour_angle(-0.8333, lat_rad, decl)  # standard refraction/disc correction
    sunrise_utc = dhuhr_utc - (t_sunrise / 15) if t_sunrise is not None else None

    # --- Asr ---
    asr_alt = _asr_altitude(shadow_factor, lat_rad, decl)
    t_asr = _hour_angle(asr_alt, lat_rad, decl)
    asr_utc = dhuhr_utc + (t_asr / 15) if t_asr is not None else None

    # --- Maghrib (Sunset) ---
    maghrib_utc = dhuhr_utc + (t_sunrise / 15) if t_sunrise is not None else None

    # --- Isha ---
    isha_param = params["isha"]
    if isinstance(isha_param, str):
        # Fixed minutes after Maghrib (e.g. Makkah method = 90 min)
        isha_utc = maghrib_utc + int(isha_param) / 60 if maghrib_utc is not None else None
    else:
        t_isha = _hour_angle(-isha_param, lat_rad, decl)
        isha_utc = dhuhr_utc + (t_isha / 15) if t_isha is not None else None

    # --- Convert all to datetime objects ---
    def to_dt(utc_hours):
        if utc_hours is None:
            return None
        return _decimal_hours_to_time(utc_hours, tz, prayer_date)

    return [
        {"name": "Fajr", "time": to_dt(fajr_utc)},
        {"name": "Sunrise", "time": to_dt(sunrise_utc)},
        {"name": "Dhuhr", "time": to_dt(dhuhr_utc)},
        {"name": "Asr", "time": to_dt(asr_utc)},
        {"name": "Maghrib", "time": to_dt(maghrib_utc)},
        {"name": "Isha", "time": to_dt(isha_utc)}
    ]