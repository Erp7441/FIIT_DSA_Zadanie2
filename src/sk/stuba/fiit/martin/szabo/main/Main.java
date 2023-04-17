package sk.stuba.fiit.martin.szabo.main;

import sk.stuba.fiit.martin.szabo.bdd.Expression;

public class Main{
    public static void main(String[] args){

        String expres = "A.!B.!C + A.B.C + !A.B.!C + !A.!B.C";

        Expression expression = new Expression();

        expression.insertExpression(expres);
        expression.minimize(expression.getRoot());
        System.out.println(expression.getRoot());
    }
}