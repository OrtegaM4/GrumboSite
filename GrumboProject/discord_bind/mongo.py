from pymongo import MongoClient
from bson.json_util import dumps
#     user: 'grumbo_reader',
#     pwd: 'wellifitisntgrumbo',
#     roles: [{ role: 'read', db:'grumbobattlebot'}]
# })
##db ip 35.182.223.175:27017
# mon
uid="177882100291207168"

client = MongoClient('mongodb://35.182.223.175:27017/grumbobattlebot')
db = client.grumbobattlebot
collection=db.characters
myquery= {"_id": uid}
mydoc=collection.find(myquery)
ha=''
print(mydoc)
for x in mydoc:
    if {'wins'} in mydoc:
        ha={'wins'}
    print(x)
    print(ha)
    # return bince
    # return render(request,'grumbo/stats.html',context={'post':post,})
