"""Money: exact conversion to tiyn and formatting."""

# [readme]
from decimal import Decimal

from tungoai import MoneyError, TungoMoney, is_valid_bin_iin

print(TungoMoney.to_tiyn("45000.50"))  # 4500050
print(TungoMoney.to_tiyn(Decimal("1.005")))  # 101: half away from zero, no float error
print(TungoMoney.to_tiyn(1.005))  # 101: a float goes through its shortest decimal form
print(TungoMoney.format_tiyn(4_500_000))  # 45 000,00 ₸
print(TungoMoney.format_tiyn(-50, "USD"))  # -0,50 $

try:
    TungoMoney.to_tiyn("12,5")
except MoneyError as error:
    print(error)

print(is_valid_bin_iin("990140000017"))  # True
# [/readme]
