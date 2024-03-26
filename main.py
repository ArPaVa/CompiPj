import regex

re = regex.regex('hey+')

# print(re.nfa.powerset_construction())
print(re.match('heyyyyyyyyyyyyyyyyy'))
print(re.match('heyyyuyyyyyyyyyyyyy'))
print(re.match('heuyyyyyyyyyyyyyyyy'))

re = regex.regex('blue|red')

print(re.match('blue'))
print(re.match('red'))

re = regex.regex('He is a fine man you know!!( Or is he\\?)?')

print(re.match('He is a fine man you know!!'))
print(re.match('He is a fine man you know!! Or is he?'))

re = regex.regex('((pi+|pika+|pikachu)( *)?)+')

print(re.match('pika pika piii pikachu pi pikaaaaaaaaa pikachu pika pii'))

re = regex.regex('[a-zA-Z]+')

print(re.match('kajsdkajsdkajsnkjnKBJGVYACSYAVysGVAsgVYAgsvUAGVsUTA'))

re = regex.regex('[0-9]+')

print(re.match('123'))

re = regex.regex('\\**')

print(re.match('**************************'))
print(re.match(''))

re = regex.regex('listen carefully ([A-Z][a-zA-Z]*) (cough!? ?)* the secret code is ([a-zA-Z0-9\\*\\+=,.!\\?]+)')

print(re.match('listen carefully Natasha cough! cough cough! the secret code is l!ea$v,em.ea9384lone'))
