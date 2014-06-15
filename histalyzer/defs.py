MAXFRAME = 331

ALL_CATEGORIES = ['apple','ball','banana','bell-pepper','binder','bowl','calculator','camera','cap','cell-phone','cereal-box','coffee-mug','comb','dry-battery','flashlight','food-bag','food-box','food-can','food-cup','food-jar','garlic','glue-stick','greens','hand-towel','instant-noodles','keyboard','kleenex','lemon','lightbulb','lime','marker','mushroom','notebook','onion','orange','peach','pear','pitcher','plate','pliers','potato','rubber-eraser','scissors','shampoo','soda-can','sponge','stapler','tomato','toothbrush','toothpaste','water-bottle'] 
RUN1 = ['apple','ball','banana','bell-pepper','binder','bowl','calculator','camera','cap','cell-phone','cereal-box','coffee-mug','comb','dry-battery','flashlight','food-bag']
RUN2 = ['food-box','food-can','food-cup','food-jar','garlic','glue-stick','greens','hand-towel','instant-noodles']
RUN3 = ['keyboard','kleenex','lemon','lightbulb','lime','marker','mushroom','notebook','onion','orange','peach','pear','pitcher','plate']
RUN4 = ['pliers','potato','rubber-eraser','scissors','shampoo','soda-can','sponge','stapler','tomato','toothbrush','toothpaste','water-bottle']

RUN12 = RUN1 + RUN2
RUN34 = RUN3 + RUN4



RUN81 = ['apple','ball','banana','bell-pepper','binder','bowl','calculator','camera']
RUN82 = ['cap','cell-phone','cereal-box','coffee-mug','comb','dry-battery','flashlight','food-bag']
RUN83 = ['food-box','food-can','food-cup']
RUN84 = ['food-jar','garlic','glue-stick','greens','hand-towel','instant-noodles']
RUN85 = ['keyboard','kleenex','lemon','lightbulb','lime','marker','mushroom']
RUN86 = ['notebook','onion','orange','peach','pear','pitcher','plate']
RUN87 = ['pliers','potato','rubber-eraser','scissors','shampoo','soda-can','sponge']
RUN88 = ['stapler','tomato','toothbrush','toothpaste','water-bottle']



RUN161 = ['apple','ball','banana','bell-pepper']
RUN162 = ['binder','bowl','calculator','camera']
RUN163 = ['cap','cell-phone','cereal-box','coffee-mug']
RUN164 = ['comb','dry-battery','flashlight','food-bag']
RUN165 = ['food-can']
RUN166 = ['food-box','food-cup']
RUN167 = ['food-jar','garlic','glue-stick']
RUN168 = ['greens','hand-towel','instant-noodles']
RUN169 = ['keyboard','kleenex','lemon']
RUN1610= ['lightbulb','lime','marker','mushroom']
RUN1611 = ['notebook','onion','orange']
RUN1612 = ['peach','pear','pitcher','plate']
RUN1613 = ['pliers','potato','rubber-eraser','scissors']
RUN1614 = ['shampoo','soda-can','sponge']
RUN1615 = ['stapler','tomato']
RUN1616 = ['toothbrush','toothpaste','water-bottle']

ALL_FRAMES = (range(1, MAXFRAME), "allFrames")
EVERY_2ND = (range(1, MAXFRAME, 2), "ev2nd")
EVERY_3RD = (range(1, MAXFRAME, 3), "ev3rd")
EVERY_5TH = (range(1, MAXFRAME, 5), "ev5th")
EVERY_10TH = (range(1, MAXFRAME, 10), "ev10th")
EVERY_15TH = (range(1, MAXFRAME, 15), "ev15th")
EVERY_25TH = (range(1, MAXFRAME, 25), "ev25th")
EVERY_50TH = (range(1, MAXFRAME, 50), "ev50th")
EVERY_100TH = (range(1, MAXFRAME, 100), "ev100th")
EVERY_200TH = (range(1, MAXFRAME, 200), "ev200th")
EVERY_300TH = (range(1, MAXFRAME, 300), "ev300th")
EVERY_400TH = (range(1, MAXFRAME, 400), "ev400th")
EVERY_500TH = (range(1, MAXFRAME, 500), "ev500th")
EVERY_600TH = (range(1, MAXFRAME, 600), "ev600th")

framesets = {
        1 : ALL_FRAMES,
        2 : EVERY_2ND,
        3 : EVERY_3RD,
        5 : EVERY_5TH,
        10: EVERY_10TH,
        15: EVERY_15TH,
        25: EVERY_25TH,
        50: EVERY_50TH,
        100: EVERY_100TH,
        200: EVERY_200TH,
        300: EVERY_300TH,
        400: EVERY_400TH,
        500: EVERY_500TH,
        600: EVERY_600TH
        }

def get_frameset(n):
    return framesets[n]

DATA_DIR = __file__



