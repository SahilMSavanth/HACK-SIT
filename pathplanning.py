################### Path planning for a given map ####################

import numpy as np
import cv2

######### Functions to detect map parameters using image processing and storing it inside a dictionary ########
def detect_all_nodes(image):  
	traffic_signals = []
	start_node = ""
	end_node = ""


	green=np.array([0,255,0])
	purple=np.array([189,43,105])
	red=np.array([0,0,255])
	lst_y=[100,200,300,400,500,600]
	str_x='ABCDEF'

	for i in lst_y:
		for j in lst_y:
			ind=lst_y.index(j)
			color=image[i,j]
			s1=str_x[ind:ind+1]
			s2=str(lst_y.index(i)+1)
			if np.array_equal(color,green):
				start_node=s1 + s2
           
			elif np.array_equal(color,purple):
				s1=str_x[ind:ind+1]
				s2=str(lst_y.index(i)+1)
				end_node=s1+s2
            
			elif np.array_equal(color,red):
				s1=str_x[ind:ind+1]
				s2=str(lst_y.index(i)+1)
				detected_traffic_light=s1+s2
				traffic_signals.append(detected_traffic_light)
	traffic_signals.sort()
###########################################

	return traffic_signals, start_node, end_node

def detect_paths_to_graph(image):
	paths = {}
	black=np.array([0,0,0])
	white=np.array([255,255,255])

	lst_y=[100,200,300,400,500,600]
	str_x='ABCDEF'

	for i in lst_y:
		for j in lst_y:
        
			ind=lst_y.index(j)
			inc_ind=lst_y.index(i)
			inc=lst_y.index(i)+1
        
			s1=str_x[ind:ind+1]
			s2=str(lst_y.index(i)+1)
			current_node=s1 + s2 #<-- for current node
			color=image[i,j]
        
			s_right_x=str_x[ind+1:ind+2] #<-- for right neighbours
			right_node=s_right_x + s2

			s_left_x=str_x[ind-1:ind] #<-- for left neighbours
			left_node=s_left_x+s2

			s_up_x=str_x[ind:ind+1] #<--for upward neighbours
			s_up_y=str(inc_ind)
			up_node=s_up_x + s_up_y

			s_down_x=str_x[ind:ind+1] #<--for downward neighbours
			s_down_y=str(inc+1)
			down_node=s_down_x + s_down_y
        	#print('left:',left_node,'right:',right_node,'up:',up_node,'down:',down_node,'current:',current_node)
			right,left,up,down=image[i,j+99],image[i,j-99],image[i-99,j],image[i+99,j]
			right_road=image[i,j+50]
			left_road=image[i,j-50]
			up_road=image[i-50,j]
			down_road=image[i+50,j]
       
			if np.array_equal(right,white) or np.array_equal(left,white) or np.array_equal(up,white) or np.array_equal(down,white):
				flag=True
			else:
				flag=False
			if flag==False:
				paths.update({current_node:{right_node:1,left_node:1,up_node:1,down_node:1}})
               
			elif flag==True:
				if np.array_equal(up,white):
					up_test_case=True
				else:
					up_test_case=False
            
				if np.array_equal(down,white):
					down_test_case=True
				else:
					down_test_case=False
            
           
				if np.array_equal(up,white):   #<-- for fisrt row
					if np.array_equal(left,white):
						paths.update({current_node:{right_node:1,down_node:1}})
					elif np.array_equal(right,white):
						paths.update({current_node:{left_node:1,down_node:1}})
					else:
						paths.update({current_node:{right_node:1,left_node:1,down_node:1}})
                    
				if np.array_equal(down,white):  #<-- for last row
					if np.array_equal(left,white):
						paths.update({current_node:{right_node:1,up_node:1}})
					elif np.array_equal(right,white):
						paths.update({current_node:{left_node:1,up_node:1}})
					else:
						paths.update({current_node:{right_node:1,left_node:1,up_node:1}})
                    

				if (np.array_equal(left,white) and up_test_case== False) :  #<-- for first coloumn
					if down_test_case== True:
						continue
					paths.update({current_node:{right_node:1,up_node:1,down_node:1}})
                
				if np.array_equal(right,white) and up_test_case== False:  #<-- for last coloumn
					if down_test_case== True:
						continue
					paths.update({current_node:{left_node:1,up_node:1,down_node:1}})

			if j<600:      #<----deleting unconstructed roads
				if np.array_equal(right_road,white):
					del paths[current_node][right_node]
			if j>100 and i>100:
				if np.array_equal(left_road,white):
					del paths[current_node][left_node]
			if i>100:
				if np.array_equal(up_road,white):
					del paths[current_node][up_node]
			if  i<600: 
				if np.array_equal(down_road,white):
					del paths[current_node][down_node] 
	if np.array_equal(image[600,550],white):
		del paths[current_node][left_node]
	if np.array_equal(image[550,600],white):
		del paths[current_node][up_node]
	if np.array_equal(image[600,150],white):
		del paths['A6']['B6']
	if np.array_equal(image[550,100],white):
		del paths['A6']['A5']
	##################################################

	return paths

