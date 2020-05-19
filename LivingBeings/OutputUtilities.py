from LivingBeings.Lumberjack import Lumberjack
from LivingBeings.Bear import Bear
from LivingBeings.Tree import Tree

class PrintPrefabs:
    def resources():
        print(f"Lumber collected:{Lumberjack.lumber}\tKills:{Bear.kills}")

    def population():
        print(f"Trees: {len(Tree.alive)}\t " +
              f"Lumberjacks: {len(Lumberjack.alive)}\t " +
              f"Bears: {len(Bear.alive)}")