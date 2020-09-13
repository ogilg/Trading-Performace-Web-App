def get_win_rate(positive_stocks, total_stocks):
  """Return the overall portfolio win rate"""
  win_rate = round((positive_stocks / total_stocks)*100)
  print(f"Your overall portfolio win rate is {win_rate}%")

# Test 1:
win_rate1 = get_win_rate(45,66)
# Test 2:
win_rate2 = get_win_rate(total_stocks= 66, positive_stocks= 45)

