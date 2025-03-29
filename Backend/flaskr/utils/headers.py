

def check_headers(headers):
    # Prüfe, ob alle benötigten Spalten vorhanden sind
    expected_columns = ["Kunden-Nr.", "Kürzel", "Bereich", "Gruppe-Nr.", "Gruppen-Name 1", "Gruppen-Name 2"]
    missing_columns = [col for col in expected_columns if col not in headers]
    return missing_columns
