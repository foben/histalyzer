MAXFRAME = 331

ALL_CATEGORIES = ['apple','ball','banana','bell-pepper','binder','bowl','calculator','camera','cap','cell-phone','cereal-box','coffee-mug','comb','dry-battery','flashlight','food-bag','food-box','food-can','food-cup','food-jar','garlic','glue-stick','greens','hand-towel','instant-noodles','keyboard','kleenex','lemon','lightbulb','lime','marker','mushroom','notebook','onion','orange','peach','pear','pitcher','plate','pliers','potato','rubber-eraser','scissors','shampoo','soda-can','sponge','stapler','tomato','toothbrush','toothpaste','water-bottle'] 
RUN1 = ['apple','ball','banana','bell-pepper','binder','bowl','calculator','camera','cap','cell-phone','cereal-box','coffee-mug','comb','dry-battery','flashlight']
RUN2 = ['food-bag','food-box','food-can','food-cup','food-jar','garlic','glue-stick','greens','hand-towel','instant-noodles']
RUN3 = ['keyboard','kleenex','lemon','lightbulb','lime','marker','mushroom','notebook','onion','orange','peach','pear','pitcher','plate']
RUN4 = ['pliers','potato','rubber-eraser','scissors','shampoo','soda-can','sponge','stapler','tomato','toothbrush','toothpaste','water-bottle']

RUN12 = RUN1 + RUN2
RUN34 = RUN3 + RUN4

EVERY_5TH = (range(1, MAXFRAME, 5), "ev5th")
EVERY_10TH = (range(1, MAXFRAME, 10), "ev5th")
EVERY_15TH = (range(1, MAXFRAME, 15), "ev15th")
EVERY_25TH = (range(1, MAXFRAME, 25), "ev25th")
EVERY_50TH = (range(1, MAXFRAME, 50), "ev25th")
EVERY_100TH = (range(1, MAXFRAME, 100), "ev100th")
EVERY_200TH = (range(1, MAXFRAME, 200), "ev200th")
EVERY_300TH = (range(1, MAXFRAME, 300), "ev200th")

framesets = {
        5 : EVERY_5TH,
        10: EVERY_10TH,
        15: EVERY_15TH,
        25: EVERY_25TH,
        50: EVERY_50TH,
        100: EVERY_100TH,
        200: EVERY_200TH,
        300: EVERY_300TH
        }

def get_frameset(n):
    return framesets[n]

DATA_DIR = __file__



