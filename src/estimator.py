
input_data = {
    "region": {
        "name": "Africa",
        "avgAge": 19.7,
        "avgDailyIncomeInUSD": 5,
        "avgDailyIncomePopulation": 0.71
    },
    "periodType": "days",
    "timeToElapse": 58,
    "reportedCases": 674,
    "population": 66622705,
    "totalHospitalBeds": 1380614
}

# leverage Python's power of first class functions and store
# functions to convert weeks and days into months as lambda function objects

# putting the functions in a dictionary will simulate the
# switch case that exists in other languages
days_convert = {
    # conversion of weeks to days. 7 days make a week
    'weeks': lambda weeks_number: weeks_number * 7,
    # conversion of months into days. 30 days make a month
    'months': lambda months_number: months_number * 30
}


def estimator(data):
    estimate =  _create_dictionary(data)
    return estimate


def _impact_func(multiplier, **data):
    stored_dict = dict()
    _data = data
    # currently_infected
    curr_inf = _data['reportedCases'] * multiplier
    actual_days = None

    # a try/except conditional clause in case a periodType unaccounted for is used
    try:
        if _data['periodType'] == 'days':
            actual_days = _data['timeToElapse']
        else:
            # else convert TimeToElapse key into days
            conversion_function = days_convert[_data.get('periodType')]
            actual_days = conversion_function(_data.get('timeToElapse'))
    except KeyError:
        raise Exception('periodType should either be in weeks or days or months')

    # infections by requested time
    infec_by_reqtime = curr_inf * (2 ** _factor(actual_days))

    # severe_cases_by_requested_time
    sev_case_time = _percentage_determinations(15, infec_by_reqtime)

    # hospitalBedsByRequestedTime
    available_beds = _percentage_determinations_retain_decimals(35, _data['totalHospitalBeds'])
    hosp_beds_by_reqtime = int(available_beds - sev_case_time)

    # cases for ICU BY RequestedTime
    cases_for_ICU_by_reqtime = _percentage_determinations(5, infec_by_reqtime)

    # cases for Venilators By RequestedTime
    cases_for_vent_by_reqtime = _percentage_determinations(2, infec_by_reqtime)

    # dollars in flight
    mul = _data['region']['avgDailyIncomeInUSD'] * _data['region']['avgDailyIncomePopulation']
     
    dollars_in_flight = int((infec_by_reqtime * mul/ actual_days))
 

    stored_dict['currentlyInfected'] = curr_inf
    stored_dict['infectionsByRequestedTime'] = infec_by_reqtime
    stored_dict['severeCasesByRequestedTime'] = sev_case_time
    stored_dict['hospitalBedsByRequestedTime'] = hosp_beds_by_reqtime
    stored_dict['casesForICUByRequestedTime'] = cases_for_ICU_by_reqtime
    stored_dict['casesForVentilatorsByRequestedTime'] = cases_for_vent_by_reqtime
    stored_dict['dollarsInFlight'] = dollars_in_flight

    return stored_dict


def _factor(num_days):
    factor = int(num_days / 3)
    return factor


def _percentage_determinations(percent, value):
    decimal = percent / 100
    result = int(decimal * value)
    return result

def _percentage_determinations_retain_decimals(percent, value):
    decimal = percent / 100
    result = decimal * value
    return result


def _create_dictionary(data):
  _data = data
  impact = _impact_func(10, **_data)
  severe_impact = _impact_func(50, **_data)
    
  estimate = {'data': data, 'impact': impact, 'severeImpact': severe_impact}

  return estimate


