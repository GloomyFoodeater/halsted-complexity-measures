var ListNode = function (data) {
    this.data = data;
    this.next = null;
};
// Constructor for stack object
var Stack = function () {
    this.top = null;
};
// Method to push data to stack
Stack.prototype.push = function (data) {
    if (!this.empty()) {
        // Create new node and make it top element
        var node = new ListNode(data);
        node.next = this.top;
        this.top = node;
    }
    else
        this.top = new ListNode(data);
};
// Method to pop data from stack
Stack.prototype.pop = function () {
    if (!this.empty()) {
        // Get data from top and switch to next element
        var res = this.top.data;
        this.top = this.top.next;
        return res;
    }
    else
        throw new Error('Stack already empty.');
};
// Method to get top value of stack without removing it
Stack.prototype.peek = function () {
    if (!this.empty())
        return this.top.data;
    else
        throw new Error('Stack was already empty.');
};
// Check whether stack is empty
Stack.prototype.empty = function () {
    return this.top === null;
};
// Constructor for queue object
var Queue = function () {
    this.head = this.tail = null;
};
// Method to add element to queue
Queue.prototype.enqueue = function (data) {
    if (!this.empty()) {
        // Put element to tail
        this.tail.next = new ListNode(data);
        this.tail = this.tail.next;
    }
    else {
        // Put element to head and tail
        this.head = new ListNode(data);
        this.tail = this.head;
    }
};
// Method to retrieve head element
Queue.prototype.dequeue = function () {
    if (!this.empty()) {
        // Get value and change head 
        var res = this.head.data;
        this.head = this.head.next;
        return res;
    }
    else
        throw new Error('Queue was already empty.');
};
// Method to get head element without removing it
Queue.prototype.peek = function () {
    if (!this.empty())
        return this.head.data;
    else
        throw new Error('Queue was already empty.');
};
// Check whether queue is empty
Queue.prototype.empty = function () {
    return this.head === null;
};
// Constructor for binary nodes
var BinaryNode = function (key, data) {
    this.key = key;
    this.data = data;
    this.right = null;
    this.left = null;
};
// Constructor for binary tree
var BinarySearchTree = function () {
    this.root = null;
};
// Method to insert new element to search tree
BinarySearchTree.prototype.insert = function (key, data) {
    // Recursive search for a spot
    function _insert(root, key, data) {
        if (root.key > key) {
            // Spot is in left subtree
            if (root.left !== null)
                _insert(root.left, key, data);
            else
                root.left = new BinaryNode(key, data);
        }
        else {
            // Spot it in right subtree
            if (root.right !== null)
                _insert(root.right, key, data);
            else
                root.right = new BinaryNode(key, data);
        }
    }
    // Enter recursive function
    if (!this.empty())
        _insert(this.root, key, data);
    else
        this.root = new BinaryNode(key, data);
};
// Method to find data by its key
BinarySearchTree.prototype.find = function (key) {
    // Recursive search of data
    function _find(root, key) {
        // Data does not exist
        if (root === null)
            return undefined;
        // Data is found
        if (root.key == key)
            return root.data;
        // Continue recursive search
        if (root.key > key)
            return _find(root.left, key);
        else
            return _find(root.right, key);
    }
    // Enter recursive function
    if (!this.empty())
        return _find(this.root, key);
    else
        return undefined;
};
// Check whether tree is empty
BinarySearchTree.prototype.empty = function () {
    return this.root === null;
};
try {
    // Initialize stack, queue, tree
    var stack = new Stack(), queue = new Queue(), tree = new BinarySearchTree();
    // Initialize data for structures
    var keys = [], samples = ['cherry', 'apple', 'pear', 'strawberry', 'grape', 'juniper'];
    // Filling structures and outputting array
    for (var i in samples) {
        stack.push(samples[i]);
        queue.enqueue(samples[i]);
        keys[i] = Math.floor(Math.random() * 90 + 10);
        tree.insert(keys[i], samples[i]);
        console.log(keys[i], samples[i]);
    }
    // Releasing stack
    console.log('Stack: ');
    console.log('---------------------------------');
    while (!stack.empty()) {
        console.log(stack.peek());
        stack.pop();
    }
    console.log('---------------------------------');
    // Releasing queue
    console.log('Queue: ');
    console.log('---------------------------------');
    while (!queue.empty()) {
        console.log(queue.peek());
        queue.dequeue();
    }
    console.log('---------------------------------');
    // Searhing in binary tree
    console.log('Tree: ');
    console.log('---------------------------------');
    for (var i in keys) {
        console.log(keys[i], tree.find(keys[i]));
    }
    console.log('---------------------------------');
    console.log(tree);
}
catch (e) {
    console.log(e);
}
finally {
    // Test finally
    var x = 10 ? 29 : 30, ob = null;
    var y = ob !== null && ob !== void 0 ? ob : 10;
    var z = ob === null || ob === void 0 ? void 0 : ob.right;
}
try {
}
catch (_a) {
    // Test catch
    var break_1 = 0;
    do {
        for (var j = 1; j < 10; j++) {
            --j;
            ++j;
        }
    } while (break_1);
}
