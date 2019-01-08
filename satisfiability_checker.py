class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


def isLiteral(formula):
    if not (formula == 'p' or formula == 'q' or formula == 'r'):
        if not (formula == '-p' or formula == '-q' or formula == '-r'):
            return False
    return True


def exp(theory):
    for i in theory:
        if not isLiteral(i):
            return False
    return True


def C(theory):
    for i in theory:
        if ('-' + i) in theory:
            return True
    return False


def findBC(formula):
    if formula[0] == '-':
        return findBC(formula[1:]) + 1
    if formula[0] == '(':
        braces = -1
        for i in range(len(formula)):
            if formula[i] == '(':
                braces += 1
            if formula[i] == ')':
                braces -= 1
            if formula[i] == '>' or formula[i] == '^' or formula[i] == 'v':
                if braces == 0:
                    return i
    return 0


def getRule(formula):

    BC = formula[findBC(formula)]
    #print(" GS ", formula, BC)
    if formula[0] == '-' and formula[1] == '-':
        return 1
    if formula[0] == '-':
        if BC == '^':
            return 6
        if BC == 'v':
            return 2
        if BC == '>':
            return 3
    else:
        if BC == '^':
            return 4
        if BC == 'v':
            return 5
        if BC == '>':
            return 7
    print("ERR")


def appendParts(c, s):
    bc_index = findBC(c)
    i = 0
    while c[i] != '(':
        i += 1
    s.append(c[i+1:bc_index])
    s.append(c[bc_index+1:-1])


def parts(formula):
    rule = getRule(formula)
    if rule == 1:
        return [formula[2:]]
    res = []
    i = 0
    while formula[i] != '(':
        i += 1

    left = formula[i+1:findBC(formula)]
    right = formula[findBC(formula)+1:-1]

    if rule == 2:
        res.append('-' + left)
        res.append('-' + right)
    if rule == 3:
        res.append(left)
        res.append('-' + right)
    if rule == 4:
        res.append(left)
        res.append(right)
    if rule == 5:
        res.append(left)
        res.append(right)
    if rule == 6:
        res.append('-' + left)
        res.append('-' + right)
    if rule == 7:
        res.append('-' + left)
        res.append(right)
    return (res)


def part2(formula):
    return formula[findBC(formula)+1:-1]


def closed(formula):
    tab = Queue()
    tab.enqueue([formula])
    while tab.size() > 0:
        sigma = tab.dequeue()
        if exp(sigma) and not C(sigma):
            return("satisfiable")
        else:
            for nonLiteral in [elem for elem in sigma if not isLiteral(elem)]:
                # print(nonLiteral)
                if getRule(nonLiteral) < 5:
                    sigma = sigma + parts(nonLiteral)
                    sigma.remove(nonLiteral)
                    if not C(sigma) and sigma not in tab.items:
                        tab.enqueue(sigma)
                elif getRule(nonLiteral) > 4:
                    sigma1 = sigma + [parts(nonLiteral)[0]]
                    sigma1.remove(nonLiteral)
                    if not C(sigma1) and sigma1 not in tab.items:
                        tab.enqueue(sigma1)

                    sigma2 = sigma + [parts(nonLiteral)[1]]
                    sigma2.remove(nonLiteral)
                    if not C(sigma2) and sigma2 not in tab.items:
                        tab.enqueue(sigma2)
    return("not satisfiable")


print(closed("-(p>(q>p))"))
