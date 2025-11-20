from analyzer.impact_engine import analyze_impact

def test_impact_on_known_file():
    res = analyze_impact(['utils/crypto.py'])
    assert res['overall_risk'] > 0
    assert any(m['module'] == 'service:billing' or m['module'] == 'lib:utils' for m in res['impacted_modules'])
