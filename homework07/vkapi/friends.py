import dataclasses
import math
import time
import typing as tp

from homework07.vkapi.config import VK_CONFIG
# from vkapi.exceptions import APIError

from homework07.vkapi.session import Session

QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(
        user_id: int, count: int = 5000, offset: int = 0, fields: tp.Optional[tp.List[str]] = None
) -> FriendsResponse:
    """
    Получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).

    :param user_id: Идентификатор пользователя, список друзей для которого нужно получить.
    :param count: Количество друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества друзей.
    :param fields: Список полей, которые нужно получить для каждого пользователя.
    :return: Список идентификаторов друзей пользователя или список пользователей.
    """
    start = Session(VK_CONFIG["domain"])
    resp = FriendsResponse(0, [0])
    try:
        friends = start.get("friends.get", params={"access_token": VK_CONFIG["access_token"],
                                                   "v": VK_CONFIG["version"],
                                                   "user_id": user_id,
                                                   "count": count,
                                                   "offset": offset,
                                                   "fields": fields})
        resp = FriendsResponse(friends.json()['response']['count'], friends.json()['response']['items'])
        print(resp)
    except:
        pass
    return resp


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
        source_uid: tp.Optional[int] = None,
        target_uid: tp.Optional[int] = None,
        target_uids: tp.Optional[tp.List[int]] = None,
        order: str = "",
        count: tp.Optional[int] = None,
        offset: int = 0,
        progress=None,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    """
    Получить список идентификаторов общих друзей между парой пользователей.

    :param source_uid: Идентификатор пользователя, чьи друзья пересекаются с друзьями пользователя с идентификатором target_uid.
    :param target_uid: Идентификатор пользователя, с которым необходимо искать общих друзей.
    :param target_uids: Cписок идентификаторов пользователей, с которыми необходимо искать общих друзей.
    :param order: Порядок, в котором нужно вернуть список общих друзей.
    :param count: Количество общих друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества общих друзей.
    :param progress: Callback для отображения прогресса.
    """
    start = Session(VK_CONFIG["domain"])
    all_friends = []
    if target_uids:
        for i in range(((len(target_uids) - 1) // 100) + 1):
            try:
                mutual_friends = start.get("friends.getMutual",
                                           params={"access_token": VK_CONFIG["access_token"],
                                                   "v": VK_CONFIG["version"],
                                                   "source_uid": source_uid,
                                                   "target_uid": target_uid,
                                                   "target_uids": ','.join(list(map(str, target_uids))),
                                                   "order": order,
                                                   "count": 100,
                                                   "offset": i * 100})
                for friend in mutual_friends.json()['response']:
                    all_friends.append(
                        MutualFriends(id=friend['id'], common_friends=list(map(int, friend['common_friends'])),
                                      common_count=friend['common_count']))
            except:
                pass
            time.sleep(0.5)
        return all_friends
    try:
        mutual_friends = start.get("friends.getMutual", params={"access_token": VK_CONFIG["access_token"],
                                                                "v": VK_CONFIG["version"],
                                                                "source_uid": source_uid,
                                                                "target_uid": target_uid,
                                                                "target_uids": target_uids,
                                                                "order": order,
                                                                "count": count,
                                                                "offset": offset})
        all_friends.extend(mutual_friends.json()['response'])
    except:
        pass
    return all_friends


if __name__ == "__main__":
    friends = get_friends(user_id=250240920).items
    print(friends)
    print(get_mutual(250240920, target_uids=[136475]))