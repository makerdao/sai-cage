import json

with open('cups.json') as f:
    allcups = json.load(f)

for cup in allcups:
    cup['ink'] = float(cup['ink'])
    cup['tab'] = float(cup['tab'])

cups = [cup for cup in allcups if cup['tab'] != 0 or cup['ink'] !=0]

def bite(cup, tag, axe):
    ink = cup['ink']
    tab = cup['tab']

    pro = ink * tag
    con = tab

    owe = con * axe
    cab = owe / tag

    if ink < cab: cab = ink

    cup['tab'] = 0
    cup['ink'] = ink - cab

    return cup


def diff(cup, air, tag, ice, pie, per):
    ink = cup['ink']
    tab = cup['tab']

    pie_ = pie - ice / (tag / per)

    d = (air * tag - ice * 1.2) * (air * tag - ice * 1.0)

    return tag * pie_ * (1.2 - 1.0) * (ink * ice - tab * air) / d


PER = 1.005681415025275361506073015
FIX = 0.001283667386376181294912313  # cage price, ETH per Sai
TAG = PER * 1 / FIX
AIR = sum(cup['ink'] for cup in cups)
ICE = sum(cup['tab'] for cup in cups)
PIE = AIR * PER
PIE_ = PIE - ICE / (TAG / PER)

print("ice:  ", ICE)
print("air:  ", AIR)
print("pie:  ", PIE)
print("pie': ", PIE_)
print("jam:  ", PIE - PIE_)

print("CDP    ETH diff  Owner")
for cup in cups:
    #  if diff(cup, AIR, TAG, ICE, PIE, PER) > 0 : continue
    print('{:>3}:  {:+09.4f}  {}'.format(int(cup["cup"], 16),
                                       diff(cup, AIR, TAG, ICE, PIE, PER),
                                       cup['lad']))

loss = -sum(diff(cup, AIR, TAG, ICE, PIE, PER) for cup in cups if diff(cup, AIR, TAG, ICE, PIE, PER) < 0)
gain =  sum(diff(cup, AIR, TAG, ICE, PIE, PER) for cup in cups if diff(cup, AIR, TAG, ICE, PIE, PER) > 0)

print("Total gain: {:05.2f}".format(gain))
print("Total loss: {:05.2f}".format(loss))
