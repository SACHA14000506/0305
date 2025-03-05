import src.utils as utils
import sys, os, random, time
from gen import mk_gen
import pandas as pd
import src.settings as settings
import datetime

class Fuzzer:
    def __init__(self, parameter):
        self.init_time = parameter.time0
        self.time0 = parameter.time0
        self.it = 0
        self.find = False
        self.num_mutations = 10  # 每个种子变异20次
        self.start_pop = settings.FuzzerNumberPopulationStart
        self.num_pop = 100  # 初始种群大小为100
        self.num_keep = settings.FuzzerNumberOfHardestKept  # 选择保留的个体数量
        self.mutation_rate = 0.5  # 突变概率
        self.max_iterations = 100  # 最大迭代次数
        self.gen = mk_gen()  # 初始化实例生成器
        self.all_solved = set()  # 存储已解决的实例
        self.pop = []  # 种群列表
        self.all_achived = set()  # 存储成功实例

    def initialize_population(self):
        """
        初始化种群，生成100个种子。
        """
        print("Initializing population...\n")
        for i in range(self.num_pop):
            inst = self.gen.gen()  # 生成实例

            while str(inst) in self.all_solved:  # 确保实例是新的
                inst = self.gen.gen()
            inst.solve()
            self.pop.append(inst)  # 添加到种群
            self.print_instance_info(i, "Initial Pop", inst)
            self.all_solved.add(str(inst))  # 记录已解决实例

    def print_instance_info(self, index, label, inst):
        """
        打印实例信息。
        """
        print("(%d/%-d)%-15sTimes = %-25s Score = %-7f IsSat = %-25s" % (
            index + 1, self.num_pop, label, utils.roundedmap(inst.times, 3), inst.score(), inst.results,
            ))
        print("score:", inst._score)

    def fitness_function(self, inst):
        """
        计算个体的适应度，使用实例的得分。
        """
        return inst._score()  # 示例中使用实例自带的 score 方法

    def mutate(self, individual):
        """
        对个体进行突变操作，确保突变后的个体未被求解过。
        """
        while True:
            mutated = self.gen.mutate(individual)
            if str(mutated) not in self.all_solved:
                mutated.solve()  # 对突变后的个体进行求解
                self.all_solved.add(str(mutated))
                break
            else:
                print("Retry! Mutated individual already solved.")
        return mutated

    def pick(self, pop):
        """
        查找符合条件的个体，如果找到则保存并生成文件。
        """
        is_find = False
        for i in range(len(pop)):
            if pop[i]._score >= 5:
                is_find = True
                if str(pop[i].primaries) not in self.all_achived:
                    settings.reg_num += 1
                    utils.generate_file(pop[i].primaries,
                                        settings.reg_path, settings.mode + str(settings.reg_num) + '.smt2')
                    settings.file_num += 1
                    df1 = pd.DataFrame({
                        'File': [settings.mode + str(settings.reg_num) + '.smt2'],
                        'Solver1_Time': [pop[i].times[settings.solvers[0]]],
                        'Solver2_Time': [pop[i].times[settings.solvers[1]]],
                        'Solver3_Time': [pop[i].times[settings.solvers[2]]],
                        'Time': [datetime.datetime.now().strftime("%Y-%m-%d %H:%M")]
                    })
                    df1.to_csv('./Results.csv', mode='a', header=False, index=False)
                    pop[i] = self.gen.gen()  # 生成新的实例
                    pop[i].solve()
                    settings.found_time_list.append(
                        [pop[i].times[settings.solvers[0]],
                         pop[i].times[settings.solvers[1]], pop[i].times[settings.solvers[2]]])
        return pop, is_find

    def evolve(self):
        """
        进化过程，每个种子变异20次，取分数最高的作为下一代种子。
        """
        iteration = 0
        print("Evolving population...")

        while iteration < self.max_iterations:
            iteration += 1
            print("----------------------------------------------------------------------------------")
            print(f"Iteration: {iteration}/{self.max_iterations}")
            print("----------------------------------------------------------------------------------")

            next_generation = []
            for individual in self.pop:
                # 对每个种子进行20次变异
                mutants = []
                for mutation_count in range(self.num_mutations):
                    mutated = self.mutate(individual)
                    print(f"第{iteration}轮，第{mutation_count + 1}次变异得分:",mutated.score())
                    mutants.append(mutated)
    
                # 从20个变异体中选择分数最高的作为下一代种子
                if mutants:

                    best_mutant = max(mutants, key=lambda x: x._score)
                    # 输出最佳变异体及其score
                    print(f"第{iteration}轮，最佳score：Score = {best_mutant._score}")
                    next_generation.append(best_mutant)

            # 更新种群
            self.pop = next_generation[:self.num_pop]

            # 查找目标并更新种群
            self.pop, is_find = self.pick(self.pop)

            # 记录并输出每一代的种群信息
            for j, inst in enumerate(self.pop):
                inst.solve()
                self.print_instance_info(j, "Rand", inst)

    def run(self):
        """
        运行模糊测试器。
        """
        print("Starting Fuzzer...")
        self.initialize_population()  # 初始化种群
        self.evolve()  # 运行进化过程
