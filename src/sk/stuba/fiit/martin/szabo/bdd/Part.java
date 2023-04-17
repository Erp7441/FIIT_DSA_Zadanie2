package sk.stuba.fiit.martin.szabo.bdd;

import sk.stuba.fiit.martin.szabo.utils.Operator;

import java.util.ArrayList;

public class Part{
    private ArrayList<Node> nodes;
    private Operator operator = Operator.MUL;

    public Part(){
        nodes = new ArrayList<>();
    }

    public Part(ArrayList<Node> nodes){
        this.nodes = nodes;
    }

    public void add(Node node){
        this.getNodes().add(node);
    }
    public void add(char value, boolean truthValue){
        this.getNodes().add(new Node(value, truthValue));
    }
    public void add(char value){
        this.getNodes().add(new Node(value));
    }

    public void remove(Node node){
        this.getNodes().remove(node);
    }

    public void remove(char value){
        this.getNodes().removeIf(node -> value == node.getValue());
    }

    public Node get(int index){
        return this.getNodes().get(index);
    }
    public Node get(char value){
        for(Node node: this.getNodes()){
            if(value == node.getValue()){
                return node;
            }
        }
        return null;
    }

    public ArrayList<Character> getValues(){
        ArrayList<Character> values = new ArrayList<>();

        for(Node node : this.getNodes()){
            values.add(node.getValue());
        }

        return values;
    }

    public ArrayList<Character> getCommonValues(ArrayList<Character> array){
        ArrayList<Character> values = new ArrayList<>();

        for(Node node : this.getNodes()){
            if(array.contains(node.getValue())){
                values.add(node.getValue());
            }
        }

        return values;
    }

    public boolean contains(Node node){
        return this.getNodes().contains(node);
    }

    public boolean contains(char value){
        for(Node node: this.getNodes()){
            if(value == node.getValue()){
                return true;
            }
        }
        return false;
    }

    public ArrayList<Node> getNodes(){
        return nodes;
    }

    public void setNodes(ArrayList<Node> nodes){
        this.nodes = nodes;
    }

    public Operator getOperator(){
        return operator;
    }

    public void setOperator(Operator operator){
        this.operator = operator;
    }
}
