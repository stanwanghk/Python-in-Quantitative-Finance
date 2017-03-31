import read_data as rd



def sign_value(x):
    if x.price > x.mid_quote:
        return 1
    elif x.price < x.mid_quote:
        return -1
    else:
        return 0


def Lee_Ready(combine):
    # combine = rd.combine_all()
    combine = combine.assign(mid_quote=lambda x: (x.AskPrice1 + x.BidPrice1) / 2)
    combine.ix[combine.price > combine.mid_quote, 'sign'] = 'B'
    combine.ix[combine.price == combine.mid_quote, 'sign'] = 'M'
    combine.ix[combine.price < combine.mid_quote, 'sign'] = 'S'
    combine.ix[combine.sign == combine.BS, 'lee_ready'] = 1
    combine.ix[combine.sign != combine.BS, 'lee_ready'] = 0
    right_rate = combine.lee_ready.mean()
    count = combine['lee_ready'].value_counts()
    return right_rate,count
