### Tests cases input, partial order, relevance, etc.

import pytest
from aacbr.cases import Case, different_outcomes, inconsistent_pair #, mostConcise, attacks, newcaseattacks, 

def test_create_case():
  empty_case = Case('empty', set())
  print(empty_case)
  pass

def test_specificity():
  case1 = Case('1', {'a'})
  case2 = Case('2', {'a','b'})
  assert case2 >=  case1
  assert case2 > case1
  assert not case1 >= case2
  assert case1 >= case1
  assert not case1 > case1
  assert case2 >= case2

def test_different_outcomes():
  case1 = Case('1', {'a'}, outcome=0)
  case2 = Case('2', {'a','b'}, outcome=1)
  assert different_outcomes(case1, case2)
  assert different_outcomes(case2, case1)
  assert not different_outcomes(case1, case1)
  assert not different_outcomes(case2, case2)
  
# def test_conciseness():
#   case1 = Case('1', {'a'})
#   case2 = Case('2', {'a','b'})
#   case3 = Case('3', {'a','b','c'})
#   cases = [case1, case2, case3]
#   assert mostConcise(cases, case2, case1)
#   assert not mostConcise(cases, case3, case1)
#   assert not mostConcise(cases, case1, case2)

# def test_newcaseattack():
#   newcase = Case('new', {'a'})
#   case1 = Case('1', {'a'}, outcome=0)
#   case2 = Case('2', {'a','b'}, outcome=1)
#   default = Case('default', set(), outcome=0)
#   cases = (default, case1, case2, newcase)
#   assert newcaseattacks(newcase, case2)
#   assert not newcaseattacks(newcase, case1)
#   assert not newcaseattacks(newcase, default)
  
def test_inconsistent_pair():
  case1 = Case('1', {'a','b'}, outcome=0)
  case2 = Case('2', {'a','b'}, outcome=1)
  assert inconsistent_pair(case1, case2)

def test_order_notation():
  default = Case('default', set(), outcome=0)
  case1 = Case('1', {'a'}, outcome=1)
  case2 = Case('2', {'a','b'}, outcome=0)
  case2b = Case('2b', {'a','b'}, outcome=1)
  case3 = Case('3', {'c'})
  case4 = Case('4', {'a','b', 'c'}, outcome=1)
  cases = [default, case1, case2, case2b, case3, case4]
  assert all([default <= case for case in cases])
  assert all([case <= case for case in cases])
  assert not any([case < case for case in cases])
  assert case1 < case2
  assert not case1 < case3
  assert not case3 < case1
  assert all([case >= default for case in cases])
  assert all([case >= case for case in cases])
  assert case4 > case1 and case4 > case3
  assert case4 > case2 and case4 > case2b
  assert case2 >= case2b and case2b >= case2
  assert not case2 == case2b
  assert case2 != case2b

def test_data_partial_order_with_date():
  older = Case('older', {'a'}, data={'site_area': 10, 'date': (2024, 11, 5)}, outcome=1)
  newer = Case('newer', {'a'}, data={'site_area': 10, 'date': (2025, 11, 5)}, outcome=1)
  larger_newer = Case('larger_newer', {'a'}, data={'site_area': 20, 'date': (2025, 11, 6)}, outcome=1)
  earlier_year_larger_month = Case('earlier_year_larger_month', {'a'}, data={'site_area': 10, 'date': (2024, 12, 31)}, outcome=1)
  next_year = Case('next_year', {'a'}, data={'site_area': 10, 'date': (2025, 1, 1)}, outcome=1)

  assert older <= newer
  assert older <= larger_newer
  assert not newer <= older
  assert earlier_year_larger_month <= next_year
  assert older.data['date'] == (2024, 11, 5)

def test_positional_outcome_backwards_compatibility():
  case = Case('1', {'a'}, 0)
  assert case.outcome == 0
  assert case.data is None
  
def test_alternative_partial_order():  
  class OrderedPair:
    """Pair (a,b) where (a,b) are natural numbers.
    Partial order is defined by (a,b) <= (c,d) iff a<=c and b<=d."""
    
    def __init__(self, x, y):
      self.x: int = x
      self.y: int = y
      
    def __eq__(self, other):
      return self.x == other.x and self.y == other.y
    def __le__(self, other):
      return self.x <= other.x and self.y <= other.y
    def __lt__(self, other):
      """Not necessary for Cases, but recommended."""
      return self <= other and self != other
    def __hash__(self):
      return hash((self.x, self.y))

  default = Case('default', OrderedPair(0,0), outcome=0)
  case1 = Case('1', OrderedPair(1,0), outcome=1)
  case2 = Case('2', OrderedPair(0,1), outcome=0)
  case2b = Case('2b', OrderedPair(0,1), outcome=1)
  case3 = Case('3', OrderedPair(2,1), outcome=0)
  cb = (case1, case2, case2b, case3)
  assert default <= default
  assert not default < default
  for case in cb:
    assert default < case
    assert not case < default
  assert not case2 < case1
  assert not case2 > case1
  assert case2 >= case2b
  assert case2b >= case2
  assert not case2 > case2b
  assert not case2b > case2
  assert case3 > case1
  assert case2 < case3
  
def test_load_cases():
  # TODO: implement
  pass

def test_list_of_numbers_partial_order():
  # TODO: implement
  pass

def test_arbitrary_partial_order():
  # TODO: implement
  pass
