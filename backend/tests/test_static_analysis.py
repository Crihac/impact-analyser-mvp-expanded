from analyzer.static_analysis import parse_changed_files

def test_parse_simple_diff():
    diff = '+++ b/services/billing/charge.py\n--- a/services/billing/old.py\n'
    files = parse_changed_files(diff)
    assert 'services/billing/charge.py' in files
