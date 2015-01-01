import requests
import datetime
import json

"""
EXAMPLE DATA 
=======================
{'addr_state': 'ca',
 'annual_inc': 22000.0,
 'collections_12_mths_ex_med': 0.0,
 'credit_history_age_months': 43,
 'delinq_2yrs': 0,
 'dti': 24.71,
 'earliest_cr_line': 'jun-2004',
 'emp_length': '6 years',
 'fico_range_high': 1,
 'fico_range_low': 1,
 'funded_amnt': 4350,
 'funded_amnt_inv': 1129.09,
 'grade': 'c',
 'home_ownership': 'rent',
 'initial_list_status': 'f',
 'inq_last_6mths': 1,
 'installment': 143.53,
 'int_rate': 0.1154,
 'is_inc_v': 'not verified',
 'last_fico_range_high': 739,
 'last_fico_range_low': 735,
 'last_pymnt_amnt': 10.36,
 'loan_amnt': 4350,
 'mths_since_last_delinq': 0,
 'mths_since_last_major_derog': nan,
 'mths_since_last_record': 0,
 'open_acc': 10,
 'percentage_misspelled_words_in_desc': 0.0,
 'policy_code': 1,
 'pub_rec': 0.0,
 'purpose': 'debt_consolidation',
 'revol_bal': 5967,
 'revol_util': '25.5%',
 'sub_grade': 'c5',
 'term': '36 months',
 'total_acc': 10,
 'zip_code': '917xx'}
"""

class LoanEntry:
	def __init__(self, data_raw, data_standardized):
		self.data_raw = data_raw
		self.data_standardized = data_standardized

def getDatetimeFromTimestamp(timestamp):
	yyyymmdd = timestamp.split("T")[0]
	return datetime.datetime.strptime(yyyymmdd, "%Y-%m-%d").date()
	
def getCreditHistoryAgeMonths(earliestCrLine):
	earliestCreditDate = getDatetimeFromTimestamp(earliestCrLine)
	today = datetime.date.today()	
	timeDelta = today - earliestCreditDate
        creditHistoryDays = timeDelta.days
        return creditHistoryDays / 30

def convertEmpLengthCategorical(empLength):
	print("ER")

def transform_api_response_to_standard_format(raw_data):
	standardized = {}
	standardized['addr_state'] = str(raw_data['addrState'].strip().lower())
	standardized['annual_inc'] = float(raw_data['annualInc'])
	standardized['collections_12_mths_ex_med'] = float(raw_data['collections12MthsExMed'])
	standardized['credit_history_age_months'] = getCreditHistoryAgeMonths(raw_data['earliestCrLine'])
	standardized['delinq_2yrs'] = int(raw_data['delinq2Yrs'])
	standardized['dti'] = float(raw_data['dti'])
	standardized['emp_length'] = raw_data['empLength']

def get_loans_with_auth_key(auth):
	headers = {'Authorization': auth}
	r = requests.get("https://api.lendingclub.com/api/investor/v1/loans/listing?showAll=true", headers=headers)
	data = json.loads(r.text)
	return data['loans']

