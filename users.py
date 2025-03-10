user = {}

while True:
  ch = 'y'
  while ch != 'n':
    name = input("Enter Name or DIE: ")
    age = int(input("Enter Age: "))
    user[name] = age
    print("Do you want to add one more user (y/n)?")
    ch = input(">")
  print("Viewing Users:")
  for key, value in user.items():
    print(f"{key} : {value}")
  break
