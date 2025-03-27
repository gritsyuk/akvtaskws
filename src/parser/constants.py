from enum import Enum, IntEnum

MAX_CONCURRENT_REQUESTS = 10


class ApprovalStatus(str, Enum):
    APPROVAL = 'Согласование'
    APPROVED = 'Согласован'
    REJECTED = 'Отказано'
    CANCELLED = 'Анулирован'

    def __str__(self):
        return self.value


class UserStatusApproval(IntEnum):
    NOT_MARKED = 0
    YES = 1
    YES_WITH_COMMENTS = 2
    NO = 3


CONSTARCTION = {
    'Аквилон Park': {
        "pattern": r'park|парк|сосенское|коммунарка',
        "buildings": [{'name_allio': 'Аквилон Парк 1 очередь', 'name_building': 'С1-9', 'task_building_id': 59}]
    },
    'Митино': {
        "pattern": r'митино',
        "buildings": [
            {'name_allio': 'Аквилон Митино 1 корпус', 'name_building': 'К16', 'task_building_id': 88},
            {'name_allio': 'Аквилон Митино 2 корпус', 'name_building': 'К16.1', 'task_building_id': 89},
            {'name_allio': 'Аквилон Митино 3 корпус', 'name_building': 'К17', 'task_building_id': 90},
            {'name_allio': 'Аквилон Митино 4 корпус', 'name_building': 'К18', 'task_building_id': 113},
            {'name_allio': None, 'name_building': 'ДОО', 'task_building_id': None},
            {'name_allio': None, 'name_building': 'Г17', 'task_building_id': None}]
    },
    'Beside 1': {
        "pattern": r'beside|бисайд 1|рязанка',
        "buildings": [
            {'name_allio': 'Аквилон BESIDE 1 очередь 1 корпус', 'name_building': 'К1', 'task_building_id': 98},
            {'name_allio': 'Аквилон BESIDE 1 очередь 2 корпус', 'name_building': 'К2', 'task_building_id': 99}
            ]
    },
    'Beside Школа': {
        "pattern": r'школа|825',
        "buildings": [{'name_allio': None, 'name_building': 'Школа на 825 мест', 'task_building_id': None}]
    },
    'Indy Towers': {
        "pattern": r'indy|towers|куусинена',
        "buildings":[
            {'name_allio': 'Indy Towers by Akvilon 1 очередь A корпус', 'name_building': 'Корпус А', 'task_building_id': 144},
            {'name_allio': 'Indy Towers by Akvilon 1 очередь C корпус', 'name_building': 'Корпус С', 'task_building_id': 145},
            {'name_allio': 'Indy Towers by Akvilon 1 очередь B корпус', 'name_building': 'Корпус B', 'task_building_id': 146}]
    },
    'Beside 2': {
        "pattern": r'beside 2|бисайд 2',
        "buildings": [{'name_allio': 'Аквилон BESIDE 2.0 2 очередь 1 корпус', 'name_building': '', 'task_building_id': 163}]
    },
    'Signal': {
        "pattern": r'signal|сигнальн(?:ый|ая)|сигнал',
        "buildings": [
            {'name_allio': 'Аквилон SIGNAL 1 (for life) корпус', 'name_building': '', 'task_building_id': 167 },
            {'name_allio': 'Аквилон SIGNAL 2 (for life) корпус', 'name_building': '', 'task_building_id': 168},
            {'name_allio': 'Аквилон SIGNAL 3 (for business) корпус', 'name_building': '', 'task_building_id': 169},
            {'name_allio': 'Аквилон SIGNAL 4 (for business) корпус', 'name_building': '', 'task_building_id': 170}],
    },
    'Ярцевская': {
        "pattern": r'ярцев(?:ская|о)',
        "buildings": [{'name_allio': None, 'name_building': None, 'task_building_id': None}],
    },
    'Жуков': {
        "pattern": r'жуков',
        "buildings": [{'name_allio': None, 'name_building': None, 'task_building_id': None}],
    },
    'Нагорный проезд': {
        "pattern": r'нагорн',
        "buildings": [{'name_allio': None, 'name_building': None, 'task_building_id': None}],
    },
    'Валуево': {
        "pattern": r'валуев',
        "buildings": [{'name_allio': None, 'name_building': None, 'task_building_id': None}],
    },
    'Теплый стан': {
        "pattern": r'теплый стан|крт',
        "buildings": [{'name_allio': None, 'name_building': None, 'task_building_id': None}],
    }
}
