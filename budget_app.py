class Category:

  def __init__(self,name) -> None:
    self.name = name
    self.ledger = []
  
  def __str__(self) -> str:
    
    title = self.name.center(30,'*')

    def line(dict):
      lenDesc = len(dict['description'])
      amountFormat = str('{:.2f}'.format(dict['amount']))
      eachLine = dict['description']
     
      lenAmount = len(amountFormat)

      if lenAmount > 7:
        amountFormat = amountFormat[:7]
      if lenDesc > 23:
        eachLine = dict['description'][:23]
        lenDesc = 23
      
      return eachLine + amountFormat.rjust(30-lenDesc)
    
    totalAmount = '{:.2f}'.format(self.get_balance())
    
    return title + '\n' + '\n'.join(map(line,self.ledger)) + '\n' + f'Total: {totalAmount}'

  def deposit(self,amount,description=''):
    content = {'amount' : amount, 'description' : description}
    self.ledger.append(content)
  
  def get_balance(self):
    currentBalance = 0
    for i in range(len(self.ledger)):
      currentBalance += self.ledger[i]['amount']
    return currentBalance
  
  def check_funds(self,amount):
    if self.get_balance() < amount:
      return False
    else:
      return True
  
  def withdraw(self,amount,description=''):
    if self.check_funds(amount) == True:
      content = {'amount' : -amount, 'description' : description}
      self.ledger.append(content)
      return True
    else:
      return False

  def transfer(self,amount,type):
    if self.withdraw(amount, f'Transfer to {type.name}') == False:
      return False
    else:
      type.deposit(amount, f'Transfer from {self.name}')
    return True


def create_spend_chart(categories):
  allSpent = []

  for eachCategory in categories:
    spent = 0
    for i in eachCategory.ledger:
      if i['amount'] < 0:
        spent += i['amount']
    allSpent.append(spent)

  total = sum(allSpent)

  percentage = []
  for eachSpent in allSpent:
    percen = (eachSpent / total) * 100
    percentage.append(int(percen)//10)

  allBubble = {

  }

  for x in range(len(categories)):
      allBubble[categories[x].name] = []
      for n in range(percentage[x]+1):
        allBubble[categories[x].name].append('o')
      for o in range(max(percentage)-percentage[x]):
        allBubble[categories[x].name].append(' ')
  
  eachLine = ''

  for line in range(10,-1,-1):
    eachLine += f'{line*10}| '.rjust(len('100| '))
    
    for bbl in range(len(allBubble)):
      getList = allBubble[list(allBubble.keys())[bbl]]
      if line < len(getList):
        eachLine += getList[line]
        eachLine += '  '
      else:
        eachLine += '   '
    eachLine = eachLine
    eachLine += '\n'
    
  eachLine += '-'.rjust(len('100| ')) + '-'*3*len(allBubble) + '\n'

  lenNames = []
  for name in list(allBubble.keys()):
    lenNames.append(len(name))

  categoryNames = []
  for name in list(allBubble.keys()):
    words = []
    for word in range(max(lenNames)):
      if word < len(name):
        words.append(name[word])
      else:
        words.append(' ')
    categoryNames.append(words)

  for title in range(max(lenNames)):
    eachLine += ' '*5
    for getWords in categoryNames:
      eachLine += getWords[title]
      eachLine += '  '
    if title != max(lenNames)-1:
      eachLine += '\n'

  return 'Percentage spent by category\n' + eachLine


food = Category('Food')
food.deposit(1000.99,'deposit')
food.withdraw(500.87,'coffe')
# food.transfer(20,'Clothing')
laundry = Category('Laundry')
laundry.deposit(4000)
laundry.withdraw(300)
food.transfer(100,laundry)
cinema = Category('Cinema')
cinema.deposit(5000)
cinema.withdraw(1400)
cinema.transfer(100,food)
entertainment = Category('Entertainment')
entertainment.deposit(400)
cinema.transfer(50,entertainment)
# print(entertainment)
# print(food)
# print(laundry)
print(cinema)
print(create_spend_chart([food,laundry,cinema,entertainment]))
