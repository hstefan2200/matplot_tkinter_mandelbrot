import json
def partitions(n):
    part_set = set()
    part_set.add((n, ))

    for i in range(1, n):
        n2 = n-i
        for j in partitions(n2):
            part_set.add((tuple((i, ) + j)))
    parts = list(sorted(part_set))
    return parts
            
# print(partitions(4))

# parts = partitions(4)
# j_parts = json.dumps(partitions(4))
# #print(j_parts, str(len(parts)))
# for i in parts:
#     print(json.dumps(i))
# print(i for i in j_parts)

def conv():
    partition_list = partitions(3)
    j_parts = json.dumps(partition_list)
    num_parts = len(partition_list)
    
    r_val = {}
    x = 1
    for i in partition_list:
        r_val[f'partition #{x}'] =  json.dumps(i)
        x+=1
        
    f_d = {'The number entered: ': "4", 
           'The number of partitions found: ': num_parts
        }
    fin_r = f_d | r_val
    return fin_r
print(conv())