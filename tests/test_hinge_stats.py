from hp_class_action.hinge_issue.data_analyses.histo_claims import (chart_claim_hidden_claims,
                                                                    chart_claim_hidden_claims_as_percent)


def test_chart_percent():
    chart_claim_hidden_claims_as_percent(from_year=2017,
                                         show_chart=False)


def test_chart_raw():
    chart_claim_hidden_claims(from_year=2017,
                              show_chart=False)


if __name__ == '__main__':
    test_chart_raw()
    test_chart_percent()
