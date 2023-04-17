package sk.stuba.fiit.martin.szabo.bdd;

import java.util.ArrayList;

public class BDD{
    private ArrayList<Layer> layers;

    public BDD(){
        layers = new ArrayList<>();
    }

    public BDD(String exp){
        layers = new ArrayList<>();
        this.create(exp);
    }

    public void create(String exp){
        Expression expression = new Expression(exp);
        this.addLayer(expression);

        // TODO:: Troubleshoot this loop
        Layer lastLayer = this.getLayers().get(this.getLayers().size() - 1);
        while(lastLayer.getLeft() != null || lastLayer.getRight() != null){
            if(lastLayer.getLeft() != null){
                this.addLayer(lastLayer.getLeft());
            }
            if(lastLayer.getRight() != null){
                this.addLayer(lastLayer.getRight());
            }

            lastLayer = this.getLayers().get(this.getLayers().size() - 1);
        }
    }

    public void evaulateVector(){
        return; // TODO:: Implement
    }

    private void addLayer(Expression exp){
        Layer layer = Expression.decompose(exp);
        if(layer != null){
            this.getLayers().add(layer);
        }
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
