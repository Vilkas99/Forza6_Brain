
class MinHeap:
    def __init__(self, array):
        self.nodePositionsInHeap = {node.id: idx for idx, node in enumerate(array)}
        self.heap = self.buildHeap(array)
    
    def isEmpty(self):
        return len(self.heap) == 0
    
    def buildHeap(self, array):
        firstParentIdx = (len(array) - 2) // 2
        for currentIdx in reversed(range(firstParentIdx + 1)):
            self.siftDown(currentIdx, len(array) - 1, array)
        
        return array
    
    def siftDown(self, currentIdx, endIdx, heap):
        childOneIdx = currentIdx * 2 + 1
        while childOneIdx <= endIdx:
            childTwoIdx = currentIdx * 2 + 2 if currentIdx * 2 + 2 <= endIdx else -1
            if (
                childTwoIdx != -1
                and heap[childTwoIdx].estimatedDistanceToEnd < heap[childOneIdx].estimatedDistanceToEnd
            ):
                idxToSwap = childTwoIdx
            else:
                idxToSwap = childOneIdx
                
            if heap[idxToSwap].estimatedDistanceToEnd < heap[currentIdx].estimatedDistanceToEnd:
                self.swap(currentIdx, idxToSwap, heap)
                currentIdx = idxToSwap
                childOneIdx = currentIdx * 2 + 1
            else:
                return
    

    def siftUp(self, currentIdx, heap):
        parentIdx = (currentIdx-1)//2
        while currentIdx > 0 and heap[currentIdx].estimatedDistanceToEnd < heap[parentIdx].estimatedDistanceToEnd:
            self.swap(currentIdx, parentIdx, heap)
            currentIdx = parentIdx
            parentIdx = (currentIdx - 1) // 2       
    
    def remove(self): 
        if self.isEmpty():
            return

        self.swap(0, len(self.heap) - 1, self.heap)
        node = self.heap.pop()
        del self.nodePositionsInHeap[node.id]
        self.siftDown(0, len(self.heap) - 1, self.heap)
        return node
    
    def insert(self, node):
        self.heap.append(node)
        self.nodePositionsInHeap[node.id] = len(self.heap) - 1
        self.siftUp(len(self.heap) - 1, self.heap)
    
    def swap(self, i, j, heap): 
        self.nodePositionsInHeap[heap[i].id] = j
        self.nodePositionsInHeap[heap[j].id] = i
        heap[i], heap[j] = heap[j], heap[i]
    
    def containsNode(self, node): 
        return node.id in self.nodePositionsInHeap

    def update(self, node): 
        self.siftUp(self.nodePositionsInHeap[node.id], self.heap)
        