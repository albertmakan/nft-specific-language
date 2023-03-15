
def take_input(input_message, default = None):
  
  console_message = input_message
  if default is not None:
    console_message = f"{input_message} (Leave empty for '{default}')"

  while True:
    print(console_message, end=': ')
    user_input = input().strip()
    if user_input is not None and len(user_input) > 0:
      return user_input
    
    if default is not None:
      return default