def paths_to_moves(paths, traffic_signal):
	
	list_moves=[]
	origin=1
	for i in range(1,len(paths)):
		if ((paths[i][0]==paths[i-1][0]) and origin==1) or ((paths[i][1]==paths[i-1][1]) and origin==0) or ((paths[i][1]==paths[i-1][1]) and origin==2):
				list_moves.append('STRAIGHT')
		elif (origin==1) and (paths[i][0]<paths[i-1][0]):
				list_moves.append('LEFT')
				origin=0
		elif (origin==1) and (paths[i][0]>paths[i-1][0]):
				list_moves.append('RIGHT')
				origin=2
		elif (origin==0) and (paths[i][1]<paths[i-1][1]):
				list_moves.append('RIGHT')
				origin=1
		elif (origin==0) and (paths[i][1]>paths[i-1][1]):
				list_moves.append('LEFT')
				origin=1
		elif (origin==2) and (paths[i][1]<paths[i-1][1]):
			list_moves.append('LEFT')
			origin=1
		elif (origin==2) and (paths[i][1]>paths[i-1][1]):
			list_moves.append('RIGHT')
			origin=1
		
		if paths[i] in traffic_signal:
			list_moves.append('WAIT_5')
	##################################################

	return str(list_moves)

def detect_arena_parameters(maze_image):
	
        arena_parameters = {}
        traffic_signals,start_node,end_node=detect_all_nodes(maze_image)
        paths=detect_paths_to_graph(maze_image)
        arena_parameters={"traffic_signals":traffic_signals,"start_node":start_node,"end_node":end_node,"paths":paths}
        ##################################################
        
        return arena_parameters



def path_planning(graph, start, end):

	backtrace_path=[]
	
	shortest_distance={}  
	track_previous={}
	unseen_nodes=graph
	infinity=999999
	
	for node in unseen_nodes:
		shortest_distance[node]=infinity
	shortest_distance[start]=0

	while unseen_nodes:
		min_distance_node=None
		for node in unseen_nodes:
			if min_distance_node is None:
				min_distance_node=node
			elif shortest_distance[node]< shortest_distance[min_distance_node]:
				min_distance_node=node
        
		path_options=graph[min_distance_node].items()  #<---- accessing neighbouring nodes

		for child_node,weight in path_options:
			if weight+shortest_distance[min_distance_node] < shortest_distance[child_node]:
				shortest_distance[child_node]=weight + shortest_distance[min_distance_node]
				track_previous[child_node]=min_distance_node

		unseen_nodes.pop(min_distance_node)

	currentNode=end
	while currentNode != start:
		try:
			backtrace_path.insert(0,currentNode)
			currentNode=track_previous[currentNode]
		except KeyError:
			break
	backtrace_path.insert(0,start)

	if shortest_distance[end]!=infinity:
	##################################################


		return backtrace_path
	
######## Main function #########
if __name__=="__main__":
    image = cv2.imread("C:\\Users\\EJ511TS\\OneDrive\\Desktop\\maze_007.png")
    arena_parameters = detect_arena_parameters(image)
    print(arena_parameters["start_node"], ">>> ", arena_parameters["end_node"] )

    # path planning and getting the moves
    back_path=path_planning(arena_parameters["paths"], arena_parameters["start_node"], arena_parameters["end_node"])
    moves=paths_to_moves(back_path,arena_parameters['traffic_signals'])

    print("PATH PLANNED: ", back_path)
    print("MOVES TO TAKE: ", moves)

    # display the test image
    cv2.imshow("image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    
