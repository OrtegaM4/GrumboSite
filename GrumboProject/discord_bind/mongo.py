from pymongo import MongoClient
from discord_bind.models import DiscordUser
##db.createUser({
    user: 'grumbo_reader',
    pwd: 'wellifitisntgrumbo',
    roles: [{ role: 'read', db:'grumbobattlebot'}]
})
##db ip 35.182.223.175:27017

client = MongoClient('mongodb://grumbo_reader:wellifitisntgrumbo@35.182.223.175:27017/grumbobattlebot')
dbs = c.database_names()
for db in dbs:
    print db
    for col in c[db].collection_names():
        print '\t', col
        for pag in c[db][col].find():
            print page
