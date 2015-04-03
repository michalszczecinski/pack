"""
module producing list of items to pack
"""
from __future__ import division

import itertools
import argparse
import math
import sys

import numpy as np
import pandas as pd

parser = argparse.ArgumentParser(description='Pack Command Line')
parser.add_argument('-d', default=2, type=int, dest='days')
parser.add_argument('-v', default=20000, type=int, dest='volume')
parser.add_argument('-w', default=20000, type=int, dest='weight')
parser.add_argument('-s', default=None, type=str, dest='save')
parser.add_argument('-o', default=[], metavar='N', type=str, dest='options', nargs='+',
                    help='a list of options to prioritize')


def load_inv():
    path = 'inventory.csv'
    df = pd.read_csv(path)
    df['number'].fillna(1, inplace=True)  # if numbers are not filled assume 1
    df['meta_category'].fillna('UNDEFINED', inplace=True)  # to make sure grouping and agg for rank works
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


def add_rank(df, options=[]):
    df['rank'] = 100  # add initial rank with high number, the lower the more important

    # incentivize for diversity of meta categories,
    # to avoid situation where there is 5 shirts and no trousers
    df['units_cumsum'] = df.groupby('meta_category')['number'].apply(lambda x: x.cumsum())
    df.loc[:, 'rank'] = df.units_cumsum * df.importance  # slice copy

    # pack necessary items and specifically requested options first
    df.loc[df.importance == 0, 'rank'] = 0
    df.loc[df['options'].isin(options), 'rank'] = 0
    return df


def get_items_volume(df, volume):
    df['volume_cumsum'] = df.sort('rank')['volume'].cumsum()
    return df.query('volume_cumsum <= @volume'), df.query('volume_cumsum > @volume')


# def get_items(inv, days=2, baggage=1, options=[]):
#     # inv = inv[inv.importance == 0]
#     inv['number_needed'] = days / inv['duration']
#     inv['number_needed'] = inv['number_needed'].fillna(1).round()  # xx should always round to nearest top integer
#     inv['number_taken'] = inv[['number', 'number_needed']].fillna(1).apply(min, axis=1)
#     inv['lists'] = inv.apply(lambda x: [x['item']] * int(x['number_taken']), axis=1)
#     items = inv['lists'].sum()
#     return list(items)

def get_items_weight(df, weight):
    df['weight_cumsum'] = df.sort('rank')['weight'].cumsum()
    return df.query('weight_cumsum <= @weight'), df.query('weight_cumsum > @weight')


def optimize_for_covering_body():
    """
    incentivize rank model for making sure full body is covered
    so that there is no situation where 5 shirts are packed but no trousers
    """
    pass


def produce_category_summary(df, days):

    cols = ['duration_cumsum', 'duration', 'units_cumsum']
    cat_stats = df.groupby('meta_category').max()[cols]
    # query_string = 'duration_cumsum != 0 and (duration_cumsum *  units_cumsum < @args.days)'
    # cat_stats = cat_stats.query(query_string)
    cat_stats['days'] = days
    # filling needed with 1s for items that dont have duration, consider filling this at the top
    # xx produces negative values
    cat_stats['needed'] = (cat_stats.days / cat_stats.duration).apply(math.ceil).fillna(1)
    cat_stats['deficit'] = cat_stats.needed - cat_stats.units_cumsum
    cat_stats['washes_required'] = (cat_stats.needed / cat_stats.deficit).apply(math.ceil)
    cat_stats['washes_required'].replace([np.inf, -np.inf], 0, inplace=True)
    cat_stats.sort('washes_required', ascending=False, inplace=True)
    return cat_stats


def produce_output(pack, cut_off, cat_stats, volume):
    print '============================================================='
    print 'total items packed:', pack.description.count()
    print 'volume packed:', pack.volume.sum()
    print 'volume left:', volume - pack.volume.sum()
    print '-------------------------------------------------------------'
    print 'important items cut off:', cut_off[cut_off['rank'] == 0]['description'].count()
    print 'important items volume cut off:', cut_off[cut_off['rank'] == 0]['volume'].sum()
    print 'total items cut off:', cut_off.description.count()
    print 'total volume cut off:', cut_off.volume.sum()
    print '-------------------------------------------------------------'
    print 'category stats:'
    print cat_stats[['units_cumsum', 'needed', 'deficit', 'duration', 'washes_required']]
    print '============================================================='
    print 'Pack:'
    pack = pack.sort(['rank', 'meta_category'])
    cols = ['meta_category', 'description', 'rank']
    print pack[cols]
    print '-------------------------------------------------------------'
    print 'Not packed but important:'
    print cut_off[cut_off['rank'] == 0][cols]


def main(days, volume, weight, options, save):
    inv = load_inv()
    inv = produce_full_inventory(inv)
    pack = get_items_days(inv, days)
    pack = add_rank(pack, options)
    pack, cut_off = get_items_volume(pack, volume)
    pack, cut_off = get_items_weight(pack, weight)
    cat_stats = produce_category_summary(pack, days)
    produce_output(pack, cut_off, cat_stats, volume)
    return pack, cut_off, cat_stats


if __name__ == '__main__':

    kwargs = dict(parser.parse_args(sys.argv[1:])._get_kwargs())
    print kwargs
    main(**kwargs)
    # sys.exit(main(**kwargs))
