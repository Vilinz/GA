import random
import matplotlib.pyplot as plt


class GA:
    def __init__(self):
        self.city = {}
        self.population_size = 100
        self.city_size = 101
        self.population = []
        self.point = 0
        self.percent = 0.2

        self.ax = 0

    def init_point(self):
        plt.ion()
        fig = plt.figure()
        self.ax = fig.add_subplot(111)
        self.ax.set_title("GA")

        for c in self.city:
            plt.scatter(self.city[c][0], self.city[c][1], color='r', linewidths=2, marker=".")

    def read_file(self):
        f = open('kroA200')
        count = 0
        for line in f.readlines():
            if count == 0:
                count += 1
                self.point = int(line.strip())
                continue
            if line.strip() != 'EOF':
                print(line.strip())
                str = line.strip().split(' ')
                index = int(str[0])
                x = int(str[1])
                y = int(str[2])
                point = [x, y]
                self.city[index] = point
        f.close()
        print("Read file end", len(self.city))

    def path_cost(self, path):
        cost = 0
        for i in range(1, self.point):
            sub_x = self.city[path[i]][0] - self.city[path[i-1]][0]
            sub_y = self.city[path[i]][1] - self.city[path[i-1]][1]
            dis = pow((sub_x*sub_x + sub_y*sub_y), 0.5)
            cost += dis

        sub_x = self.city[path[0]][0] - self.city[path[self.point - 1]][0]
        sub_y = self.city[path[0]][1] - self.city[path[self.point - 1]][1]
        dis = pow((sub_x*sub_x + sub_y*sub_y), 0.5)
        cost += dis
        return cost

    def update(self, cost, gen):
        x = []
        y = []
        self.ax.lines = []
        self.ax.set_title("GA   " + "cost: " + str(cost) + "    generation: " + str(gen))

        for i in self.population[0]:
            x.append(self.city[i][0])
            y.append(self.city[i][1])

        for i in range(0, self.point - 1):
            plt.plot((x[i], x[i+1]), (y[i], y[i+1]), color='b')

        plt.plot((x[self.point - 1], x[0]), (y[self.point - 1], y[0]), color='b')

        plt.draw()
        plt.pause(0.0001)
        plt.show()

    def init_population(self):

        temp = list(range(1, self.point + 1))
        current = [temp[0]]
        del temp[0]
        while len(current) < self.point:
            min = 100000000
            index = 0
            for i in range(len(temp)):
                current_index = current[len(current) - 1]
                sub_x = self.city[temp[i]][0] - self.city[current_index][0]
                sub_y = self.city[temp[i]][1] - self.city[current_index][1]
                dis = pow((sub_x * sub_x + sub_y * sub_y), 0.5)
                if dis < min:
                    index = i
                    min = dis
            current.append(temp[index])
            del temp[index]
        self.population.append(current)

        p = int(self.population_size*self.percent)

        for i in range(p - 1):
            tag = True
            new_path = current.copy()
            while tag:
                ran1 = random.randint(0, self.point - 1)
                ran2 = random.randint(0, self.point - 1)
                if ran1 == ran2:
                    continue
                tag = False
                if ran1 > ran2:
                    temp = ran1
                    ran1 = ran2
                    ran2 = temp
                j = ran1
                while j <= ran2:
                    new_path[ran2 - (j - ran1)] = current[j]
                    j += 1
                # t = new_path[ran1]
                # new_path[ran1] = new_path[ran2]
                # new_path[ran2] = t
            self.population.append(new_path)
            print('cost ', self.path_cost(new_path))

        i = p - 1
        while i < self.population_size:
            i += 1
            new_path = current.copy()
            random.shuffle(new_path)
            self.population.append(new_path)

        print('current ', current)
        print('cost ', self.path_cost(current))
        print(len(self.population))

    def find(self, value, start, end, array):
        while start <= end:
            if value == array[start]:
                return True
            start += 1
        return False

    def local_search(self):
        for i in range(int(self.population_size/2)):
            r = random.randint(0, self.population_size - 1)
            tag = True
            new_path = []
            while tag:
                ran1 = random.randint(1, self.point - 2)
                ran2 = random.randint(1, self.point - 2)
                if ran1 == ran2:
                    continue
                tag = False
                new_path = self.population[r].copy()
                if ran1 > ran2:
                    temp = ran1
                    ran1 = ran2
                    ran2 = temp
                j = ran1
                while j <= ran2:
                    new_path[ran2 - (j - ran1)] = self.population[r][j]
                    j += 1
            if self.path_cost(self.population[r]) > self.path_cost(new_path):
                self.population[r] = new_path.copy()

    def selection_crosscover(self, g):
        temp_population = self.population.copy()
        sum_of_fit = 0
        fit = []
        for i in range(self.population_size):
            temp = 1/self.path_cost(self.population[i])
            fit.append(temp)
            sum_of_fit += temp

        current_value = []
        for i in range(self.population_size):
            if i == 0:
                current_value.append(fit[i]/sum_of_fit)
            else:
                current_value.append(fit[i]/sum_of_fit + current_value[i - 1])
        '''
        for i in range(self.population_size):
            parent1 = []
            parent2 = []
            ran1 = random.random()
            ran2 = random.random()
            for j in range(self.population_size):
                # print(current_value[j])
                if current_value[j] >= ran1:
                    # print('in1')
                    parent1 = self.population[j].copy()
                    break
            for j in range(self.population_size):
                if current_value[j] >= ran2:
                    # print('in2')
                    parent2 = self.population[j].copy()
                    break
            tag = True
            while tag:
                ran1 = random.randint(1, self.point - 2)
                ran2 = random.randint(1, self.point - 2)
                if ran1 == ran2:
                    continue
                break
            if ran1 > ran2:
                temp = ran1
                ran1 = ran2
                ran2 = temp
            new_path = []
            unused = []
            for k in range(self.point):
                if parent2[k] not in parent1[ran1:ran2]:
                    unused.append(parent2[k])

            for k in range(len(unused)):
                if k == ran1:
                    new_path.extend(parent1[ran1:ran2])
                    new_path.append(unused[k])
                else:
                    new_path.append(unused[k])
            temp_population.append(new_path)
            # print('len', len(new_path))
        '''
        for i in range(int(self.population_size/2)):
            parent1 = []
            parent2 = []
            ran1 = random.random()
            ran2 = random.random()
            for j in range(self.population_size):
                # print(current_value[j])
                if current_value[j] >= ran1:
                    # print('in1')
                    parent1 = self.population[j].copy()
                    break
            for j in range(self.population_size):
                if current_value[j] >= ran2:
                    # print('in2')
                    parent2 = self.population[j].copy()
                    break
            tag = True
            while tag:
                ran1 = random.randint(1, self.point - 2)
                ran2 = random.randint(1, self.point - 2)
                if ran1 == ran2:
                    continue
                break
            if ran1 > ran2:
                temp = ran1
                ran1 = ran2
                ran2 = temp

            left = {}
            right = {}
            k = ran1
            while k <= ran2:
                left[parent1[k]] = parent2[k]
                right[parent2[k]] = parent1[k]
                k += 1

            # print('ran1', ran1)
            # print('ran2', ran2)
            temp1 = parent1[ran1:ran2+1].copy()
            temp2 = parent2[ran1:ran2+1].copy()
            # print(temp1)
            # print(temp2)

            parent1[ran1:ran2 + 1] = temp2.copy()
            parent2[ran1:ran2 + 1] = temp1.copy()
            # print(parent1)
            # print(parent2)
            # print("pppp")
            for p in range(self.point):
                if p < ran1 or p > ran2:
                    w = parent1[p]
                    while self.find(w, ran1, ran2, parent1):
                        w = right[w]
                    parent1[p] = w
            for p in range(self.point):
                if p < ran1 or p > ran2:
                    w = parent2[p]
                    while self.find(w, ran1, ran2, parent2):
                        w = left[w]
                    parent2[p] = w
            # print(parent1)
            # print(parent2)
            temp_population.append(parent1)
            temp_population.append(parent2)

        temp_population.sort(key=lambda x: self.path_cost(x))
        self.population = temp_population[0: self.population_size].copy()
        # self.population.extend(temp_population[-10: 0])
        for i in range(2, len(self.population)):
            ran = random.random()
            new_path = []
            if ran < 0.01:
                tag = True
                while tag:
                    ran1 = random.randint(1, self.point - 2)
                    ran2 = random.randint(1, self.point - 2)
                    if ran1 == ran2:
                        continue
                    tag = False
                    new_path = self.population[i].copy()
                    if ran1 > ran2:
                        temp = ran1
                        ran1 = ran2
                        ran2 = temp
                    # j = ran1
                    # while j <= ran2:
                    #     new_path[ran2 - (j - ran1)] = self.population[i][j]
                    #     j += 1
                    temp = new_path[ran1]
                    new_path[ran1] = new_path[ran2]
                    new_path[ran2] = temp
                self.population[i] = new_path.copy()

        self.local_search()

        self.population.sort(key=lambda x: self.path_cost(x))
        cost = self.path_cost(self.population[0])
        if g%20 == 0:
            self.update(cost, g)
        print(cost)


def main():
    ga = GA()
    ga.read_file()
    ga.init_population()
    gen = 0
    ga.init_point()
    while gen <= 1500:
        print('gen ', gen)
        ga.selection_crosscover(gen)
        gen += 1
    print("Run end")
    plt.ioff()
    plt.show()


if __name__ == '__main__':
    main()