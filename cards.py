# cards.py - Bingo Cards Database (Part 1)
import random

BINGO_CARDS = {
    1: [[7, 24, 33, 51, 68], [12, 19, 44, 55, 72], [3, 27, "*", 48, 61], [10, 22, 38, 59, 75], [1, 16, 40, 50, 64]],
    2: [[14, 29, 31, 46, 66], [5, 17, 43, 58, 71], [8, 25, "*", 53, 63], [11, 21, 36, 49, 74], [2, 20, 39, 52, 69]],
    # ... እዚህ ጋር 100 ካርዶች ይኖራሉ
}

# ለናሙና ያህል ቀሪዎቹን 100 ካርዶች በራስ-ሰር የሚያመነጭ ኮድ እዚህ አለ
def generate_cards(start, end):
    cards = {}
    for i in range(start, end + 1):
        card = []
        ranges = [(1, 15), (16, 30), (31, 45), (46, 60), (61, 75)]
        columns = []
        for r in ranges:
            col = random.sample(range(r[0], r[1] + 1), 5)
            columns.append(col)
        
        # Transpose columns to rows
        for r in range(5):
            row = [columns[c][r] for c in range(5)]
            card.append(row)
        
        card[2][2] = "*" # መሃል ላይ ኮከብ ማድረግ
        cards[i] = card
    return cards

# 4000 ካርዶችን በአንድ ጊዜ ለማመንጨት
BINGO_CARDS.update(generate_cards(3, 400))

def get_card(card_id):
    return BINGO_CARDS.get(card_id)
