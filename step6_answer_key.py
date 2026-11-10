"""Step 6 answer key: the exact answers, computed with code (not predicted text).

Run:  python step6_answer_key.py
"""
from decimal import Decimal, ROUND_HALF_UP
import math

# --- Retailer profit -------------------------------------------------------
bought = 1247
unit_cost = Decimal("38.75")
list_price = Decimal("64.90")
discount = Decimal("0.12")
unsold_price = Decimal("21.40")
shipping_per_unit = Decimal("2.85")
fixed_costs = Decimal("6730")

sold = math.floor(Decimal("0.83") * bought)          # rounded down to whole units
returned = math.floor(Decimal("0.07") * sold)        # rounded down; full refund, not resold
kept = sold - returned
unsold = bought - sold                               # returned units are NOT resold
sale_price = list_price * (1 - discount)

revenue_kept = kept * sale_price
revenue_unsold = unsold * unsold_price
purchase_cost = bought * unit_cost
shipping = bought * shipping_per_unit
profit = revenue_kept + revenue_unsold - purchase_cost - shipping - fixed_costs

print("RETAILER PROFIT")
print(f"  units sold (83%, rounded down)   : {sold}")
print(f"  units returned (7%, rounded down): {returned}")
print(f"  units kept by customers          : {kept}")
print(f"  units unsold                     : {unsold}")
print(f"  discounted price                 : EUR {sale_price}")
print(f"  revenue from kept units          : EUR {revenue_kept}")
print(f"  revenue from unsold units        : EUR {revenue_unsold}")
print(f"  purchase cost                    : EUR {purchase_cost}")
print(f"  shipping                         : EUR {shipping}")
print(f"  fixed costs                      : EUR {fixed_costs}")
print(f"  FINAL PROFIT                     : EUR {profit.quantize(Decimal('0.01'), ROUND_HALF_UP)}")

# --- Small "tokenization" tasks --------------------------------------------
print("\nTOKENIZATION TASKS")
print(f"  larger of 9.11 and 9.9 : {max(9.11, 9.9)}")
print(f"  r's in 'strawberry'    : {'strawberry'.count('r')}")
word = "Ubiquitous"
print(f"  every 3rd char of '{word}' from the 1st: {word[::3]!r}  (positions 1, 4, 7, 10)")
