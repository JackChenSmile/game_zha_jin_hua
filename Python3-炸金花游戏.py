import random
import time

# 分别定义全局变量：牌面值，花色，牌型，玩家姓名
FACES = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
COLORS = ['黑桃♠', '红心♥', '方块♦', '梅花♣']
TYPE = ['豹子', '顺金', '顺子', '对子', '单张']
NAMES = ['#Player1', '#Player2', '#Player3', '#Player4', '#Player5']

# 牌组列表初始化为空，玩家组列表初始化为空
CARD_GROUP = list()
PLAYERS = list()


# PRIORITY数组用于比较牌面值，花色，牌型的优先级
# A>K>Q>...>2
# 黑桃>红心>方块>梅花
# 豹子>顺金>顺子>对子>单张
PRIORITY = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
            '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14,
            '梅花♣': 1, '方块♦': 2, '红心♥': 3, '黑桃♠': 4,
            '单张': 1, '对子': 2, '顺子': 3, '顺金': 4, '豹子': 5
            }


# 定义一个Card类，由牌面和花色初始化
class Card:
    def __init__(self, face="", color=""):
        self.face = face                # 牌面，字符串类型
        self.color = color              # 花色，字符串类型
        self.name = color + face        # 牌的完整名称
        self.prior1 = PRIORITY[face]     # 牌面对应的优先级
        self.prior2 = PRIORITY[color]     # 牌花色对应的优先级

    def __lt__(self, other):            # 此处重写Card类的'<'符号，先比较牌面，再比较花色，当调用sort函数时，其会自动采用该内置函数比较
        if self.prior1 == other.prior1:
            return self.prior2 <= other.prior2
        else:
            return self.prior1 < other.prior1


# 定义一个Player类,由玩家姓名初始化
class Player:
    def __init__(self, name=""):
        self.card = list()      # 玩家拥有的牌存储在card里面，元素类型为Card
        self.name = name        # 玩家姓名
        self.type = ''          # 牌型
        self.winner = False     # 标志，记录该玩家是否是最后的赢家
        self.pair = 0           # 记录第一张对子牌的索引，默认为0

    def __lt__(self, other):    # 此处重写Player类的'<'符号，先比较牌型，再比较每张牌，当调用sort函数时，其会自动采用该内置函数比较
        n = len(self.card)
        if PRIORITY[self.type] == PRIORITY[other.type]:     # 若牌型相同，则比较牌大小。注意：对子牌型需要先比对，再比单。
            for i in range(n):
                index = (self.pair + i) % n                     # 0,1,2或者是1,2,0比较
                if self.card[index] != other.card[index]:
                    return self.card[index] < other.card[index]
            # 循环外这种情况是，玩家所有牌全部一样，也返回True。
            # 当然，看花色的情况下，第一张牌就可以比较出玩家输赢
            return True
        else:
            return PRIORITY[self.type] < PRIORITY[other.type]

    def info(self):
        print(self.name, end='\t')          # 输出玩家姓名
        for c in self.card:                 # 输出牌面
            print(c.name, end='\t')
        if not self.winner:                 # 若不是赢家，则只用输出牌型
            print(self.type)
        else:                               # 若是赢家，则还要加上庆祝语
            print(self.type, '\tWinner! 🎉🎉🎉')

    def judge_type(self):                   # 判断牌型,这个过程中，若出现对子类型的牌，则更新属性self.pair
        self.card.sort(reverse=True)        # 对玩家的牌按照优先级从大到小排序，比如3，6，5会被排成6,5,3
        cards = self.card
        if cards[0].prior1 == cards[1].prior1 and cards[0].prior1 == cards[2].prior1:
            self.type = '豹子'
        elif cards[0].prior1-cards[1].prior1 == 1 and cards[1].prior1-cards[2].prior1 == 1:
            if cards[0].prior2 == cards[1].prior2 and cards[0].prior2 == cards[2].prior2:
                self.type = '顺金'
            else:
                self.type = '顺子'
        elif cards[0].prior1 == cards[1].prior1:
            self.type = '对子'
        elif cards[1].prior1 == cards[2].prior1:        # 排序过后，若出现对子牌，那么它们必定连在一起，所以其实索引0和2不用比较
            self.type = '对子'
            self.pair = 1
        else:
            self.type = '单张'


