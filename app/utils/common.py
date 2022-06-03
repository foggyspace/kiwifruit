def parse_crontab(crontab):
    try:
        crontabs = crontab.split(" ")
    except Exception:
        return None
    if len(crontabs) == 5:
        return crontabs
    return crontabs
