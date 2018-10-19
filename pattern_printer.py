class Paper:
    blank_char = " "
    line_sep_char = "\n"
    end_with_sep = False
    initial_position = [1, 1]
    is_editing_list = False
    auto_clean_blank = True
    use_default_settings = True
    paperdict = dict()
    paperlist = list()

    def __init__(self,
                 paperdict=None,
                 paperlist=None,
                 default_settings=None,
                 blank_char=" ",
                 line_sep_char="\n",
                 end_with_sep=False,
                 initial_position=None,
                 is_editing_list=False,
                 auto_clean_blank=True,
                 use_default_settings=True):
        self.paperdict = dict() if paperdict is None else paperdict
        self.paperlist = list() if paperlist is None else paperlist
        if default_settings is None:
            default_settings = self.use_default_settings
        if default_settings:
            self.default()
        # print(self, "initialized")

    def clear(self):
        self.paperlist.clear()
        self.paperdict.clear()

    def default(self):
        self.is_editing_list = False
        self.auto_clean_blank = True
        self.blank_char = " "
        self.line_sep_char = "\n"
        self.end_with_sep = False
        self.initial_position = [1, 1]

    def sync2dict(self):
        self.paperdict.clear()
        for charpoint in self.paperlist:
            self.paperdict[tuple(charpoint[0])] = str(charpoint[1])
        if self.auto_clean_blank:
            while self.blank_char in self.paperdict:
                self.paperdict.pop(self.blank_char)

    def switch2dict(self, nosync=False, force=False):
        if (not nosync) and (self.is_editing_list or force):
            self.sync2dict()
        self.is_editing_list = False

    def sync2list(self):
        self.paperlist = [
            [list(key), self.paperdict[key]]
            for key in self.paperdict.keys()]
        self.paperlist.sort()

    def switch2list(self, nosync=False, force=False):
        if (not nosync) and ((not self.is_editing_list) or force):
            self.sync2list()
        self.is_editing_list = True

    def fresh(self):
        if self.is_editing_list:
            self.switch2dict()
            self.switch2list()
        else:
            self.switch2list()
            self.switch2dict()

    def edge(self, horizontal, fmm):
        return fmm(key[horizontal] for key in self.paperdict.keys())

    def right(self):  # used in the square option of sprint
        return self.edge(1, max)

    def left(self):
        return self.edge(1, min)

    def down(self):
        return self.edge(0, max)

    def up(self):
        return self.edge(0, min)

    def sprint(self, fill_right=False, no_change=False, right_min=0):
        if no_change:
            from copy import deepcopy
            papertemp = deepcopy(self)
            return papertemp.sprint(fill_right=fill_right,
                                    no_change=False,
                                    right_min=right_min)
        strout = ""
        # ADDRESS PROBLEM, A MATTER OF SAFTY
        position_now = self.initial_position.copy()
        self.fresh()
        self.switch2dict()
        if fill_right:
            right_min = self.right()
        for k in self.paperdict.keys():
            if k[0] > position_now[0]:
                strout += (self.blank_char *
                           max(right_min - position_now[0], 0) +
                           self.line_sep_char)
                position_now[0] += 1
                strout += ((self.blank_char*right_min +
                            self.line_sep_char) *
                           (k[0]-position_now[0]))
                position_now = [k[0], self.initial_position[1]]
            if k[0] == position_now[0] and k[1] > position_now[1]:
                strout += self.blank_char*(k[1]-position_now[1])
                position_now[1] = k[1]
            strout += str(self.paperdict[k])
            position_now[1] += 1
        if self.end_with_sep:
            strout += self.line_sep_char
        return strout

    # extra functions
    def translate(self, vector, stay_in_list=False):
        was_editing_list = self.is_editing_list
        self.switch2list()
        self.paperlist = [
            [[point[0][0]+vector[0], point[0][1]+vector[1]],
             point[1]]
            for point in self.paperlist]
        if stay_in_list and not was_editing_list:
            self.switch2dict()

    def translated(self, vector, stay_in_list=False):
        from copy import deepcopy
        paperout = deepcopy(self)
        paperout.translate(vector, stay_in_list=False)
        return paperout


"""
paper1 = Paper()
paper1.paperdict[(4, 5)] = "3"
#paper1.translate([-1, -3])
print(paper1.sprint())
"""
