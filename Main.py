import vk_api
import random
import time

def Authorization(login,password):
    vk_session = vk_api.VkApi(token=token)
    vk_session._auth_token()
    return vk_session

def GetVK(vk_session):
    vk = vk_session.get_api()
    return vk

def GetLastPostId(groupId):
    LastPost = vk.wall.get(owner_id=groupId, offset=1, count=1)
    LastPostId = LastPost["items"][0]["id"]
    return LastPostId

def GetWinner(groupId,postId):
    allActivity= []
    while True:
        likes = vk.likes.getList(type='post', owner_id=groupId, item_id=postId, extended=1, count=1000)
        if likes['count'] >= 10:
            comments = vk.wall.getComments(owner_id=groupId, post_id=postId)
            for like in likes["items"]:
                allActivity.append(like["id"])
            for comment in comments["items"]:
                try:
                    allActivity.append(comment["from_id"])
                except KeyError:
                    print("Комментарий удален")
                    continue

            random.shuffle(allActivity)
            onlyOne = allActivity[0]
            winnerInfo = vk.users.get(user_ids=onlyOne)
            winner = {'first_name': winnerInfo[0]["first_name"], 'last_name': winnerInfo[0]["last_name"],'id': winnerInfo[0]["id"]}
            print(winner)
            return winner
        else:
            print(str(likes['count']) + " лайков недостаточно")
            time.sleep(300)

def GetIdOfAvatarPhoto(winner,vk):
    idOfAvatarPosts = []
    try:
        postID = vk.photos.get(owner_id=winner["id"], rev=1, extended=1, count=1, album_id='profile')
        idOfAvatarPosts.append(postID['items'][0]['id'])
        print(postID['items'][0]['id'])
    except vk_api.exceptions.ApiError:
        print("error 1")
        return False
    except IndexError:
        print("error 2")
        return False
    return idOfAvatarPosts

def GetPhotoString(winner,idOfAvatarPosts):
    Link = []
    flag = False
    while flag!= True:
        try:
            Link.append("photo" + str(winner["id"]) + "_" + str(idOfAvatarPosts[0]))
            flag = True
        except:
            continue
    return Link

def MakePost(Link):
    postId = vk.wall.post(message="&#129304; Победитель &#128073;	 [id" + str(winner['id']) + "|"+ winner['first_name'] + " " + winner['last_name'] + "] &#128072;! Лайкаем! &#129304; \n  &#128293; &#128293;	&#128293; Оставляй коменты, чтобы увеличить свои шансы в разы!! &#128293; &#128293; &#128293; \n &#9757; P.S. Набираем >10 лайков и следующий пост \n Оцени эту фотку от 0 до 10 в коментах &#128540;	",
                         owner_id=groupId,
                         from_group=1,
                         attachments=[Link[0]])
    return postId
token="c9cda5680f7f33cac65d923c0b24e11fa9edbb5a70d8f43f4b151c251ee490cdc37b246ed4b93bc861dd6"
login = '+79789801942'
password = 'adjbADb6bdhoa3dnjn'
groupId = -170119223

while True:
    vk_session = Authorization(login,password)
    vk = GetVK(vk_session)
    LastPostId = GetLastPostId(groupId)
    print("Id последнего поста: ",LastPostId)

    while True:
        winner = GetWinner(groupId, LastPostId)
        while True:
            if winner['id'] == 65461369 or winner['id'] == 398965538 or winner['id'] == 479839324:
                winner = GetWinner(groupId, LastPostId)
            else:
                break
        while winner['id'] == 65461369 or winner['id'] == 398965538 or winner['id'] == 479839324:
            print("Был выбран админ, переигрываем")
            winner = GetWinner(groupId, LastPostId)
        if GetIdOfAvatarPhoto(winner,vk) == False:
            continue
        else:
            idOfAvatarPosts = GetIdOfAvatarPhoto(winner, vk)
            break

    Link = GetPhotoString(winner,idOfAvatarPosts)
    NewPostId=MakePost(Link)
    time.sleep(1800)
