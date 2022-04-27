import socket
from emoji import demojize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'VibeMeter'
token = 'oauth:mg31dpbx7ggtbcde3cvxaqbe7zufpc'
channel = '#corceon'

sock = socket.socket()
sock.connect((server, port))
sock.send(f"PASS {token}\r\n".encode('utf-8'))
sock.send(f"NICK {nickname}\r\n".encode('utf-8'))
sock.send(f"JOIN {channel}\r\n".encode('utf-8'))

ANALYZER = SentimentIntensityAnalyzer()
MAGICAL_NUMBER = 130
overall_sentiment = {'compound': 0, 'neg': 0.1, 'neu': 0, 'pos': 0.1, 'total': 0.0}

# Init graph
fig, axs = plt.subplots(1,1,figsize=(3, 5),facecolor='lime')
fig.tight_layout(pad=3.0)
axs.bar(['Vibe'], [0], color=['orange'])
axs.set_facecolor('lime')
axs.set_title('VibeMeter')
axs.set_ylabel('Relative vibe')
axs.set_ylim([0, MAGICAL_NUMBER])

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

    axs.cla()
    current_vibe = (overall_sentiment['pos']/overall_sentiment['total'])*MAGICAL_NUMBER
    vibemeter = axs.bar(['Vibe'], current_vibe, color=['orange'])
    axs.set_title('VibeMeter')
    axs.set_ylabel('Relative vibe')
    axs.set_facecolor('lime')
    axs.set_ylim([0, MAGICAL_NUMBER])

    for p in vibemeter:
        width = p.get_width()
        height = p.get_height()
        x, y = p.get_xy()
        plt.text(x + width / 2,
                 y + height * 1.01,
                 '{0:.2f}'.format(current_vibe) + '%',
                 ha='center',
                 weight='bold')



def main():
    ani = FuncAnimation(fig, udpate_graph, interval=300)
    plt.show()

if __name__ == '__main__':
    main()