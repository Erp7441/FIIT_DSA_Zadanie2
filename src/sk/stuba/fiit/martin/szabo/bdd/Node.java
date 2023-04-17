package sk.stuba.fiit.martin.szabo.bdd;

public class Node{

    private Character value;
    private Boolean truthValue;

    public Node(Character value, Boolean truthValue){
        this.value = value;
        this.truthValue = truthValue;
    }

    public Node(Character value){
        this.value = value;
        this.truthValue = Boolean.TRUE;
    }

    public Character getValue(){
        return value;
    }

    public void setValue(Character value){
        this.value = value;
    }

    public Boolean getTruthValue(){
        return truthValue;
    }

    public void setTruthValue(Boolean truthValue){
        this.truthValue = truthValue;
    }

    @Override
    public boolean equals(Object o){
        if(this == o) return true;
        if(o == null || getClass() != o.getClass()) return false;

        Node node = (Node) o;

        if(getValue() != null ? !getValue().equals(node.getValue()) : node.getValue() != null) return false;
        return getTruthValue() != null ? getTruthValue().equals(node.getTruthValue()) : node.getTruthValue() == null;
    }

    @Override
    public int hashCode(){
        int result = getValue() != null ? getValue().hashCode() : 0;
        result = 31 * result + (getTruthValue() != null ? getTruthValue().hashCode() : 0);
        return result;
    }
}
