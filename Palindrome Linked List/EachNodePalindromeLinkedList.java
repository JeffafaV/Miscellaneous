//import java.util.Stack; // import the Stack class

// linked list class that checks if each node in the linked list is a palindrome
public class Main {
	// references the head node of the linked list
    Node head;

	// static nested class for individual nodes of the linked list
	// it is nested since the outside class will only access it to provide encapsulation
	// it is static since it doesn't need access to any members of the outside class
    // and for memory efficiency since static objects only create one instance of itself
    static class Node {
        String data; // holds a String
        Node next; // reference to the next node

		// parameterized constructor
        public Node(String d) {
            data = d; // sets data to d variable
            next = null; // sets next to null
        }
    }

    // method to append nodes to the end of the linked list
    void appendNode(String s) {
        
        // create a new node
        Node newNode = new Node(s);

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
    
    // check if the given node's string variable is a palindrome
    boolean NodeisPalindrome(Node n) {
        int left = 0;
        int right = n.data.length() - 1;
        
        while (left < right) {
            if (n.data.charAt(left) != n.data.charAt(right)) {
                return false;
            }

            left = left + 1;
            right = right - 1;
        }

        return true;
    }

    // check if all the nodes' string variable in linked list is a palindrome
    boolean allNodesPalindrome() {
        Node temp = head;

        while (temp != null) {
            if (NodeisPalindrome(temp) == false) {
                return false;
            }
            
            temp = temp.next;
        }

        return true;
    }

    public static void main(String[] args) {
        
        // create class object
        Main list = new Main();

        // adding nodes
        list.appendNode("aba");
        list.appendNode("aba");
        list.appendNode("aba");
        list.appendNode("aba");
        list.appendNode("aba");

        // print nodes
        list.printList();
        // prints true or false depending if palindrome is true or false
        System.out.println(list.allNodesPalindrome());
    }
}