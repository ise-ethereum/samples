import numpy as np
import matplotlib.pyplot as plt
import math

K = 20

x = np.linspace(-800, 800, 1600)

E = np.linspace(-0.9999, 0.9999, 10000)
difference = (400*np.log10(1/E-1))/(np.log10(10))

prev_s = 20
for i, d in enumerate(difference):
    scoreChange = (1-E[i])*20
    if not math.isnan(d) and prev_s != round(scoreChange):
        prev_s = round(scoreChange)
        print(int(scoreChange+1), int(d))

y = 1/(1+10**(x/400))
p1, = plt.plot(x, y)
plt.xlabel('$R_B$ - $R_A$ (Elo difference)')
plt.ylabel('$E_A$ (Expected score)')
plt.title('Expected score')
plt.show()

results = ('lose', 'draw', 'win',)
players = ('A', 'B',)

for p, player in enumerate(players):
    if p == 0:
        y = 1/(1+10**(x/400))
    else:
        y = 1/(1+10**(-x/400))

    for i, result in enumerate((0, 0.5, 1,)):
        resultStr = results[i]
        _x = x[:]
        if p == 1:
            result = 1 - result
            resultStr = results[::-1][i]
            _x = x[::-1]
        ax = plt.subplot(2, 3, 3*p+(i+1))

        scoreChange = (result-y) * K
        scoreChangeRound = np.vectorize(lambda x: round(x), otypes=[np.int])(scoreChange)

        p1, = plt.plot(_x, scoreChange)
        p3, = plt.plot(_x, scoreChangeRound)

        if p == 1:
            plt.xlabel('$R_A$ - $R_B$ (absolute Elo difference)')
        if i == 0:
            plt.ylabel('$R+_%s = K*(S_%s - E_%s)$ (Elo change for %s)' % (player, player, player, player))
        plt.title('%s %s ($S_%s = %.1f)$' % (player, resultStr, player, result))
        #plt.legend([p1, p3], ['Original curve', 'Round'], loc=2)
        ax = plt.gca()

        if p == 0 and i == 0:
            ax.scatter([200], [-5], s=120, c='red', marker='+')
            ax.annotate('-5', xy=(200, -5), xytext=(300, -6))

        if p == 1 and i == 0:
            ax.scatter([200], [15], s=120, c='red', marker='+')
            ax.annotate('+15', xy=(200, 15), xytext=(300, 14))

        ax.set_ylim(-21, 21)
        ax.set_xlim(-800, 800)
        ax.grid(True)



fig = plt.gcf()
fig.suptitle("Elo score change vs previous Elo score difference", fontsize=16)
plt.show()
