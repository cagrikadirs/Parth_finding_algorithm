from sys import argv
import copy

#returns lists inside of lists to find cost of a coordinate
def cost_finder(field_list, cost1, cost2, cost3):
    field_cost = []

    for row in field_list:
        field_cost.append(row.copy())

    for i, row in enumerate(field_list):
        for j, element in enumerate(row):
            '''checks if the element is on the edge to evulate correctly
            if not checks the near coordinates to find if there is any 0'''
            if element == "1":
                if i == 0:
                    n = "1"
                else:
                    n = field_list[i - 1][j]
                if j == 0:
                    w = "1"
                else:
                    w = row[j - 1]
                if i == len(field_list) - 1:
                    s = "1"
                else:
                    s = field_list[i + 1][j]
                if j == len(row) - 1:
                    e = "1"
                else:
                    e = row[j + 1]

                if n == "0" or s == "0" or e == "0" or w == "0":
                    field_cost[i][j] = int(cost3)
                else:
                    #this time checks if if its corner or edge
                    if i==0:
                        if j==0:
                            nw,ne,sw,se="1","1","1",field_list[i+1][j+1]
                        elif j==len(row)-1:
                            ne,nw,se,sw="1","1","1",field_list[i+1][j-1]
                        else:
                            nw,ne,se,sw="1","1",field_list[i+1][j+1],field_list[i+1][j-1]
                    elif i==len(field_list)-1:
                        if j==0:
                            sw,se,nw,ne="1","1","1",field_list[i-1][j+1]
                        elif j==len(row)-1:
                            se,sw,nw,ne="1","1",field_list[i-1][j-1],"1"
                        else:
                            sw,se,nw,ne="1","1",field_list[i-1][j-1],field_list[i-1][j+1]
                    elif j==0:
                        nw,sw,ne,se="1","1",field_list[i-1][j+1],field_list[i+1][j+1]
                    elif j==len(row)-1:
                        ne,se,nw,sw="1","1",field_list[i-1][j-1],field_list[i+1][j-1]
                    # is not on the edge or corner so checks for zeros with coordinates
                    else:
                        nw,ne,sw,se=field_list[i-1][j-1],field_list[i-1][j+1],field_list[i+1][j-1],field_list[i+1][j+1]

                    if nw=="0" or sw=="0" or se=="0" or ne=="0":
                        field_cost[i][j] = int(cost2)
                    else:
                        field_cost[i][j] = int(cost1)
            else:
                field_cost[i][j] = 0

    return field_cost


#trys every direction and possibility. with each move calls itself to find the cheapest path returns cheapest at the moment
def pathfinder(field,field_cost,coordinate,cost,path,cheapest):
    #only runs in the first call of the function to try every coordinate on the left
    if coordinate=="start":
        for i in range(len(field)):
            x,y=0,i
            path = []
            cost = 0

            if field[i][0]!="0":
                path.append((x, y))
                cost += field_cost[y][x]

                # algorithm should go right for shortest in beginning
                if field[y][x + 1] == "1":
                    cheapest= pathfinder(field, field_cost, [x + 1, y], cost, path, cheapest)
        return cheapest

    else:
        x, y = coordinate[0], coordinate[1]
        path_temp=copy.deepcopy(path)
        path_temp.append((x,y))
        cost+=field_cost[y][x]

        #if it is firt try assumes that first is shortest to create a temporary shortest value
        if cheapest!=None:
            #if new path costs equal or more stop the algorithm and return previous cheapest
            if cost>=cheapest[0]:
                return cheapest

        #if function arrives to the end that means this is the cheapest path returns the new cheapest cost
        if x==len(field[0])-1:
            return [cost,path_temp]

        else:
            # moves right
            if field[y][x + 1] == "1":
                if (x+1,y) not in path_temp:
                    cheapest=pathfinder(field, field_cost, [x + 1, y], cost,path_temp,cheapest)
            # moves up
            if y!=0:
                if field[y - 1][x] == "1":
                    if (x, y-1) not in path_temp:
                        cheapest= pathfinder(field, field_cost, [x, y - 1], cost,path_temp ,cheapest)
            # moves down
            if y!=len(field)-1:
                if field[y + 1][x] == "1":
                    if (x, y+1) not in path_temp:
                        cheapest = pathfinder(field, field_cost, [x, y + 1], cost,path_temp,cheapest)
            #moves left
            if field[y][x - 1] == "1":
                if (x - 1, y) not in path_temp:
                    cheapest=pathfinder(field, field_cost, [x-1, y ], cost,path_temp,cheapest)

            return cheapest


#gets a list of cheapest cost and its path then gets the field and draws the path
def draw_path(list,field):
        with open(argv[2],"w") as output_file:
            try:
                cost, path = list[0], list[1]
                output_file.write(f"Cost of the route: {cost}\n")

                for coord in path:
                    field[coord[1]][coord[0]] = "X"

                for i,row in enumerate(field):
                    output_file.write(" ".join(row))
                    if i != len(field)-1:
                        output_file.write("\n")
            except TypeError:
                output_file.write("There is no possible route!")


def main():
    input_file = open(argv[1],"r")

    costs=input_file.readline().strip("\n").split(" ")
    cost1, cost2, cost3 = costs[0], costs[1], costs[2]

    field=input_file.readlines()

    #fields list has all rows as lists
    for i,row in enumerate(field):
        field[i]=row.strip("\n").split(" ")

    cost_list=cost_finder(field,cost1,cost2,cost3)
    cheapest_path=pathfinder(field,cost_list,"start",0,[],None)
    draw_path(cheapest_path,field)

    input_file.close()


if __name__ == '__main__':
    main()