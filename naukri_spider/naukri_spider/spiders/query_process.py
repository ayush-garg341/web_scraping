def process_query(query):
    new_query = ''
    count = 0
    for letter in query:
        if letter == '.' and count != 0 :
            new_query = new_query + '-dot-'
            count = count + 1

        elif letter == '.' and count == 0 :
            new_query = new_query + 'dot-'
            count = count + 1

        elif letter == ', ':
            new_query = new_query + '-'
            count = count + 1

        elif letter == ',':
            new_query = new_query + '-'
            count = count + 1

        elif letter == ' ':
            new_query = new_query + '-'
            count = count + 1

        elif letter == '&':
            new_query = new_query + '-'
            count = count + 1

        elif letter == ';':
            new_query = new_query + '-'
            count = count + 1

        elif letter == '/':
            new_query = new_query + '-'
            count = count + 1

        elif letter == '+':
            new_query = new_query + '-plus-'
            count = count + 1

        elif letter == '#':
            new_query = new_query + '-sharp-'
            count = count + 1

        elif letter == '(':
            new_query = new_query + '-'
            count = count + 1

        elif letter == ')':
            new_query = new_query + '-'
            count = count + 1

        else:
            new_query = new_query + letter
            count = count + 1

    transformed_query = [el for el in new_query.split('-') if el != '' and el != 'amp']

    return '-'.join(transformed_query)