import phonenumbers
from phonenumbers import carrier, geocoder, timezone

def phone_intel(phone_number, region="US"):
    report = {'number': phone_number}
    try:
        parsed = phonenumbers.parse(phone_number, region)
        report['valid'] = phonenumbers.is_valid_number(parsed)
        if report['valid']:
            report['type'] = 'Mobile' if phonenumbers.number_type(parsed) == 1 else 'Fixed-line'
            report['location'] = geocoder.description_for_number(parsed, "en")
            report['carrier'] = carrier.name_for_number(parsed, "en")
            report['timezones'] = ', '.join(timezone.time_zones_for_number(parsed))
        else:
            report['error'] = 'Invalid phone number'
    except Exception as e:
        report['error'] = str(e)
    return report
