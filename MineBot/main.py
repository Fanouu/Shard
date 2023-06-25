from javascript import require, On, Once, AsyncTask, once, off

from manager.ConfigManager import getConfig

mineflayer = require('mineflayer')
pathfinder = require('mineflayer-pathfinder')

BOT_USERNAME = getConfig("bot.username")
bot = mineflayer.createBot({
  'host': 'gamster.org',
  'username': 'Capybara',
  'version': '1.8.9'
})

bot.loadPlugin(pathfinder.pathfinder)
print("Started mineflayer")

@On(bot, 'spawn')
def handle(*args):
  print("I spawned 👋")
  movements = pathfinder.Movements(bot)

  @On(bot, 'chat')
  def handleMsg(this, sender, message, *args):
    print("Got message", sender, message)
    if sender and (sender != BOT_USERNAME):
      bot.chat('Hi, you said ' + message)
      if 'come' in message:
        player = bot.players[sender]
        print("Target", player)
        target = player.entity
        if not target:
          bot.chat("I don't see you !")
          return

        pos = target.position
        bot.pathfinder.setMovements(movements)
        bot.pathfinder.setGoal(pathfinder.goals.GoalNear(pos.x, pos.y, pos.z, 1))

@On(bot, "end")
def handle(*args):
  print("Bot ended!")