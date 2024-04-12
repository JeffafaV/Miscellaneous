import java.util.Stack; // import the Stack class

// linked list class that checks if the nodes create a palindrome
public class PalindromeLinkedList {
	// references the head of the linked list
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
    void appendNode(Node newNode) {
        if (head == null) {
            head = newNode;
            return;
        }

        Node lastNode = head;
        while (lastNode.next != null) {
            lastNode = lastNode.next;
        }

        lastNode.next = newNode;
    }

    // Method to print the linked list
    void printList() {
        Node temp = head;
        while (temp != null) {
            System.out.print(temp.data + " ");
            temp = temp.next;
        }
        System.out.println();
    }
    
    // Method to check if the linked list contains a palindrome
    boolean isPalindrome() {
    Node slow = head;
    Node fast = head;
    Stack<Character> stack = new Stack<Character>();

    // Push elements of first half to stack using two pointers (slow and fast)
    while (fast != null && fast.next != null) {
        stack.push(slow.data);
        slow = slow.next;
        fast = fast.next.next;  // move two nodes at a time
    }

    // If length of linked list is odd, skip middle element
    if (fast != null)
        slow = slow.next;

    // Compare remaining half with stack
    while (slow != null) {
        char top = stack.pop();

        // If values are different then it's not a palindrome
        if (top != slow.data)
            return false; // Mismatch found

        slow = slow.next;
    }

    return true; // No mismatch found
}

    public static void main(String[] args) {
        CharLinkedList list = new CharLinkedList();

        list.appendNode(new Node('A'));
        list.appendNode(new Node('B'));
        list.appendNode(new Node('C'));
        list.appendNode(new Node('B'));
        list.appendNode(new Node('B'));

        list.printList(); 
        System.out.println(list.isPalindrome());
    }
}