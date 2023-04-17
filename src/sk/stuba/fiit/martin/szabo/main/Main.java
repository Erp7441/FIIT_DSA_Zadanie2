package sk.stuba.fiit.martin.szabo.main;

import sk.stuba.fiit.martin.szabo.bdd.BDD;
import sk.stuba.fiit.martin.szabo.bdd.Expression;
import sk.stuba.fiit.martin.szabo.bdd.Layer;

public class Main{
    public static void main(String[] args){

        String exp = "A.!B.!C + A.B.C + !A.B.!C + !A.!B.C";

        BDD bdd = new BDD(exp);
    }
}