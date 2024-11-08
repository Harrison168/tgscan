from datetime import datetime

INSERT_ROOM_QUERY = """
INSERT INTO room_v2 (room_id, link, name, jhi_desc, member_cnt, msg_cnt, type, status, collected_at, lang, tags, extra)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (room_id) DO UPDATE SET
    link = EXCLUDED.link,
    name = EXCLUDED.name,
    jhi_desc = EXCLUDED.jhi_desc,
    member_cnt = EXCLUDED.member_cnt,
    msg_cnt = EXCLUDED.msg_cnt,
    type = EXCLUDED.type,
    collected_at = EXCLUDED.collected_at,
    lang = EXCLUDED.lang,
    tags = EXCLUDED.tags,
    extra = EXCLUDED.extra
RETURNING id;
"""

CHECK_ROOM_EXISTS_QUERY = "SELECT link FROM room_v2 WHERE link IN %s"

def prepare_room_data(item):
    # 将 chat_id 作为 room_id
    room_id = item.get('chat_id')
    
    # 将 title 作为 name
    name = item.get('title')
    
    # 使用 description 作为 jhi_desc
    jhi_desc = item.get('description')
    
    # 使用 count 作为 member_cnt
    member_cnt = item.get('count')
    
    # 我们没有直接对应的 msg_cnt，可以设为 None 或 0
    msg_cnt = None
    
    # 使用 chat_type 作为 type
    type = item.get('chat_type')
    
    # 将 status 转换为字符串
    status = str("NEW")
    
    # 使用 update_time 作为 collected_at，需要转换为 datetime 对象
    collected_at = datetime.strptime(item.get('update_time'), "%Y-%m-%d %H:%M:%S")
    
    # 使用 language 作为 lang
    lang = item.get('language')
    
    # 我们没有直接对应的 tags，可以留空
    tags = ''
    
    # 将其他不直接映射的字段放入 extra
    extra = {
        # 'id': item.get('id'),
        # 'username': item.get('username'),
        # 'photo': item.get('photo'),
        # 'click': item.get('click'),
        # 'weight': item.get('weight'),
        # 'is_read': item.get('is_read'),
        # 'bot': item.get('bot'),
        # 'create_time': item.get('create_time')
    }
    extra = str(extra)  # 将字典转换为字符串

    return (
        room_id,
        item.get('link'),
        name,
        jhi_desc,
        member_cnt,
        msg_cnt,
        type,
        status,
        collected_at,
        lang,
        tags,
        extra
    )
