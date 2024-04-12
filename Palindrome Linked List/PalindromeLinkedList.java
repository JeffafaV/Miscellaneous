import java.util.Stack; // import the Stack class

// linked list class that checks if the nodes create a palindrome
public class PalindromeLinkedList {
	// references the head node of the linked list
    Node head;

	// static nested class for individual nodes of the linked list
	// it is nested since the outside class will only access it to provide encapsulation
	// it is static since it doesn't need access to any members of the outside class
	// https://www.baeldung.com/java-static
    static class Node {
        char data; // holds a character
        Node next; // reference to the next node

		// parameterized constructor
        public Node(char d) {
            data = d; // sets data to d variable
            next = null; // sets next to null
        }
    }

    // method to append nodes to the end of the linked list
    void appendNode(char c) {
        
        // create a new node
        Node newNode = new Node(c);

        // check to see if linked list is empty
        if (head == null) {
            
            // set the new node to be the head of linked list
            head = newNode;
            // return since no further changes are needed
            return;
        }

        // create a new node to traverse to last node
        Node lastNode = head;

        // traverse until we reach the last node
        while (lastNode.next != null) {

            // move to the next node
            lastNode = lastNode.next;
        }

        // the last node now references the new node which is the new last node
        lastNode.next = newNode;
    }

    // method to print the linked list
    void printList() {

        // temporary node used to traverse the linked list
        Node temp = head;

        // traverse linked list until we reach the end
        while (temp != null) {

            // print the data of the current node
            System.out.print(temp.data + " ");
            // move to the next node
            temp = temp.next;
        }
        // move to new line
        System.out.println();
    }
    
    // method to check if the linked list contains a palindrome
    // utilizes fast and slow pointer method and stack
    boolean isPalindrome() {

        // slow pointer moves 1 node at a time
        Node slow = head;
        // fast pointer moves 2 nodes at a time
        Node fast = head;

        // creates a stack container to hold chars from the first half of the 
        // linked list in reverse order. then we can compare the reversed first half 
        // and the second half to see if it is a palindrome or not
        Stack<Character> stack = new Stack<Character>();

        // continue traversing until fast is at the last node or end of linked list
        while (fast != null && fast.next != null) {
            // push the char of the current node in slow
            stack.push(slow.data);
            slow = slow.next; // move one node at a time
            fast = fast.next.next;  // move two nodes at a time
        }

        // we want the slow pointer to point at the first node of the second half.
        // if the linked list is odd then slow is pointing to the middle node, 
        // not the first node of the second half. so if the linked list is odd 
        // we move slow up one node. we can check if the linked list is odd by 
        // checking if the fast pointer is null or not
        if (fast != null)
            // move slow to the next node
            slow = slow.next;

        // travese the second half of the linked list
        while (slow != null) {
            
            // retrieve the data of the top of the stack and pop it from stack
            char top = stack.pop();

            // compare stack value with current node value
            // if values are different then it's not a palindrome
            if (top != slow.data)

                // mismatch found
                return false;

            // move to the next node
            slow = slow.next;
        }

        return true; // no mismatch found
    }

    public static void main(String[] args) {
        
        // create class object
        CharLinkedList list = new CharLinkedList();

        // adding nodes
        list.appendNode('A');
        list.appendNode('B');
        list.appendNode('C');
        list.appendNode('B');
        list.appendNode('B');

        // print nodes
        list.printList();
        // prints true or false depending if palindrome is true or false
        System.out.println(list.isPalindrome());
    }
}