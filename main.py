import socket
from emoji import demojize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'VibeMeter'
token = 'oauth:mg31dpbx7ggtbcde3cvxaqbe7zufpc'
channel = '#tarik'

sock = socket.socket()
sock.connect((server, port))
sock.send(f"PASS {token}\r\n".encode('utf-8'))
sock.send(f"NICK {nickname}\r\n".encode('utf-8'))
sock.send(f"JOIN {channel}\r\n".encode('utf-8'))

ANALYZER = SentimentIntensityAnalyzer()
overall_sentiment = {'compound': 0, 'neg': 0.1, 'neu': 0, 'pos': 0.1, 'total': 0}

# Init graph
fig, axs = plt.subplots(2,1,figsize=(6, 10))
fig.tight_layout(pad=3.0)
axs[0].bar(['Positive', 'Negative', 'Neutral'], [0, 0, 0], color=['green', 'red', 'grey'])
axs[0].set_title('VibeMeter')
axs[0].set_ylabel('Relative vibe')
axs[1].pie([0.5, 0.5], labels=['Positive', 'Negative'], colors=['green', 'red'])



def udpate_graph(arg):
    resp = sock.recv(2048).decode('utf-8')

    if resp.startswith('PING'):
        sock.send("PONG\n".encode('utf-8'))
    elif len(resp) > 0:
        if ':streamlabs' not in resp:
            demojized = demojize(resp)
            cut = demojized.split(':')
            sentiment_dict = ANALYZER.polarity_scores(cut[-1])
            print(cut[-1])
            print('===============================')
            print(sentiment_dict)
            print('===============================')
            overall_sentiment['compound'] += sentiment_dict['compound']
            overall_sentiment['neg'] += sentiment_dict['neg']
            overall_sentiment['neu'] += sentiment_dict['neu']
            overall_sentiment['pos'] += sentiment_dict['pos']
            overall_sentiment['total'] = overall_sentiment['neg'] + overall_sentiment['pos']
            print(overall_sentiment)

    axs[0].cla()
    axs[1].cla()
    axs[0].bar(['Positive', 'Negative'], [overall_sentiment['pos']/overall_sentiment['total'], overall_sentiment['neg']/overall_sentiment['total']], color=['green', 'red'])
    axs[1].pie([overall_sentiment['pos']/overall_sentiment['total'], overall_sentiment['neg']/overall_sentiment['total']], labels=['Positive', 'Negative'], colors=['green', 'red'])
    axs[0].set_title('VibeMeter')

def main():
    ani = FuncAnimation(fig, udpate_graph, interval=300)
    plt.show()

if __name__ == '__main__':
    main()