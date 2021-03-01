# -*- coding: utf-8 -*-
import utils.robotdata as robotdata
import random


class NameWidget():
    def __init__(self):
        self.name = ""
        self.shape = 1

    def RandomCreateAge(self):
        age = 18
        new_age = random.randint(18, 40)
        return new_age

    def RandomCreatePwd(self):
        tt = ""
        for i in range(1,6+1):
            idx = random.randint(1, 9);
            tt += str(idx)
        return tt

    def RandomCreateUg(self):

        new_ug_id = random.randint(1,5)
        return new_ug_id



    def RandomCreateName(self):
        idx = random.randint(1, 100);
        if idx >= 1 and idx <= 35:  # 0:35%概率:A+B
            self.RandomSelChar(0);
        elif idx >= 36 and idx <= 50:  # 1:15%概率:C+A+B
            self.RandomSelChar(1);
        elif idx >= 51 and idx <= 70:  # 2:20%概率:A+C+B
            self.RandomSelChar(2);
        elif idx >= 71 and idx <= 79:  # 3:9%概率:A+B+C
            self.RandomSelChar(3);
        elif idx >= 80 and idx <= 90:  # 4:11%概率:C+A+B+C
            self.RandomSelChar(4);
        elif idx >= 91 and idx <= 93:  # 5:3%概率:C+A+C+B
            self.RandomSelChar(5);
        elif idx >= 94 and idx <= 96:  # 6:3%概率:A+C+B+C
            self.RandomSelChar(6);
        else:  # 7:4%概率:C+A+C+B+C
            self.RandomSelChar(7);

        return self.name

    def RandomSelChar(self, nSel):
        self.shape = random.randint(1, 2);
        self.name = '';
        sex = '男'
        if self.shape % 2 == 0:
            sex = '女'
        val = None;
        lenMA = len(robotdata.RANDOMNAME_DATA_DICT['MA'])
        lenMB = len(robotdata.RANDOMNAME_DATA_DICT['MB'])
        lenWA = len(robotdata.RANDOMNAME_DATA_DICT['WA'])
        lenWB = len(robotdata.RANDOMNAME_DATA_DICT['WB'])
        lenC = len(robotdata.RANDOMNAME_DATA_DICT['C'])
        if lenMA <= 0 or lenMB <= 0 or lenWA <= 0 or lenWB <= 0 or lenC <= 0:
            return;
        if nSel == 0:  # 0:35%概率:A+B
            if sex == '男':
                idx1 = random.randint(0, lenMA - 1);
                idx2 = random.randint(0, lenMB - 1);
                self.name += robotdata.RANDOMNAME_DATA_DICT['MA'][idx1];
                self.name += robotdata.RANDOMNAME_DATA_DICT['MB'][idx2];
            else:
                idx1 = random.randint(0, lenWA - 1);
                idx2 = random.randint(0, lenWB - 1);
                self.name += robotdata.RANDOMNAME_DATA_DICT['WA'][idx1];
                self.name += robotdata.RANDOMNAME_DATA_DICT['WB'][idx2];
            self.set_name_lone();
        elif nSel == 1:  # 2:20%概率:A+C+B
            if sex == '男':
                idx1 = random.randint(0, lenC - 1);
                idx2 = random.randint(0, lenMA - 1);
                idx3 = random.randint(0, lenMB - 1);
                self.name += robotdata.RANDOMNAME_DATA_DICT['C'][idx1];
                self.name += robotdata.RANDOMNAME_DATA_DICT['MA'][idx2];
                self.name += robotdata.RANDOMNAME_DATA_DICT['MB'][idx3];
            else:
                idx1 = random.randint(0, lenC - 1);
                idx2 = random.randint(0, lenWA - 1);
                idx3 = random.randint(0, lenWB - 1);
                self.name += robotdata.RANDOMNAME_DATA_DICT['C'][idx1];
                self.name += robotdata.RANDOMNAME_DATA_DICT['WA'][idx2];
                self.name += robotdata.RANDOMNAME_DATA_DICT['WB'][idx3];
            self.set_name_lone();
        elif nSel == 2:  # 2:20%概率:A+C+B
            if sex == '男':
                idx1 = random.randint(0, lenMA - 1);
                idx2 = random.randint(0, lenC - 1);
                idx3 = random.randint(0, lenMB - 1);
                self.name += robotdata.RANDOMNAME_DATA_DICT['MA'][idx1];
                self.name += robotdata.RANDOMNAME_DATA_DICT['C'][idx2];
                self.name += robotdata.RANDOMNAME_DATA_DICT['MB'][idx3];
            else:
                idx1 = random.randint(0, lenWA - 1);
                idx2 = random.randint(0, lenC - 1);
                idx3 = random.randint(0, lenWB - 1);
                self.name += robotdata.RANDOMNAME_DATA_DICT['WA'][idx1];
                self.name += robotdata.RANDOMNAME_DATA_DICT['C'][idx2];
                self.name += robotdata.RANDOMNAME_DATA_DICT['WB'][idx3];
            self.set_name_lone();
        elif nSel == 3:  # 3:9%概率:A+B+C
            if sex == '男':
                idx1 = random.randint(0, lenMA - 1);
                idx2 = random.randint(0, lenMB - 1);
                idx3 = random.randint(0, lenC - 1);
                self.name += robotdata.RANDOMNAME_DATA_DICT['MA'][idx1];
                self.name += robotdata.RANDOMNAME_DATA_DICT['MB'][idx2];
                self.name += robotdata.RANDOMNAME_DATA_DICT['C'][idx3];
            else:
                idx1 = random.randint(0, lenWA - 1);
                idx2 = random.randint(0, lenWB - 1);
                idx3 = random.randint(0, lenC - 1);
                self.name += robotdata.RANDOMNAME_DATA_DICT['WA'][idx1];
                self.name += robotdata.RANDOMNAME_DATA_DICT['WB'][idx2];
                self.name += robotdata.RANDOMNAME_DATA_DICT['C'][idx3];
            self.set_name_lone();
        elif nSel == 4:  # 4:11%概率:C+A+B+C
            if sex == '男':
                idx1 = random.randint(0, lenC - 1);
                idx2 = random.randint(0, lenMA - 1);
                idx3 = random.randint(0, lenMB - 1);
                idx4 = random.randint(0, lenC - 1);
                self.name += robotdata.RANDOMNAME_DATA_DICT['C'][idx1];
                self.name += robotdata.RANDOMNAME_DATA_DICT['MA'][idx2];
                self.name += robotdata.RANDOMNAME_DATA_DICT['MB'][idx3];
                self.name += robotdata.RANDOMNAME_DATA_DICT['C'][idx4];
            else:
                idx1 = random.randint(0, lenC - 1);
                idx2 = random.randint(0, lenWA - 1);
                idx3 = random.randint(0, lenWB - 1);
                idx4 = random.randint(0, lenC - 1);
                self.name += robotdata.RANDOMNAME_DATA_DICT['C'][idx1];
                self.name += robotdata.RANDOMNAME_DATA_DICT['WA'][idx2];
                self.name += robotdata.RANDOMNAME_DATA_DICT['WB'][idx3];
                self.name += robotdata.RANDOMNAME_DATA_DICT['C'][idx4];
            if len(self.name) > 14:
                self.name = self.name[0: 14];
        elif nSel == 5:  # 5:3%概率:C+A+C+B
            if sex == '男':
                idx1 = random.randint(0, lenC - 1);
                idx2 = random.randint(0, lenMA - 1);
                idx3 = random.randint(0, lenC - 1);
                idx4 = random.randint(0, lenMB - 1);
                self.name += robotdata.RANDOMNAME_DATA_DICT['C'][idx1];
                self.name += robotdata.RANDOMNAME_DATA_DICT['MA'][idx2];
                self.name += robotdata.RANDOMNAME_DATA_DICT['C'][idx3];
                self.name += robotdata.RANDOMNAME_DATA_DICT['MB'][idx4];
            else:
                idx1 = random.randint(0, lenC - 1);
                idx2 = random.randint(0, lenWA - 1);
                idx3 = random.randint(0, lenC - 1);
                idx4 = random.randint(0, lenWB - 1);
                self.name += robotdata.RANDOMNAME_DATA_DICT['C'][idx1];
                self.name += robotdata.RANDOMNAME_DATA_DICT['WA'][idx2];
                self.name += robotdata.RANDOMNAME_DATA_DICT['C'][idx3];
                self.name += robotdata.RANDOMNAME_DATA_DICT['WB'][idx4];
            if len(self.name) > 14:
                self.name = self.name[0: 14];
        elif nSel == 6:  # 6:3%概率:A+C+B+C
            if sex == '男':
                idx1 = random.randint(0, lenMA - 1);
                idx2 = random.randint(0, lenC - 1);
                idx3 = random.randint(0, lenMB - 1);
                idx4 = random.randint(0, lenC - 1);
                self.name += robotdata.RANDOMNAME_DATA_DICT['MA'][idx1];
                self.name += robotdata.RANDOMNAME_DATA_DICT['C'][idx2];
                self.name += robotdata.RANDOMNAME_DATA_DICT['MB'][idx3];
                self.name += robotdata.RANDOMNAME_DATA_DICT['C'][idx4];
            else:
                idx1 = random.randint(0, lenWA - 1);
                idx2 = random.randint(0, lenC - 1);
                idx3 = random.randint(0, lenWB - 1);
                idx4 = random.randint(0, lenC - 1);
                self.name += robotdata.RANDOMNAME_DATA_DICT['WA'][idx1];
                self.name += robotdata.RANDOMNAME_DATA_DICT['C'][idx2];
                self.name += robotdata.RANDOMNAME_DATA_DICT['WB'][idx3];
                self.name += robotdata.RANDOMNAME_DATA_DICT['C'][idx4];
            if len(self.name) > 14:
                self.name = self.name[0: 14];
        elif nSel == 7:  # 7:4%概率:C+A+C+B+C
            if sex == '男':
                idx1 = random.randint(0, lenC - 1);
                idx2 = random.randint(0, lenMA - 1);
                idx3 = random.randint(0, lenC - 1);
                idx4 = random.randint(0, lenMB - 1);
                idx5 = random.randint(0, lenC - 1);
                self.name += robotdata.RANDOMNAME_DATA_DICT['C'][idx1];
                self.name += robotdata.RANDOMNAME_DATA_DICT['MA'][idx2];
                self.name += robotdata.RANDOMNAME_DATA_DICT['C'][idx3];
                self.name += robotdata.RANDOMNAME_DATA_DICT['MB'][idx4];
                self.name += robotdata.RANDOMNAME_DATA_DICT['C'][idx5];
            else:
                idx1 = random.randint(0, lenC - 1);
                idx2 = random.randint(0, lenWA - 1);
                idx3 = random.randint(0, lenC - 1);
                idx4 = random.randint(0, lenWB - 1);
                idx5 = random.randint(0, lenC - 1);
                self.name += robotdata.RANDOMNAME_DATA_DICT['C'][idx1];
                self.name += robotdata.RANDOMNAME_DATA_DICT['WA'][idx2];
                self.name += robotdata.RANDOMNAME_DATA_DICT['C'][idx3];
                self.name += robotdata.RANDOMNAME_DATA_DICT['WB'][idx4];
                self.name += robotdata.RANDOMNAME_DATA_DICT['C'][idx5];
            self.set_name_lone();
        return;

    def set_name_lone(self):
        if len(self.name) > 16:
            self.name = self.name[2: 16];
        elif len(self.name) > 14:
            self.name = self.name[0: 14];
        return

