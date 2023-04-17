package sk.stuba.fiit.martin.szabo.bdd;

import java.util.ArrayList;

public class BDD{
    private ArrayList<Layer> layers;

    public BDD(){
        layers = new ArrayList<>();
    }

    public BDD(ArrayList<Layer> layers){
        this.layers = layers;
    }

    public ArrayList<Layer> getLayers(){
        return layers;
    }

    public void setLayers(ArrayList<Layer> layers){
        this.layers = layers;
    }
}
