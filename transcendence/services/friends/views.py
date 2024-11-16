from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from transcendence.services.responses import error_response, success_response
from transcendence.services.models.user import User
from transcendence.services.models.friend import Friend

@api_view(['POST'])
@permission_classes([AllowAny])
def friends(request):
    username = request.data.get('username')
    if (username is None or User.objects.filter(username=username).exists() is False):
        return error_response('User not found', 'User not found', 'error', 404)
    if not Friend.objects.filter(user=request.user, friend__username=username).exists():
        if (Friend.objects.filter(friend=request.user, user__username=username).exists()):
            Friend.objects.filter(friend=request.user, user__username=username).update(is_accepted=True)
            return success_response('Friend request accepted', 'Successfully accepted friend request', 'success', 200)
        else:
            Friend.objects.create(user=request.user, friend=User.objects.get(username=username))
            return success_response('Friend request sent', 'Successfully sent friend request', 'success', 200)
    else:
        return error_response('Friend request already sent', 'Friend request already sent', 'error', 400)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_friends(request, username):
    friend = {}
    friend = Friend.objects.filter(user=request.user, friend__username=username, is_accepted=True).first()
    if friend is None:
        friend = Friend.objects.filter(friend=request.user, user__username=username, is_accepted=True).first()
        if friend is not None:
            friend = {
                "id": friend.user.id,
                "username": friend.user.username,
                "email": friend.user.email,
                "last_activity": friend.user.last_activity,
                "image": friend.user.image
            }
        else:
            return error_response('Friend not found', 'Friend not found', 'error', 404)
    else:
        friend = {
            "id": friend.friend.id,
            "username": friend.friend.username,
            "email": friend.friend.email,
            "last_activity": friend.friend.last_activity,
            "image": friend.friend.image
        }
    return success_response('Friends found', "Successfully found friends", 'success', 200, {
        "friend": friend
    }, None, False)

@api_view(['PUT'])
@permission_classes([AllowAny])
def accept_friend(request, friend_id):
    if not Friend.objects.filter(friend=request.user, user__id=friend_id).exists():
        return error_response('Friend request not found', 'Friend request not found', 'error', 404)
    if Friend.objects.filter(friend=request.user, user__id=friend_id).first().is_accepted:
        return error_response('Friend request already accepted', 'Friend request already accepted', 'error', 400)
    Friend.objects.filter(friend=request.user, user__id=friend_id).update(is_accepted=True)
    return success_response('Friend request accepted', 'Successfully accepted friend request', 'success', 200)

@api_view(['DELETE'])
@permission_classes([AllowAny])
def reject_friend(request, friend_id):
    if not Friend.objects.filter(friend=request.user, user__id=friend_id).exists():
        return error_response('Friend request not found', 'Friend request not found', 'error', 404)
    Friend.objects.filter(friend=request.user, user__id=friend_id).delete()
    return success_response('Friend request rejected', 'Successfully rejected friend request', 'success', 200)