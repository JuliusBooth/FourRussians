import java.util.HashMap;
import java.util.Objects;

public class FourRussiansSpeedup {

    private String firstSeq, secondSeq;


    private void preProcess() {

    }
}

class BlockFunctionArgs {
    private String S1, S2, V1, V2;
    private String hStr;
    private int hHashCode;

    public BlockFunctionArgs(String S1, String S2, String V1, String V2) {
        this.S1 = S1;
        this.S2 = S2;
        this.V1 = V1;
        this.V2 = V2;
        buildH();
    }

    private void buildH() {
        StringBuilder h = new StringBuilder(S1);
        h.append("#");
        h.append(S2);
        h.append("#");
        h.append(V1);
        h.append("#");
        h.append(V2);
        hStr = h.toString();
        hHashCode = hStr.hashCode();
    }

    @Override
    public boolean equals(Object o) {
        if (o instanceof BlockFunctionArgs) {
            BlockFunctionArgs other = (BlockFunctionArgs) o;
            return this.hStr.equals(other.hStr);
        }
        return false;
    }

    @Override
    public int hashCode() {
        return this.hHashCode;
    }
}
