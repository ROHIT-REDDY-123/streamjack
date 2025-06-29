
import streamlit as st
import random

# ----- Setup -----
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7,
          'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

# ----- Classes -----
class Card:
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
    def __str__(self):
        return self.rank + " of " + self.suit

class Deck:
    def __init__(self):
        self.deck = [Card(suit, rank) for suit in suits for rank in ranks]
    def shuffle(self):
        random.shuffle(self.deck)
    def deal(self):
        return self.deck.pop()

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1
        self.adjust_for_ace()
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

# ----- Initialize Streamlit App -----
st.title("🃏 Blackjack Game")

if 'deck' not in st.session_state:
    st.session_state.deck = Deck()
    st.session_state.deck.shuffle()
    st.session_state.player_hand = Hand()
    st.session_state.dealer_hand = Hand()
    for _ in range(2):
        st.session_state.player_hand.add_card(st.session_state.deck.deal())
        st.session_state.dealer_hand.add_card(st.session_state.deck.deal())
    st.session_state.game_over = False
    st.session_state.result = ""

# ----- Display Cards -----
st.subheader("Your Hand:")
for card in st.session_state.player_hand.cards:
    st.write(card)
st.write(f"Total value: {st.session_state.player_hand.value}")

st.subheader("Dealer's Hand:")
st.write(st.session_state.dealer_hand.cards[0])
st.write("Second card is hidden.")

# ----- Game Actions -----
if not st.session_state.game_over:
    if st.button("Hit"):
        st.session_state.player_hand.add_card(st.session_state.deck.deal())
        if st.session_state.player_hand.value > 21:
            st.session_state.result = "You bust! Dealer wins."
            st.session_state.game_over = True

    if st.button("Stand"):
        while st.session_state.dealer_hand.value < 17:
            st.session_state.dealer_hand.add_card(st.session_state.deck.deal())
        dealer_val = st.session_state.dealer_hand.value
        player_val = st.session_state.player_hand.value
        if dealer_val > 21:
            st.session_state.result = "Dealer busts! You win!"
        elif dealer_val > player_val:
            st.session_state.result = "Dealer wins!"
        elif dealer_val < player_val:
            st.session_state.result = "You win!"
        else:
            st.session_state.result = "It's a tie!"
        st.session_state.game_over = True

# ----- Display Result -----
if st.session_state.game_over:
    st.subheader("Dealer's Final Hand:")
    for card in st.session_state.dealer_hand.cards:
        st.write(card)
    st.write(f"Total value: {st.session_state.dealer_hand.value}")
    st.success(st.session_state.result)
    if st.button("Play Again"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
