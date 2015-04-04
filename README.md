#pack: simple utility for producing list of items to pack based on inventory and number of criteria


##What is it

**pack** is a Python tool for automatically creating checklists for packing. 
Basically if you dont want to think what you need to pack every time you travel or move, that is the tool for you :)

##Input:
Inventory list in csv

##Output:
- **list of items to pack**
- list of items cut off (needed but not fitting criterias, for example exceeding volume)
- item statistics like:


|ix |all_cut_off|imp_cut_off|packed|left|bag_pct_packed|imp_pct_packed|
|---|---|---|---|---|---|                                                                           
|number|18|0|33|NaN|nan%|100%|
|volume|8120|0|19280|720|96%|100%|
|weight|3600|0|6600|13400|33%|100%|


- category statistics like:


<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>needed</th>
      <th>deficit</th>
      <th>washes_required</th>
    </tr>
    <tr>
      <th>meta_category</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>top</th>
      <td> 5</td>
      <td> 2</td>
      <td>  3</td>
    </tr>
    <tr>
      <th>bottom</th>
      <td> 2</td>
      <td> 1</td>
      <td>  2</td>
    </tr>
    <tr>
      <th>socks</th>
      <td> 5</td>
      <td> 0</td>
      <td>  0</td>
    </tr>
    <tr>
      <th>...</th>
      <td> ...</td>
      <td> ...</td>
      <td> ...</td>
    </tr>
  </tbody>
</table>



## Example use cases

1. Going for a weekend trip to London.
2. Decluterring stuff, with ambitious aspiration to fit all possessions in two large suitcases. :) 
3. Going for two weeks holiday to a hot country.
4. Going to a Salsa Congress .. ;)


## How to run

```sh
python pack.py
```

or to specify custom number of days (-d), volume (-v) or weight (-w):

```sh
python pack.py -d 2 -v 20000 -w 10000
```

you can also specify additional options that you want to prioritize (you can add list of tags in the inventory file in the 'options' field)

```sh
python pack.py -o dance swim
```


## Metadata definitions

- number - number of items, you dont want to type each socks you posess..
- description - unique id of an item, for example "black versache trousers"
- importance - how necessary the item is , 0 is the lowest.Items with 0 will be packed in the first priority and reported if they dont fit in the baggage.
- options - custom tags that can raise the importance of items, for example +dqncing will prioritize dancing shoes, +hot will prioritize shorts, and importantly +swim will remind you about those swimming googles!..
- meta_category - meta data describing item like for example shoes, bottom , top etc. Used - for example to make sure you dont just take 5 shirts and no trousers ;)
- volume - approximate volume (currently in cm3), used to pack number of items that fits the specified size of the baggage.
- weight - approximate weight (currently in g), used to cut off items that dont fit required weight criteria
- comments - any additional info, for example why the item is important or other details.

## Asumptions

- items tagged with specifically declared options will get assigned importance 0
- importance left blank means to never pack the thing unless their assign option is declared


## Additional Info

- 1 backpack - 43 x 33 x 13, 20 litres
- 1 small bag - 56 x 45 x 25 cm - 63 litres, weight 10 kg
- 1 large bag = 90 x 75 x 43 cm - 290 litres, weight 23 kg


## To do

- saving and reading list
- convenience arguments for custom baggage sizes (backpack, hand baggage etc)


## Bonus

* [article](http://foodandphotosrtw.com/2015/03/23/declutter-apartment/) with some tips on decluterring for travel