class PageInfo(object):
    def __init__(self,current_page,all_count,base_url,per_page,show_page = 11):
        try:
            self.current_page = int(current_page)
        except Exception as e:
            self.current_page = 1
        self.per_page = per_page

        a,b = divmod(all_count,per_page)
        if b:
            a = a+1

        self.all_paper = a

        self.show_page = show_page

        self.base_url = base_url

    def start(self):
        return (self.current_page - 1) * self.per_page

    def end(self):
        return self.current_page * self.per_page

    def pager(self):
        v = "<a style='display:inline-block; padding:5px; margin:5px' href='/user/custom/?page=1'>1</a>"

        # 如果数据库的总页数 < 11:
        page_list = []
        begin = 0
        stop = 0

        if self.all_paper < self.show_page:
            begin = 1
            stop = self.all_paper + 1
        else:
            half = int((self.show_page - 1)/2)
            #
            # begin = max(self.current_page - 5, 1)
            # stop = min(self.current_page + 5 +1,self.all_paper + 1)

            # 如果当前页 <= 5 永远显示 1-11
            if self.current_page <= half:
                begin = 1
                stop = self.show_page + 1
            else:
                if self.current_page + half > self.all_paper:
                    begin = self.all_paper - self.show_page + 1
                    stop = self.all_paper + 1
                else:
                    begin = self.current_page - half
                    stop = self.current_page + half + 1
                    # print ("keke2222:%s,%s"%(begin,stop))
        prev = ""
        if self.current_page <= 1:
            # prev = "<a style='display:inline-block; padding:5px; margin:5px;' href='#'>上一页</a>"
            prev = "<li><a href='#'>上一页</a><li>"
        else:
            # prev = "<a style='display:inline-block; padding:5px; margin:5px;' href='%s/?page=%s'>上一页</a>" % (self.base_url,self.current_page - 1)
            prev = "<li><a href='%s/?page=%s'>上一页</a><li>"% (self.base_url,self.current_page - 1)
        page_list.append(prev)

        for i in range(begin,stop):
            if i == self.current_page:
                # temp = "<a style='display:inline-block; padding:5px; margin:5px; background-color:red;' href='%s/?page=%s'>%s</a>"%(self.base_url,i,i)
                temp = "<li class='active'><a  href='%s/?page=%s'>%s</a><li>" % (
                self.base_url, i, i)
            else:
                # temp = "<a style='display:inline-block; padding:5px; margin:5px;' href='/user/custom/?page=%s'>%s</a>" % (i, i)
                temp = "<li><a href='%s/?page=%s'>%s</a><li>" % ( self.base_url,
                i, i)
            page_list.append(temp)

        next = ""
        if self.current_page >= self.all_paper:
            # next = "<a style='display:inline-block; padding:5px; margin:5px;' href='#'>下一页</a>"
            next = "<li><a href='#'>下一页</a></li>"
        else:
            next = "<li><a href='%s/?page=%s'>下一页</a><li>" % ( self.base_url,self.current_page + 1)
        page_list.append(next)



        return "".join(page_list)





