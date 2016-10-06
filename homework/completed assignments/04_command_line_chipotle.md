## Lesson 4 Homework: Command Line Chipotle
    ### Rebecca Minich
    ### 10.03.16

### Answers
#### Answer 1
* Look at the head and the tail of **chipotle.tsv** in the **data** subdirectory of this repo. Think for a minute about how the data is structured. What do you think each column means? What do you think each row means? Tell me! (If you're unsure, look at more of the file contents.)
* Work Part A:
* $ head chipotle.tsv
    * order_id        quantity        item_name       choice_description      item_price
1       1       Chips and Fresh Tomato Salsa    NULL    $2.39
1       1       Izze    [Clementine]    $3.39
1       1       Nantucket Nectar        [Apple] $3.39
1       1       Chips and Tomatillo-Green Chili Salsa   NULL    $2.39
2       2       Chicken Bowl    [Tomatillo-Red Chili Salsa (Hot), [Black Beans, Rice, Cheese, Sour Cream]]      $16.98
3       1       Chicken Bowl    [Fresh Tomato Salsa (Mild), [Rice, Cheese, Sour Cream, Guacamole, Lettuce]]     $10.98
3       1       Side of Chips   NULL    $1.69
4       1       Steak Burrito   [Tomatillo Red Chili Salsa, [Fajita Vegetables, Black Beans, Pinto Beans, Cheese, Sour                                               Cream, Guacamole, Lettuce]]    $11.75
4       1       Steak Soft Tacos        [Tomatillo Green Chili Salsa, [Pinto Beans, Cheese, Sour Cream, Lettuce]]    $                                              9.25

* $ tail chipotle.tsv
    * 1831    1       Carnitas Bowl   [Fresh Tomato Salsa, [Fajita Vegetables, Rice, Black Beans, Cheese, Sour Cream, Lettuc                                              e]]     $9.25
1831    1       Chips   NULL    $2.15
1831    1       Bottled Water   NULL    $1.50
1832    1       Chicken Soft Tacos      [Fresh Tomato Salsa, [Rice, Cheese, Sour Cream]]        $8.75
1832    1       Chips and Guacamole     NULL    $4.45
1833    1       Steak Burrito   [Fresh Tomato Salsa, [Rice, Black Beans, Sour Cream, Cheese, Lettuce, Guacamole]]    $                                              11.75
1833    1       Steak Burrito   [Fresh Tomato Salsa, [Rice, Sour Cream, Cheese, Lettuce, Guacamole]]    $11.75
1834    1       Chicken Salad Bowl      [Fresh Tomato Salsa, [Fajita Vegetables, Pinto Beans, Guacamole, Lettuce]]   $                                              11.25
1834    1       Chicken Salad Bowl      [Fresh Tomato Salsa, [Fajita Vegetables, Lettuce]]      $8.75
1834    1       Chicken Salad Bowl      [Fresh Tomato Salsa, [Fajita Vegetables, Pinto Beans, Lettuce]] $8.75


* Part B: What do you think each column means?
* Answers: there are five columns they are defined as:
    * 1. Order_id: Unique numerical value associated with each order
    * 2. quantity: number of menu items ordered (only more than one if customer orders multiples like two sides of chips or two canned sodas).
    * 3. item_name: name of menu item (what the name the customer sees on the menu)
    * 4. choice_description: the contents of the menu item for mixed dishes or the flavor for canned soda. probably to keep track of inventory and to add extra cost for guac/sour cream.
    * 5. item_price: total cost of the menu item(s). for example: if customer orders 1 soda item_price = 1.08

####  Answer 2
* How many orders do there appear to be?
* Answer: According to the tail there appear to be 1,834 orders.

#### Answer 3
* How many lines are in this file?
* Answer: 4,623
* Work:
    * <$ wc -l chipotle.tsv>
    * 4623 chipotle.tsv


####  Answer 4
* Which burrito is more popular, steak or chicken? For this set of orders:
* Answer: Chicken (Steak burritos sold: N_steak = 386, chicken burritos sold: N_chicken = 591)
* Work:
    * Step 1: first I sorted steak burritos by quantity per order to determine highest number of multiples; this was 3:
        * <$ grep "Steak Burrito" chipotle.tsv | sort -k 2,2>
    * Step 2 : I determined the numeber of burritos per each multiple as follows:
        * TOTAL "Steak Burrito orders":
        <$ grep "Steak Burrito" chipotle.tsv | wc -l>
        368
        * Orders with 2 burritos:
        <$ grep "Steak Burrito" chipotle.tsv | cut -f2 | grep "2" | wc -l>
        14
        * Orders with 3 burritos:
        <$ grep "Steak Burrito" chipotle.tsv | cut -f2 | grep "3" | wc -l>
        2
    * Step 3 : Simple arithmetic
        * N_steak = 368 - 14 - 2 + (14*2) + (2*3)
        * N_steak = 386
    * Repeat steps 1-3 with Chicken Burrito
        * N_chicken = 553 - 28 - 2 - 2 + (28*2) + (2*3) + (2*4)
        * N_Chicken = 591

####  Answer 5
* Do chicken burritos more often have black beans or pinto beans?
* Answer: Black beans (burritos w/pinto beans = 105, w/black beans = 282. Of these, 20 have both )
* Work:
    * <$ grep "Chicken Burrito" chipotle.tsv | grep "Pinto Beans" | wc -l>
        105
    * <$ grep "Chicken Burrito" chipotle.tsv | grep "Black Beans" | wc -l>
        282
    * <$ grep "Chicken Burrito" chipotle.tsv | grep "Black Beans" | grep "Pinto Beans" | wc -l>
        20

####  Answer 6
* Make a list of all of the CSV or TSV files in the [our class repo]
* Work:
    * <$ find ~/dropbox/generalassembly/ds-sea-4 -name "*.tsv">

        * /c/Users/minire/dropbox/generalassembly/ds-sea-4/data/chipotle.tsv
/c/Users/minire/dropbox/generalassembly/ds-sea-4/data/sms.tsv
/c/Users/minire/dropbox/generalassembly/ds-sea-4/data/steak_burrito.tsv

    * <$ find ~/dropbox/generalassembly/ds-sea-4 -name "*.csv">
        * /c/Users/minire/dropbox/generalassembly/ds-sea-4/data/airlines.csv
/c/Users/minire/dropbox/generalassembly/ds-sea-4/data/Airline_on_time_west_coast.csv
/c/Users/minire/dropbox/generalassembly/ds-sea-4/data/bank-additional.csv
/c/Users/minire/dropbox/generalassembly/ds-sea-4/data/bikeshare.csv
/c/Users/minire/dropbox/generalassembly/ds-sea-4/data/citibike_feb2014.csv
/c/Users/minire/dropbox/generalassembly/ds-sea-4/data/drinks.csv
/c/Users/minire/dropbox/generalassembly/ds-sea-4/data/drones.csv
/c/Users/minire/dropbox/generalassembly/ds-sea-4/data/hitters.csv
/c/Users/minire/dropbox/generalassembly/ds-sea-4/data/icecream.csv
/c/Users/minire/dropbox/generalassembly/ds-sea-4/data/imdb_1000.csv
/c/Users/minire/dropbox/generalassembly/ds-sea-4/data/mtcars.csv
/c/Users/minire/dropbox/generalassembly/ds-sea-4/data/NBA_players_2015.csv
/c/Users/minire/dropbox/generalassembly/ds-sea-4/data/ozone.csv
/c/Users/minire/dropbox/generalassembly/ds-sea-4/data/pronto_cycle_share/2015_station_data.csv
/c/Users/minire/dropbox/generalassembly/ds-sea-4/data/pronto_cycle_share/2015_trip_data.csv
/c/Users/minire/dropbox/generalassembly/ds-sea-4/data/pronto_cycle_share/2015_weather_data.csv
/c/Users/minire/dropbox/generalassembly/ds-sea-4/data/rossmann.csv
/c/Users/minire/dropbox/generalassembly/ds-sea-4/data/rt_critics.csv
/c/Users/minire/dropbox/generalassembly/ds-sea-4/data/stores.csv
/c/Users/minire/dropbox/generalassembly/ds-sea-4/data/syria.csv
/c/Users/minire/dropbox/generalassembly/ds-sea-4/data/time_series_train.csv
/c/Users/minire/dropbox/generalassembly/ds-sea-4/data/titanic.csv
/c/Users/minire/dropbox/generalassembly/ds-sea-4/data/ufo.csv
/c/Users/minire/dropbox/generalassembly/ds-sea-4/data/vehicles_test.csv
/c/Users/minire/dropbox/generalassembly/ds-sea-4/data/vehicles_train.csv
/c/Users/minire/dropbox/generalassembly/ds-sea-4/data/yelp.csv



#### Answer 7
* Count the approximate number of occurrences of the word "dictionary"
* Answer: There are approximately 79 occurences of the word "dictionary" in ds-sea-4
* Work:
<$ grep -r -i "dictionary" ~/dropbox/generalassembly/ds-sea-4 | wc -l>
79
