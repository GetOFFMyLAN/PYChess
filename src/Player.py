from Pieces import King


class Player:
    p_name = ''
    p_id = -1
    p_team = ''
    p_king = None

    def __init__(self, name, _id, team, king_obj):
        self.p_name = name
        self.p_id = _id
        self.p_team = team
        self.p_king = king_obj

    def get_name(self):
        return self.p_name

    def get_id(self):
        return self.p_id

    def get_team(self):
        return self.p_team

    def get_king(self):
        return self.p_king

    def set_king(self, obj):
        self.p_king = obj
