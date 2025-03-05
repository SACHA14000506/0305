import os, random, time
import src.settings as settings
from smtlib.script import SMTLIBScript
from src.solver import run_solver
import pandas as pd
# from src.parser import args

def par2(x):
    if x < settings.timeout:
        return x
    else:
        return settings.timeout


def generate_file(ast, path, name):
    # with open(path, 'w+') as file:
    if not os.path.exists(path):
        os.mkdir(path)
    file = open(os.path.join(path, name), 'w+')
    file.write(ast)
    file.close()


class Instance(SMTLIBScript):
    def __init__(self, val=None, statistics=None):
        if settings.theory == 'QF_S' or settings.theory == 'QF_SLIA':
            assert isinstance(val, str)  # 如果理论是 QF_S 或 QF_SLIA，val 必须是字符串
        else:
            assert isinstance(val, list)  # 否则，val 必须是列表
        super().__init__()  # 调用父类的初始化方法
        self.primaries = val  # 将 val 作为实例的主要数据
        self.times = {}  # 初始化一个空字典，用于记录时间相关信息
        self.results = {}  # 初始化一个空字典，用于存储结果
        self.name = str(time.time()).replace(".", "") + str(os.getpid()) + str(random.randint(0, 99999999)) + ".smt2"
        # 生成唯一文件名，包括时间戳、进程 ID 和随机数，后缀为 .smt2
        self.err_log = {}  # 初始化一个空字典，用于记录错误日志
        self._score = None  # 初始化评分为 None
        self.time_list = [0, 0, 0]  # 初始化一个包含三个时间统计的列表

    def solve(self):

        for solver in settings.solvers:
            out, time, dump = run_solver(self, solver, settings.mode)
            settings.average_time[0] +=1
            self.results[solver] = out
            self.times[solver] = par2(time)
            if out == 'err': self.err_log[solver] = dump
        return settings.average_time

    # if len(self.err_log) > 0:
    # 	self.to_file(settings.db + '/crashes/')

    def score(self):
        if self._score != None: return self._score
        if self.inconsistent():
            self._score = par2(self.times[settings.solvers[0]]) - min(
                [par2(self.times[solver]) for solver in settings.solvers if solver != settings.solvers[0]])
        elif settings.BugMode:
            self._score = -9.9
        elif len(self.err_log) > 0:
            self._score = 0.0
        elif len(self.times) == 1:
            self._score = par2(self.times[settings.solvers[0]]) if settings.solvers[0] not in self.err_log else float(
                '-inf')
        else:
            # print('111111solvers:', settings.solvers)
            # print(f"Recorded times: {self.times}")

            self._score = par2(self.times[settings.solvers[0]]) - min([par2(self.times[solver]) for solver in settings.solvers if solver != settings.solvers[0]])
        return self._score

    def __lt__(self, other):
        return self.score() < other.score()

    def __str__(self):
        return self.primaries

    __repr__ = __str__

    def inconsistent(self):
        for solver in self.results:
            clean = ""
            for i in range(len(self.results[solver])):
                if self.results[solver][i].isalpha():
                    clean = clean + self.results[solver][i]
            self.results[solver] = clean
        ans = ""
        says_sat = False
        says_unsat = False
        for solver in self.results:
            if self.results[solver] == "sat":
                says_sat = True
            if self.results[solver] == "unsat":
                says_unsat = True
        return says_sat and says_unsat

