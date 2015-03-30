"""
module producing list of items to pack
"""
from __future__ import division
import argparse
import pandas as pd
import itertools


def load_inv():
    path = 'inventory.csv'
    df = pd.read_csv(path)
    df['number'].fillna(1, inplace=True)  # if numbers are not filled assume 1
    return df


def produce_full_inventory(df):
    """
    result is unaggregated dataframe
    this approach uses multiplying rows and then flattenning the lists
    other could be just appending modified list directly,
    but then would likely need to have nested loop
    """
    full_list = []
    for i, row in df.iterrows():
        full_list.append([list(row)] * int(row.number))
    chain = itertools.chain.from_iterable(full_list)  # flatenning the list
    df_new = pd.DataFrame(list(chain), columns=df.columns)
    df_new['number'] = 1  # fill number with 1s now
    return df_new


def get_items_days(df, days):
    # add ordering by preference or importance
    df['duration_cumsum'] = df.groupby('meta_category')['duration'].apply(lambda x: x.cumsum())
    df['duration_cumsum'].fillna(0, inplace='True')
    return df.query('duration_cumsum <= @days')


def get_items(inv, days=2, baggage=1, options=[]):
    # inv = inv[inv.importance == 0]
    inv['number_needed'] = days / inv['duration']
    inv['number_needed'] = inv['number_needed'].fillna(1).round()  # xx should always round to nearest top integer
    inv['number_taken'] = inv[['number', 'number_needed']].fillna(1).apply(min, axis=1)
    inv['lists'] = inv.apply(lambda x: [x['item']] * int(x['number_taken']), axis=1)
    items = inv['lists'].sum()
    return list(items)


def get_items_volume(df, volume):
    df['volume_cumsum'] = df.sort('importance')['volume'].cumsum()
    return df.query('volume_cumsum <= @volume')


def choose_and_sort_items(inv):
    inv = inv.sort(['tier'])
    return inv[['items', 'volume']].iterrows()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pack Command Line')
    parser.add_argument('-d', default=20, type=int, dest='days')
    parser.add_argument('-v', default=20000, type=int, dest='volume')
    args = parser.parse_args()

    inv = load_inv()
    inv = produce_full_inventory(inv)
    pack = get_items_days(inv, args.days)
    pack = get_items_volume(pack, args.volume)
    pack = pack.sort(['meta_category', 'importance'])
    print pack[['meta_category', 'description']]
