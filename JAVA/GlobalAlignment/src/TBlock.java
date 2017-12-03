/**
 * Created by mohsenkatebi on 2017-12-02.
 */
public class TBlock {
    private int[] offsetRowFirst, offsetColFirst;
    private int[] offsetRowLast, offsetColLast;

    public TBlock(int t) {
        offsetRowFirst = new int[t - 1];
        offsetRowLast = new int[t - 1];
        offsetColFirst = new int[t - 1];
        offsetColLast = new int[t - 1];
    }

    public void setOffsetRowLast(int[] offsetRowLast) {
        this.offsetRowLast = offsetRowLast;
    }

    public void setOffsetColLast(int[] offsetColLast) {
        this.offsetColLast = offsetColLast;
    }

    public int[] getOffsetRowFirst() {
        return offsetRowFirst;
    }

    public int[] getOffsetColFirst() {
        return offsetColFirst;
    }

    public int[] getOffsetRowLast() {
        return offsetRowLast;
    }

    public int[] getOffsetColLast() {
        return offsetColLast;
    }
}
