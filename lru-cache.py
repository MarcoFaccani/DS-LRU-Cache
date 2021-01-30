class DoublyLinkedList(object):
    def __init__(self, capacity):
        self.head = None # most recently used element
        self.tail = None # olderst used element
        self.capacity = capacity # I wanted to make this var private and not give a setter so it couldn't be changed. How do I do this in Python? I know final variables aren't possible in Python and either declare it private
        self.num_elements = 0 


class DoublyLinkedListNode(object):
    def __init__(self, key, value):
        self.previous = None
        self.next = None
        self.key = key
        self.value = value


class LRU_Cache(object):

    def __init__(self, capacity):
        self.map = {}
        self.doublyLinkedList = DoublyLinkedList(capacity)
        self.size = self.doublyLinkedList.num_elements

    def createNewNodeAndInsertInMap(self, key, value):
        new_node = DoublyLinkedListNode(key, value)
        self.map[key] = new_node
        return new_node

    def removeTailAndDeleteKeyFromMap(self, old_tail):
        self.doublyLinkedList.tail = old_tail.previous
        self.doublyLinkedList.tail.next = None
        self.map.pop(old_tail.key)

    def swapHead(self, head, new_node):
        head.previous = new_node
        new_node.next = head
        self.doublyLinkedList.head = new_node

    def upgradeNodeToHead(self, nodeToUpgrade):
        if nodeToUpgrade.next is None: # upgrading tail to head
            nodeToUpgrade.previous.next = None
        else:
            nodeToUpgrade.previous.next = nodeToUpgrade.next
            nodeToUpgrade.next.previous = nodeToUpgrade.previous
        self.swapHead(self.doublyLinkedList.head, nodeToUpgrade)

        
    def get(self, key):
        node = self.map.get(key)
        if node is None:
            return -1
        else:
            self.upgradeNodeToHead(node)
            return node.value

    def set(self, key, value):
        if self.doublyLinkedList.head is None:
            new_node = self.createNewNodeAndInsertInMap(key, value)
            self.doublyLinkedList.head = new_node
            self.doublyLinkedList.tail = new_node
            self.doublyLinkedList.num_elements = 1

        elif self.doublyLinkedList.num_elements == 5:
            self.removeTailAndDeleteKeyFromMap(self.doublyLinkedList.tail)
            new_node = self.createNewNodeAndInsertInMap(key, value)
            self.swapHead(self.doublyLinkedList.head, new_node)
        else:
            new_node = self.createNewNodeAndInsertInMap(key, value)
            self.swapHead(self.doublyLinkedList.head, new_node)
            self.doublyLinkedList.num_elements += 1


# define tests

""" Insert 6 elements and verify that oldest elements are deleted from DoublyLinkedList and relative keys removed from map; 
    Also verify that elements are inserted in the proper order"""
def test_1():
    print("====== TEST 1-A ======")
    lru_cache = LRU_Cache(5)
    lru_cache.set("key1","value1")
    lru_cache.set("key2","value2")
    lru_cache.set("key3","value3")
    lru_cache.set("key4","value4")
    lru_cache.set("key5","value5")
    lru_cache.set("key6","value6")
    print("is Head (newest element) value6?: {}".format("Yes" if lru_cache.doublyLinkedList.head.value == "value6" else "No - Error!")) # assert head is 6
    print("is Tail (oldest element) value2?: {}".format("Yes" if lru_cache.doublyLinkedList.tail.value == "value2" else "No - Error!")) # assert tail is 2
    print("Has 'key1' been deleted from map? {}".format("Yes" if lru_cache.get("key1") == -1 else "No - Error!"))

    print("____TEST-1B____")
    lru_cache.set("key7","value7")
    print("is Head (newest element) value7?: {}".format("Yes" if lru_cache.doublyLinkedList.head.value == "value7" else "No - Error!")) # assert head is 7
    print("is Tail (oldest element) value3?: {}".format("Yes" if lru_cache.doublyLinkedList.tail.value == "value3" else "No - Error!")) # assert tail is 3
    print("Has 'key2' been deleted from map? {}".format("Yes" if lru_cache.get("key2") == -1 else "No - Error!"))




""" insert 5 elements then retrieve the oldest element and verify that such element is now the head"""
def test_2():
    print("====== TEST 2 ======")
    lru_cache = LRU_Cache(5)
    lru_cache.set("key1","value1")
    lru_cache.set("key2","value2")
    lru_cache.set("key3","value3")
    lru_cache.set("key4","value4")
    lru_cache.set("key5","value5")
    lru_cache.get("key2")
    print("is Head (newest element) value2?: {}".format("Yes" if lru_cache.doublyLinkedList.head.value == "value2" else "No - Error!")) # assert head is 2


""" verify both test_1 and test_2 in the same test for collisions """
def test_3():
    print("====== TEST 3 ======")
    lru_cache = LRU_Cache(5)
    lru_cache.set("key1","value1")
    lru_cache.set("key2","value2")
    lru_cache.set("key3","value3")
    lru_cache.set("key4","value4")
    lru_cache.set("key5","value5")
    lru_cache.get("key2")
    lru_cache.set("key6","value6")
    lru_cache.get("key3")
    print("is Head (newest element) value3?: {}".format("Yes" if lru_cache.doublyLinkedList.head.value == "value3" else "No - Error!")) # assert head is 3
    print("is the second newest element value6?: {}".format("Yes" if lru_cache.doublyLinkedList.head.next.value == "value6" else "No - Error!")) # assert head is 3
    print("Has 'key1' been deleted from map? {}".format("Yes" if lru_cache.get("key1") == -1 else "No - Error!"))



#Run Tests
test_1()
test_2()
test_3()