# 输入：无
# 输出：无
# 功能：初始化52张的扑克牌列表，即生成一副完整的牌，然后初始化玩家列表
def init():
    CARD_GROUP.clear()  # 清空牌组列表
    for f in FACES:  # 遍历牌面值
        for c in COLORS:  # 遍历花色
            CARD_GROUP.append(Card(f, c))  # 添加扑克牌
    for name in NAMES:  # 初始化玩家列表
        PLAYERS.append(Player(name))  # 添加玩家


# 输入：无
# 输出：无
# 功能：实现发牌
def deal():
    # 因为每人需要发三张牌，所以用三次循环实现
    # 模拟随机发牌过程：每次随机抽取一张牌，然后从列表移除
    circle = 3
    for i in range(circle):
        print('第{0}轮发牌：'.format((i + 1)), end='\t')
        for p in PLAYERS:
            temp = random.choice(CARD_GROUP)        # 随机抽牌
            CARD_GROUP.remove(temp)                 # 从牌组移除这张牌
            p.card.append(temp)                     # 将牌加入玩家的card列表里面
            time.sleep(0.7)                         # 体现发牌停顿感，暂停0.7s
            print(temp.name, end='\t\t')            # 打印牌名称
        print()
    print()


# 输入：无
# 输出：无
# 功能：判断输赢
def win():
    divide = {'豹子': [], '顺金': [], '顺子': [], '对子': [], '单张': []}     # 按照牌型对玩家进行划分
    print('提示：玩家牌型正在分析中。')
    time.sleep(2)
    print('=' * 20, '玩家牌型情况如下', '=' * 20)  # 输出发牌情况提示语
    for p in PLAYERS:       # 输出玩家的牌，以及所执的牌型
        p.judge_type()      # 分析牌型
        p.info()            # 输出排序后的执牌情况
        divide[p.type].append(p)        # 将玩家加入该种牌型字典

    print('\n提示：玩家排名正在计算中。')
    time.sleep(2)
    print('=' * 20, '玩家排名情况如下', '=' * 20)  # 输出排名情况提示语'

    # 开始对玩家进行排序
    result = list()                             # 存储最后排序结果
    for k, v in divide.items():
        if len(v) > 0:                          # 若存在玩家是这种牌型
            v.sort(reverse=True)                # 对玩家的牌组进行排序
            result += v                         # 将v中数据合并到result列表中

    # 下面输出排名结果
    for i in range(len(result)):               # 输出玩家排序后的结果
        p = result[i]
        if i == 0:                              # 第一个人是赢家，winner要修改成True
            p.winner = True
        p.info()                                # 输出玩家信息


# 输入：无
# 输出：无
# 功能：开始游戏
def start():
    print('=' * 40, '欢迎体验炸金花小游戏', '=' * 40)       # 输出游戏标题
    init()                                              # 调用init函数，初始化相关数据
    print('提示：牌组已生成完毕，准备开始随机发牌。\n')         # 输出提示语
    print('=' * 20, '实时发牌情况如下', '=' * 20)           # 输出发牌情况提示语
    print('轮数/玩家', end='\t')
    for p in PLAYERS:                   # 输出玩家姓名，以\t分隔
        print(p.name, end='\t')
    print()
    deal()                              # 调用deal函数，开始模拟发牌
    win()                               # 调用win函数，判断输赢
    print('\n', '=' * 40, '欢迎体验炸金花小游戏', '=' * 40)  # 输出游戏标题


if __name__ == '__main__':
    start()
