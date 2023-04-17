package sk.stuba.fiit.martin.szabo.bdd;

import java.util.ArrayList;

public class Layer{
    private Character root;
    private Expression left;
    private Expression right;

    public Layer(Character root){
        this.root = root;
    }

    public Layer(Character root, Expression left, Expression right){
        this.root = root;
        this.left = left;
        this.right = right;
    }

    public Character getRoot(){
        return root;
    }

    public void setRoot(Character root){
        this.root = root;
    }

    public Expression getLeft(){
        return left;
    }

    public void setLeft(Expression left){
        this.left = left;
    }

    public Expression getRight(){
        return right;
    }

    public void setRight(Expression right){
        this.right = right;
    }
}
