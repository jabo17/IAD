"""
 Find a way out of the maze labyrinth
 with adjacencylists
"""

graph = [
    [1],  # 0
    [3, 2, 0],  # 1
    [1],  # 2
    [5, 4, 1],  # 3
    [3],  # 4
    [7, 6, 3],  # 5
    [5],  # 6
    [10, 8, 5],  # 7
    [10, 9],  # 8
    [8],  # 9
    [11, 8, 7],  # 10
    [13, 12, 10],  # 11
    [11],  # 12
    [15, 14, 11],  # 13
    [13],  # 14
    [13]  # 15
]

def way_out(graph, startnode, targetnode):
    current_path = [startnode]
    deadends = 0

    def visit(node):
        nonlocal deadends
        if len(graph[node]) == 1 and graph[node][0] in current_path:
            print("dead end")
            deadends += 1
            current_path.pop()
            return False

        for neighbour in graph[node]:
            if neighbour not in current_path:
                current_path.append(neighbour)
                if neighbour is not targetnode:
                    print(f"visiting {neighbour}")
                    if visit(neighbour):
                        return True
                    print(f"backtrack {neighbour}")
                else:
                    print("target reached")
                    return True
        current_path.pop()
        return False

    visit(startnode)
    print(current_path)
    print(f"deadends {deadends}")

def way_out_stack(graph, startnode, targetnode):
    current_path = [startnode]
    jobs = [[startnode, 0]]
    deadends = 0

    while len(jobs) != 0:
        # get next job
        node, neighbour = jobs.pop()
        # append job for next neighbour of node
        if neighbour < len(graph[node]):
            jobs.append([node, neighbour+1])

            neighbour = graph[node][neighbour]
            # is this a circle?
            if neighbour not in current_path:

                # visiting neighbour
                current_path.append(neighbour)
                print(f"visiting {neighbour}")
                # is neighbour our target?
                if neighbour != targetnode:
                    # is neighbour a dead end
                    if len(graph[neighbour]) == 1:
                        deadends += 1
                        print("dead end")
                        current_path.pop()
                        print(f"backtrack {neighbour}")
                    else:
                        # lets try to find the way out of the labyrinth from here
                        jobs.append([neighbour, 0])
                else:
                    # yay we found it
                    print("target reached")
                    break

        elif neighbour == len(graph[node]):
            # well we need to go back, because neighbour is only a recursive dead end
            current_path.pop()
            print(f"backtrack {node}")

    print(current_path)
    print(f"deadends {deadends}")

way_out(graph, 15, 0)
way_out_stack(graph, 15, 0)