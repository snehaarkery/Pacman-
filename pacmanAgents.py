# pacmanAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from pacman import Directions
from game import Agent
from heuristics import scoreEvaluation
import random



class RandomAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        actions = state.getLegalPacmanActions()
        # returns random action from all the valide actions
        return actions[random.randint(0,len(actions)-1)]

class GreedyAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        print state
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        legal = state.getLegalPacmanActions()
        # get all the successor state for these actions
        successors = [(state.generateSuccessor(0, action), action) for action in legal]
        # evaluate the successor states using scoreEvaluation heuristic
        scored = [(scoreEvaluation(state), action) for state, action in successors]
        # get best choice
        bestScore = max(scored)[0]
        # get all actions that lead to the highest score
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        # return random action from the list of the best actions
        return random.choice(bestActions)

class BFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write BFS Algorithm instead of returning Directions.STOP
        queue = []  #creating a queue
        leaves = []

        legal = state.getLegalPacmanActions()
        if legal:
            successor = [(state.generatePacmanSuccessor(action), action) for action in legal]
        for i in successor:
            node = {}
            node["parent"] = node
            node["action"] = i[1]
            node["state"] = i[0]
            queue.append(node)

        while queue:
            node = queue.pop(0)
            curr_state = node["state"]
            parent_action = node["action"]

            if curr_state is not None:
                legal = curr_state.getLegalPacmanActions()
                if legal is not None:
                    successor = []
                    for action in legal:
                        instance = curr_state.generatePacmanSuccessor(action)
                        if(instance is not None):
                            successor.append((instance,parent_action))


                if (curr_state.isWin() or curr_state.isLose() or instance is None):
                    leaves.append(node)
                else:
                     for child in successor:
                         sub_node ={}
                         sub_node["state"] = child[0]
                         sub_node["action"] = child[1]
                         sub_node["parent"] = node
                         queue.append(sub_node)


        max_score = -9999

        if leaves:
            for value in leaves:
                 if((scoreEvaluation(value["state"])>max_score)):
                     max_score  = scoreEvaluation(value["state"])
                     result = value["action"]
            return result


class DFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write DFS Algorithm instead of returning Directions.STOP

        stack = []   #creating a stack
        leaves = []

        legal = state.getLegalPacmanActions()
        successor = [(state.generatePacmanSuccessor(action),action) for action in legal]
        for i in successor:
            node = {}
            node["parent"] = node
            node["action"] = i[1]
            node["state"] =i[0]
            stack.append(node)

        while stack:
            node = stack.pop()
            curr_state = node["state"]
            parent_action = node["action"]

            if curr_state is not None:
                legal = curr_state.getLegalPacmanActions()
                if legal is not None:
                    #successor =[]
                    for action in legal:
                        instance = curr_state.generatePacmanSuccessor(action)
                        if(instance is not None):
                            successor = [(instance,parent_action)]

                if (curr_state.isWin()) or (curr_state.isLose()) or (instance is None):
                    leaves.append(node)
                else:
                     for child in successor:
                         sub_node ={}
                         sub_node["state"] = child[0]
                         sub_node["action"] = child[1]
                         sub_node["parent"] = node
                         stack.append(sub_node)

        max_score = -9999999
        if leaves:
            for value in leaves:
                 if(scoreEvaluation(value["state"])>max_score):
                     max_score  = scoreEvaluation(value["state"])
                     result = value["action"]
            return result

class AStarAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    def sort_nodes(self, list):
        new = sorted(list, key=lambda k: k['cost'])
        return new

    # GetAction Function: Called with every frame
    def getAction(self, state):
        pqueue = []  #creating a priority queue
        leaves = []
        root = state
        legal = state.getLegalPacmanActions()
        successor = [(state.generatePacmanSuccessor(action), action) for action in legal]
        for i in successor: #Push the successors of parent node into the queue
            node = {}
            node["parent"] = state
            node["action"] = i[1]
            node["state"] = i[0]
            node["depth"] = 1
            node["score"] = scoreEvaluation(root) - scoreEvaluation(node["state"])
            node["cost"] = node["depth"] + node["score"]
            pqueue.append(node)

        while pqueue:
            pqueue = self.sort_nodes(pqueue)
            node = pqueue.pop(0)
            curr_state = node["state"]
            act = node["action"]
            depth = node["depth"]

            if curr_state is not None:
                legal = curr_state.getLegalPacmanActions()
                if legal:
                    for action in legal:
                        successor = []
                        s = curr_state.generatePacmanSuccessor(action)
                        if s is not None:
                            successor.append((s, act))

                if (curr_state.isWin()) or (curr_state.isLose()) or (s is None):
                    leaves.append(node)

                else:

                    for child in successor:
                        if (child[0] is not None):
                            sub_node = {}
                            sub_node["state"] = child[0]
                            sub_node["action"] = act
                            sub_node["parent"] = node
                            sub_node["depth"] = depth + 1
                            sub_node["score"] = scoreEvaluation(root) - scoreEvaluation(child[0])
                            sub_node["cost"] = sub_node["depth"] + sub_node["score"]
                            pqueue.append(sub_node)

        max_score = -99999999
        if leaves:

            for value in leaves:
                leaf_score = scoreEvaluation(value["state"])
                if (leaf_score > max_score):
                    max_score = leaf_score
                    result = value["action"]
            return result


			class RandomSequenceAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        self.actionList = [];
        for i in range(0,10):
            self.actionList.append(Directions.STOP);
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        possible = state.getAllPossibleActions();
        for i in range(0,len(self.actionList)):
            self.actionList[i] = possible[random.randint(0,len(possible)-1)];
        tempState = state;
        for i in range(0,len(self.actionList)):
            if tempState.isWin() + tempState.isLose() == 0:
                tempState = tempState.generatePacmanSuccessor(self.actionList[i]);
            else:
                break;
        # returns random action from all the valide actions
        return self.actionList[0];

class GreedyAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        legal = state.getLegalPacmanActions()
        # get all the successor state for these actions
        successors = [(state.generatePacmanSuccessor(action), action) for action in legal]
        # evaluate the successor states using scoreEvaluation heuristic
        scored = [(scoreEvaluation(state), action) for state, action in successors]
        # get best choice
        bestScore = max(scored)[0]
        # get all actions that lead to the highest score
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        # return random action from the list of the best actions
        return random.choice(bestActions)

class HillClimberAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        self.total_actions = []
        for i in range(5):
            self.total_actions.append(Directions.STOP);
        return;

    def populateRandomly(self,possible):
        #list_temp = [None] * 5
        list_temp  = []
        for i in range(5):
            list_temp.append(possible[random.randint(0, len(possible) - 1)])
        return list_temp

    def score(self, chromosomes, state):
        curr_state = state
        sflag = True
        for i in range(len(chromosomes)):
            if curr_state:
                if curr_state.isWin() + curr_state.isLose() == 0:
                    curr_state = curr_state.generatePacmanSuccessor(chromosomes[i])
                else:
                    break
        if curr_state is None:
            sflag = False
            return -9999, sflag
        else:
            return scoreEvaluation(curr_state), sflag

    def getAction(self, state):
        # TODO: write Hill Climber Algorithm instead of returning Directions.STOP
        possible = state.getAllPossibleActions();
        # Randomly Populate the ActionList
        self.total_actions = self.populateRandomly(possible)
        maxScore = -9999
        actionToReturn = Directions.STOP
        flag = True
        while flag:
            for i in range(0, len(self.total_actions)):
                randomValue = random.randint(0, 1)
                if (randomValue > 0):
                    self.total_actions[i] = possible[random.randint(0, len(possible) - 1)]
            tempScore, tflag = self.score(self.total_actions, state)
            flag = tflag
            if flag == True:
                if tempScore > maxScore:
                    actionToReturn = self.total_actions[0]
                    maxScore = tempScore
        return actionToReturn



class GeneticAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        self.total_actions = [[],[],[],[],[],[],[],[]]
        for i in range(8):
            for j in range(5):
                self.total_actions[i].append(Directions.STOP)
        #print self.total_actions
        return;

    def selectParent(self,cr):
        prob_each = []
        probability = 0
        for i in cr:
            probability = probability + int(i["rank"])
            prob_each.append(float(i["rank"]/probability))
        selction = random.uniform(0,probability)
        sum = 0
        for ele in cr:
            sum += ele["rank"]
            if sum > selction:
                return ele
        return selction

    def crossover(self,parent1,parent2):
        child = []
        for i in range(5):
            if random.randint(0,1) < 0.5:
                child.append(parent1[i])
            else:
                child.append(parent2[i])
        return child

    def mutate(self,nextgen,state):
        #print nextgen
        all = state.getAllPossibleActions()
        replacement = random.randint(0,4)
        #print replacement
        nextgen[replacement] = all[random.randint(0, len(all) - 1)]
        return nextgen


    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write Genetic Algorithm instead of returning Directions.STOP
        self.flag = True
        all = state.getAllPossibleActions()
        #print all
        for i in range(8):
            for j in range(5):
                self.total_actions[i][j]= all[random.randint(0, len(all) - 1)]
        #print self.total_actions

        #calculate score for each sequence
        score = []
        cur_state = state

        for i in range(8):
            for j in range(5):
                if cur_state.isWin():
                    return self.total_actions[i][0]
                elif cur_state.isLose():
                    break
                else:
                    #print self.total_actions[j]
                    cur_state = cur_state.generatePacmanSuccessor(self.total_actions[i][j])
                    #print scoreEvaluation(cur_state)
            #print cur_state
            score.append(scoreEvaluation(cur_state))

        #print "Before",self.total_actions

        while self.flag:
            i = 0
            chrom = []
            for s in score:
                parent = {}
                parent["actions"] = list(self.total_actions[i])
                parent["score"] = s
                parent["id"] = i
                chrom.append(parent)
                i = i + 1

            chrom.sort(key=lambda x: x["score"])

            #print chrom

            rank = 1
            for i in range(8):
                chrom[i]["rank"] = i + 1

            #############################################
            # find children
            random_test = random.randint(0,1)
            next_generation = []
            for i in range(0,4):
                parent1 = self.selectParent(chrom)
                #print parent1
                parent2 = self.selectParent(chrom)
                if random_test < 0.7:
                    child1 = self.crossover(parent1["actions"], parent2["actions"])
                    child2 = self.crossover(parent1["actions"], parent2["actions"])
                    next_generation.append(list(child1))
                    next_generation.append(list(child2))

                else:
                    #print parent1
                    child1 = list(parent1["actions"])
                    child2 = list(parent2["actions"])
                    next_generation.append(child1)
                    next_generation.append(child2)

            ###############################################
            #print next_generation
            new_generation = []
            random_check = random.randint(0,1)
            for i in range(8):
                if random_check < 0.1:
                    new_gen = self.mutate(next_generation[i],state)
                else:
                    new_gen = next_generation[i]
                    #print new_gen
                new_generation.append(new_gen)

            #print new_generation
            ###scoring
            scores = []
            cur_state = state
            if cur_state is None:
                self.flag = None
                break
            for i in range(8):
                for j in range(5):
                    if cur_state:
                        if cur_state.isWin():
                            return new_generation[i][0]
                        elif cur_state.isLose():
                            break
                        else:
                            # print self.total_actions[j]
                            cur_state = cur_state.generatePacmanSuccessor(new_generation[i][j])

                        # print scoreEvaluation(cur_state)
                    elif cur_state is None:
                        self.flag = False
                        break
                if cur_state:
                    scores.append(scoreEvaluation(cur_state))
            #print score

            for i in range(8):
                for j in range(5):
                    self.total_actions[i][j] = new_generation[i][j]

            for i in range(len(scores)):
                score[i] = scores[i]

        i = 0
        chrome = []
        for s in scores:
            children = {}
            children["actions"] = list(new_generation[i])
            #print next_generation[i]
            children["score"] = s
            children["id"] = i
            chrome.append(children)
            i = i + 1

        chrome.sort(key=lambda x: x["score"])
        #print chrome

        dict = chrom[7]
        return dict["actions"][0]
        #return Directions.STOP


class MCTSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    def expansion(self, node):
        state = node["state"]
        chose_action = None

        legal = state.getLegalPacmanActions()
        if node is not None:
            for i in range(len(node["action_list"])):
                action = node["action_list"][i]
                if action in legal:
                    legal.remove(action)

        chose_action = legal[random.randint(0,len(legal)-1)]
        instances = state.generatePacmanSuccessor(chose_action)

        if instances is None:
            self.flag = False
            return None

        sub_node = {}
        sub_node["parent"] = node
        sub_node["action"] = chose_action
        sub_node["state"] = instances
        sub_node["children"] = False
        sub_node["visited"] = 0
        sub_node["score"] = 0
        sub_node["action_list"] = []
        sub_node["child_list"] =[]

        node["child_list"].append(sub_node)

        node["action_list"].append(chose_action)

        if len(legal) == 1:
            node["children"] = True

        return sub_node

    #selection
    def selection(self,node,c):
        children = node["child_list"]
        maxi = -9999
        for i in children:

            exploitation = normalizedScoreEvaluation(node["state"],i["state"])
            exploration = c * math.sqrt((math.log(node["visited"])) / (i["visited"]))
            ucb = exploitation + exploration
            if ucb > maxi:
                maxi = ucb
                ret_node = i

        return ret_node

    #tree policy
    def treePolicy(self,node):
        while node["state"].isWin() + node["state"].isLose() == 0:
            if node["children"] == False:
                return self.expansion(node)
            else:
                node = self.selection(node,1)
                if node["state"] is None:
                    return None
        return node

    #Default Policy
    def defaultPolicy(self,state):
        rollout = 0
        while rollout < 5:
            if state.isWin() or state.isLose():
                return scoreEvaluation(state)
            else:
                legal = state.getLegalPacmanActions()
                if legal:
                    random_action = legal[random.randint(0, len(legal) - 1)]
                    state = state.generatePacmanSuccessor(random_action)
                    if state is None:
                        self.flag = False
                        return 0
            rollout = rollout + 1
        return scoreEvaluation(state)

    def backup(self,node,score):
        while node:
            node["score"] = node["score"] + score
            node["visited"] = node["visited"] + 1
            node = node["parent"]

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write MCTS Algorithm instead of returning Directions.STOP
        self.flag = True
        node = {}
        node["parent"] = None
        node["action"] = None
        node["visited"] = 0
        node["state"] = state
        node["score"] = 0
        node["children"] = False
        node["child_list"] = []
        node["action_list"] = []


        while self.flag:
            expanded_node = self.treePolicy(node)
            #print node
            if expanded_node is not None:
                score = self.defaultPolicy(expanded_node["state"])
                self.backup(expanded_node,score)
            else:
                break


        maxi = -9999
        action_list = node["action_list"]
        child_list = node["child_list"]
        for i in range(len(node["action_list"])):
            action = action_list[i]
            child = child_list[i]
            visits = child["visited"]
            if visits > maxi:
                maxi = visits
                result = action
        return result