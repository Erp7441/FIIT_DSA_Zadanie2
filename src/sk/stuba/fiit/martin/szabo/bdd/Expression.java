package sk.stuba.fiit.martin.szabo.bdd;

import java.util.ArrayList;
import java.util.List;

public class Expression{

    private ArrayList<Part> parts;

    public Expression(){
        parts = new ArrayList<>();
    }

    public Expression(List<Part> parts){
        this.parts = (ArrayList<Part>) parts;
    }

    public void insertExpression(String expression){
        if(expression == null) return;

        boolean negative = false;

        this.getParts().add(new Part());
        for(char character : expression.toCharArray()){

            if(character == '+'){
                this.getParts().add(new Part());
            }

            if(character == '+' || character == ' ' || character == '.') continue;

            if(character == '!' && !negative){
                negative = true;
            }
            else if(character == '!'){
                negative = false;
            }
            else{
                this.getParts().get(this.getParts().size() - 1).add(new Node(character, !negative));
                negative = false;
            }
        }
    }

    public boolean minimize(char root){

        for(Part part : this.getParts()){
            if(!part.contains(root)){
                return false;
            }
            part.remove(root);

        }

        return true;
    }

    public Character getRoot(){
        ArrayList<Character> alphabet = this.getAlphabet();
        boolean foundRoot;

        for(Character letter : alphabet){
            foundRoot = true;

            for(Part part : this.getParts()){
                if(!part.contains(letter)){
                    foundRoot = false;
                    break;
                }
            }

            if(foundRoot){
                return letter;
            }
        }

        return null;
    }

    private ArrayList<Character> getAlphabet(){
        ArrayList<Character> alphabet = new ArrayList<>();
        for(Part part : this.getParts()){
            part.getNodes().forEach(node -> {
                if(!alphabet.contains(node.getValue())){
                    alphabet.add(node.getValue());
                }
            });
        }
        return alphabet;
    }

    public ArrayList<Part> getParts(){
        return parts;
    }

    public void setParts(ArrayList<Part> parts){
        this.parts = parts;
    }
}
